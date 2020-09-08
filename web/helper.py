""" Helper for youtube API research class. """

from jsonschema import validate, ValidationError
from json import loads, dumps
from Data import Data
from Items import Items
from flask import jsonify


class InvalidSchemaError(Exception):
    """ Raised if schema is not valid. """


# ! hardcoded schema_errors
schema_errors = [
    "Failed validating 'type' in schema",
    "Failed validating 'required' in schema",
    "Failed validating 'minLength' in schema",
    "Failed validating 'maxLength' in schema",
    "Failed validating 'minimum' in schema",
    "Failed validating 'maximum' in schema",
    "Failed validating 'minItems' in schema",
    "Failed validating 'maxItems' in schema"
]

INVALID_SCHEMA = 451


def validate_schema(schema: dict, data: dict):
    """ Schemma validation.

    Args:
        schema (dict): valid dictionary
        data (dict): dictionary for validation

    Raises:
        InvalidSchemaError: if data (schema) is not valid
    """
    data = dumps(data)
    try:
        validate(loads(data), schema)
    except ValidationError as ex:
        # take exception's string representation
        ex_str = str(ex)
        # looking for message in schema_error that matches our error
        for message in schema_errors:
            if message in ex_str:
                raise InvalidSchemaError(ex_str, INVALID_SCHEMA)


outter_keys_valid = ["kind", "etag", "nextPageToken", "regionCode", "pageInfo"]


def send_data_values(data: dict) -> str:
    """ Send data to Data class as arguments.

    Args:
        data (dict): dictionary with all data

    Raises:
        ValueError: if value on pageInfo key is not valid

    Returns:
        string representation of Data's instance
    """
    values_data = []
    keys = list(data.keys())
    for key in outter_keys_valid:
        # we do the schema validation, so we are sure
        # that all keys exists in dictionary
        values_data.append(data[key])
    data_obj = Data(*values_data)
    # if there is no exception, we want to return Data instance
    # otherwise, exception will be raised
    return str(data_obj)


item_keys_valid = ["kind", "etag", "id"]


def send_items_values(data: dict) -> list:
    """ Send data to Items class as arguments.

    Args:
        data (dict): dictionary with all data

    Raises:
        ValueError: if value on id key is not valid

    Returns:
        list with all Items objects
    """
    items = data["items"]
    data_items = [item[key] for item in items for key in item_keys_valid]
    item_objects_str = []

    for item in items:
        values_list = list(item.values())
        item_object = Items(*values_list)
        item_objects_str.append(str(item_object))

    return item_objects_str


def validation(
    data_outter: dict, data_result: dict, schema: dict
) -> object:
    """ Validation for all data (outter, items and result).

    Args:
        data_outter (dict): outter data dictionary
        data_result (dict): result data dictionary
        schema (dict): schema for validation

    Returns:
        tuple with exception data if exception occured
        list with valid data
    """
    try:
        validate_schema(schema, data_outter)
        validate_schema(schema, data_result)
    except InvalidSchemaError as ex:
        return ex.args[0], ex.args[1]

    try:
        str_data = send_data_values(data_outter)
        str_result = send_data_values(data_result)
    except (KeyError, ValueError) as ex:
        return ex.args[0], ex.args[1]

    try:
        data_items = send_items_values(data_outter)
        result_items = send_items_values(data_result)
    except (KeyError, ValueError) as ex:
        return ex.args[0], ex.args[1]

    return [str_data, str_result, data_items, result_items]
