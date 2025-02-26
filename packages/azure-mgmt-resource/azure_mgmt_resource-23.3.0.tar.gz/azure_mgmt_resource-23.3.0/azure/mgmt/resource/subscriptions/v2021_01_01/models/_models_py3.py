# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from ... import _serialization

if TYPE_CHECKING:
    from .. import models as _models


class AvailabilityZonePeers(_serialization.Model):
    """List of availability zones shared by the subscriptions.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar availability_zone: The availabilityZone.
    :vartype availability_zone: str
    :ivar peers: Details of shared availability zone.
    :vartype peers: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Peers]
    """

    _validation = {
        "availability_zone": {"readonly": True},
    }

    _attribute_map = {
        "availability_zone": {"key": "availabilityZone", "type": "str"},
        "peers": {"key": "peers", "type": "[Peers]"},
    }

    def __init__(self, *, peers: Optional[List["_models.Peers"]] = None, **kwargs: Any) -> None:
        """
        :keyword peers: Details of shared availability zone.
        :paramtype peers: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Peers]
        """
        super().__init__(**kwargs)
        self.availability_zone = None
        self.peers = peers


class CheckResourceNameResult(_serialization.Model):
    """Resource Name valid if not a reserved word, does not contain a reserved word and does not start
    with a reserved word.

    :ivar name: Name of Resource.
    :vartype name: str
    :ivar type: Type of Resource.
    :vartype type: str
    :ivar status: Is the resource name Allowed or Reserved. Known values are: "Allowed" and
     "Reserved".
    :vartype status: str or
     ~azure.mgmt.resource.subscriptions.v2021_01_01.models.ResourceNameStatus
    """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "status": {"key": "status", "type": "str"},
    }

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        type: Optional[str] = None,
        status: Optional[Union[str, "_models.ResourceNameStatus"]] = None,
        **kwargs: Any
    ) -> None:
        """
        :keyword name: Name of Resource.
        :paramtype name: str
        :keyword type: Type of Resource.
        :paramtype type: str
        :keyword status: Is the resource name Allowed or Reserved. Known values are: "Allowed" and
         "Reserved".
        :paramtype status: str or
         ~azure.mgmt.resource.subscriptions.v2021_01_01.models.ResourceNameStatus
        """
        super().__init__(**kwargs)
        self.name = name
        self.type = type
        self.status = status


class CheckZonePeersRequest(_serialization.Model):
    """Check zone peers request parameters.

    :ivar location: The Microsoft location.
    :vartype location: str
    :ivar subscription_ids: The peer Microsoft Azure subscription ID.
    :vartype subscription_ids: list[str]
    """

    _attribute_map = {
        "location": {"key": "location", "type": "str"},
        "subscription_ids": {"key": "subscriptionIds", "type": "[str]"},
    }

    def __init__(
        self, *, location: Optional[str] = None, subscription_ids: Optional[List[str]] = None, **kwargs: Any
    ) -> None:
        """
        :keyword location: The Microsoft location.
        :paramtype location: str
        :keyword subscription_ids: The peer Microsoft Azure subscription ID.
        :paramtype subscription_ids: list[str]
        """
        super().__init__(**kwargs)
        self.location = location
        self.subscription_ids = subscription_ids


class CheckZonePeersResult(_serialization.Model):
    """Result of the Check zone peers operation.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar subscription_id: The subscription ID.
    :vartype subscription_id: str
    :ivar location: the location of the subscription.
    :vartype location: str
    :ivar availability_zone_peers: The Availability Zones shared by the subscriptions.
    :vartype availability_zone_peers:
     list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.AvailabilityZonePeers]
    """

    _validation = {
        "subscription_id": {"readonly": True},
    }

    _attribute_map = {
        "subscription_id": {"key": "subscriptionId", "type": "str"},
        "location": {"key": "location", "type": "str"},
        "availability_zone_peers": {"key": "availabilityZonePeers", "type": "[AvailabilityZonePeers]"},
    }

    def __init__(
        self,
        *,
        location: Optional[str] = None,
        availability_zone_peers: Optional[List["_models.AvailabilityZonePeers"]] = None,
        **kwargs: Any
    ) -> None:
        """
        :keyword location: the location of the subscription.
        :paramtype location: str
        :keyword availability_zone_peers: The Availability Zones shared by the subscriptions.
        :paramtype availability_zone_peers:
         list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.AvailabilityZonePeers]
        """
        super().__init__(**kwargs)
        self.subscription_id = None
        self.location = location
        self.availability_zone_peers = availability_zone_peers


class ErrorAdditionalInfo(_serialization.Model):
    """The resource management error additional info.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar type: The additional info type.
    :vartype type: str
    :ivar info: The additional info.
    :vartype info: JSON
    """

    _validation = {
        "type": {"readonly": True},
        "info": {"readonly": True},
    }

    _attribute_map = {
        "type": {"key": "type", "type": "str"},
        "info": {"key": "info", "type": "object"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.type = None
        self.info = None


class ErrorDetail(_serialization.Model):
    """The error detail.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar code: The error code.
    :vartype code: str
    :ivar message: The error message.
    :vartype message: str
    :ivar target: The error target.
    :vartype target: str
    :ivar details: The error details.
    :vartype details: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.ErrorDetail]
    :ivar additional_info: The error additional info.
    :vartype additional_info:
     list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.ErrorAdditionalInfo]
    """

    _validation = {
        "code": {"readonly": True},
        "message": {"readonly": True},
        "target": {"readonly": True},
        "details": {"readonly": True},
        "additional_info": {"readonly": True},
    }

    _attribute_map = {
        "code": {"key": "code", "type": "str"},
        "message": {"key": "message", "type": "str"},
        "target": {"key": "target", "type": "str"},
        "details": {"key": "details", "type": "[ErrorDetail]"},
        "additional_info": {"key": "additionalInfo", "type": "[ErrorAdditionalInfo]"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.code = None
        self.message = None
        self.target = None
        self.details = None
        self.additional_info = None


class ErrorResponse(_serialization.Model):
    """Common error response for all Azure Resource Manager APIs to return error details for failed
    operations. (This also follows the OData error response format.).

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar code: The error code.
    :vartype code: str
    :ivar message: The error message.
    :vartype message: str
    :ivar target: The error target.
    :vartype target: str
    :ivar details: The error details.
    :vartype details: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.ErrorResponse]
    :ivar additional_info: The error additional info.
    :vartype additional_info:
     list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.ErrorAdditionalInfo]
    """

    _validation = {
        "code": {"readonly": True},
        "message": {"readonly": True},
        "target": {"readonly": True},
        "details": {"readonly": True},
        "additional_info": {"readonly": True},
    }

    _attribute_map = {
        "code": {"key": "code", "type": "str"},
        "message": {"key": "message", "type": "str"},
        "target": {"key": "target", "type": "str"},
        "details": {"key": "details", "type": "[ErrorResponse]"},
        "additional_info": {"key": "additionalInfo", "type": "[ErrorAdditionalInfo]"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.code = None
        self.message = None
        self.target = None
        self.details = None
        self.additional_info = None


class ErrorResponseAutoGenerated(_serialization.Model):
    """Common error response for all Azure Resource Manager APIs to return error details for failed
    operations. (This also follows the OData error response format.).

    :ivar error: The error object.
    :vartype error: ~azure.mgmt.resource.subscriptions.v2021_01_01.models.ErrorDetail
    """

    _attribute_map = {
        "error": {"key": "error", "type": "ErrorDetail"},
    }

    def __init__(self, *, error: Optional["_models.ErrorDetail"] = None, **kwargs: Any) -> None:
        """
        :keyword error: The error object.
        :paramtype error: ~azure.mgmt.resource.subscriptions.v2021_01_01.models.ErrorDetail
        """
        super().__init__(**kwargs)
        self.error = error


class Location(_serialization.Model):
    """Location information.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: The fully qualified ID of the location. For example,
     /subscriptions/00000000-0000-0000-0000-000000000000/locations/westus.
    :vartype id: str
    :ivar subscription_id: The subscription ID.
    :vartype subscription_id: str
    :ivar name: The location name.
    :vartype name: str
    :ivar type: The location type. Known values are: "Region" and "EdgeZone".
    :vartype type: str or ~azure.mgmt.resource.subscriptions.v2021_01_01.models.LocationType
    :ivar display_name: The display name of the location.
    :vartype display_name: str
    :ivar regional_display_name: The display name of the location and its region.
    :vartype regional_display_name: str
    :ivar metadata: Metadata of the location, such as lat/long, paired region, and others.
    :vartype metadata: ~azure.mgmt.resource.subscriptions.v2021_01_01.models.LocationMetadata
    """

    _validation = {
        "id": {"readonly": True},
        "subscription_id": {"readonly": True},
        "name": {"readonly": True},
        "type": {"readonly": True},
        "display_name": {"readonly": True},
        "regional_display_name": {"readonly": True},
    }

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "subscription_id": {"key": "subscriptionId", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
        "regional_display_name": {"key": "regionalDisplayName", "type": "str"},
        "metadata": {"key": "metadata", "type": "LocationMetadata"},
    }

    def __init__(self, *, metadata: Optional["_models.LocationMetadata"] = None, **kwargs: Any) -> None:
        """
        :keyword metadata: Metadata of the location, such as lat/long, paired region, and others.
        :paramtype metadata: ~azure.mgmt.resource.subscriptions.v2021_01_01.models.LocationMetadata
        """
        super().__init__(**kwargs)
        self.id = None
        self.subscription_id = None
        self.name = None
        self.type = None
        self.display_name = None
        self.regional_display_name = None
        self.metadata = metadata


class LocationListResult(_serialization.Model):
    """Location list operation response.

    :ivar value: An array of locations.
    :vartype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Location]
    """

    _attribute_map = {
        "value": {"key": "value", "type": "[Location]"},
    }

    def __init__(self, *, value: Optional[List["_models.Location"]] = None, **kwargs: Any) -> None:
        """
        :keyword value: An array of locations.
        :paramtype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Location]
        """
        super().__init__(**kwargs)
        self.value = value


class LocationMetadata(_serialization.Model):
    """Location metadata information.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar region_type: The type of the region. Known values are: "Physical" and "Logical".
    :vartype region_type: str or ~azure.mgmt.resource.subscriptions.v2021_01_01.models.RegionType
    :ivar region_category: The category of the region. Known values are: "Recommended", "Extended",
     and "Other".
    :vartype region_category: str or
     ~azure.mgmt.resource.subscriptions.v2021_01_01.models.RegionCategory
    :ivar geography_group: The geography group of the location.
    :vartype geography_group: str
    :ivar longitude: The longitude of the location.
    :vartype longitude: str
    :ivar latitude: The latitude of the location.
    :vartype latitude: str
    :ivar physical_location: The physical location of the Azure location.
    :vartype physical_location: str
    :ivar paired_region: The regions paired to this region.
    :vartype paired_region:
     list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.PairedRegion]
    :ivar home_location: The home location of an edge zone.
    :vartype home_location: str
    """

    _validation = {
        "region_type": {"readonly": True},
        "region_category": {"readonly": True},
        "geography_group": {"readonly": True},
        "longitude": {"readonly": True},
        "latitude": {"readonly": True},
        "physical_location": {"readonly": True},
        "home_location": {"readonly": True},
    }

    _attribute_map = {
        "region_type": {"key": "regionType", "type": "str"},
        "region_category": {"key": "regionCategory", "type": "str"},
        "geography_group": {"key": "geographyGroup", "type": "str"},
        "longitude": {"key": "longitude", "type": "str"},
        "latitude": {"key": "latitude", "type": "str"},
        "physical_location": {"key": "physicalLocation", "type": "str"},
        "paired_region": {"key": "pairedRegion", "type": "[PairedRegion]"},
        "home_location": {"key": "homeLocation", "type": "str"},
    }

    def __init__(self, *, paired_region: Optional[List["_models.PairedRegion"]] = None, **kwargs: Any) -> None:
        """
        :keyword paired_region: The regions paired to this region.
        :paramtype paired_region:
         list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.PairedRegion]
        """
        super().__init__(**kwargs)
        self.region_type = None
        self.region_category = None
        self.geography_group = None
        self.longitude = None
        self.latitude = None
        self.physical_location = None
        self.paired_region = paired_region
        self.home_location = None


class ManagedByTenant(_serialization.Model):
    """Information about a tenant managing the subscription.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar tenant_id: The tenant ID of the managing tenant. This is a GUID.
    :vartype tenant_id: str
    """

    _validation = {
        "tenant_id": {"readonly": True},
    }

    _attribute_map = {
        "tenant_id": {"key": "tenantId", "type": "str"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.tenant_id = None


class Operation(_serialization.Model):
    """Microsoft.Resources operation.

    :ivar name: Operation name: {provider}/{resource}/{operation}.
    :vartype name: str
    :ivar display: The object that represents the operation.
    :vartype display: ~azure.mgmt.resource.subscriptions.v2021_01_01.models.OperationDisplay
    """

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "display": {"key": "display", "type": "OperationDisplay"},
    }

    def __init__(
        self, *, name: Optional[str] = None, display: Optional["_models.OperationDisplay"] = None, **kwargs: Any
    ) -> None:
        """
        :keyword name: Operation name: {provider}/{resource}/{operation}.
        :paramtype name: str
        :keyword display: The object that represents the operation.
        :paramtype display: ~azure.mgmt.resource.subscriptions.v2021_01_01.models.OperationDisplay
        """
        super().__init__(**kwargs)
        self.name = name
        self.display = display


class OperationDisplay(_serialization.Model):
    """The object that represents the operation.

    :ivar provider: Service provider: Microsoft.Resources.
    :vartype provider: str
    :ivar resource: Resource on which the operation is performed: Profile, endpoint, etc.
    :vartype resource: str
    :ivar operation: Operation type: Read, write, delete, etc.
    :vartype operation: str
    :ivar description: Description of the operation.
    :vartype description: str
    """

    _attribute_map = {
        "provider": {"key": "provider", "type": "str"},
        "resource": {"key": "resource", "type": "str"},
        "operation": {"key": "operation", "type": "str"},
        "description": {"key": "description", "type": "str"},
    }

    def __init__(
        self,
        *,
        provider: Optional[str] = None,
        resource: Optional[str] = None,
        operation: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        :keyword provider: Service provider: Microsoft.Resources.
        :paramtype provider: str
        :keyword resource: Resource on which the operation is performed: Profile, endpoint, etc.
        :paramtype resource: str
        :keyword operation: Operation type: Read, write, delete, etc.
        :paramtype operation: str
        :keyword description: Description of the operation.
        :paramtype description: str
        """
        super().__init__(**kwargs)
        self.provider = provider
        self.resource = resource
        self.operation = operation
        self.description = description


class OperationListResult(_serialization.Model):
    """Result of the request to list Microsoft.Resources operations. It contains a list of operations
    and a URL link to get the next set of results.

    :ivar value: List of Microsoft.Resources operations.
    :vartype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Operation]
    :ivar next_link: URL to get the next set of operation list results if there are any.
    :vartype next_link: str
    """

    _attribute_map = {
        "value": {"key": "value", "type": "[Operation]"},
        "next_link": {"key": "nextLink", "type": "str"},
    }

    def __init__(
        self, *, value: Optional[List["_models.Operation"]] = None, next_link: Optional[str] = None, **kwargs: Any
    ) -> None:
        """
        :keyword value: List of Microsoft.Resources operations.
        :paramtype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Operation]
        :keyword next_link: URL to get the next set of operation list results if there are any.
        :paramtype next_link: str
        """
        super().__init__(**kwargs)
        self.value = value
        self.next_link = next_link


class PairedRegion(_serialization.Model):
    """Information regarding paired region.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar name: The name of the paired region.
    :vartype name: str
    :ivar id: The fully qualified ID of the location. For example,
     /subscriptions/00000000-0000-0000-0000-000000000000/locations/westus.
    :vartype id: str
    :ivar subscription_id: The subscription ID.
    :vartype subscription_id: str
    """

    _validation = {
        "name": {"readonly": True},
        "id": {"readonly": True},
        "subscription_id": {"readonly": True},
    }

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "id": {"key": "id", "type": "str"},
        "subscription_id": {"key": "subscriptionId", "type": "str"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.name = None
        self.id = None
        self.subscription_id = None


class Peers(_serialization.Model):
    """Information about shared availability zone.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar subscription_id: The subscription ID.
    :vartype subscription_id: str
    :ivar availability_zone: The availabilityZone.
    :vartype availability_zone: str
    """

    _validation = {
        "subscription_id": {"readonly": True},
        "availability_zone": {"readonly": True},
    }

    _attribute_map = {
        "subscription_id": {"key": "subscriptionId", "type": "str"},
        "availability_zone": {"key": "availabilityZone", "type": "str"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.subscription_id = None
        self.availability_zone = None


class ResourceName(_serialization.Model):
    """Name and Type of the Resource.

    All required parameters must be populated in order to send to server.

    :ivar name: Name of the resource. Required.
    :vartype name: str
    :ivar type: The type of the resource. Required.
    :vartype type: str
    """

    _validation = {
        "name": {"required": True},
        "type": {"required": True},
    }

    _attribute_map = {
        "name": {"key": "name", "type": "str"},
        "type": {"key": "type", "type": "str"},
    }

    def __init__(self, *, name: str, type: str, **kwargs: Any) -> None:
        """
        :keyword name: Name of the resource. Required.
        :paramtype name: str
        :keyword type: The type of the resource. Required.
        :paramtype type: str
        """
        super().__init__(**kwargs)
        self.name = name
        self.type = type


class Subscription(_serialization.Model):
    """Subscription information.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: The fully qualified ID for the subscription. For example,
     /subscriptions/00000000-0000-0000-0000-000000000000.
    :vartype id: str
    :ivar subscription_id: The subscription ID.
    :vartype subscription_id: str
    :ivar display_name: The subscription display name.
    :vartype display_name: str
    :ivar tenant_id: The subscription tenant ID.
    :vartype tenant_id: str
    :ivar state: The subscription state. Possible values are Enabled, Warned, PastDue, Disabled,
     and Deleted. Known values are: "Enabled", "Warned", "PastDue", "Disabled", and "Deleted".
    :vartype state: str or ~azure.mgmt.resource.subscriptions.v2021_01_01.models.SubscriptionState
    :ivar subscription_policies: The subscription policies.
    :vartype subscription_policies:
     ~azure.mgmt.resource.subscriptions.v2021_01_01.models.SubscriptionPolicies
    :ivar authorization_source: The authorization source of the request. Valid values are one or
     more combinations of Legacy, RoleBased, Bypassed, Direct and Management. For example, 'Legacy,
     RoleBased'.
    :vartype authorization_source: str
    :ivar managed_by_tenants: An array containing the tenants managing the subscription.
    :vartype managed_by_tenants:
     list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.ManagedByTenant]
    :ivar tags: The tags attached to the subscription.
    :vartype tags: dict[str, str]
    """

    _validation = {
        "id": {"readonly": True},
        "subscription_id": {"readonly": True},
        "display_name": {"readonly": True},
        "tenant_id": {"readonly": True},
        "state": {"readonly": True},
    }

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "subscription_id": {"key": "subscriptionId", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
        "tenant_id": {"key": "tenantId", "type": "str"},
        "state": {"key": "state", "type": "str"},
        "subscription_policies": {"key": "subscriptionPolicies", "type": "SubscriptionPolicies"},
        "authorization_source": {"key": "authorizationSource", "type": "str"},
        "managed_by_tenants": {"key": "managedByTenants", "type": "[ManagedByTenant]"},
        "tags": {"key": "tags", "type": "{str}"},
    }

    def __init__(
        self,
        *,
        subscription_policies: Optional["_models.SubscriptionPolicies"] = None,
        authorization_source: Optional[str] = None,
        managed_by_tenants: Optional[List["_models.ManagedByTenant"]] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> None:
        """
        :keyword subscription_policies: The subscription policies.
        :paramtype subscription_policies:
         ~azure.mgmt.resource.subscriptions.v2021_01_01.models.SubscriptionPolicies
        :keyword authorization_source: The authorization source of the request. Valid values are one or
         more combinations of Legacy, RoleBased, Bypassed, Direct and Management. For example, 'Legacy,
         RoleBased'.
        :paramtype authorization_source: str
        :keyword managed_by_tenants: An array containing the tenants managing the subscription.
        :paramtype managed_by_tenants:
         list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.ManagedByTenant]
        :keyword tags: The tags attached to the subscription.
        :paramtype tags: dict[str, str]
        """
        super().__init__(**kwargs)
        self.id = None
        self.subscription_id = None
        self.display_name = None
        self.tenant_id = None
        self.state = None
        self.subscription_policies = subscription_policies
        self.authorization_source = authorization_source
        self.managed_by_tenants = managed_by_tenants
        self.tags = tags


class SubscriptionListResult(_serialization.Model):
    """Subscription list operation response.

    All required parameters must be populated in order to send to server.

    :ivar value: An array of subscriptions.
    :vartype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Subscription]
    :ivar next_link: The URL to get the next set of results. Required.
    :vartype next_link: str
    """

    _validation = {
        "next_link": {"required": True},
    }

    _attribute_map = {
        "value": {"key": "value", "type": "[Subscription]"},
        "next_link": {"key": "nextLink", "type": "str"},
    }

    def __init__(self, *, next_link: str, value: Optional[List["_models.Subscription"]] = None, **kwargs: Any) -> None:
        """
        :keyword value: An array of subscriptions.
        :paramtype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.Subscription]
        :keyword next_link: The URL to get the next set of results. Required.
        :paramtype next_link: str
        """
        super().__init__(**kwargs)
        self.value = value
        self.next_link = next_link


class SubscriptionPolicies(_serialization.Model):
    """Subscription policies.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar location_placement_id: The subscription location placement ID. The ID indicates which
     regions are visible for a subscription. For example, a subscription with a location placement
     Id of Public_2014-09-01 has access to Azure public regions.
    :vartype location_placement_id: str
    :ivar quota_id: The subscription quota ID.
    :vartype quota_id: str
    :ivar spending_limit: The subscription spending limit. Known values are: "On", "Off", and
     "CurrentPeriodOff".
    :vartype spending_limit: str or
     ~azure.mgmt.resource.subscriptions.v2021_01_01.models.SpendingLimit
    """

    _validation = {
        "location_placement_id": {"readonly": True},
        "quota_id": {"readonly": True},
        "spending_limit": {"readonly": True},
    }

    _attribute_map = {
        "location_placement_id": {"key": "locationPlacementId", "type": "str"},
        "quota_id": {"key": "quotaId", "type": "str"},
        "spending_limit": {"key": "spendingLimit", "type": "str"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.location_placement_id = None
        self.quota_id = None
        self.spending_limit = None


class TenantIdDescription(_serialization.Model):
    """Tenant Id information.

    Variables are only populated by the server, and will be ignored when sending a request.

    :ivar id: The fully qualified ID of the tenant. For example,
     /tenants/00000000-0000-0000-0000-000000000000.
    :vartype id: str
    :ivar tenant_id: The tenant ID. For example, 00000000-0000-0000-0000-000000000000.
    :vartype tenant_id: str
    :ivar tenant_category: Category of the tenant. Known values are: "Home", "ProjectedBy", and
     "ManagedBy".
    :vartype tenant_category: str or
     ~azure.mgmt.resource.subscriptions.v2021_01_01.models.TenantCategory
    :ivar country: Country/region name of the address for the tenant.
    :vartype country: str
    :ivar country_code: Country/region abbreviation for the tenant.
    :vartype country_code: str
    :ivar display_name: The display name of the tenant.
    :vartype display_name: str
    :ivar domains: The list of domains for the tenant.
    :vartype domains: list[str]
    :ivar default_domain: The default domain for the tenant.
    :vartype default_domain: str
    :ivar tenant_type: The tenant type. Only available for 'Home' tenant category.
    :vartype tenant_type: str
    :ivar tenant_branding_logo_url: The tenant's branding logo URL. Only available for 'Home'
     tenant category.
    :vartype tenant_branding_logo_url: str
    """

    _validation = {
        "id": {"readonly": True},
        "tenant_id": {"readonly": True},
        "tenant_category": {"readonly": True},
        "country": {"readonly": True},
        "country_code": {"readonly": True},
        "display_name": {"readonly": True},
        "domains": {"readonly": True},
        "default_domain": {"readonly": True},
        "tenant_type": {"readonly": True},
        "tenant_branding_logo_url": {"readonly": True},
    }

    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "tenant_id": {"key": "tenantId", "type": "str"},
        "tenant_category": {"key": "tenantCategory", "type": "str"},
        "country": {"key": "country", "type": "str"},
        "country_code": {"key": "countryCode", "type": "str"},
        "display_name": {"key": "displayName", "type": "str"},
        "domains": {"key": "domains", "type": "[str]"},
        "default_domain": {"key": "defaultDomain", "type": "str"},
        "tenant_type": {"key": "tenantType", "type": "str"},
        "tenant_branding_logo_url": {"key": "tenantBrandingLogoUrl", "type": "str"},
    }

    def __init__(self, **kwargs: Any) -> None:
        """ """
        super().__init__(**kwargs)
        self.id = None
        self.tenant_id = None
        self.tenant_category = None
        self.country = None
        self.country_code = None
        self.display_name = None
        self.domains = None
        self.default_domain = None
        self.tenant_type = None
        self.tenant_branding_logo_url = None


class TenantListResult(_serialization.Model):
    """Tenant Ids information.

    All required parameters must be populated in order to send to server.

    :ivar value: An array of tenants.
    :vartype value: list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.TenantIdDescription]
    :ivar next_link: The URL to use for getting the next set of results. Required.
    :vartype next_link: str
    """

    _validation = {
        "next_link": {"required": True},
    }

    _attribute_map = {
        "value": {"key": "value", "type": "[TenantIdDescription]"},
        "next_link": {"key": "nextLink", "type": "str"},
    }

    def __init__(
        self, *, next_link: str, value: Optional[List["_models.TenantIdDescription"]] = None, **kwargs: Any
    ) -> None:
        """
        :keyword value: An array of tenants.
        :paramtype value:
         list[~azure.mgmt.resource.subscriptions.v2021_01_01.models.TenantIdDescription]
        :keyword next_link: The URL to use for getting the next set of results. Required.
        :paramtype next_link: str
        """
        super().__init__(**kwargs)
        self.value = value
        self.next_link = next_link
