# enphase-poller
An application for polling the Enphase Envoy for power information and storing it into a database.

## Development

This library uses [Python Poetry](https://python-poetry.org/) for builds, tests, and deployment. Once you've installed Poetry you can install this project's dependencies with this command:

```
poetry install
```

Assuming that you have set up your environment as described later in this document, you can test the application by running this command:

```
poetry run enphase_poller --api-url=http://localhost:8080/
```

Still assuming that your environment is configured, an alternative way to run this is with Docker, like this:

```
docker build -t enphase_poller .
docker run --rm enphase_poller --api-url=http://envoy-proxy:8080
```

## Configuration

### `--api-url`

The full URL to your local [Enphase Envoy Proxy](https://github.com/paullockaby/enphase-proxy). This might be something like `http://192.168.1.200/` or `http://enphase-proxy.tools.svc.cluster.local:8080/`.

## Example

Once you've configured your poller to collect the data that you want, [there is an example dashboard in the `examples` directory](https://github.com/paullockaby/enphase-poller/blob/main/examples/basic-grafana-dashboard.png?raw=true). It looks like this:

![Example Grafana Dashboard for Enphase Poller](https://github.com/paullockaby/enphase-poller/blob/main/examples/basic-grafana-dashboard.png?raw=true)

## Notes

If you lose power during the day then your production and consumption data for the day will reset. This is because the Enphase device resets its counters and returns bad data. Currently the way to fix that is to wait until the next day after all of the readings for the day have finished. Then look at the database and find the last reading before the power went out and the last reading for the day. Then update the readings after the last reading before the power reset. (If the power resets multiple times then you may need to redo this.) Run these database queries:

```
SELECT reading_time, vah_today, varh_lag_today, varh_lead_today, wh_today FROM public.consumption ORDER BY reading_time;
SELECT reading_time, vah_today, varh_lag_today, varh_lead_today, wh_today FROM public.production ORDER BY reading_time;

-- change these values as appropriate
UPDATE public.consumption SET
    vah_today = vah_today + 40918.156,
    varh_lag_today = varh_lag_today + 6065.929,
    varh_lead_today = varh_lead_today + 14410.183,
    wh_today = wh_today + 22639.963
    WHERE reading_time > '2023-04-13 22:19:01+00' AND reading_time < '2023-04-14 07:05:10+00';
UPDATE public.production SET
    vah_today = vah_today + 30284.884,
    varh_lag_today = varh_lag_today + 6064.926,
    varh_lead_today = varh_lead_today + 193.035,
    wh_today = wh_today + 24088.960
    WHERE reading_time > '2023-04-13 22:19:01+00' AND reading_time < '2023-04-14 07:05:10+00';
```

## Trademarks

Enphase(R), Envoy(R) are trademarks of Enphase Energy(R).

All trademarks are the property of their respective owners.

Any trademarks used in this project are used in a purely descriptive manner and to state compatability.
