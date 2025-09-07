"""Tests for CLI functionality."""

import pytest
from click.testing import CliRunner
from pathlib import Path

from apkpatcher.cli import cli


def test_cli_version():
    """Test version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert "APKPatcher" in result.output


def test_cli_help():
    """Test help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "APKPatcher" in result.output


def test_pull_command_missing_package():
    """Test pull command without package name."""
    runner = CliRunner()
    result = runner.invoke(cli, ['pull'])
    assert result.exit_code != 0


def test_decode_command_missing_apk():
    """Test decode command without APK file."""
    runner = CliRunner()
    result = runner.invoke(cli, ['decode'])
    assert result.exit_code != 0


def test_build_command_missing_dir():
    """Test build command without directory."""
    runner = CliRunner()
    result = runner.invoke(cli, ['build'])
    assert result.exit_code != 0


def test_patch_command_missing_args():
    """Test patch command without required arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ['patch'])
    assert result.exit_code != 0


def test_rename_command_missing_args():
    """Test rename command without required arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ['rename'])
    assert result.exit_code != 0


def test_sign_command_missing_apk():
    """Test sign command without APK file."""
    runner = CliRunner()
    result = runner.invoke(cli, ['sign'])
    assert result.exit_code != 0
