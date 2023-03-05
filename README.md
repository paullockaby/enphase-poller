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
docker run --rm \
    -e ENPHASE_LOCAL_API_URL=$ENPHASE_LOCAL_API_URL \
    enphase_poller
```

## Configuration

### `ENPHASE_LOCAL_API_URL`

The full URL to your local Enphase Envoy Proxy. This might be something like `https://192.168.1.200/` or `https://envoy-proxy.tools.svc.cluster.local`.

## Trademarks

Enphase(R), Envoy(R) are trademarks of Enphase Energy(R).

All trademarks are the property of their respective owners.

Any trademarks used in this project are used in a purely descriptive manner and to state compatability.
