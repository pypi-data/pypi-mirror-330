from abc import ABC
from amazon_q_developer_jupyterlab_ext.client.codewhisperer.client_config import CodeWhispererClientConfig


class CodeWhispererSSOStrategy:
    """
    Enumeration class representing different strategies for Single Sign-On (SSO) authentication.
    """
    HEADER = "header"
    COOKIE = "cookie"
    FILE = "file"


class CodeWhispererSSOClientConfig(CodeWhispererClientConfig, ABC):
    """
    Abstract base class for CodeWhisperer client configurations that use Single Sign-On (SSO) authentication.
    """
    def __init__(self, auth_z_strategy, q_dev_profile_strategy):
        """
        Initializes an instance of CodeWhispererSSOClientConfig.

        Args:
            auth_z_strategy (CodeWhispererSSOStrategy): The strategy for obtaining the authorization token.
            q_dev_profile_strategy (CodeWhispererSSOStrategy): The strategy for obtaining the developer profile.
        """
        self.auth_z_strategy = auth_z_strategy
        self.q_dev_profile_strategy = q_dev_profile_strategy


class MDCodeWhispererSSOClientConfig(CodeWhispererSSOClientConfig, ABC):
    """
    Concrete implementation of CodeWhispererSSOClientConfig for MD SSO authentication.
    """
    def __init__(self):
        super().__init__(CodeWhispererSSOStrategy.FILE, CodeWhispererSSOStrategy.FILE)


class SageMakerCodeWhispererSSOClientConfig(CodeWhispererSSOClientConfig, ABC):
    """
    Concrete implementation of CodeWhispererSSOClientConfig for SageMaker SSO authentication.
    """
    def __init__(self):
        super().__init__(CodeWhispererSSOStrategy.FILE, CodeWhispererSSOStrategy.FILE)


class JupyterOSSCodeWhispererSSOClientConfig(CodeWhispererSSOClientConfig, ABC):
    """
    Concrete implementation of CodeWhispererSSOClientConfig for Jupyter OSS SSO authentication.
    """
    def __init__(self):
        super().__init__(CodeWhispererSSOStrategy.HEADER, None)
