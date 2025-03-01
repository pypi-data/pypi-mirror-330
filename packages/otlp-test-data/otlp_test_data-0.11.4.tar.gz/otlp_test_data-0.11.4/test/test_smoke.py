import json

from otlp_test_data import sample_proto, sample_spans, sample_json


def test_spans():
    assert sample_spans()


def test_json():
    data = sample_json()
    assert json.loads(data)
    # Ensure that all enum labels have been converted to ints
    assert b"SPAN_KIND_" not in data
    assert b"SPAN_FLAGS_" not in data
    assert b"STATUS_CODE_" not in data
    # Metrics
    assert b"AGGREGATION_TEMPORALITY_" not in data
    assert b"DATA_POINT_FLAGS_" not in data
    # Logs
    assert b"SEVERITY_NUMBER_" not in data
    assert b"LOG_RECORD_FLAGS_" not in data


def test_proto():
    assert sample_proto()
