import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from aiobotocore.session import get_session
from botocore.exceptions import ClientError, ConnectTimeoutError
from amazon_q_developer_jupyterlab_ext.utils import (
    generate_succeeded_service_response,
    generate_client_error_codewhisperer_service_response,
    generate_connect_error_codewhisperer_service_response, generate_client_error_response,
)
from amazon_q_developer_jupyterlab_ext.exceptions import ClientExtensionException

logging.basicConfig(format="%(levelname)s: %(message)s")

# Interface for managing lifecycles of different sdk clients.
class CodeWhispererClientManager(ABC):
    _instance = None

    READ_TIMEOUT_IN_SEC = 15
    CONNECT_TIMEOUT_IN_SEC = 5

    def __init__(self, client_config):
        self.client_config = client_config
        self.session = get_session()
        session_folder = f"{Path(__file__).parent.parent}/service_models"
        self.session.get_component('data_loader').search_paths.append(session_folder)
        self._user_agent = ""

    def __new__(cls, client_config):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    async def invoke_recommendations(self, request_headers, request, opt_out):
        pass

    async def generate_recommendations(self, request_headers, recommendation_request, opt_out):
        invocation_start_time_ms = time.time()
        try:
            recommendation_response = await self.invoke_recommendations(request_headers, recommendation_request, opt_out)
            logging.info(f"Q developer service latency in ms: {round((time.time() - invocation_start_time_ms) * 1000)}")
            return generate_succeeded_service_response(recommendation_response)
        except ClientError as e:
            return generate_client_error_codewhisperer_service_response(e)
        except ConnectTimeoutError as e:
            logging.warning(f"Cannot access Q developer service: {e}")
            return generate_connect_error_codewhisperer_service_response(e)
        except ClientExtensionException as e:
            return generate_client_error_response(e.message)
