from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    response.data['error'] = response.data.pop('detail', None)

    return response
