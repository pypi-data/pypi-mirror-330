CODEWHISPERER_PYPI_JSON_URL = "https://pypi.org/pypi/amazon-q-developer-jupyterlab-ext/json"

TELEMETRY_PROD_ENDPOINT = "https://client-telemetry.us-east-1.amazonaws.com"
PROD_COGNITO_POOL_ID = "us-east-1:820fd6d1-95c0-4ca4-bffb-3f01d32da842"

INVALID_TOKEN_EXCEPTION_MESSAGE = "The security token included in the request is expired"
RTS_PROD_ENDPOINT = "https://codewhisperer.us-east-1.amazonaws.com/"
RTS_PROD_REGION = "us-east-1"

DUMMY_AUTH_TOKEN = "xx"
SIGV4 = "sigv4"
BEARER = "bearer"
RESPONSE_SESSION_ID_HEADER_NAME = "x-amzn-sessionid"
REQUEST_OPTOUT_HEADER_NAME="x-amzn-codewhisperer-optout"


class PostMetricsRequestConstants:
    AWS_PRODUCT = "AWSProduct"
    AWS_PRODUCT_VERSION = "AWSProductVersion"
    CLIENT_ID = "ClientID"
    METRIC_DATA = "MetricData"


# TODO: add more mapping from a specific (error_code, error_message) combo to a user-friendly error message
ERROR_CODE_TO_USER_MESSAGE_MAP = {
    'InvalidGrantException: Invalid grant provided': 'InvalidGrantException: Login failed. Try login again later.'
}

NEW_VERSION_USER_MESSAGE = "New version of Amazon Q Developer -  v{} is available! Update now to enjoy the latest features and improvements."
SAGEMAKER_CONNECT_ERROR = "Cannot connect to Amazon Q Developer services, please make sure that the domain has internet access or a VPC Endpoint for AWS Q Developer if using a VPCOnly domain."

START_URL = "https://view.awsapps.com/start"
SSO_OIDC = "sso-oidc"
OIDC_BUILDER_ID_ENDPOINT = "https://oidc.us-east-1.amazonaws.com"
OIDC_BUILDER_ID_REGION = "us-east-1"
SCOPES = ["codewhisperer:completions"]
CLIENT_NAME = "Amazon Q Developer for JupyterLab"
CLIENT_REGISTRATION_TYPE = "public"
DEVICE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
REFRESH_GRANT_TYPE = "refresh_token"
SM_STUDIO_ENV_NAME = "SageMaker Studio"
JUPYTER_OSS_ENV_NAME = "Jupyter OSS"

# The environment variable to identify which instance is this (e.g. Glue Studio Notebook or SageMaker Studio)
CONSUMER_ENV_KEY = "CONSUMER_ID"
CONSUMER_ENV_VALUE_GLUE_STUDIO = "GlueStudioNotebook"
MD_NOTEBOOK = "MD Notebook"