from django.conf import settings
from django.db import models
from django.db.models import Avg, Count

from ..core.utils import Round  # Round rate


class Make(models.Model):
    make_id = models.IntegerField(
        unique=True,
    )
    make_name = models.CharField(
        max_length=200,
        unique=True,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )
    modified_date = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        app_label = 'cars_proj.cars'


class Car(models.Model):
    model_id = models.IntegerField(
        unique=True,
    )
    model_name = models.CharField(
        max_length=200,
        unique=True,
    )
    make = models.ForeignKey(
        Make,
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )
    modified_date = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        app_label = 'cars_proj.cars'

    def get_average_rate(self):
        return Rate.objects.filter(car=self).aggregate(rate__avg=Round(Avg('rate')))['rate__avg']

    @staticmethod
    def get_popular():
        return Rate.objects.annotate(
            count=Count('id')
        ).order_by(
            '-count'
        )[:10]


class Rate(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    rate = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        app_label = 'cars_proj.cars'
        constraints = [
            models.CheckConstraint(
                check=models.Q(rate__gte=1) & models.Q(rate__lte=5),
                name="A rate value is valid between 1 and 10",
            )
        ]
        unique_together = (
            'car',
            'user',
        )
