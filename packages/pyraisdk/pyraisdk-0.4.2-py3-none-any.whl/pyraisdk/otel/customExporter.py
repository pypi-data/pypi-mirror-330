
import logging
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricExportResult, MetricsData

from .auth import AuthClient

logger = logging.getLogger("otel.CustomOTLPMetricExporter")
class CustomOTLPMetricExporter(OTLPMetricExporter):
    def __init__(self, auth_client: AuthClient, **kwargs):
        self.auth_client = auth_client
        super().__init__(**kwargs)

    def export(self,
        metrics_data: MetricsData,
        timeout_millis: float = 10_000,
        **kwargs):
        try:
            token =  self.auth_client.get_token()
            self.update_authorization_header(token.token)
        except:
            logger.error(f"Skipping export due to Token fetch error.", exc_info=True)
            return MetricExportResult.FAILURE
        return super().export(metrics_data, timeout_millis, **kwargs)

    def update_authorization_header(self, token: str):
        token = token if token.startswith("Bearer ") else f"Bearer {token}"
        self._session.headers.update({
            "authorization": token
        })