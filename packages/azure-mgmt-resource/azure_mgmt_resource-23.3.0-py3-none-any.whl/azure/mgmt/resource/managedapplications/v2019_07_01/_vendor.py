# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from abc import ABC
from typing import TYPE_CHECKING

from ._configuration import ApplicationClientConfiguration

if TYPE_CHECKING:
    from azure.core import PipelineClient

    from .._serialization import Deserializer, Serializer


class ApplicationClientMixinABC(ABC):
    """DO NOT use this class. It is for internal typing use only."""

    _client: "PipelineClient"
    _config: ApplicationClientConfiguration
    _serialize: "Serializer"
    _deserialize: "Deserializer"
