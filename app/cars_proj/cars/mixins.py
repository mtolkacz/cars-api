import logging

from django.db import IntegrityError
from rest_framework import status

from .models import Make, Car, Rate
from ..core.utils import deserialize_response, get_response
from .exceptions import InvalidQueryParameterInBody, CarNotFound, CarParserException, MakeIdNotFound, \
    CarDatabaseFailure, IncorrectRateBody, APIIntegrityError

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CarDownloader:
    source_url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/"

    def __init__(self, make_name, model_name):

        # "make" parameter from POST body
        self.make_name = make_name

        # "model" parameter from POST body
        self.model_name = model_name

        # URL from which json is downloaded
        self.url = self.source_url + (self.make_name or '') + '?format=json'

        # A json response placeholder
        self.response = None

        # Make object placeholder
        self.make_obj = None

        # Car dict from json document
        self.car_dict = {}

    def get_cars(self):
        """
        Get and deserialize response.
        Return car dictionary if success and exist, else raise CarNotFound.
        """

        # Get and set response. May raise GetResponseError.
        self.set_response()

        car_json = deserialize_response(self.response)
        return car_json

    def manage_make(self):
        if 'make_id' in self.car_dict:
            make_id = self.car_dict['make_id']
            self.car_dict['make'], created = Make.objects.update_or_create(
                make_name=self.make_name,
                make_id=make_id,
            )

            self.car_dict.pop('make_id')  # to prevent inserting this field to car model
        else:
            raise MakeIdNotFound

    def manage_car(self):
        """
        Create or update car
        """
        # To consider more efficient db operation, like update if changed
        obj, created = Car.objects.update_or_create(**self.car_dict)

        if not obj:
            raise CarDatabaseFailure

        return obj, created

    def set_response(self):
        self.response = get_response(self.url)

    def set_car(self):
        car_json = self.get_cars()
        try:
            cars = car_json['Results']
            for car in cars:
                if self.model_name == car['Model_Name']:
                    self.car_dict['model_id'] = car['Model_ID']
                    self.car_dict['model_name'] = car['Model_Name']
                    self.car_dict['make_id'] = car['Make_ID']
                    break
        except KeyError as err:
            logger.error(f"Incorrect input data. Critical car data is not provided - {err}")
            raise CarParserException

        if not self.car_dict:
            logger.error(f"Car not found")
            raise CarNotFound

    def perform(self):
        """
        Get and set car and make and try to create/update model's object
        :return: Car object and response code (200/201).
        """
        self.set_car()  # Try to get car from source and raise exceptions if failed
        self.manage_make()  # Update or create make model object
        obj, created = self.manage_car()  # Update or create car model object
        response_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return obj, response_code


class CarCreateUpdateMixin(object):
    """
    Create/update car model instances.
    """

    @staticmethod
    def get_parameters(request):
        """
        Get and set POST request "make" and "model" parameters.
        :return: Value of POST parameters, otherwise raise an InvalidQueryParameterInBody exception
        """

        make, model = request.POST.get("make", "").upper(), request.POST.get("model", "")
        if not make or not model:
            raise InvalidQueryParameterInBody
        return make, model

    def create_or_update(self, request, *args, **kwargs):
        """
        Process request to create/update cars.
        :return: Response with status code 201 if success.
        """
        # Get "make" and "model" parameters. May raise InvalidQueryParameterInBody exception
        make_name, model_name = self.get_parameters(request)

        # Proper create/update operation
        # Return car object and response code
        return CarDownloader(make_name, model_name).perform()


class CarRateMixin(object):

    @staticmethod
    def get_rate(request, *args, **kwargs):
        """
        Get car by pk
        :return: Integer value of the model rate from POST request.
        """
        try:
            rate = int(request.POST.get("rate"))
        except(TypeError, ValueError, OverflowError):
            raise IncorrectRateBody(f"Incorrect rate value '{request.POST.get('rate', '')}' provided in the Rate body.")

        return rate

    def get_object(self, request, *args, **kwargs):
        """
        Get car object by its pk passed in POST request body.
        """
        try:
            pk = request.POST.get("pk")
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise CarNotFound
        except ValueError:
            raise IncorrectRateBody('Incorrect primary key of the Car provided in the Rate body.')

    def create_rate(self, request):
        """
        Create rate based on POST request.
        :param request
        :return: Rate
        """
        car = self.get_object(request)
        rate = self.get_rate(request)
        user = request.user
        try:
            return Rate.objects.create(car=car, rate=rate, user=user)
        except IntegrityError:
            raise APIIntegrityError('Integrity error while creating the Rate model object.')
