import logging
import os
from unittest import TestCase
from dotenv import load_dotenv

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter as HTTPOTLPMetricExporter,
)
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from src.pyeqx.opentelemetry.constants import (
    DEFAULT_OTLP_GRPC_ENDPOINT,
    DEFAULT_OTLP_METRICS_HTTP_ENDPOINT,
)
from src.pyeqx.opentelemetry.metrics import (
    OTLP_METRICS_ENDPOINT_KEY,
    MetricInitializationConfig,
    initialize_metric,
)

load_dotenv()

default_config = MetricInitializationConfig(
    serviceName="test-service",
    type="grpc",
    endpoint=os.environ.get(OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT),
    insecure=True,
)

provider = initialize_metric(config=default_config)


class TestMetrics(TestCase):
    def test_initialize_metric_should_success_with_grpc_type(self):

        meter = metrics.get_meter(name="test-service")

        counter = meter.create_counter(name="test_counter", description="test counter")
        counter.add(10)

        self.assertEqual(meter.name, "test-service")
        self.assertIsNotNone(counter)

    def test_initialize_metric_should_success_with_http_type(self):
        original_readers = provider._all_metric_readers.copy()

        exporter = HTTPOTLPMetricExporter(endpoint=default_config.endpoint)
        reader = PeriodicExportingMetricReader(exporter=exporter)

        provider._all_metric_readers = [reader]

        meter = metrics.get_meter(name="test-service")

        counter = meter.create_counter(name="test_counter", description="test counter")
        counter.add(19)

        self.assertEqual(meter.name, "test-service")
        self.assertIsNotNone(counter)

        provider._all_metric_readers = original_readers

    def test_initialize_metric_should_raise_attribute_error_with_no_config(self):
        with self.assertRaises(AttributeError):
            initialize_metric(config=None)

    def test_initialize_metric_should_raise_value_error_with_none_type(self):
        config = MetricInitializationConfig(
            serviceName="test-service",
            type=None,
            endpoint=os.environ.get(
                OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT
            ),
            insecure=True,
        )

        self.assertEqual(config.type, "grpc")

    def test_initialize_metric_should_raise_value_error_with_invalid_type(self):
        with self.assertRaises(ValueError):
            MetricInitializationConfig(
                serviceName="test-service",
                type="invalid",
                endpoint=os.environ.get(
                    OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT
                ),
                insecure=True,
            )

    def test_initialize_metric_should_set_default_endpoint(self):
        grpc_config = MetricInitializationConfig(
            serviceName="test-service",
            type="grpc",
            endpoint=None,
            insecure=True,
        )
        http_config = MetricInitializationConfig(
            serviceName="test-service",
            type="http",
            endpoint=None,
            insecure=True,
        )

        self.assertEqual(
            grpc_config.endpoint,
            os.environ.get(OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_GRPC_ENDPOINT),
        )
        self.assertEqual(
            http_config.endpoint,
            os.environ.get(
                OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_METRICS_HTTP_ENDPOINT
            ),
        )

    def test_initialize_metric_should_log_already_initialized(self):
        config = MetricInitializationConfig(
            serviceName="test-service",
            type="http",
            endpoint=os.environ.get(
                OTLP_METRICS_ENDPOINT_KEY, DEFAULT_OTLP_METRICS_HTTP_ENDPOINT
            ),
            insecure=True,
        )

        logger = logging.getLogger("opentelemetry")
        with self.assertLogs(logger=logger, level=logging.WARNING) as log:
            initialize_metric(config=config)

            self.assertTrue(
                any(
                    "Overriding of current MeterProvider is not allowed" in message
                    for message in log.output
                )
            )

    def test_initialize_metric_should_raise_value_error_with_no_valid_type(self):
        with self.assertRaises(ValueError):
            config = MetricInitializationConfig(
                serviceName="test-service",
                type="grpc",
                endpoint=None,
                insecure=True,
            )
            config.type = "invalid"

            initialize_metric(config=config)
