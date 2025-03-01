import time
import logging
from botocore.exceptions import ClientError
import boto3
from pathlib import Path
import os
from amazon_q_developer_jupyterlab_ext.constants import RESPONSE_SESSION_ID_HEADER_NAME

TIMEOUT = 70 # 2 minutes 
SLEEP_INTERVAL = 1
ERROR_MESSAGE: str = "We did not find an answer to your question, please reach out to support.\n"

logging.basicConfig(format="%(levelname)s: %(message)s")

class GlueClient():
    def __init__(self):
        self.session = boto3.Session()
        # the following regions are not supported by glue completion APIs. If in these regions, we'll fall back to us-east-1
        self.unsupported_regions = ["il-central-1", "ap-southeast-4", "ap-south-2", "eu-south-2", "eu-central-2"]
        self.env_order = [self.session.region_name, os.environ.get("region"), os.environ.get("AWS_DEFAULT_REGION"), "us-east-1"]
        self.client = None

    async def _get_region(self):
        for env in self.env_order:
            if env is not None:
                return env

    async def _setup_client(self):
        endpoint = ""
        region = await self._get_region()
        logging.info("region from env: " + region)
        if region in self.unsupported_regions:
            endpoint = "https://glue.us-east-1.amazonaws.com"
            region = "us-east-1"
        else:
            endpoint = f"https://glue.{region}.amazonaws.com"
        logging.info("Setting Glue endpoint: " + endpoint)
        session_folder = f"{Path(__file__).parent.parent}/service_models"
        self.session._loader.search_paths.insert(0, session_folder)
        self.client = self.session.client(
            "glue",
            region_name=region,
            endpoint_url=endpoint,
        )
    
    def _format_response(self,response):
        # remove backticks from response
        response = response.replace("```", "")
        return response

    """
    Passes a prompt to the start_completion Sensei API, which provides enhanced completions for Glue-related queries, and
    checks get_completion until the completion request either succeeds or fails. The completion includes sources appended to the the
    end of the response.
    """
    async def query(self, prompt: str):
        invocation_start_time_ms = time.time()
        if self.client is None:
            await self._setup_client()
        try:
            # pass context to the start_completion API to identify requests coming from MD
            response = self.client.start_completion(Prompt=prompt, Context=[{ "key": "ApiCaller", "value": "MD" }])
            completion_id = response["CompletionId"]
            start_time = time.time()
            while True:
                if time.time() - start_time > TIMEOUT:
                    logging.error("Request timed out. Completion id: " + completion_id)
                    return {"data": {"completions": []}, "status": "CLIENT_ERR","x-amzn-requestid": None, "x-amzn-sessionid": None, "message": ERROR_MESSAGE + "Completion ID: " + completion_id }
                response = self.client.get_completion(CompletionId=completion_id)
                if response["Status"] == "SUBMITTED" or response["Status"] == "RUNNING":
                    time.sleep(SLEEP_INTERVAL)
                    continue
                elif response["Status"] == "SUCCEEDED":
                    result = self._format_response(response["Completion"])
                    new_response = {"data": {"completions": [{"content": result, "mostRelevantMissingImports": [], "references": []}], "nextToken": ""}, "status": "SUCCEEDED", "x-amzn-requestid": response["ResponseMetadata"]["RequestId"] , "x-amzn-sessionid": response["ResponseMetadata"]['HTTPHeaders'].get(RESPONSE_SESSION_ID_HEADER_NAME)}
                    logging.info(f"Sensei service latency: {round((time.time() - invocation_start_time_ms) * 1000)}")
                    return new_response
                else:  # Status FAILED, EXPIRED, or DELETED but only FAILED should occur through the plugin
                    print(ERROR_MESSAGE)
                    if response["ErrorMessage"] and response["ErrorMessage"] != "N/A":
                        logging.error(response["ErrorMessage"] )
                        return {"data": {"completions": []}, "status": response["Status"], "x-amzn-requestid": None, "x-amzn-sessionid": None, "message": response["ErrorMessage"] + "Completion id: " + completion_id }
                    else:
                        logging.error("Request failed. Completion id: " + completion_id)
                        return {"data": {"completions": []}, "status": response["Status"], "x-amzn-requestid": None, "x-amzn-sessionid": None, "message": ERROR_MESSAGE + "Completion id: " + completion_id}
        except ClientError as e:
            logging.error(e.response["Error"]["Message"])
            # Prevents a null pointer exception
            return {"data": {"completions": []}, "status": "CLIENT_ERR", "x-amzn-requestid": None, "x-amzn-sessionid": None, "message": e.response["Error"]["Message"] }#