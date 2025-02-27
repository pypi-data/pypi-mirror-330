from dataclasses import dataclass
import logging
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCOTLPSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPOTLPSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .constants import (
    DEFAULT_OTLP_GRPC_ENDPOINT,
    DEFAULT_OTLP_TRACES_HTTP_ENDPOINT,
    DEFAULT_OTLP_TYPE,
    OTLP_TRACES_ENDPOINT_KEY,
    OTLP_TYPE,
)

logger = logging.getLogger("pyeqx.opentelemetry")


@dataclass
class TraceInitializationConfig:
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
                    OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT
                )
            else:
                parsed_endpoint = os.environ.get(
                    OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_TRACES_HTTP_ENDPOINT
                )
        else:
            parsed_endpoint = endpoint

        self.endpoint = parsed_endpoint
        self.insecure = insecure


def initialize_trace(config: TraceInitializationConfig):
    logger.info("initializing trace")

    # create resource
    resource = Resource.create({SERVICE_NAME: config.serviceName})

    # create exporter
    exporter = __build_exporter(
        type=config.type,
        endpoint=config.endpoint,
        insecure=config.insecure,
    )

    # create trace provider
    provider = TracerProvider(
        resource=resource,
    )
    provider.add_span_processor(BatchSpanProcessor(span_exporter=exporter))

    # set provider
    trace.set_tracer_provider(tracer_provider=provider)

    return provider


def __build_exporter(type: str, endpoint: str, insecure: bool):
    if type == "grpc":
        return GRPCOTLPSpanExporter(endpoint=endpoint, insecure=insecure)
    elif type == "http":
        return HTTPOTLPSpanExporter(endpoint=endpoint)
    else:
        raise ValueError(f"Invalid OTLP type: {type}")
