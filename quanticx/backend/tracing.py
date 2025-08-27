from __future__ import annotations

import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_tracing(app) -> None:
    endpoint = os.getenv('OTLP_ENDPOINT')
    if not endpoint:
        return
    provider = TracerProvider()
    trace.set_tracer_provider(provider)
    span_exporter = OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")
    provider.add_span_processor(BatchSpanProcessor(span_exporter))
    FastAPIInstrumentor.instrument_app(app)

