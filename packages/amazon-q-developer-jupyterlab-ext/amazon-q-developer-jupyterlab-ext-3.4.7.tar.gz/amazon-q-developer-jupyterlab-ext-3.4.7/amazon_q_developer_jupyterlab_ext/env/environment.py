import json
import logging
import os

import aiohttp
from aiohttp import ClientTimeout
from packaging.version import Version
from amazon_q_developer_jupyterlab_ext.client.sagemaker.client import get_sagemaker_client
from amazon_q_developer_jupyterlab_ext.constants import CODEWHISPERER_PYPI_JSON_URL, NEW_VERSION_USER_MESSAGE, \
    CONSUMER_ENV_KEY, CONSUMER_ENV_VALUE_GLUE_STUDIO
from importlib import metadata

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class Environment:
    SM_STUDIO = "SageMaker Studio"
    SM_STUDIO_SSO = "SageMaker Studio SSO"
    JUPYTER_OSS = "Jupyter OSS"
    GLUE_STUDIO_NOTEBOOK = "Glue Studio Notebook"
    MD_IDC = "MD_IDC"
    MD_IAM = "MD_IAM"
    MD_SAML = "MD_SAML"
    _cached_env = None
    _cached_q_enabled = None

    @staticmethod
    async def get_update_notification():
        try:
            # Glue Studio environment doesn't want any update and update notification
            is_sm_studio = await Environment.is_sm_studio()
            if Environment.is_glue_studio() or is_sm_studio:
                return "", ""

            # Get the URL from environment variable or fall back to default
            url = os.environ.get("JSON_URL", CODEWHISPERER_PYPI_JSON_URL)

            # Download the JSON data
            async with aiohttp.ClientSession() as session:
                # Define the timeout duration (in seconds)
                timeout_duration = 2  # Timeout after 2 seconds

                # Create a ClientTimeout object
                timeout = ClientTimeout(total=timeout_duration)

                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()
                    data = await response.json()

            # Get the latest version and launch date
            latest_version = data["info"]["version"]

            # Compare the current version with the latest version
            if Version(latest_version) > Version(metadata.version("amazon-q-developer-jupyterlab-ext")):
                return NEW_VERSION_USER_MESSAGE.format(latest_version), latest_version
            else:
                return "", ""
        except Exception as e:
            print(f"Error: {e}")
            return "", ""

    @staticmethod
    async def get_environment():
        if Environment._cached_env is None or Environment._cached_q_enabled is None:
            logging.info("Detecting environment for the first time")
            environment_cfg = await Environment._detect_environment()
            Environment._cached_env = environment_cfg.env
            Environment._cached_q_enabled = environment_cfg.q_enabled
            env = environment_cfg.env
            logging.info(f"Environment is {env}")
        return EnvironmentConfiguration(Environment._cached_env, Environment._cached_q_enabled)
    
    @staticmethod
    async def clear_env_cache():
        Environment._cached_env = None
        Environment._cached_q_enabled = None

    @staticmethod
    async def _detect_environment():
        env = Environment.JUPYTER_OSS
        q_enabled = True
        try:
            if Environment.is_glue_studio():
                return EnvironmentConfiguration(env, q_enabled)

            with open('/opt/ml/metadata/resource-metadata.json', 'r') as f:
                data = json.load(f)
                if 'AdditionalMetadata' in data and ('AmazonDataZoneScopeName' in data['AdditionalMetadata'] or 'DataZoneScopeName' in data['AdditionalMetadata']):
                    # fetch the auth mode from amazon_q settings
                    try: 
                        with open('/home/sagemaker-user/.aws/amazon_q/settings.json') as g:
                            settings = json.load(g)
                            q_enabled = settings.get('q_enabled')
                            auth_mode = settings.get('auth_mode')
                            logging.info('Q inline auth_mode: ' + auth_mode)
                            if auth_mode == "IAM":
                                env = Environment.MD_IAM
                            elif auth_mode == "SAML":
                                env = Environment.MD_SAML
                            else:
                                env = Environment.MD_IDC
                    except: 
                        # if settings file is not available, set default to free tier enabled
                        q_enabled = True
                        env = Environment.MD_IAM
                        logging.info("Q settings could not be read")
                elif 'ResourceArn' in data:
                    sm_domain_id = data['DomainId']
                    logging.info(f"DomainId - {sm_domain_id}")
                    sm_client = get_sagemaker_client()
                    try:
                        domain_details = await sm_client.describe_domain(sm_domain_id)
                        logging.info(f"Studio domain level details: {domain_details}")
                        if (domain_details.get('AuthMode') == "SSO"
                                and (domain_details.get('DomainSettings') is not None
                                    and domain_details.get('DomainSettings').get('AmazonQSettings') is not None
                                    and domain_details.get('DomainSettings').get('AmazonQSettings').get('Status') == 'ENABLED')):
                            env = Environment.SM_STUDIO_SSO
                        else:
                            env = Environment.SM_STUDIO
                    except Exception as e:
                        logging.info(f"Failed to get Studio domain details {str(e)}")
                        env = Environment.SM_STUDIO
        except Exception as e:
            logging.error(f"Error detecting environment: {str(e)}")
        return EnvironmentConfiguration(env, q_enabled)

    @staticmethod
    def is_glue_studio():
        return CONSUMER_ENV_KEY in os.environ and os.environ.get(CONSUMER_ENV_KEY) == CONSUMER_ENV_VALUE_GLUE_STUDIO

    @staticmethod
    async def is_sm_studio():
        return (await Environment.get_environment())["env"] == Environment.SM_STUDIO
    
class EnvironmentConfiguration:
    def __init__(self, env, q_enabled):
        self.env = env 
        self.q_enabled = q_enabled

    @property
    def __dict__(self):
        return {
            'env': self.env,
            'q_enabled': self.q_enabled
        }
