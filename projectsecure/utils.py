from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response.data.get('detail', None) is not None:
        response.data['error'] = response.data.pop('detail', None)

    return response


def page_not_found(_):
    return Response(data={'error': 'Route not found,'}, status=HTTP_404_NOT_FOUND)


def server_error(_):
    return Response(data={'error': 'Internal server error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


def bad_request(_):
    return Response(data={'error': 'Bad request'}, status=HTTP_400_BAD_REQUEST)


def permission_denied(_):
    return Response(data={'error': 'Forbidden'}, status=HTTP_403_FORBIDDEN)
