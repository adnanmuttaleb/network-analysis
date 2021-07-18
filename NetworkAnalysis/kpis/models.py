from django.db import models
from django.db.models.aggregates import Sum
from numpy import mod

from kpis.constants import KPI, Interval


class BaseKPI(models.Model):
    interval_start_timestamp = models.DateTimeField()

    interval_end_timestamp = models.DateTimeField()

    interval = models.SmallIntegerField(
        choices=Interval.choices, default=Interval.FIVE_MINUTES)

    class Meta:
        abstract = True


class ServiceTrafficVolKPIManager(models.Manager):

    def aggregate_stats(self, start_date, end_date, n=3):
        qs = self.get_queryset() \
            .filter(interval_end_timestamp__lte=end_date, interval_start_timestamp__gte=start_date) \
            .values('service_id') \
            .annotate(total_bytes=Sum('total_bytes')) \
            .order_by('-total_bytes')

        return qs[:n]


class ServiceTrafficVolKPI(BaseKPI):
    service_id = models.IntegerField()

    total_bytes = models.IntegerField()

    objects = ServiceTrafficVolKPIManager()

    identifier = KPI.ServiceTrafficVolume


class CellUniqueUsersKPIManager(models.Manager):

    def aggregate_stats(self, start_date, end_date, n=3):
        qs = self.get_queryset() \
            .filter(interval_end_timestamp__lte=end_date, interval_start_timestamp__gte=start_date) \
            .values('cell_id') \
            .annotate(number_of_unique_users=Sum('number_of_unique_users')) \
            .order_by('-number_of_unique_users')

        return qs[:n]


class CellUniqueUsersKPI(BaseKPI):
    cell_id = models.IntegerField()

    number_of_unique_users = models.IntegerField()

    objects = CellUniqueUsersKPIManager()

    identifier = KPI.CellUniqueUsers


class Jobs(models.Model):
    total_file_count = models.IntegerField()

    end_date = models.DateTimeField(db_index=True)

    def __str__(self) -> str:
        return str(self.end_date)
