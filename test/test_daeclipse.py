"""Test to cover daeclipse library."""

from daeclipse import __version__


def test_version():
    """Test daeclipse library version."""
    assert __version__ == '0.1.0'
