from abc import ABC
import logging
from botocore import client
from amazon_q_developer_jupyterlab_ext.client.codewhisperer.client_manager import CodeWhispererClientManager
from amazon_q_developer_jupyterlab_ext.constants import (
    RTS_PROD_ENDPOINT,
    RTS_PROD_REGION,
    SIGV4
)

logging.basicConfig(format="%(levelname)s: %(message)s")


class CodeWhispererIamClientManager(CodeWhispererClientManager, ABC):

    def __init__(self, client_config):
        super().__init__(client_config)

        self.cfg = client.Config(
            connect_timeout=self.CONNECT_TIMEOUT_IN_SEC,
            read_timeout=self.READ_TIMEOUT_IN_SEC,
            retries={"total_max_attempts": 2},
            user_agent=self._user_agent
        )

    def get_client(self):
        return self.session.create_client(
            service_name=SIGV4,
            endpoint_url=RTS_PROD_ENDPOINT,
            region_name=RTS_PROD_REGION,
            verify=False,
            config=self.cfg
        )

    async def invoke_recommendations(self, request_headers, request, opt_out):
        self._user_agent = request_headers.get('User-Agent', '')
        self.cfg = client.Config(
            connect_timeout=self.CONNECT_TIMEOUT_IN_SEC,
            read_timeout=self.READ_TIMEOUT_IN_SEC,
            retries={"total_max_attempts": 2},
            user_agent=self._user_agent
        )
        async with self.get_client() as iam_client:
            return await iam_client.generate_recommendations(**request)
