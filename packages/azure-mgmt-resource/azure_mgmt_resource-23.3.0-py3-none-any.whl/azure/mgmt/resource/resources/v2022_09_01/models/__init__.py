# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
# pylint: disable=wrong-import-position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._patch import *  # pylint: disable=unused-wildcard-import


from ._models_py3 import (  # type: ignore
    Alias,
    AliasPath,
    AliasPathMetadata,
    AliasPattern,
    ApiProfile,
    BasicDependency,
    DebugSetting,
    Dependency,
    Deployment,
    DeploymentExportResult,
    DeploymentExtended,
    DeploymentExtendedFilter,
    DeploymentListResult,
    DeploymentOperation,
    DeploymentOperationProperties,
    DeploymentOperationsListResult,
    DeploymentParameter,
    DeploymentProperties,
    DeploymentPropertiesExtended,
    DeploymentValidateResult,
    DeploymentWhatIf,
    DeploymentWhatIfProperties,
    DeploymentWhatIfSettings,
    ErrorAdditionalInfo,
    ErrorResponse,
    ExportTemplateRequest,
    ExpressionEvaluationOptions,
    ExtendedLocation,
    GenericResource,
    GenericResourceExpanded,
    GenericResourceFilter,
    HttpMessage,
    Identity,
    IdentityUserAssignedIdentitiesValue,
    KeyVaultParameterReference,
    KeyVaultReference,
    OnErrorDeployment,
    OnErrorDeploymentExtended,
    Operation,
    OperationDisplay,
    OperationListResult,
    ParametersLink,
    Permission,
    Plan,
    Provider,
    ProviderConsentDefinition,
    ProviderExtendedLocation,
    ProviderListResult,
    ProviderPermission,
    ProviderPermissionListResult,
    ProviderRegistrationRequest,
    ProviderResourceType,
    ProviderResourceTypeListResult,
    Resource,
    ResourceGroup,
    ResourceGroupExportResult,
    ResourceGroupFilter,
    ResourceGroupListResult,
    ResourceGroupPatchable,
    ResourceGroupProperties,
    ResourceListResult,
    ResourceProviderOperationDisplayProperties,
    ResourceReference,
    ResourcesMoveInfo,
    RoleDefinition,
    ScopedDeployment,
    ScopedDeploymentWhatIf,
    Sku,
    StatusMessage,
    SubResource,
    TagCount,
    TagDetails,
    TagValue,
    Tags,
    TagsListResult,
    TagsPatchResource,
    TagsResource,
    TargetResource,
    TemplateHashResult,
    TemplateLink,
    WhatIfChange,
    WhatIfOperationResult,
    WhatIfPropertyChange,
    ZoneMapping,
)

from ._resource_management_client_enums import (  # type: ignore
    AliasPathAttributes,
    AliasPathTokenType,
    AliasPatternType,
    AliasType,
    ChangeType,
    DeploymentMode,
    ExpressionEvaluationOptionsScopeType,
    ExtendedLocationType,
    OnErrorDeploymentType,
    PropertyChangeType,
    ProviderAuthorizationConsentState,
    ProvisioningOperation,
    ProvisioningState,
    ResourceIdentityType,
    TagsPatchOperation,
    WhatIfResultFormat,
)
from ._patch import __all__ as _patch_all
from ._patch import *
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "Alias",
    "AliasPath",
    "AliasPathMetadata",
    "AliasPattern",
    "ApiProfile",
    "BasicDependency",
    "DebugSetting",
    "Dependency",
    "Deployment",
    "DeploymentExportResult",
    "DeploymentExtended",
    "DeploymentExtendedFilter",
    "DeploymentListResult",
    "DeploymentOperation",
    "DeploymentOperationProperties",
    "DeploymentOperationsListResult",
    "DeploymentParameter",
    "DeploymentProperties",
    "DeploymentPropertiesExtended",
    "DeploymentValidateResult",
    "DeploymentWhatIf",
    "DeploymentWhatIfProperties",
    "DeploymentWhatIfSettings",
    "ErrorAdditionalInfo",
    "ErrorResponse",
    "ExportTemplateRequest",
    "ExpressionEvaluationOptions",
    "ExtendedLocation",
    "GenericResource",
    "GenericResourceExpanded",
    "GenericResourceFilter",
    "HttpMessage",
    "Identity",
    "IdentityUserAssignedIdentitiesValue",
    "KeyVaultParameterReference",
    "KeyVaultReference",
    "OnErrorDeployment",
    "OnErrorDeploymentExtended",
    "Operation",
    "OperationDisplay",
    "OperationListResult",
    "ParametersLink",
    "Permission",
    "Plan",
    "Provider",
    "ProviderConsentDefinition",
    "ProviderExtendedLocation",
    "ProviderListResult",
    "ProviderPermission",
    "ProviderPermissionListResult",
    "ProviderRegistrationRequest",
    "ProviderResourceType",
    "ProviderResourceTypeListResult",
    "Resource",
    "ResourceGroup",
    "ResourceGroupExportResult",
    "ResourceGroupFilter",
    "ResourceGroupListResult",
    "ResourceGroupPatchable",
    "ResourceGroupProperties",
    "ResourceListResult",
    "ResourceProviderOperationDisplayProperties",
    "ResourceReference",
    "ResourcesMoveInfo",
    "RoleDefinition",
    "ScopedDeployment",
    "ScopedDeploymentWhatIf",
    "Sku",
    "StatusMessage",
    "SubResource",
    "TagCount",
    "TagDetails",
    "TagValue",
    "Tags",
    "TagsListResult",
    "TagsPatchResource",
    "TagsResource",
    "TargetResource",
    "TemplateHashResult",
    "TemplateLink",
    "WhatIfChange",
    "WhatIfOperationResult",
    "WhatIfPropertyChange",
    "ZoneMapping",
    "AliasPathAttributes",
    "AliasPathTokenType",
    "AliasPatternType",
    "AliasType",
    "ChangeType",
    "DeploymentMode",
    "ExpressionEvaluationOptionsScopeType",
    "ExtendedLocationType",
    "OnErrorDeploymentType",
    "PropertyChangeType",
    "ProviderAuthorizationConsentState",
    "ProvisioningOperation",
    "ProvisioningState",
    "ResourceIdentityType",
    "TagsPatchOperation",
    "WhatIfResultFormat",
]
__all__.extend([p for p in _patch_all if p not in __all__])  # pyright: ignore
_patch_sdk()
