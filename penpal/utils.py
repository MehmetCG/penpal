from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail


def custom_exception_handler(exc, context):
    """
    DRF return all fields with their specific error messages like below example.
    We implement custom exception handler to show only one field in message.

    {
        "username":["A user with that username already exists."],
        "email":["user with this email address already exists."]
    }

    This will return  "username - A user with that username already exists"
    """
    response = exception_handler(exc, context)

    if response is not None:
        for key, value in response.data.items():
            key, value = get_flatten_error(key, value)
            response.data = f"{key} - {value}"
            break

    return response


def get_flatten_error(field, value):
    """Returns string key and string value"""
    if type(value) is dict:
        for key in value:
            field = key
            value = value[key]
            break

    if type(value) is list:
        for item in value:
            if item:
                value = item
                break

    if type(value) is not ErrorDetail:
        field, value = get_flatten_error(field, value)

    return field, value
