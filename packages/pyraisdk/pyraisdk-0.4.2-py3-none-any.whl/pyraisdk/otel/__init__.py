import logging
import os
import signal
import threading
from typing import Optional
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators import composite
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
from opentelemetry.sdk.metrics import MeterProvider, Counter, UpDownCounter, Histogram, ObservableCounter, ObservableUpDownCounter, ObservableGauge
from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_NAMESPACE, SERVICE_VERSION, SERVICE_INSTANCE_ID, HOST_NAME
from opentelemetry.semconv.metrics import MetricInstruments
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View

from .auth import AuthClient
from .config import OtelConfig
from .customExporter import CustomOTLPMetricExporter

_logger = logging.getLogger("pyraisdk.otel")
_stop_evt = threading.Event()

otel_config = OtelConfig()

def initialize(
    service_name: Optional[str] = None, 
    service_namespace: Optional[str] = None, 
    service_version: Optional[str]=None, 
    service_instance_id: Optional[str]=None
):
    if not otel_config.is_active():
        _logger.warning(f"Not configuring OTEL due to missing configuration")
        return

    if OTEL_EXPORTER_OTLP_ENDPOINT not in  os.environ:
        os.environ.setdefault(OTEL_EXPORTER_OTLP_ENDPOINT, otel_config.endpoint)

    if OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE not in os.environ:
        os.environ.setdefault(OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE, "DELTA")

    res = Resource(
            attributes={
                SERVICE_NAME: service_name if service_name != None else os.environ.get("ENDPOINT_NAME", ""),
                SERVICE_NAMESPACE: service_namespace if service_namespace != None else os.environ.get("MODEL_NAME", ""),
                SERVICE_VERSION: service_version if service_version != None else os.environ.get("ENDPOINT_VERSION", ""),
                SERVICE_INSTANCE_ID: service_instance_id if service_instance_id != None else f"{os.environ.get('MODEL_NAME', '')}|{os.environ.get('ENDPOINT_NAME', '')}|{os.environ.get('ENDPOINT_VERSION', '')}|{os.environ.get('HOSTNAME', '')}" ,
            },
            schema_url=MetricInstruments.SCHEMA_URL
        )
    auth_client = AuthClient(otel_config, _stop_evt)
    try:
        # attempt getting the token to avoid configuring OTEL in case of errors
        auth_client.get_token()
        set_global_textmap(composite.CompositePropagator([TraceContextTextMapPropagator(), W3CBaggagePropagator()]))

        exporter = CustomOTLPMetricExporter(auth_client)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis= 30 * 1000)
        meter_provider = MeterProvider(metric_readers=[reader], resource=res, views=[View(
            instrument_name="*", 
            # The default bucket boundaries are (0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000).
            # This is not good enough for our latency measurement, thus adding more buckets from 0 - 100.
            # Also, we have a lot of model latency where p99 is around 100 - 200 ms. Thus, we are adding 125, 150, 175, 200, and 350
            # to create a few more buckets. This should not significantly increase memory usage, but it will give us a better percentile demonstration.
            # NOTE: Keep this in sync wtih bucketBoundaries at pkg/raiootel/log/logimp.go line #104
            aggregation=ExplicitBucketHistogramAggregation(
                [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 125, 150, 175, 200, 250, 350, 500, 750, 1000, 2500, 5000, 7500, 10000]
        ))])
        set_meter_provider(meter_provider) 
        
        def handle_signal(signal_number, frame):
            _logger.warning(f"Received signal: {signal_number}")
            shutdown()

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
    except:
        _stop_evt.set()
        _logger.error(f"Skipping OTEL due to error", exc_info=True)

def shutdown():
    if not _stop_evt.is_set():
        _logger.warning(f"Shutting down OTEL")
        _stop_evt.set()
        try:
            meter_provider = get_meter_provider()
            if hasattr(meter_provider, "shutdown") and callable(meter_provider.shutdown):
                meter_provider.shutdown() # this will internally shutdown the exporter, reader and provider
        except:
            # swallow errors during shutdown to avoid breaking the main process
            _logger.error("Error during meter provider shutdown", exc_info=True)
            return