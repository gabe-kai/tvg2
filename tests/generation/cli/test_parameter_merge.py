# tests/generation/cli/test_parameter_merge.py
"""
Unit tests for resolve_stage_params in cli/parameter_merge.py.
"""

import pytest
from generation.cli.parameter_merge import resolve_stage_params
from generation.cli.constants import CRATON_PARAMS
from shared.config.planet_gen_config import PlanetGenConfig


class DummyConfig:
    """Minimal stand-in for PlanetGenConfig with a craton_seeding block."""
    def __init__(self, craton_seeding=None):
        self.craton_seeding = craton_seeding or {}


def test_merge_prefers_cli_over_config():
    cli_args = {"count": 12}
    config = DummyConfig(craton_seeding={"count": 5})
    result = resolve_stage_params("craton_seeding", CRATON_PARAMS, cli_args, config)
    assert result["count"] == 12


def test_merge_uses_config_when_cli_missing():
    cli_args = {}
    config = DummyConfig(craton_seeding={"count": 7})
    result = resolve_stage_params("craton_seeding", CRATON_PARAMS, cli_args, config)
    assert result["count"] == 7


def test_merge_falls_back_to_schema_default():
    cli_args = {}
    config = DummyConfig(craton_seeding={})
    result = resolve_stage_params("craton_seeding", CRATON_PARAMS, cli_args, config)
    assert result["spacing_factor"] == 1.0


def test_type_coercion_from_cli():
    cli_args = {"count": "8", "spacing_factor": "2.5"}  # strings instead of int/float
    config = DummyConfig()
    result = resolve_stage_params("craton_seeding", CRATON_PARAMS, cli_args, config)
    assert isinstance(result["count"], int)
    assert isinstance(result["spacing_factor"], float)
    assert result["count"] == 8
    assert result["spacing_factor"] == 2.5
