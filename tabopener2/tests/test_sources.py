import json
import os
import tempfile

import pytest
import sources


def test_format_model_display_claude():
    assert sources.format_model_display("claude-haiku-4-5") == "Haiku 4.5"
    assert sources.format_model_display("claude-sonnet-4-6") == "Sonnet 4.6"
    assert sources.format_model_display("claude-opus-4-7") == "Opus 4.7"


def test_format_model_display_passthrough():
    assert sources.format_model_display("gemini-2.5-pro") == "gemini-2.5-pro"
    assert sources.format_model_display("") == ""
    assert sources.format_model_display(None) == ""


def test_parse_last_usage_returns_zeros_for_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write("")
        path = f.name
    try:
        total, pct, cache_r, model = sources.parse_last_usage(path)
        assert total == 0
        assert pct == 0
        assert cache_r == 0
        assert model is None
    finally:
        os.unlink(path)


def test_parse_last_usage_reads_tokens():
    line = json.dumps({
        "message": {
            "model": "claude-sonnet-4-6",
            "usage": {
                "input_tokens": 50000,
                "cache_read_input_tokens": 10000,
                "cache_creation_input_tokens": 0,
                "output_tokens": 2000,
            }
        }
    })
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(line + "\n")
        path = f.name
    try:
        total, pct, cache_r, model = sources.parse_last_usage(path)
        assert total == 62000
        assert pct == round(min(100, 62000 / 200000 * 100))
        assert cache_r == 10000
        assert model == "claude-sonnet-4-6"
    finally:
        os.unlink(path)


def test_parse_last_usage_skips_synthetic():
    line = json.dumps({
        "message": {"model": "<synthetic>", "usage": {"input_tokens": 1000}}
    })
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(line + "\n")
        path = f.name
    try:
        _, _, _, model = sources.parse_last_usage(path)
        assert model is None
    finally:
        os.unlink(path)


def test_gemini_project_hash_is_sha256():
    import hashlib
    cwd = "/Users/test/myproject"
    expected = hashlib.sha256(os.path.abspath(cwd).encode()).hexdigest()
    assert sources._gemini_project_hash(cwd) == expected
