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

## Trademarks

Enphase(R), Envoy(R) are trademarks of Enphase Energy(R).

All trademarks are the property of their respective owners.

Any trademarks used in this project are used in a purely descriptive manner and to state compatability.
