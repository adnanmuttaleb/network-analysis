from django.urls import path

from kpis.constants import KPI
from kpis.views import ServiceTrafficVolKPIListView, CellUniqueUsersKPIListView, KPIsListView


urlpatterns = [
    path('KPIs/', KPIsListView.as_view(), name='list-kpis'),

    path(f'KPIs/{KPI.ServiceTrafficVolume}/',
         ServiceTrafficVolKPIListView.as_view(), name=KPI.ServiceTrafficVolume.name),

    path(f'KPIs/{KPI.CellUniqueUsers}/',
         CellUniqueUsersKPIListView.as_view(), name=KPI.CellUniqueUsers.name)
]
