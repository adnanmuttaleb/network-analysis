from os import listdir

from datetime import datetime

from os.path import isfile, join
from typing import Dict, Iterable, List, Tuple

from django.conf import settings

import pandas as pd

import pytz

from kpis.constants import KPI


class FileReader:

    INPUT_DIR = settings.INPUT_DIR

    @classmethod
    def get_file_details(cls, file_name: str) -> Tuple[datetime, int]:
        _, ts, index, *_ = file_name.split('.')

        _, ts = ts.split('-')

        return pytz.UTC.localize(datetime.fromtimestamp(int(ts)/1e3)), int(index)

    @classmethod
    def list_files(cls) -> Iterable[Tuple[str, datetime, int]]:
        for file in listdir(cls.INPUT_DIR):

            if isfile(join(cls.INPUT_DIR, file)):

                yield join(cls.INPUT_DIR, file), *cls.get_file_details(file)

    @classmethod
    def list_files_by_interval(cls, interval_start, interval_end) -> Iterable[Tuple[str, datetime, int]]:
        return ((file, ts, indx) for file, ts, indx in cls.list_files() if interval_start <= ts <= interval_end)


class ServiceTrafficVolKPIAgg:

    def __init__(self):
        self.aggregated = None

    def __call__(self, df: pd.DataFrame):
        df["total_bytes"] = df["bytes_downlink"] + df["bytes_uplink"]

        df = df[['service_id', 'total_bytes']]

        total_bytes = df.groupby("service_id").sum().total_bytes

        try:
            self.aggregated = self.aggregated.add(total_bytes, fill_value=0)
        except AttributeError:
            self.aggregated = total_bytes

    def max(self, n=3) -> List[Dict]:
        if self.aggregated is None:
            return []

        top_rows = self.aggregated.sort_values(ascending=False)[:n]

        result = []

        for service_id, total_bytes in top_rows.items():

            result.append(dict(service_id=service_id, total_bytes=total_bytes))

        return result

    @property
    def identifier(self) -> int:
        return KPI.ServiceTrafficVolume


class CellUniqueUsersKPIAgg:

    def __init__(self):
        self.aggregated = None

    def __call__(self, df: pd.DataFrame):
        user_counts = df.groupby(["cell_id", "msisdn"]).size()

        try:
            self.aggregated = self.aggregated.add(user_counts, fill_value=0)
        except AttributeError:
            self.aggregated = user_counts

    def max(self, n=3) -> List[Dict]:
        if self.aggregated is None:
            return []

        top_rows = self.aggregated.groupby(
            level=0).count().sort_values(ascending=False)[:n]

        result = []

        for cell_id, number_of_unique_users in top_rows.items():

            result.append(
                dict(cell_id=cell_id, number_of_unique_users=number_of_unique_users))

        return result

    @property
    def identifier(self) -> int:
        return KPI.CellUniqueUsers


def pipeline(interval_start_ts, interval_end_ts) -> Tuple[int, Dict]:
    kpis = (CellUniqueUsersKPIAgg(), ServiceTrafficVolKPIAgg())

    file_count = 0

    for file, *_ in FileReader.list_files_by_interval(interval_start_ts, interval_end_ts):

        df = pd.read_csv(file)

        for kpi in kpis:

            kpi(df.copy())

        file_count += 1

    return file_count, {kpi.identifier: kpi.max() for kpi in kpis}
