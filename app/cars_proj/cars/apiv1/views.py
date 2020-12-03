from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CarSerializer, PopularCarSerializer
from ..mixins import CarCreateUpdateMixin, CarRateMixin
from ..models import Car, Rate


class CarAPIView(APIView):
    model = Car


class CarListCreateUpdateAPIView(CarCreateUpdateMixin, CarAPIView, ListCreateAPIView):
    """
    Concrete view to list or to create/update Car model instances.
    """
    template_name = 'cars/list.html'
    serializer_class = CarSerializer
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Car.objects.all().only(
        'model_name',
        'make__make_name',
    )
    # queryset = Car.objects.all()
    # queryset = Car.objects.all()

    def get(self, request, *args, **kwargs):
        cars = self.get_queryset()
        serialized_books = self.get_serializer(cars, many=True)
        context = {
            'cars': serialized_books.data
        }
        print(context)
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            car_obj, response_code = self.create_or_update(request, *args, **kwargs)

        # catch any APIException during create/update operation
        except APIException as err:
            response_code = err.status_code
            context = {
                'error_detail': err,
            }

        # when create/update operation has been successful then prepare serialized data
        else:
            print(self.queryset)
            serialized_car = self.get_serializer(car_obj)
            print(serialized_car.data)
            context = {
                'car': serialized_car.data,
                'response_code': response_code,
            }

        return Response(context, status=response_code)


class PopularCarListAPIView(CarCreateUpdateMixin, CarAPIView, ListAPIView):
    """
    Concrete view to list of the most popular Car model instances.
    """
    template_name = 'cars/popular.html'
    serializer_class = PopularCarSerializer
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Rate.objects.select_related(
        'car'
    ).values(
        'car__id',
        'car__model_name',
        'car__make__make_name'
    ).annotate(
        count=Count('id')
    ).order_by(
        '-count'
    )[:10]

    def get(self, request, *args, **kwargs):
        cars = self.get_queryset()
        serialized_books = self.get_serializer(cars, many=True)
        context = {
            'cars': serialized_books.data
        }
        return Response(context, status=status.HTTP_200_OK)


class CarRateAPIView(CarRateMixin, CarAPIView, CreateAPIView):
    """
    View to rate car models.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        obj = self.create_rate(request)

        return Response(f"Success: car={obj.car.model_name}, rate={obj.rate}, user={obj.user.username}",
                        status=status.HTTP_200_OK)

