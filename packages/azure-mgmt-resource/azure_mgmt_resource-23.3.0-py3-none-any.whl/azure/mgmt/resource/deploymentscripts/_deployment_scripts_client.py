# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from typing import Any, Optional, TYPE_CHECKING
from typing_extensions import Self

from azure.core.pipeline import policies
from azure.mgmt.core import ARMPipelineClient
from azure.mgmt.core.policies import ARMAutoResourceProviderRegistrationPolicy
from azure.profiles import KnownProfiles, ProfileDefinition
from azure.profiles.multiapiclient import MultiApiClientMixin

from ._configuration import DeploymentScriptsClientConfiguration
from ._serialization import Deserializer, Serializer

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials import TokenCredential

class _SDKClient(object):
    def __init__(self, *args, **kwargs):
        """This is a fake class to support current implemetation of MultiApiClientMixin."
        Will be removed in final version of multiapi azure-core based client
        """
        pass

class DeploymentScriptsClient(MultiApiClientMixin, _SDKClient):
    """The APIs listed in this specification can be used to manage Deployment Scripts resource through the Azure Resource Manager.

    This ready contains multiple API versions, to help you deal with all of the Azure clouds
    (Azure Stack, Azure Government, Azure China, etc.).
    By default, it uses the latest API version available on public Azure.
    For production, you should stick to a particular api-version and/or profile.
    The profile sets a mapping between an operation group and its API version.
    The api-version parameter sets the default API version if the operation
    group is not described in the profile.

    :param credential: Credential needed for the client to connect to Azure. Required.
    :type credential: ~azure.core.credentials.TokenCredential
    :param subscription_id: Subscription Id which forms part of the URI for every service call. Required.
    :type subscription_id: str
    :param api_version: API version to use if no profile is provided, or if missing in profile.
    :type api_version: str
    :param base_url: Service URL
    :type base_url: str
    :param profile: A profile definition, from KnownProfiles to dict.
    :type profile: azure.profiles.KnownProfiles
    :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
    """

    DEFAULT_API_VERSION = '2023-08-01'
    _PROFILE_TAG = "azure.mgmt.resource.deploymentscripts.DeploymentScriptsClient"
    LATEST_PROFILE = ProfileDefinition({
        _PROFILE_TAG: {
            None: DEFAULT_API_VERSION,
        }},
        _PROFILE_TAG + " latest"
    )

    def __init__(
        self,
        credential: "TokenCredential",
        subscription_id: str,
        api_version: Optional[str]=None,
        base_url: str = "https://management.azure.com",
        profile: KnownProfiles=KnownProfiles.default,
        **kwargs: Any
    ):
        if api_version:
            kwargs.setdefault('api_version', api_version)
        self._config = DeploymentScriptsClientConfiguration(credential, subscription_id, **kwargs)
        _policies = kwargs.pop("policies", None)
        if _policies is None:
            _policies = [
                policies.RequestIdPolicy(**kwargs),
                self._config.headers_policy,
                self._config.user_agent_policy,
                self._config.proxy_policy,
                policies.ContentDecodePolicy(**kwargs),
                ARMAutoResourceProviderRegistrationPolicy(),
                self._config.redirect_policy,
                self._config.retry_policy,
                self._config.authentication_policy,
                self._config.custom_hook_policy,
                self._config.logging_policy,
                policies.DistributedTracingPolicy(**kwargs),
                policies.SensitiveHeaderCleanupPolicy(**kwargs) if self._config.redirect_policy else None,
                self._config.http_logging_policy,
            ]
        self._client: ARMPipelineClient = ARMPipelineClient(base_url=base_url, policies=_policies, **kwargs)
        super(DeploymentScriptsClient, self).__init__(
            api_version=api_version,
            profile=profile
        )

    @classmethod
    def _models_dict(cls, api_version):
        return {k: v for k, v in cls.models(api_version).__dict__.items() if isinstance(v, type)}

    @classmethod
    def models(cls, api_version=DEFAULT_API_VERSION):
        """Module depends on the API version:

           * 2019-10-01-preview: :mod:`v2019_10_01_preview.models<azure.mgmt.resource.deploymentscripts.v2019_10_01_preview.models>`
           * 2020-10-01: :mod:`v2020_10_01.models<azure.mgmt.resource.deploymentscripts.v2020_10_01.models>`
           * 2023-08-01: :mod:`v2023_08_01.models<azure.mgmt.resource.deploymentscripts.v2023_08_01.models>`
        """
        if api_version == '2019-10-01-preview':
            from .v2019_10_01_preview import models
            return models
        elif api_version == '2020-10-01':
            from .v2020_10_01 import models
            return models
        elif api_version == '2023-08-01':
            from .v2023_08_01 import models
            return models
        raise ValueError("API version {} is not available".format(api_version))

    @property
    def deployment_scripts(self):
        """Instance depends on the API version:

           * 2019-10-01-preview: :class:`DeploymentScriptsOperations<azure.mgmt.resource.deploymentscripts.v2019_10_01_preview.operations.DeploymentScriptsOperations>`
           * 2020-10-01: :class:`DeploymentScriptsOperations<azure.mgmt.resource.deploymentscripts.v2020_10_01.operations.DeploymentScriptsOperations>`
           * 2023-08-01: :class:`DeploymentScriptsOperations<azure.mgmt.resource.deploymentscripts.v2023_08_01.operations.DeploymentScriptsOperations>`
        """
        api_version = self._get_api_version('deployment_scripts')
        if api_version == '2019-10-01-preview':
            from .v2019_10_01_preview.operations import DeploymentScriptsOperations as OperationClass
        elif api_version == '2020-10-01':
            from .v2020_10_01.operations import DeploymentScriptsOperations as OperationClass
        elif api_version == '2023-08-01':
            from .v2023_08_01.operations import DeploymentScriptsOperations as OperationClass
        else:
            raise ValueError("API version {} does not have operation group 'deployment_scripts'".format(api_version))
        self._config.api_version = api_version
        return OperationClass(self._client, self._config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)), api_version)

    def close(self):
        self._client.close()
    def __enter__(self):
        self._client.__enter__()
        return self
    def __exit__(self, *exc_details):
        self._client.__exit__(*exc_details)
