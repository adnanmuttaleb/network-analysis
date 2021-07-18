# Network-Analysis

## Installation Guide

1. Create new Virtual Environment:

`virtualenv venv`

2. Install requirements:

`pip install -r requirements.txt`

3. Change db setting to your local settings, e.g:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodatabase',
        'USER': 'dbadmin',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. Run migrations:

`python manage.py migrate`

5. Optionally create a superuser in order to log into the admin site:

`python manage.py createsuperuser`


## System Design

Because the system is mainly a data pipeline that run at equal intervals, the diagram-type chosen to illustrate the design is flowchart: 

![FlowChart](https://user-images.githubusercontent.com/9295683/126075765-586c19e6-2464-4952-9225-bdd6ed201675.png)

At the implementation level this pipeline is implemented in two separate modules:

1. `kpis/pipeline.py`: This module is pythonic (has no dependency on Django), and its responsability is to read the files, one by one so that memory footprint 
at minimum, parse them and aggregate them in *pandas* `Dataframe`.

2. `kpis/management/commands/update_network_stats.py`: This is a custom *Django* management command, which initiate the update process and persist the results.
Also in this command, a check is performed to see if we should do the *one-hour* aggregations step. 

To run this pipeline, you could set a cronjob inside the *crontab*, which runs at every 5th minute:

```
 */5 * * * * cd /home/my/NetworkAnalysis && /home/my/virtual/bin/python /home/my/NetworkAnalysis/manage.py update_network_stats > /tmp/cronlog.txt 2>&1

```

## API Design

1. `GET /api/KPIs/`

List all the available KPIs, sample response:

```
[
    {
        "id": 1,
        "name": "ServiceTrafficVolume"
    },
    {
        "id": 2,
        "name": "CellUniqueUsers"
    }
]
```

2. `GET /api/KPIs/<id>/`

List the data available for kpi with identifier `id`. This endpoint is filterbale by three parameters:

- `interval_start_timestamp__gte`: List records with `interval_start_timestamp` greater than or equal to the value passed.

- `interval_end_timestamp__lte`: List records with `interval_end_timestamp` less than or equal to the value passed.

- `interval`: Filter records by interval type *five-minutes* (with value of `1`), or *one-hour* (with value of `2`).

Sample response:

```

Request: GET /api/KPIs/1/?interval_start_timestamp__gte=2021-07-17T23%3A10%3A00Z&interval_end_timestamp__lte=&interval=1

Reponse:

[
    {
        "id": 1,
        "interval_start_timestamp": "2021-07-18T00:00:00Z",
        "interval_end_timestamp": "2021-07-18T00:05:00Z",
        "interval": 1,
        "service_id": 1,
        "total_bytes": 16100
    },
    {
        "id": 2,
        "interval_start_timestamp": "2021-07-18T00:00:00Z",
        "interval_end_timestamp": "2021-07-18T00:05:00Z",
        "interval": 1,
        "service_id": 3,
        "total_bytes": 11500
    },
    {
        "id": 3,
        "interval_start_timestamp": "2021-07-18T00:00:00Z",
        "interval_end_timestamp": "2021-07-18T00:05:00Z",
        "interval": 1,
        "service_id": 2,
        "total_bytes": 9260
    }
]
```







