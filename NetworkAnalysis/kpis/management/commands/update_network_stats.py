from datetime import datetime, tzinfo
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import pytz

from kpis.constants import Interval
from kpis.pipeline import pipeline
from kpis.models import CellUniqueUsersKPI, ServiceTrafficVolKPI, Jobs


class Command(BaseCommand):
    help = 'Update Network Statistics'

    def persist_result(self, start_date, end_date, interval, data):
        ServiceTrafficVolKPI.objects.bulk_create([
            ServiceTrafficVolKPI(
                interval_start_timestamp=start_date, interval_end_timestamp=end_date, interval=interval, **row) for row in data[ServiceTrafficVolKPI.identifier]
        ])

        CellUniqueUsersKPI.objects.bulk_create([
            CellUniqueUsersKPI(
                interval_start_timestamp=start_date,  interval_end_timestamp=end_date, interval=interval, **row) for row in data[CellUniqueUsersKPI.identifier]
        ])

    def aggregate_last_hour_stats(self, end_date: datetime):
        start_date = end_date - timedelta(hours=1)

        data = {
            ServiceTrafficVolKPI.identifier: ServiceTrafficVolKPI.objects.aggregate_stats(
                start_date, end_date),
            CellUniqueUsersKPI.identifier: CellUniqueUsersKPI.objects.aggregate_stats(
                start_date, end_date)
        }

        self.persist_result(start_date, end_date, Interval.ONE_HOUR, data)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated Network stats for hour {start_date}--{end_date}'))

    def handle(self, *args, **options):
        try:
            last_job_end_date = Jobs.objects.latest(
                'end_date').end_date
        except Jobs.DoesNotExist:
            last_job_end_date = datetime.today().replace(
                hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)

        current_job_end_date = last_job_end_date + \
            timedelta(minutes=5)

        total_file_count, data = pipeline(
            current_job_end_date, current_job_end_date + timedelta(minutes=1))

        self.persist_result(last_job_end_date,
                            current_job_end_date, Interval.FIVE_MINUTES, data)

        Jobs.objects.create(total_file_count=total_file_count,
                            end_date=current_job_end_date)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated Network stats for interval {last_job_end_date}--{current_job_end_date}'))

        if current_job_end_date.minute == 0 or settings.DEBUG:
            self.aggregate_last_hour_stats(current_job_end_date)
