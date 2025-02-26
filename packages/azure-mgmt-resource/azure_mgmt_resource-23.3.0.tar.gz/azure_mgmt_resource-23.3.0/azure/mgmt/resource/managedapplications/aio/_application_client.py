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
from azure.mgmt.core import AsyncARMPipelineClient
from azure.mgmt.core.policies import AsyncARMAutoResourceProviderRegistrationPolicy
from azure.profiles import KnownProfiles, ProfileDefinition
from azure.profiles.multiapiclient import MultiApiClientMixin

from .._serialization import Deserializer, Serializer
from ._configuration import ApplicationClientConfiguration
from ._operations_mixin import ApplicationClientOperationsMixin

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials_async import AsyncTokenCredential

class _SDKClient(object):
    def __init__(self, *args, **kwargs):
        """This is a fake class to support current implemetation of MultiApiClientMixin."
        Will be removed in final version of multiapi azure-core based client
        """
        pass

class ApplicationClient(ApplicationClientOperationsMixin, MultiApiClientMixin, _SDKClient):
    """ARM applications.

    This ready contains multiple API versions, to help you deal with all of the Azure clouds
    (Azure Stack, Azure Government, Azure China, etc.).
    By default, it uses the latest API version available on public Azure.
    For production, you should stick to a particular api-version and/or profile.
    The profile sets a mapping between an operation group and its API version.
    The api-version parameter sets the default API version if the operation
    group is not described in the profile.

    :param credential: Credential needed for the client to connect to Azure. Required.
    :type credential: ~azure.core.credentials_async.AsyncTokenCredential
    :param subscription_id: The ID of the target subscription. Required.
    :type subscription_id: str
    :param api_version: API version to use if no profile is provided, or if missing in profile.
    :type api_version: str
    :param base_url: Service URL
    :type base_url: str
    :param profile: A profile definition, from KnownProfiles to dict.
    :type profile: azure.profiles.KnownProfiles
    :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
    """

    DEFAULT_API_VERSION = '2019-07-01'
    _PROFILE_TAG = "azure.mgmt.resource.managedapplications.ApplicationClient"
    LATEST_PROFILE = ProfileDefinition({
        _PROFILE_TAG: {
            None: DEFAULT_API_VERSION,
        }},
        _PROFILE_TAG + " latest"
    )

    def __init__(
        self,
        credential: "AsyncTokenCredential",
        subscription_id: str,
        api_version: Optional[str] = None,
        base_url: str = "https://management.azure.com",
        profile: KnownProfiles = KnownProfiles.default,
        **kwargs: Any
    ) -> None:
        if api_version:
            kwargs.setdefault('api_version', api_version)
        self._config = ApplicationClientConfiguration(credential, subscription_id, **kwargs)
        _policies = kwargs.pop("policies", None)
        if _policies is None:
            _policies = [
                policies.RequestIdPolicy(**kwargs),
                self._config.headers_policy,
                self._config.user_agent_policy,
                self._config.proxy_policy,
                policies.ContentDecodePolicy(**kwargs),
                AsyncARMAutoResourceProviderRegistrationPolicy(),
                self._config.redirect_policy,
                self._config.retry_policy,
                self._config.authentication_policy,
                self._config.custom_hook_policy,
                self._config.logging_policy,
                policies.DistributedTracingPolicy(**kwargs),
                policies.SensitiveHeaderCleanupPolicy(**kwargs) if self._config.redirect_policy else None,
                self._config.http_logging_policy,
            ]
        self._client: AsyncARMPipelineClient = AsyncARMPipelineClient(base_url=base_url, policies=_policies, **kwargs)
        super(ApplicationClient, self).__init__(
            api_version=api_version,
            profile=profile
        )

    @classmethod
    def _models_dict(cls, api_version):
        return {k: v for k, v in cls.models(api_version).__dict__.items() if isinstance(v, type)}

    @classmethod
    def models(cls, api_version=DEFAULT_API_VERSION):
        """Module depends on the API version:

           * 2019-07-01: :mod:`v2019_07_01.models<azure.mgmt.resource.managedapplications.v2019_07_01.models>`
        """
        if api_version == '2019-07-01':
            from ..v2019_07_01 import models
            return models
        raise ValueError("API version {} is not available".format(api_version))

    @property
    def application_definitions(self):
        """Instance depends on the API version:

           * 2019-07-01: :class:`ApplicationDefinitionsOperations<azure.mgmt.resource.managedapplications.v2019_07_01.aio.operations.ApplicationDefinitionsOperations>`
        """
        api_version = self._get_api_version('application_definitions')
        if api_version == '2019-07-01':
            from ..v2019_07_01.aio.operations import ApplicationDefinitionsOperations as OperationClass
        else:
            raise ValueError("API version {} does not have operation group 'application_definitions'".format(api_version))
        self._config.api_version = api_version
        return OperationClass(self._client, self._config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)), api_version)

    @property
    def applications(self):
        """Instance depends on the API version:

           * 2019-07-01: :class:`ApplicationsOperations<azure.mgmt.resource.managedapplications.v2019_07_01.aio.operations.ApplicationsOperations>`
        """
        api_version = self._get_api_version('applications')
        if api_version == '2019-07-01':
            from ..v2019_07_01.aio.operations import ApplicationsOperations as OperationClass
        else:
            raise ValueError("API version {} does not have operation group 'applications'".format(api_version))
        self._config.api_version = api_version
        return OperationClass(self._client, self._config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)), api_version)

    @property
    def jit_requests(self):
        """Instance depends on the API version:

           * 2019-07-01: :class:`JitRequestsOperations<azure.mgmt.resource.managedapplications.v2019_07_01.aio.operations.JitRequestsOperations>`
        """
        api_version = self._get_api_version('jit_requests')
        if api_version == '2019-07-01':
            from ..v2019_07_01.aio.operations import JitRequestsOperations as OperationClass
        else:
            raise ValueError("API version {} does not have operation group 'jit_requests'".format(api_version))
        self._config.api_version = api_version
        return OperationClass(self._client, self._config, Serializer(self._models_dict(api_version)), Deserializer(self._models_dict(api_version)), api_version)

    async def close(self):
        await self._client.close()
    async def __aenter__(self):
        await self._client.__aenter__()
        return self
    async def __aexit__(self, *exc_details):
        await self._client.__aexit__(*exc_details)
