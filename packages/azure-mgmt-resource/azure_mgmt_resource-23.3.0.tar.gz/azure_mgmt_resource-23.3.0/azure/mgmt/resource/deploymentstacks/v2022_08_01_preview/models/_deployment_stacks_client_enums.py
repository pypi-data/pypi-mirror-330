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


class DenySettingsMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """denySettings Mode."""

    DENY_DELETE = "denyDelete"
    """Authorized users are able to read and modify the resources, but cannot delete."""
    DENY_WRITE_AND_DELETE = "denyWriteAndDelete"
    """Authorized users can only read from a resource, but cannot modify or delete it."""
    NONE = "none"
    """No denyAssignments have been applied."""


class DenyStatusMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """denyAssignment settings applied to the resource."""

    DENY_DELETE = "denyDelete"
    """Authorized users are able to read and modify the resources, but cannot delete."""
    NOT_SUPPORTED = "notSupported"
    """Resource type does not support denyAssignments."""
    INAPPLICABLE = "inapplicable"
    """denyAssignments are not supported on resources outside the scope of the deployment stack."""
    DENY_WRITE_AND_DELETE = "denyWriteAndDelete"
    """Authorized users can only read from a resource, but cannot modify or delete it."""
    REMOVED_BY_SYSTEM = "removedBySystem"
    """Deny assignment has been removed by Azure due to a resource management change (management group
    move, etc.)"""
    NONE = "None"
    """No denyAssignments have been applied."""


class DeploymentStackProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """State of the deployment stack."""

    CREATING = "Creating"
    VALIDATING = "Validating"
    WAITING = "Waiting"
    DEPLOYING = "Deploying"
    CANCELING = "Canceling"
    LOCKING = "Locking"
    DELETING_RESOURCES = "DeletingResources"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"
    DELETING = "Deleting"


class DeploymentStacksDeleteDetachEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Specifies the action that should be taken on the resource when the deployment stack is deleted.
    Delete will attempt to delete the resource from Azure. Detach will leave the resource in it's
    current state.
    """

    DELETE = "delete"
    DETACH = "detach"


class ResourceStatusMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Current management state of the resource in the deployment stack."""

    MANAGED = "Managed"
    """This resource is managed by the deployment stack."""
    REMOVE_DENY_FAILED = "removeDenyFailed"
    """Unable to remove the deny assignment on resource."""
    DELETE_FAILED = "deleteFailed"
    """Unable to delete the resource from Azure. The delete will be retried on the next stack
    deployment, or can be deleted manually."""
    NONE = "None"
    """No denyAssignments have been applied."""


class UnmanageActionManagementGroupMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """UnmanageActionManagementGroupMode."""

    DELETE = "delete"
    DETACH = "detach"


class UnmanageActionResourceGroupMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """UnmanageActionResourceGroupMode."""

    DELETE = "delete"
    DETACH = "detach"


class UnmanageActionResourceMode(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """UnmanageActionResourceMode."""

    DELETE = "delete"
    DETACH = "detach"
