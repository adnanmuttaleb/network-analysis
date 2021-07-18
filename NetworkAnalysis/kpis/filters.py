import django_filters

from kpis.models import ServiceTrafficVolKPI, CellUniqueUsersKPI


class ServiceTrafficVolKPIFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceTrafficVolKPI

        fields = {
            'interval_start_timestamp': ['gte'],
            'interval_end_timestamp': ['lte'],
            'interval': ['exact'],
        }


class CellUniqueUsersKPIFilter(django_filters.FilterSet):
    class Meta:
        model = CellUniqueUsersKPI

        fields = {
            'interval_start_timestamp': ['gte'],
            'interval_end_timestamp': ['lte'],
            'interval': ['exact'],
        }
