"""Tests for manifest utilities."""

import pytest
from pathlib import Path
import tempfile

from apkpatcher.utils.manifest import ManifestUtils


SAMPLE_MANIFEST = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app"
    android:versionCode="1"
    android:versionName="1.0">

    <application
        android:name=".App"
        android:label="Test App">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>"""


def test_get_package_name():
    """Test package name extraction."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(SAMPLE_MANIFEST)
        manifest_path = Path(f.name)

    try:
        package = ManifestUtils.get_package_name(manifest_path)
        assert package == "com.example.app"
    finally:
        manifest_path.unlink()


def test_get_main_activity():
    """Test main activity extraction."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(SAMPLE_MANIFEST)
        manifest_path = Path(f.name)

    try:
        activity = ManifestUtils.get_main_activity(manifest_path)
        assert activity == "com.example.app.MainActivity"
    finally:
        manifest_path.unlink()


def test_add_internet_permission():
    """Test adding INTERNET permission."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(SAMPLE_MANIFEST)
        manifest_path = Path(f.name)

    try:
        ManifestUtils.add_internet_permission(manifest_path)
        content = manifest_path.read_text()
        assert "android.permission.INTERNET" in content
    finally:
        manifest_path.unlink()


def test_set_extract_native_libs():
    """Test setting extractNativeLibs."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(SAMPLE_MANIFEST)
        manifest_path = Path(f.name)

    try:
        ManifestUtils.set_extract_native_libs(manifest_path, True)
        content = manifest_path.read_text()
        assert 'android:extractNativeLibs="true"' in content
    finally:
        manifest_path.unlink()
