import os
import json
import logging
from abc import ABC

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

import tornado
from tornado.web import StaticFileHandler
from amazon_q_developer_jupyterlab_ext.env import Environment
from amazon_q_developer_jupyterlab_ext.client.codewhisperer import (CodeWhispererIamClientManager,
                                                                    CodeWhispererSsoClientManager,
                                                                    MDCodeWhispererSSOClientConfig,
                                                                    JupyterOSSCodeWhispererSSOClientConfig,
                                                                    CodeWhispererIAMClientConfig,
                                                                    SageMakerCodeWhispererSSOClientConfig)
from amazon_q_developer_jupyterlab_ext.client.telemetry import ToolkitTelemetry
from amazon_q_developer_jupyterlab_ext.utils import ServiceResponse, ServiceResponseStatus, ServiceErrorInfo
from amazon_q_developer_jupyterlab_ext.validator import InputValidator
from amazon_q_developer_jupyterlab_ext.auth.sso_auth_manager import CodeWhispererSsoAuthManager
from amazon_q_developer_jupyterlab_ext.client.glue.client import GlueClient
from importlib import metadata

logging.basicConfig(format="%(levelname)s: %(message)s")

toolkit_telemetry_api = ToolkitTelemetry()
authManager = CodeWhispererSsoAuthManager()


class RecommendationHandler(APIHandler, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_validator = InputValidator()

    @staticmethod
    def get_codewhisperer_client(environment):
        if environment == Environment.MD_IDC:
            return CodeWhispererSsoClientManager(MDCodeWhispererSSOClientConfig())
        elif environment == Environment.MD_SAML:
            return CodeWhispererIamClientManager(CodeWhispererIAMClientConfig())
        elif environment == Environment.JUPYTER_OSS:
            return CodeWhispererSsoClientManager(JupyterOSSCodeWhispererSSOClientConfig())
        elif environment == Environment.SM_STUDIO_SSO:
            return CodeWhispererSsoClientManager(SageMakerCodeWhispererSSOClientConfig())
        else:
            return CodeWhispererIamClientManager(CodeWhispererIAMClientConfig())

    @tornado.web.authenticated
    async def post(self):
        input_data = self.get_json_body()
        environment_cfg = await Environment.get_environment()
        codewhisperer_client = self.get_codewhisperer_client(environment_cfg.env)
        current_version = metadata.version("amazon-q-developer-jupyterlab-ext")
        logging.info(current_version)
        try:
            if not self.input_validator.is_valid_input("generate_recommendations", input_data):
                self.set_status(400)
                await self.finish(json.dumps({'success': False,  'message': 'Invalid input data.'}))
                return
            opt_out = self.request.headers['OptOut']
            existing_user_agent = self.request.headers.get('User-Agent', '')
            self.request.headers['User-Agent'] = f"{existing_user_agent} Amazon Q For Jupyter Lab 4-{current_version}/{environment_cfg.env}"
            resp = await codewhisperer_client.generate_recommendations(self.request.headers, input_data, opt_out == 'True')
            await self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            logging.warning(f"Unexpected error while generating recommendations: {e}", exc_info=True)
            return_server_error(self)


class RegisterClientHandler(APIHandler, ABC):
    @tornado.web.authenticated
    async def get(self):
        try:
            resp = await authManager.register_client()
            await self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class DeviceAuthorizationHandler(APIHandler, ABC):
    @tornado.web.authenticated
    async def post(self):
        try:
            input_data = self.get_json_body()
            resp = await authManager.device_authorization(input_data)
            await self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class CreateTokenHandler(APIHandler, ABC):
    @tornado.web.authenticated
    async def post(self):
        try:
            input_data = self.get_json_body()
            resp = await authManager.create_token(
                input_data['clientRegistration'],
                input_data['deviceAuthorizationResponse']
            )
            if resp is None:
                await self.finish(json.dumps(resp))
            else:
                await self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class RefreshHandler(APIHandler, ABC):
    @tornado.web.authenticated
    async def post(self):
        try:
            input_data = self.get_json_body()
            resp = await authManager.refresh(input_data['clientRegistration'], input_data['token'])
            await self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            return_server_error(self)


class CancelLoginHandler(APIHandler, ABC):
    @tornado.web.authenticated
    def get(self):
        try:
            authManager.cancel_login()
            self.finish()
        except Exception as e:
            return_server_error(self)

class PostMetricsHandler(APIHandler, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @tornado.web.authenticated
    async def post(self):
        input_data = self.get_json_body()
        logging.info("input data: ", input_data)
        environment_cfg = await Environment.get_environment()
        await toolkit_telemetry_api.post_metrics(input_data, environment_cfg.env)


class GetEnvironmentHandler(APIHandler, ABC):
    @tornado.web.authenticated
    async def get(self):
        update_notification, latest_version = await Environment.get_update_notification()
        environment_cfg = await Environment.get_environment()
        await self.finish(json.dumps(ServiceResponse(
            ServiceResponseStatus.SUCCESS,
            {
                'environment': environment_cfg.env,
                'q_enabled': environment_cfg.q_enabled,
                'version_notification': update_notification,
                'latest_version': latest_version
            },
            None,
            None,
            None
        ).__dict__))

class ClearEnvironmentCacheHandler(APIHandler, ABC):
    @tornado.web.authenticated
    async def post(self): 
        logging.info("clearing env cache on page load")
        await Environment.clear_env_cache()

class GlueQueryHandler(APIHandler, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.glue_client = GlueClient()

    @tornado.web.authenticated
    async def post(self):
        input_data = self.get_json_body()
        try:
            resp = await self.glue_client.query(input_data["Prompt"]) 
            await self.finish(json.dumps(resp)) 
        except Exception as e:
            logging.warning(f"Unexpected error while generating Glue recommendations: {e}", exc_info=True)


class ListAvailableCustomizationsHandler(APIHandler, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = CodeWhispererSsoClientManager(SageMakerCodeWhispererSSOClientConfig())

    @tornado.web.authenticated
    async def post(self):
        try:
            current_version = metadata.version("amazon-q-developer-jupyterlab-ext")
            env_cfg = await Environment.get_environment()
            env = env_cfg.env
            
            existing_user_agent = self.request.headers.get('User-Agent', '')
            self.request.headers['User-Agent'] = f"{existing_user_agent} Amazon Q For Jupyter Lab 4-{current_version}/{env}"

            if env in [Environment.SM_STUDIO_SSO, Environment.MD_IDC]:
                resp = await self.client.list_available_customizations(self.request.headers, {})
                await self.finish(json.dumps(resp.__dict__))
            else:
                # this would be a rare case. listAvailableCustomizations will only be called in SSO env
                self.set_status(400)
                resp = ServiceResponse(ServiceResponseStatus.ERROR, None, ServiceErrorInfo('InvalidEnvironment', 'Invalid environment.'), None, None)
                await self.finish(json.dumps(resp.__dict__))
        except Exception as e:
            logging.warning(f"Unexpected error while listing customizations: {e}", exc_info=True)
            # always return a ServiceResponse object
            self.set_status(500)
            resp = ServiceResponse(
                ServiceResponseStatus.ERROR,
                None,
                ServiceErrorInfo('InternalServerException', str(e)),
                None,
                None
            )
            await self.finish(json.dumps(resp.__dict__))

def setup_handlers(web_app, url_path):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    # Prepend the base_url so that it works in a JupyterHub setting
    generate_recommendations_pattern = url_path_join(base_url, url_path, "generate_recommendations")
    register_client_pattern = url_path_join(base_url, url_path, "register_client")
    device_authorization_pattern = url_path_join(base_url, url_path, "device_authorization")
    create_token = url_path_join(base_url, url_path, "create_token")
    refresh_pattern = url_path_join(base_url, url_path, "refresh")
    cancel_login_pattern = url_path_join(base_url, url_path, "cancel_login")
    post_metrics_pattern = url_path_join(base_url, url_path, "post_metrics")
    get_environment_pattern = url_path_join(base_url, url_path, "get_environment")
    clear_environment_cache_pattern = url_path_join(base_url, url_path, "clear_environment_cache")
    glue_query_pattern = url_path_join(base_url, url_path, "query")
    list_available_customizations = url_path_join(base_url, url_path, "list_available_customizations")

    handlers = [(generate_recommendations_pattern, RecommendationHandler),
                (register_client_pattern, RegisterClientHandler),
                (device_authorization_pattern, DeviceAuthorizationHandler),
                (create_token, CreateTokenHandler),
                (refresh_pattern, RefreshHandler),
                (cancel_login_pattern, CancelLoginHandler),
                (post_metrics_pattern, PostMetricsHandler),
                (get_environment_pattern, GetEnvironmentHandler),
                (clear_environment_cache_pattern, ClearEnvironmentCacheHandler),
                (glue_query_pattern, GlueQueryHandler),
                (list_available_customizations, ListAvailableCustomizationsHandler)]
    web_app.add_handlers(host_pattern, handlers)

    # Prepend the base_url so that it works in a JupyterHub setting
    doc_url = url_path_join(base_url, url_path, "public")
    doc_dir = os.getenv(
        "JLAB_SERVER_EXAMPLE_STATIC_DIR",
        os.path.join(os.path.dirname(__file__), "public"),
    )
    handlers = [("{}/(.*)".format(doc_url), StaticFileHandler, {"path": doc_dir})]
    web_app.add_handlers(".*$", handlers)


def return_server_error(api_handler):
    api_handler.set_status(500)
    api_handler.finish(json.dumps(ServiceResponse(
        ServiceResponseStatus.ERROR,
        None,
        ServiceErrorInfo('InternalServerException', 'Internal server error. Try again later'),
        None,
        None
    ).__dict__))
