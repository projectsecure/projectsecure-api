from rest_framework.exceptions import APIException


class NotCompletedError(APIException):
    status_code = 400
    default_detail = 'Not all steps completed.'
    default_code = 'bad_request'


class AlreadyCompletedError(APIException):
    status_code = 400
    default_detail = 'Already completed.'
    default_code = 'bad_request'


class NotStartedError(APIException):
    status_code = 400
    default_detail = 'Not yet started.'
    default_code = 'bad_request'


class AlreadyStartedError(APIException):
    status_code = 400
    default_detail = 'Challenge was already started.'
    default_code = 'bad_request'
