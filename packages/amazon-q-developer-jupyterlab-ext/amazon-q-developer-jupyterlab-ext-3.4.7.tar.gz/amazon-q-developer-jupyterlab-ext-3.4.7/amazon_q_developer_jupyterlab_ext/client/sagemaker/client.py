import os
from typing import Dict
from pathlib import Path
import json

import botocore
from aiobotocore.session import get_session, AioSession
from botocore.session import Session

SAGEMAKER_INTERNAL_METADATA_FILE_PATH = "/opt/.sagemakerinternal/internal-metadata.json"
LOOSELEAF_STAGE_MAPPING = {"devo": "beta", "loadtest": "gamma"}


class BaseAsyncBotoClient:
    cfg: any
    partition: str
    region_name: str
    sess: AioSession

    def __init__(self, partition: str, region_name: str):
        self.cfg = botocore.client.Config(
            connect_timeout=5,
            read_timeout=15,
            retries={"max_attempts": 2},
        )
        self.partition = partition
        self.region_name = region_name

        os.environ["AMAZON_Q_DATA_PATH"] = os.path.join(
            Path(__file__).parent.parent, "service_models"
        )
        # we want to modify the default search path for service models
        # https://github.com/boto/botocore/blob/develop/botocore/configprovider.py#L53
        self.sess = get_session(
            {"data_path": ("data_path", "AMAZON_Q_DATA_PATH", None, None)}
        )


class SageMakerAsyncBoto3Client(BaseAsyncBotoClient):
    def get_stage(self):
        try:
            with open(SAGEMAKER_INTERNAL_METADATA_FILE_PATH, "r") as file:
                data = json.load(file)
                return data.get("Stage")
        except Exception as e:
            return "prod"

    def _create_sagemaker_client(self):
        # based on the Studio domain stage, we want to choose the sagemaker endpoint
        # rest of the services will use prod stages for non prod stages
        create_client_args = {
            "service_name": "sagemaker",
            "config": self.cfg,
            "region_name": self.region_name,
        }

        stage = self.get_stage()
        if stage is not None and stage != "" and stage.lower() != "prod":
            endpoint_stage = LOOSELEAF_STAGE_MAPPING.get(stage.lower())
            create_client_args["endpoint_url"] = (
                f"https://sagemaker.{endpoint_stage}.{self.region_name}.ml-platform.aws.a2z.com"
            )

        return self.sess.create_client(**create_client_args)

    async def describe_domain(self, domain_id: str) -> Dict:
        if domain_id is None:
            return {}
        async with self._create_sagemaker_client() as sm:
            return await sm.describe_domain(DomainId=domain_id)


def get_region_name():
    # Get region config in following order:
    # 1. AWS_REGION env var
    # 2. Region from AWS config (for example, through `aws configure`)
    # 3. AWS_DEFAULT_REGION env var
    # 4. If none of above are set, use us-east-1
    region_config_chain = [
        os.environ.get("AWS_REGION"),
        Session().get_scoped_config().get("region"),
        os.environ.get("AWS_DEFAULT_REGION"),
        "us-east-1",
    ]
    for region_config in region_config_chain:
        if region_config is not None:
            return region_config


def get_partition():
    return Session().get_partition_for_region(get_region_name())


def get_sagemaker_client():
    return SageMakerAsyncBoto3Client(get_partition(), get_region_name())
