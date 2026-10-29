"""
Unit tests for Industrial Resilience Engine
"""

import os
import pytest
import time
from agentic_chemeng.resilience import (
    ensure_com_initialized,
    run_with_timeout,
    validate_file_path,
    cleanup_stale_processes,
    build_response,
    EngineeringTimeoutError,
    EngineeringValidationError
)


def test_ensure_com_initialized():
    ensure_com_initialized()
    # Idempotent call
    ensure_com_initialized()


def test_run_with_timeout_success():
    def fast_fn(x, y):
        return x + y

    res = run_with_timeout(fast_fn, 10, 20, timeout_sec=2.0)
    assert res == 30


def test_run_with_timeout_exceeded():
    def slow_fn():
        time.sleep(1.0)
        return "done"

    with pytest.raises(EngineeringTimeoutError):
        run_with_timeout(slow_fn, timeout_sec=0.1)


def test_validate_file_path():
    # Valid existing file
    cur_file = os.path.abspath(__file__)
    val = validate_file_path(cur_file, allowed_extensions=[".py"], must_exist=True)
    assert os.path.exists(val)

    # Disallowed extension
    with pytest.raises(EngineeringValidationError):
        validate_file_path(cur_file, allowed_extensions=[".txt"])

    # Non-existent file with must_exist=True
    with pytest.raises(EngineeringValidationError):
        validate_file_path("non_existent_file.py", must_exist=True)


def test_build_response():
    resp = build_response(status="success", data={"cad_model": "TK-101A"})
    assert resp["status"] == "success"
    assert "timestamp_utc" in resp
    assert resp["data"]["cad_model"] == "TK-101A"

