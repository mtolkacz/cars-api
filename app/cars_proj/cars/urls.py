from django.urls import path
from .views import apiv1, index

app_name = "cars_proj.cars"

urlpatterns = [
    path(
        route='rate/',
        view=apiv1.CarRateAPIView.as_view(),
        name='rate',
    ),
    path(
        route='cars/',
        view=apiv1.CarListCreateUpdateAPIView.as_view(),
        name='list_create_update',
    ),
    path(
        route='popular/',
        view=apiv1.PopularCarListAPIView.as_view(),
        name='popular_list',
    ),
    path(
        route='',
        view=index,
        name='index',
    )
]

