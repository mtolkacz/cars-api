from django.urls import path
from .views import apiv1, index

app_name = "cars_proj.cars"

urlpatterns = [
#     # /cars
#     # eg. /cars?author=Howard&published_date=2006&published_date=1995&ordering=-published_date
#     path(
#         route='cars',
#         view=apiv1.BookListAPIView.as_view(),
#         name='list',
#     ),
#     # /cars/:pk
#     # eg. /cars/ML6TpwAACAAJ
#     path(
#         route='cars/<str:book_id>',
#         view=apiv1.BookRetrieveAPIView.as_view(),
#         name='single',
#     ),
#     # /db/
#     # eg. curl -X  POST -d "q=Hobbit' http://{host:8000}/db/
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
    # /
    path(
        route='',
        view=index,
        name='index',
    )
]

