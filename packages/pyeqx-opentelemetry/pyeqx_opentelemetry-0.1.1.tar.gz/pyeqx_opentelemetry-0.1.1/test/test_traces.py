import logging
import os
from unittest import TestCase
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from src.pyeqx.opentelemetry.constants import (
    DEFAULT_OTLP_GRPC_ENDPOINT,
    DEFAULT_OTLP_TRACES_HTTP_ENDPOINT,
    OTLP_TRACES_ENDPOINT_KEY,
)
from src.pyeqx.opentelemetry.traces import TraceInitializationConfig, initialize_trace


load_dotenv()

default_config = TraceInitializationConfig(
    serviceName="test-service",
    type="grpc",
    endpoint=os.environ.get(OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT),
    insecure=True,
)

provider = initialize_trace(
    config=default_config,
)
exporter = InMemorySpanExporter()
provider.add_span_processor(SimpleSpanProcessor(exporter))


class TestTraces(TestCase):
    def test_initialize_trace_should_success_with_grpc_type(self):
        tracer = trace.get_tracer(instrumenting_module_name="test-service")

        with tracer.start_as_current_span("test-span") as span:
            span.set_attribute("test-attribute", "test-value")

        # retrieve finished spans
        spans = exporter.get_finished_spans()

        self.assertEqual(len(spans), 1)

        # validate span properties
        span = spans[0]
        self.assertEqual(span.name, "test-span")
        self.assertEqual(span.attributes["test-attribute"], "test-value")

    def test_initialize_trace_should_raise_attribute_error_with_no_config(self):
        with self.assertRaises(AttributeError):
            initialize_trace(config=None)

    def test_initialize_trace_should_raise_value_error_with_none_type(self):
        config = TraceInitializationConfig(
            serviceName="test-service",
            type=None,
            endpoint=os.environ.get(
                OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT
            ),
            insecure=True,
        )

        self.assertEqual(config.type, "grpc")

    def test_initialize_trace_should_raise_value_error_with_invalid_type(self):
        with self.assertRaises(ValueError):
            TraceInitializationConfig(
                serviceName="test-service",
                type="invalid",
                endpoint=os.environ.get(
                    OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT
                ),
                insecure=True,
            )

    def test_initialize_trace_should_set_default_endpoint(self):
        grpc_config = TraceInitializationConfig(
            serviceName="test-service",
            type="grpc",
            endpoint=None,
            insecure=True,
        )
        http_config = TraceInitializationConfig(
            serviceName="test-service",
            type="http",
            endpoint=None,
            insecure=True,
        )

        self.assertEqual(
            grpc_config.endpoint,
            os.environ.get(OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT),
        )
        self.assertEqual(
            http_config.endpoint,
            os.environ.get(OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_TRACES_HTTP_ENDPOINT),
        )

    def test_initialize_trace_should_log_already_initialized(self):
        config = TraceInitializationConfig(
            serviceName="test-service",
            type="http",
            endpoint=os.environ.get(
                OTLP_TRACES_ENDPOINT_KEY, DEFAULT_OTLP_TRACES_HTTP_ENDPOINT
            ),
            insecure=True,
        )

        logger = logging.getLogger("opentelemetry")
        with self.assertLogs(logger=logger, level=logging.INFO) as log:
            initialize_trace(
                config=config,
            )

            self.assertTrue(
                any(
                    "Overriding of current TracerProvider is not allowed" in message
                    for message in log.output
                )
            )

    def test_initialize_trace_should_raise_value_error_with_no_valid_type(self):
        with self.assertRaises(ValueError):
            config = TraceInitializationConfig(
                serviceName="test-service",
                type="grpc",
                endpoint=None,
                insecure=True,
            )
            config.type = "invalid"

            initialize_trace(config=config)
