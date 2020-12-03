from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class InvalidQueryParameterInBody(APIException):
    """
    Raised when parameter passed in body is invalid
    In case of car, there is no 'make' and/or 'model' parameter provided.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid key has been passed in request body.')


class CarDownloaderException(APIException):
    """
    Raised when car downloading has been failed
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('CarDownloader exception.')


class CarParserException(APIException):
    """
    Raised when response deserialization has been failed
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Incorrect input data for car.')


class CarDoesNotExists(APIException):
    """
    Raised when no car has been found in source
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Cars not exists.')


class CarNotFound(APIException):
    """
    Raised when no car has been found in source
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Car not found.')


class MakeIdNotFound(APIException):
    """
    Raised when make id has not been found in source
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Make ID not found.')


class IncorrectRateBody(APIException):
    """
    Raised when provided incorrect data in Rate body.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Incorrect data provided in Rate body.')


class APIIntegrityError(APIException):
    """
    Raised when IntegrityError occurred during database operation.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('IntegrityError occurred during database operation.')


class CarDatabaseFailure(APIException):
    """
    Raised when car has not been created or updated
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Car not created or updated.')

