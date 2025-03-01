from abc import ABC
from amazon_q_developer_jupyterlab_ext.client.codewhisperer.client_config import CodeWhispererClientConfig


class CodeWhispererIAMClientConfig(CodeWhispererClientConfig, ABC):

    def __init__(self):
        """
         Initializes an instance of CodeWhispererIAMClientConfig that use IAM authentication.
        """
        pass
