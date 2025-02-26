# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from io import IOBase
import sys
from typing import Any, Callable, Dict, IO, Optional, TypeVar, Union, overload

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import AsyncHttpResponse, HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ...operations._operations import (
    build_private_link_association_delete_request,
    build_private_link_association_get_request,
    build_private_link_association_list_request,
    build_private_link_association_put_request,
    build_resource_management_private_link_delete_request,
    build_resource_management_private_link_get_request,
    build_resource_management_private_link_list_by_resource_group_request,
    build_resource_management_private_link_list_request,
    build_resource_management_private_link_put_request,
)

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class PrivateLinkAssociationOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.resource.privatelinks.v2020_05_01.aio.ResourcePrivateLinkClient`'s
        :attr:`private_link_association` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")
        self._api_version = input_args.pop(0) if input_args else kwargs.pop("api_version")

    @overload
    async def put(
        self,
        group_id: str,
        pla_id: str,
        parameters: _models.PrivateLinkAssociationObject,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.PrivateLinkAssociation:
        """Create a PrivateLinkAssociation.

        :param group_id: The management group ID. Required.
        :type group_id: str
        :param pla_id: The ID of the PLA. Required.
        :type pla_id: str
        :param parameters: Parameters supplied to create the private link association. Required.
        :type parameters:
         ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociationObject
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: PrivateLinkAssociation or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociation
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def put(
        self,
        group_id: str,
        pla_id: str,
        parameters: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.PrivateLinkAssociation:
        """Create a PrivateLinkAssociation.

        :param group_id: The management group ID. Required.
        :type group_id: str
        :param pla_id: The ID of the PLA. Required.
        :type pla_id: str
        :param parameters: Parameters supplied to create the private link association. Required.
        :type parameters: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: PrivateLinkAssociation or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociation
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def put(
        self,
        group_id: str,
        pla_id: str,
        parameters: Union[_models.PrivateLinkAssociationObject, IO[bytes]],
        **kwargs: Any
    ) -> _models.PrivateLinkAssociation:
        """Create a PrivateLinkAssociation.

        :param group_id: The management group ID. Required.
        :type group_id: str
        :param pla_id: The ID of the PLA. Required.
        :type pla_id: str
        :param parameters: Parameters supplied to create the private link association. Is either a
         PrivateLinkAssociationObject type or a IO[bytes] type. Required.
        :type parameters:
         ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociationObject or IO[bytes]
        :return: PrivateLinkAssociation or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociation
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.PrivateLinkAssociation] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(parameters, (IOBase, bytes)):
            _content = parameters
        else:
            _json = self._serialize.body(parameters, "PrivateLinkAssociationObject")

        _request = build_private_link_association_put_request(
            group_id=group_id,
            pla_id=pla_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("PrivateLinkAssociation", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def get(self, group_id: str, pla_id: str, **kwargs: Any) -> _models.PrivateLinkAssociation:
        """Get a single private link association.

        :param group_id: The management group ID. Required.
        :type group_id: str
        :param pla_id: The ID of the PLA. Required.
        :type pla_id: str
        :return: PrivateLinkAssociation or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociation
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[_models.PrivateLinkAssociation] = kwargs.pop("cls", None)

        _request = build_private_link_association_get_request(
            group_id=group_id,
            pla_id=pla_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("PrivateLinkAssociation", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def delete(self, group_id: str, pla_id: str, **kwargs: Any) -> None:
        """Delete a PrivateLinkAssociation.

        :param group_id: The management group ID. Required.
        :type group_id: str
        :param pla_id: The ID of the PLA. Required.
        :type pla_id: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_private_link_association_delete_request(
            group_id=group_id,
            pla_id=pla_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})  # type: ignore

    @distributed_trace_async
    async def list(self, group_id: str, **kwargs: Any) -> _models.PrivateLinkAssociationGetResult:
        """Get a private link association for a management group scope.

        :param group_id: The management group ID. Required.
        :type group_id: str
        :return: PrivateLinkAssociationGetResult or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.PrivateLinkAssociationGetResult
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[_models.PrivateLinkAssociationGetResult] = kwargs.pop("cls", None)

        _request = build_private_link_association_list_request(
            group_id=group_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("PrivateLinkAssociationGetResult", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore


class ResourceManagementPrivateLinkOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.resource.privatelinks.v2020_05_01.aio.ResourcePrivateLinkClient`'s
        :attr:`resource_management_private_link` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")
        self._api_version = input_args.pop(0) if input_args else kwargs.pop("api_version")

    @overload
    async def put(
        self,
        resource_group_name: str,
        rmpl_name: str,
        parameters: _models.ResourceManagementPrivateLinkLocation,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.ResourceManagementPrivateLink:
        """Create a resource management group private link.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param rmpl_name: The name of the resource management private link. Required.
        :type rmpl_name: str
        :param parameters: The region to create the Resource Management private link. Required.
        :type parameters:
         ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLinkLocation
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: ResourceManagementPrivateLink or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLink
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def put(
        self,
        resource_group_name: str,
        rmpl_name: str,
        parameters: IO[bytes],
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.ResourceManagementPrivateLink:
        """Create a resource management group private link.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param rmpl_name: The name of the resource management private link. Required.
        :type rmpl_name: str
        :param parameters: The region to create the Resource Management private link. Required.
        :type parameters: IO[bytes]
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :return: ResourceManagementPrivateLink or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLink
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @distributed_trace_async
    async def put(
        self,
        resource_group_name: str,
        rmpl_name: str,
        parameters: Union[_models.ResourceManagementPrivateLinkLocation, IO[bytes]],
        **kwargs: Any
    ) -> _models.ResourceManagementPrivateLink:
        """Create a resource management group private link.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param rmpl_name: The name of the resource management private link. Required.
        :type rmpl_name: str
        :param parameters: The region to create the Resource Management private link. Is either a
         ResourceManagementPrivateLinkLocation type or a IO[bytes] type. Required.
        :type parameters:
         ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLinkLocation or
         IO[bytes]
        :return: ResourceManagementPrivateLink or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLink
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        content_type: Optional[str] = kwargs.pop("content_type", _headers.pop("Content-Type", None))
        cls: ClsType[_models.ResourceManagementPrivateLink] = kwargs.pop("cls", None)

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(parameters, (IOBase, bytes)):
            _content = parameters
        else:
            _json = self._serialize.body(parameters, "ResourceManagementPrivateLinkLocation")

        _request = build_resource_management_private_link_put_request(
            resource_group_name=resource_group_name,
            rmpl_name=rmpl_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ResourceManagementPrivateLink", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def get(
        self, resource_group_name: str, rmpl_name: str, **kwargs: Any
    ) -> _models.ResourceManagementPrivateLink:
        """Get a resource management private link(resource-level).

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param rmpl_name: The name of the resource management private link. Required.
        :type rmpl_name: str
        :return: ResourceManagementPrivateLink or the result of cls(response)
        :rtype: ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLink
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[_models.ResourceManagementPrivateLink] = kwargs.pop("cls", None)

        _request = build_resource_management_private_link_get_request(
            resource_group_name=resource_group_name,
            rmpl_name=rmpl_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ResourceManagementPrivateLink", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def delete(self, resource_group_name: str, rmpl_name: str, **kwargs: Any) -> None:
        """Delete a resource management private link.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :param rmpl_name: The name of the resource management private link. Required.
        :type rmpl_name: str
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[None] = kwargs.pop("cls", None)

        _request = build_resource_management_private_link_delete_request(
            resource_group_name=resource_group_name,
            rmpl_name=rmpl_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})  # type: ignore

    @distributed_trace_async
    async def list(self, **kwargs: Any) -> _models.ResourceManagementPrivateLinkListResult:
        """Get all the resource management private links in a subscription.

        :return: ResourceManagementPrivateLinkListResult or the result of cls(response)
        :rtype:
         ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLinkListResult
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[_models.ResourceManagementPrivateLinkListResult] = kwargs.pop("cls", None)

        _request = build_resource_management_private_link_list_request(
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ResourceManagementPrivateLinkListResult", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @distributed_trace_async
    async def list_by_resource_group(
        self, resource_group_name: str, **kwargs: Any
    ) -> _models.ResourceManagementPrivateLinkListResult:
        """Get all the resource management private links in a resource group.

        :param resource_group_name: The name of the resource group. The name is case insensitive.
         Required.
        :type resource_group_name: str
        :return: ResourceManagementPrivateLinkListResult or the result of cls(response)
        :rtype:
         ~azure.mgmt.resource.privatelinks.v2020_05_01.models.ResourceManagementPrivateLinkListResult
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map: MutableMapping = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version: str = kwargs.pop("api_version", _params.pop("api-version", self._api_version or "2020-05-01"))
        cls: ClsType[_models.ResourceManagementPrivateLinkListResult] = kwargs.pop("cls", None)

        _request = build_resource_management_private_link_list_by_resource_group_request(
            resource_group_name=resource_group_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            headers=_headers,
            params=_params,
        )
        _request.url = self._client.format_url(_request.url)

        _stream = False
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            _request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("ResourceManagementPrivateLinkListResult", pipeline_response.http_response)

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore
