"""Tests for version utilities."""

import pytest
from apkpatcher.utils.versions import compare_versions, is_version_newer


def test_compare_versions_equal():
    """Test version comparison for equal versions."""
    assert compare_versions("1.0.0", "1.0.0") == 0


def test_compare_versions_newer():
    """Test version comparison for newer version."""
    assert compare_versions("1.0.0", "1.0.1") == -1
    assert compare_versions("1.0.1", "1.0.0") == 1


def test_compare_versions_major():
    """Test version comparison for major versions."""
    assert compare_versions("1.0.0", "2.0.0") == -1
    assert compare_versions("2.0.0", "1.0.0") == 1


def test_is_version_newer():
    """Test version newer check."""
    assert is_version_newer("1.0.0", "1.0.1") == True
    assert is_version_newer("1.0.1", "1.0.0") == False
    assert is_version_newer("1.0.0", "1.0.0") == False
