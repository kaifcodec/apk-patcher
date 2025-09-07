"""Tests for Frida service functionality."""

import pytest
from pathlib import Path
from apkpatcher.services.frida import FridaService


def test_arch_mapping():
    """Test architecture mapping."""
    service = FridaService(verbose=False)
    assert "arm" in service.ARCH_MAPPING
    assert "arm64" in service.ARCH_MAPPING
    assert "x86" in service.ARCH_MAPPING
    assert "x86_64" in service.ARCH_MAPPING


def test_invalid_architecture():
    """Test invalid architecture handling."""
    service = FridaService(verbose=False)
    # Test would check for proper error handling
    pass
