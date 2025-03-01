import tornado.gen
from aiobotocore.session import get_session
from botocore import UNSIGNED, client
from botocore.exceptions import ClientError
from amazon_q_developer_jupyterlab_ext.constants import CLIENT_REGISTRATION_TYPE, CLIENT_NAME, SCOPES, \
    START_URL, DEVICE_GRANT_TYPE, REFRESH_GRANT_TYPE, SSO_OIDC, OIDC_BUILDER_ID_ENDPOINT, OIDC_BUILDER_ID_REGION
from amazon_q_developer_jupyterlab_ext.utils import generate_succeeded_service_response, generate_client_error_oidc_service_response


class CodeWhispererSsoAuthManager:
    _instance = None
    login_cancelled = False

    def __init__(self):
        self.session = get_session()
        self.cfg = client.Config(
            signature_version=UNSIGNED
        )

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_client(self):
        return self.session.create_client(
            service_name=SSO_OIDC,
            endpoint_url=OIDC_BUILDER_ID_ENDPOINT,
            region_name=OIDC_BUILDER_ID_REGION,
            config=self.cfg
        )

    async def refresh(self, client_registration, token):
        try:
            async with self.get_client() as oidc_client:
                new_token_response = await oidc_client.create_token(
                    clientId=client_registration['clientId'],
                    clientSecret=client_registration['clientSecret'],
                    grantType=REFRESH_GRANT_TYPE,
                    refreshToken=token['refreshToken']
                )
            return generate_succeeded_service_response(new_token_response)
        except ClientError as e:
            return generate_client_error_oidc_service_response(e)

    async def register_client(self):
        try:
            async with self.get_client() as oidc_client:
                client_registration_response = await oidc_client.register_client(
                    clientName=CLIENT_NAME,
                    clientType=CLIENT_REGISTRATION_TYPE,
                    scopes=SCOPES
                )
            return generate_succeeded_service_response(client_registration_response)
        except ClientError as e:
            return generate_client_error_oidc_service_response(e)

    async def device_authorization(self, client_registration):
        try:
            async with self.get_client() as oidc_client:
                device_authorization_response = await oidc_client.start_device_authorization(
                    clientId=client_registration['clientId'],
                    clientSecret=client_registration['clientSecret'],
                    startUrl=START_URL
                )
            return generate_succeeded_service_response(device_authorization_response)
        except ClientError as e:
            return generate_client_error_oidc_service_response(e)

    async def create_token(self, client_registration, device_authorization):
        device_code = device_authorization['deviceCode']
        expires_in = device_authorization['expiresIn']
        interval = device_authorization['interval']

        for n in range(1, expires_in // interval + 1):
            if self.login_cancelled:
                self.login_cancelled = False
                return None
            await tornado.gen.sleep(interval)
            async with self.get_client() as oidc_client:
                try:
                    token_response = await oidc_client.create_token(
                        grantType=DEVICE_GRANT_TYPE,
                        deviceCode=device_code,
                        clientId=client_registration['clientId'],
                        clientSecret=client_registration['clientSecret']
                    )
                    return generate_succeeded_service_response(token_response)
                except oidc_client.exceptions.AuthorizationPendingException as e:
                    pass
                except ClientError as e:
                    return generate_client_error_oidc_service_response(e)

    def cancel_login(self):
        self.login_cancelled = True
