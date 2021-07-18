from rest_framework.generics import ListAPIView

from kpis.constants import KPI
from kpis.models import ServiceTrafficVolKPI, CellUniqueUsersKPI
from kpis.serializers import ServiceTrafficVolKPISerializer, CellUniqueUsersKPISerizliezer, KPIsSerializer
from kpis.filters import CellUniqueUsersKPIFilter, ServiceTrafficVolKPIFilter


class KPIsListView(ListAPIView):
    serializer_class = KPIsSerializer
    queryset = KPI


class ServiceTrafficVolKPIListView(ListAPIView):
    queryset = ServiceTrafficVolKPI.objects.all()

    serializer_class = ServiceTrafficVolKPISerializer

    filter_class = ServiceTrafficVolKPIFilter


class CellUniqueUsersKPIListView(ListAPIView):
    queryset = CellUniqueUsersKPI.objects.all()

    serializer_class = CellUniqueUsersKPISerizliezer

    filter_class = CellUniqueUsersKPIFilter
