import http.cookies
import json
import logging
import os
from abc import ABC
from botocore import UNSIGNED, client
from amazon_q_developer_jupyterlab_ext.client.codewhisperer.client_manager import CodeWhispererClientManager
from amazon_q_developer_jupyterlab_ext.client.codewhisperer.file_cache_manager import FileCacheManager
from amazon_q_developer_jupyterlab_ext.client.codewhisperer.sso_client_config import CodeWhispererSSOStrategy
from amazon_q_developer_jupyterlab_ext.constants import (
    REQUEST_OPTOUT_HEADER_NAME,
    RTS_PROD_ENDPOINT,
    RTS_PROD_REGION,
    BEARER
)
from amazon_q_developer_jupyterlab_ext.exceptions import ClientExtensionException, ServerExtensionException
from amazon_q_developer_jupyterlab_ext.utils import (
    generate_succeeded_service_response,
)

logging.basicConfig(format="%(levelname)s: %(message)s")


class CodeWhispererSsoClientManager(CodeWhispererClientManager, ABC):
    _initialized = False

    def __init__(self, client_config):
        if self._initialized:
            return
        self._initialized = True
        self._bearer_token = ""
        self._opt_out = False
        self.cfg = client.Config(
            connect_timeout=self.CONNECT_TIMEOUT_IN_SEC,
            read_timeout=self.READ_TIMEOUT_IN_SEC,
            retries={"total_max_attempts": 2},
            tcp_keepalive=True,
            signature_version=UNSIGNED
        )
        self.file_cache_manager = FileCacheManager()
        super().__init__(client_config)

    def _add_header(self, request, **kwargs):
        request.headers.add_header("Authorization", "Bearer " + self._bearer_token)
        request.headers.add_header(REQUEST_OPTOUT_HEADER_NAME, f"{self._opt_out}")
        request.headers.add_header('User-Agent',  self._user_agent)

    def get_client(self):
        return self.session.create_client(
            service_name=BEARER,
            endpoint_url=RTS_PROD_ENDPOINT,
            region_name=RTS_PROD_REGION,
            verify=True,
            config=self.cfg
        )

    async def invoke_recommendations(self, request_headers, request, opt_out):
        self._opt_out = opt_out
        self._bearer_token = self.__get_bearer_token(request_headers)
        self._user_agent = request_headers.get('User-Agent', '')
        if self.client_config.q_dev_profile_strategy:
            q_dev_profile_arn = self.__get_q_dev_profile_arn(request_headers)
            request["profileArn"] = q_dev_profile_arn

        try:
            customization_arn = self.__get_customization_arn()
        except (FileNotFoundError, ServerExtensionException):
            # If customization_arn.json is not found or the value is an empty string,
            # then we can assume that customization is not enabled
            customization_arn = None

        if customization_arn:
            request["customizationArn"] = customization_arn
        async with self.get_client() as sso_client:
            sso_client.meta.events.register_first("before-sign.*.*", self._add_header)
            return await sso_client.generate_completions(**request)

    async def list_available_customizations(self, request_headers, request):
        self._bearer_token = self.__get_bearer_token(request_headers)
        self._user_agent = request_headers.get('User-Agent', '')

        if self.client_config.q_dev_profile_strategy:
            q_dev_profile_arn = self.__get_q_dev_profile_arn(request_headers)
            request["profileArn"] = q_dev_profile_arn

        async with self.get_client() as q_sso_client:
            q_sso_client.meta.events.register_first("before-sign.*.*", self._add_header)
            response = await q_sso_client.list_available_customizations(**request)
            return generate_succeeded_service_response(response)
        
    def set_bearer_token(self, token):
        self._bearer_token = token

    def __get_bearer_token(self, request_headers):
        return self.__extractor(self.client_config.auth_z_strategy,
                               request_headers,
                               "Token",
                               "~/.aws/sso/idc_access_token.json",
                               lambda d: d["idc_access_token"])

    def __get_q_dev_profile_arn(self, request_headers):
        return self.__extractor(self.client_config.q_dev_profile_strategy,
                               request_headers,
                               "q-dev-profile-arn",
                               "~/.aws/amazon_q/q_dev_profile.json",
                               lambda d: d["q_dev_profile_arn"])
    
    def __get_customization_arn(self):
        return self.__extractor(CodeWhispererSSOStrategy.FILE,
                               {},
                               "customization_arn",
                               "~/.aws/amazon_q/customization_arn.json",
                               lambda d: d["customization_arn"])

    def __extractor(self, config, request_headers, key=None, file_path=None, value_extractor=None):
        val = None
        if config == CodeWhispererSSOStrategy.HEADER:
            val = request_headers[key]
            if val is None or not val.strip():
                raise ClientExtensionException(f"No value found for `{key}` in request headers.")
        elif config == CodeWhispererSSOStrategy.COOKIE:
            cookie = http.cookies.SimpleCookie(request_headers['Cookie'])
            cookie_dict = {key: morsel.value for key, morsel in cookie.items()}
            val = cookie_dict.get(key) or cookie_dict.get(key.replace("-", "_"))
            if val is None or not val.strip():
                raise ClientExtensionException(f"No value found for `{key}` in request cookies.")
        elif config == CodeWhispererSSOStrategy.FILE:
            content = json.loads(self.file_cache_manager.get_cached_file_content(os.path.expanduser(file_path)))
            val = value_extractor(content)
            if val is None or not val.strip():
                raise ServerExtensionException(f"No value found in {file_path}.")
        return val
