# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class CreatedByType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class EnforcementMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The policy assignment enforcement mode. Possible values are Default and DoNotEnforce."""

    DEFAULT = "Default"
    """The policy effect is enforced during resource creation or update."""
    DO_NOT_ENFORCE = "DoNotEnforce"
    """The policy effect is not enforced during resource creation or update."""


class OverrideKind(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The override kind."""

    POLICY_EFFECT = "policyEffect"
    """It will override the policy effect type."""


class ResourceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The identity type. This is the only required field when adding a system or user assigned
    identity to a resource.
    """

    SYSTEM_ASSIGNED = "SystemAssigned"
    """Indicates that a system assigned identity is associated with the resource."""
    USER_ASSIGNED = "UserAssigned"
    """Indicates that a system assigned identity is associated with the resource."""
    NONE = "None"
    """Indicates that no identity is associated with the resource or that the existing identity should
    be removed."""


class SelectorKind(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The selector kind."""

    RESOURCE_LOCATION = "resourceLocation"
    """The selector kind to filter policies by the resource location."""
    RESOURCE_TYPE = "resourceType"
    """The selector kind to filter policies by the resource type."""
    RESOURCE_WITHOUT_LOCATION = "resourceWithoutLocation"
    """The selector kind to filter policies by the resource without location."""
    POLICY_DEFINITION_REFERENCE_ID = "policyDefinitionReferenceId"
    """The selector kind to filter policies by the policy definition reference ID."""
