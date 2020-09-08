from jsonschema import validate, ValidationError
from json import loads, dumps
from Data import Data
from Items import Items


class InvalidSchemaError(Exception):
    """ Raised if schema is not valid. """


# todo: write docummentation and comments

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
        ex_str = str(ex)
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
        string representation of Data instance
    """
    values_data = []
    keys = list(data.keys())
    for key in outter_keys_valid:
        # we do the schema validation, so we are sure
        # that all keys exists in dictionary
        values_data.append(data[key])
    data_obj = Data(*values_data)
    data_obj.page_info_validation()
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
        item_object.id_validation()
        item_objects_str.append(str(item_object))

    return item_objects_str


def caller(data: object, helper_function: callable) -> object:
    """ Calling function and sending an argument.

    Args:
        data (object): that we want to send as argument
        helper_function (callable): function that we want to call

    Returns:
        KeyError or ValueError exception instance if exception is occured
        if data is valid, we want to return result from function
    """
    try:
        data = helper_function(data)
    except (KeyError, ValueError) as ex:
        return ex
    else:
        return data
