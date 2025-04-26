"""Unit tests for package import and version."""
from sentiment_analysis import __version__


def test_package_version():
    """Test that the package version is correctly set."""
    assert __version__ == "0.1.0"
