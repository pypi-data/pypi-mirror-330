# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class ChangeType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of change that will be made to the resource when the deployment is executed."""

    CREATE = "Create"
    """The resource does not exist in the current state but is present in the desired state. The
    resource will be created when the deployment is executed."""
    DELETE = "Delete"
    """The resource exists in the current state and is missing from the desired state. The resource
    will be deleted when the deployment is executed."""
    IGNORE = "Ignore"
    """The resource exists in the current state and is missing from the desired state. The resource
    will not be deployed or modified when the deployment is executed."""
    DEPLOY = "Deploy"
    """The resource exists in the current state and the desired state and will be redeployed when the
    deployment is executed. The properties of the resource may or may not change."""
    NO_CHANGE = "NoChange"
    """The resource exists in the current state and the desired state and will be redeployed when the
    deployment is executed. The properties of the resource will not change."""
    MODIFY = "Modify"
    """The resource exists in the current state and the desired state and will be redeployed when the
    deployment is executed. The properties of the resource will change."""


class DeploymentMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The mode that is used to deploy resources. This value can be either Incremental or Complete. In
    Incremental mode, resources are deployed without deleting existing resources that are not
    included in the template. In Complete mode, resources are deployed and existing resources in
    the resource group that are not included in the template are deleted. Be careful when using
    Complete mode as you may unintentionally delete resources.
    """

    INCREMENTAL = "Incremental"
    COMPLETE = "Complete"


class OnErrorDeploymentType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The deployment on error behavior type. Possible values are LastSuccessful and
    SpecificDeployment.
    """

    LAST_SUCCESSFUL = "LastSuccessful"
    SPECIFIC_DEPLOYMENT = "SpecificDeployment"


class PropertyChangeType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of property change."""

    CREATE = "Create"
    """The property does not exist in the current state but is present in the desired state. The
    property will be created when the deployment is executed."""
    DELETE = "Delete"
    """The property exists in the current state and is missing from the desired state. It will be
    deleted when the deployment is executed."""
    MODIFY = "Modify"
    """The property exists in both current and desired state and is different. The value of the
    property will change when the deployment is executed."""
    ARRAY = "Array"
    """The property is an array and contains nested changes."""


class ResourceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The identity type."""

    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"
    NONE = "None"


class WhatIfResultFormat(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The format of the What-If results."""

    RESOURCE_ID_ONLY = "ResourceIdOnly"
    FULL_RESOURCE_PAYLOADS = "FullResourcePayloads"
