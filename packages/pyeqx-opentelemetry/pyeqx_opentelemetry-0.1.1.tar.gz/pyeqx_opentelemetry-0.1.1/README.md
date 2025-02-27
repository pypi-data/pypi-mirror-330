# esbm-dis-dfts-pyeqx-opentelemetry

This is part of pyeqx with opentelemetry packages. (package: `pyeqx-opentelemetry`)

## Pre-requisites

Python: `3.12`

Dependencies:

- opentelemetry-api
- opentelemetry-sdk
- opentelemetry-exporter-otlp
- opentelemetry-exporter-prometheus

```bash
# setup virtual env
python3.12 -m venv .venv

# activate virtual env
source .venv/bin/activate

# install dependencies
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-exporter-prometheus

# or
pip install -e .[dev]

# install dependencies (If you want to publish)
pip install twine
```

### Environement variables

Create `.env` file with content below

```bash
PYEQX_OTLP_METRICS_ENDPOINT=localhost:4317
PYEQX_OTLP_TRACES_ENDPOINT=localhost:4317

OTLP_METRICS_HTTP_ENDPOINT=http://localhost:4318/v1/metrics
OTLP_TRACES_HTTP_ENDPOINT=http://localhost:4318/v1/traces
```

## Tests

To execute unit test run this command at root of the project

```bash
python3 -m unittest discover test -p "**.py"

# or

pytest test/ --cov=src --cov-report=term-missing
```

To execute test with coverage

```basg
pytest test/ --cov=src
```

## Build

```bash
python3 -m build
```

## Publish

To pypi

```bash
python3 -m twine upload --config-file .pypirc dist/*
```

## Remark


