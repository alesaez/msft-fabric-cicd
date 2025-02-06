# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import logging
import re
from pathlib import Path

from azure.core.credentials import TokenCredential

from fabric_cicd._common._exceptions import InputError
from fabric_cicd.fabric_workspace import FabricWorkspace

"""
Following functions are leveraged to validate user input for the fabric-cicd package
Primarily used for the FabricWorkspace class, but also intended to be leveraged for
any user input throughout the package

"""

logger = logging.getLogger(__name__)


def validate_data_type(expected_type, variable_name, input_value):
    # Mapping of expected types to their validation functions
    type_validators = {
        "string": lambda x: isinstance(x, str),
        "bool": lambda x: isinstance(x, bool),
        "list": lambda x: isinstance(x, list),
        "list[string]": lambda x: isinstance(x, list) and all(isinstance(item, str) for item in x),
        "FabricWorkspace": lambda x: isinstance(x, FabricWorkspace),
        "TokenCredential": lambda x: isinstance(x, TokenCredential),
    }

    # Check if the expected type is valid and if the input matches the expected type
    if expected_type not in type_validators or not type_validators[expected_type](input_value):
        msg = f"The provided {variable_name} is not of type {expected_type}."
        raise InputError(msg, logger)

    return input_value


def validate_item_type_in_scope(input_value, upn_auth):
    accepted_item_types_upn = FabricWorkspace.ACCEPTED_ITEM_TYPES_UPN
    accepted_item_types_non_upn = FabricWorkspace.ACCEPTED_ITEM_TYPES_NON_UPN

    accepted_item_types = accepted_item_types_upn if upn_auth else accepted_item_types_non_upn

    validate_data_type("list[string]", "item_type_in_scope", input_value)

    for item_type in input_value:
        if item_type not in accepted_item_types:
            msg = (
                f"Invalid or unsupported item type: '{item_type}'. "
                f"For User Identity Authentication, must be one of {', '.join(accepted_item_types_upn)}. "
                f"For Service Principal or Managed Identity Authentication, "
                f"must be one of {', '.join(accepted_item_types_non_upn)}."
            )
            raise InputError(msg, logger)

    return input_value


def validate_repository_directory(input_value):
    validate_data_type("string", "repository_directory", input_value)

    if not Path(input_value).is_dir():
        msg = f"The provided repository_directory '{input_value}' does not exist."
        raise InputError(msg, logger)

    return input_value


def validate_base_api_url(input_value):
    validate_data_type("string", "base_api_url", input_value)

    if not re.match(r"^https:\/\/([a-zA-Z0-9]+)\.fabric\.microsoft\.com\/$", input_value):
        msg = (
            "The provided base_api_url does not follow the 'https://<word>.fabric.microsoft.com/' syntax. "
            "Ensure the URL has a single word in between 'https://' and '.fabric.microsoft.com/', "
            "and only contains alphanumeric characters."
        )
        raise InputError(msg, logger)

    return input_value


def validate_workspace_id(input_value):
    validate_data_type("string", "workspace_id", input_value)

    if not re.match(r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", input_value):
        msg = "The provided workspace_id is not a valid guid."
        raise InputError(msg, logger)

    return input_value


def validate_environment(input_value):
    validate_data_type("string", "environment", input_value)

    return input_value


def validate_fabric_workspace_obj(input_value):
    validate_data_type("FabricWorkspace", "fabric_workspace_obj", input_value)

    return input_value


def validate_token_credential(input_value):
    validate_data_type("TokenCredential", "credential", input_value)

    return input_value
