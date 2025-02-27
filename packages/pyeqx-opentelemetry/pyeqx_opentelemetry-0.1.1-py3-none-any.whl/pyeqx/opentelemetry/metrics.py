from dataclasses import dataclass
import logging
import os

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter as GRPCOTLPMetricExporter,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter as HTTPOTLPMetricExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from .constants import (
    DEFAULT_OTLP_GRPC_ENDPOINT,
    DEFAULT_OTLP_METRICS_HTTP_ENDPOINT,
    DEFAULT_OTLP_TYPE,
    OTLP_METRICS_ENDPOINT_KEY,
    OTLP_TYPE,
)

logger = logging.getLogger("pyeqx.opentelemetry")


@dataclass
class MetricInitializationConfig:
    serviceName: str
    type: str
    endpoint: str
    insecure: bool

    def __init__(
        self,
        serviceName: str,
        type: str = None,
        endpoint: str = None,
        insecure: bool = False,
    ):
        self.serviceName = serviceName

        self.__parse(type=type, endpoint=endpoint, insecure=insecure)

    def __parse(self, type: str | None, endpoint: str | None, insecure: bool):
        # parse type
        if type is None:
            parsed_type = os.environ.get(OTLP_TYPE, DEFAULT_OTLP_TYPE)
        else:
            valid_types = ["grpc", "http"]

            raw_type = type.lower()
            if raw_type in valid_types:
                parsed_type = raw_type
            else:
                raise ValueError(
                    f"Invalid type: {raw_type}. Must be one of {valid_types}"
                )

        self.type = parsed_type

        # parse endpoint
        if endpoint is None:
            if self.type == "grpc":
                parsed_endpoint = os.environ.get(
                    OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT
                )
            else:
                parsed_endpoint = os.environ.get(
                    OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_METRICS_HTTP_ENDPOINT
                )
        else:
            parsed_endpoint = endpoint

        self.endpoint = parsed_endpoint
        self.insecure = insecure


def initialize_metric(config: MetricInitializationConfig):
    logger.info("initializing metric")

    # create resource
    resource = Resource.create({SERVICE_NAME: config.serviceName})

    # create exporter
    exporter = __build_exporter(
        type=config.type,
        endpoint=config.endpoint,
        insecure=config.insecure,
    )

    # create meter provider
    provider = MeterProvider(
        resource=resource,
        metric_readers=[
            PeriodicExportingMetricReader(exporter=exporter),
        ],
    )

    # set provider
    metrics.set_meter_provider(meter_provider=provider)

    return provider


def __build_exporter(type: str, endpoint: str, insecure: bool):
    if type == "grpc":
        return GRPCOTLPMetricExporter(endpoint=endpoint, insecure=insecure)
    elif type == "http":
        return HTTPOTLPMetricExporter(endpoint=endpoint)
    else:
        raise ValueError(f"Invalid OTLP type: {type}")
