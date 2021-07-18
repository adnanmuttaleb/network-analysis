from django.contrib import admin

from kpis.models import ServiceTrafficVolKPI, CellUniqueUsersKPI, Jobs


class KPIModelAdmin(admin.ModelAdmin):
    list_display = ('interval_start_timestamp',
                    'interval_end_timestamp', 'interval')


admin.site.register(ServiceTrafficVolKPI, KPIModelAdmin)
admin.site.register(CellUniqueUsersKPI, KPIModelAdmin)
admin.site.register(Jobs)
