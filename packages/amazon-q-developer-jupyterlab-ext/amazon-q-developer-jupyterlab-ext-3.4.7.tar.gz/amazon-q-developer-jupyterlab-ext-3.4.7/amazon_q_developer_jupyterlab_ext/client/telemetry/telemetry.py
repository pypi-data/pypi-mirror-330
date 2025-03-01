import logging

from aiobotocore.session import get_session
from botocore import client
from botocore.exceptions import ClientError
from pathlib import Path
from amazon_q_developer_jupyterlab_ext.constants import (
    MD_NOTEBOOK,
    PROD_COGNITO_POOL_ID,
    INVALID_TOKEN_EXCEPTION_MESSAGE,
    TELEMETRY_PROD_ENDPOINT,
    PostMetricsRequestConstants,
)
from amazon_q_developer_jupyterlab_ext.env.environment import Environment

logging.basicConfig(format="%(levelname)s: %(message)s")


class ToolkitTelemetry:

    READ_TIMEOUT_IN_SEC = 15
    CONNECT_TIMEOUT_IN_SEC = 5
    _credentials = None

    def __init__(self):
        self.identity_id = None
        self.session = get_session()
        self.cfg = client.Config(
            connect_timeout=self.CONNECT_TIMEOUT_IN_SEC,
            read_timeout=self.READ_TIMEOUT_IN_SEC,
            retries={"total_max_attempts": 2},
        )
        session_folder = f"{Path(__file__).parent.parent}/service_models"
        self.session.get_component('data_loader').search_paths.append(session_folder)

    def _get_cognito_client(self):
        return self.session.create_client(
            service_name="cognito-identity",
            region_name="us-east-1",
            config=self.cfg,
        )

    def _get_telemetry_client(self):
        return self.session.create_client(
            service_name="telemetry",
            region_name="us-east-1",
            endpoint_url=TELEMETRY_PROD_ENDPOINT,
            aws_access_key_id=self._credentials["AccessKeyId"],
            aws_secret_access_key=self._credentials["SecretKey"],
            aws_session_token=self._credentials["SessionToken"],
            config=self.cfg,
        )

    async def _setup_credentials(self):
        async with self._get_cognito_client() as cognito_client:
            self.identity_id = (await cognito_client.get_id(
                IdentityPoolId=PROD_COGNITO_POOL_ID
            ))["IdentityId"]
            self._credentials = (await cognito_client.get_credentials_for_identity(
                IdentityId=self.identity_id
            ))["Credentials"]

        self.credential_expire_time = self._credentials["Expiration"]

    async def post_metrics(self, request, parent_product):
        try:
            if not self._credentials:
                await self._setup_credentials()
            logging.info(request["ClientID"])
            logging.info(request["MetricData"][0]["EpochTimestamp"])
            # Append Notebook to MD environment since it is a Notebook environment.
            if parent_product == Environment.MD_IDC or parent_product == Environment.MD_IAM or Environment.MD_SAML:
                parent_product = MD_NOTEBOOK
                logging.info(f"Reset parent product to {parent_product}")
            async with self._get_telemetry_client() as telemetry_client:
                await telemetry_client.post_metrics(
                    AWSProduct=request[PostMetricsRequestConstants.AWS_PRODUCT],
                    AWSProductVersion=request[
                        PostMetricsRequestConstants.AWS_PRODUCT_VERSION
                    ],
                    ClientID=request[PostMetricsRequestConstants.CLIENT_ID],
                    MetricData=request[PostMetricsRequestConstants.METRIC_DATA],
                    ParentProduct=parent_product,
                )
            logging.info("sent telemetry")
        except ClientError as e:
            if INVALID_TOKEN_EXCEPTION_MESSAGE in e.response["Error"]["Message"]:
                logging.info("refreshing credentials")
                await self._refresh_credentials()
                async with self._get_telemetry_client() as telemetry_client:
                    await telemetry_client.post_metrics(
                        AWSProduct=request[PostMetricsRequestConstants.AWS_PRODUCT],
                        AWSProductVersion=request[
                            PostMetricsRequestConstants.AWS_PRODUCT_VERSION
                        ],
                        ClientID=request[PostMetricsRequestConstants.CLIENT_ID],
                        MetricData=request[PostMetricsRequestConstants.METRIC_DATA],
                        ParentProduct=parent_product,
                    )
            else:
                logging.error(e.response["Error"]["Message"])
                return
        except Exception as e:
            logging.warning(f"Logging telemetry error and ignoring exception {e}", exc_info=True)

    async def _refresh_credentials(self):
        async with self._get_cognito_client() as cognito_client:
            self._credentials = (await cognito_client.get_credentials_for_identity(
                IdentityId=self.identity_id
            ))["Credentials"]

        # TODO: can use expire time to refresh
        # self.credential_expire_time = credentials["Expiration"]
