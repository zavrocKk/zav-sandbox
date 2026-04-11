"""Benchmarks GSANE — mesure les performances des composants critiques."""

import glob
import time

import pytest
import yaml
from compression_tool import (
    gsane_fetch_compressed_memory,
    gsane_read_checkpoint,
    gsane_route,
)

pytestmark = pytest.mark.benchmark


def _get_baselines():
    with open("_gsane/config.yaml", encoding="utf-8") as f:
        c = yaml.safe_load(f)
    return c.get("benchmarks", {}).get("baselines", {})


def test_gsane_route_performance():
    """gsane_route doit répondre en moins de 100ms."""
    limit = _get_baselines().get("gsane_route_ms", 100)
    start = time.perf_counter()
    result = gsane_route("implement a new feature")
    elapsed = (time.perf_counter() - start) * 1000
    assert result is not None
    assert elapsed < limit, f"gsane_route régression: {elapsed:.1f}ms > {limit}ms"


def test_yaml_manifest_parse_performance():
    """Parser tous les YAML config doit prendre moins de 50ms."""
    limit = _get_baselines().get("yaml_parse_ms", 50)
    start = time.perf_counter()
    files = glob.glob("_gsane/_config/*.yaml")
    for f in files:
        with open(f, encoding="utf-8") as fh:
            yaml.safe_load(fh)
    elapsed = (time.perf_counter() - start) * 1000
    assert elapsed < limit, f"YAML parse régression: {elapsed:.1f}ms > {limit}ms"


def test_fetch_memory_performance():
    """fetch_compressed_memory doit répondre en moins de 200ms."""
    limit = _get_baselines().get("gsane_fetch_memory_ms", 200)
    start = time.perf_counter()
    result = gsane_fetch_compressed_memory("master")
    elapsed = (time.perf_counter() - start) * 1000
    assert result is not None
    assert elapsed < limit, f"fetch_memory régression: {elapsed:.1f}ms > {limit}ms"


def test_checkpoint_read_performance():
    """read_checkpoint doit répondre en moins de 100ms."""
    limit = _get_baselines().get("checkpoint_read_ms", 100)
    start = time.perf_counter()
    result = gsane_read_checkpoint()
    elapsed = (time.perf_counter() - start) * 1000
    assert result is not None
    assert elapsed < limit, f"checkpoint_read régression: {elapsed:.1f}ms > {limit}ms"
