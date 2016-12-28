from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN


def page_not_found(_):
    return Response(data={'detail': 'Route not found,'}, status=HTTP_404_NOT_FOUND)


def server_error(_):
    return Response(data={'detail': 'Internal server error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


def bad_request(_):
    return Response(data={'detail': 'Bad request'}, status=HTTP_400_BAD_REQUEST)


def permission_denied(_):
    return Response(data={'detail': 'Forbidden'}, status=HTTP_403_FORBIDDEN)
