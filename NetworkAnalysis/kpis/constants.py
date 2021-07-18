import enum

from django.db import models


class KPI(enum.IntEnum):

    ServiceTrafficVolume = 1

    CellUniqueUsers = 2


class Interval(models.IntegerChoices):
    FIVE_MINUTES = 1

    ONE_HOUR = 2
