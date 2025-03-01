"""Test that the workflow module imports are correct."""

import pytest


def test_workflow_imports():
    """Test that the workflow module imports are correct."""
    from chime_frb_api.modules import buckets, results  # noqa: F401
    from chime_frb_api.workflow import Work  # noqa: F401

    with pytest.raises(DeprecationWarning):
        buckets.Buckets()

    with pytest.raises(DeprecationWarning):
        results.Results()
