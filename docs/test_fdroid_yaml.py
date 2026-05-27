"""Tests for F-Droid submission YAML: SPEC 5.1 (draft) + SPEC 5.2 (lint)."""
import subprocess
from pathlib import Path

import yaml
import pytest

REPO = Path("/home/rob/Dev/android/Studfinder")
FDROID_DIR = REPO / "docs/fdroid"
YAML_PATH = FDROID_DIR / "metadata/org.bitanon.studfinder.yml"
PACKAGE_ID = "org.bitanon.studfinder"
EXPECTED_SIGNING_KEY = "b800dcf0a7725e2f71987c40d979757acd328a23de2e93a7efc0e400aeb2db69"
GITHUB_URL = "https://github.com/toadlyBroodle/StudFinderAndroid"


@pytest.fixture(scope="module")
def parsed():
    assert YAML_PATH.exists(), f"fdroid YAML missing at {YAML_PATH}"
    return yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))


# SPEC 5.1 — YAML structure and required fields

def test_fdroid_yaml_exists():
    assert YAML_PATH.exists(), f"fdroid YAML missing at {YAML_PATH}"


def test_fdroid_yaml_is_valid_yaml():
    assert YAML_PATH.exists()
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_fdroid_yaml_license(parsed):
    assert parsed.get("License") == "Apache-2.0", (
        f"License must be Apache-2.0, got {parsed.get('License')}"
    )


def test_fdroid_yaml_author_name(parsed):
    assert parsed.get("AuthorName") == "toadlyBroodle"


def test_fdroid_yaml_source_code(parsed):
    assert parsed.get("SourceCode") == GITHUB_URL


def test_fdroid_yaml_issue_tracker(parsed):
    assert parsed.get("IssueTracker") == f"{GITHUB_URL}/issues"


def test_fdroid_yaml_categories(parsed):
    cats = parsed.get("Categories", [])
    assert len(cats) >= 1, "At least one category required"


def test_fdroid_yaml_allowed_signing_keys(parsed):
    key = parsed.get("AllowedAPKSigningKeys")
    assert key == EXPECTED_SIGNING_KEY, (
        f"AllowedAPKSigningKeys must be {EXPECTED_SIGNING_KEY}, got {key}"
    )


def test_fdroid_yaml_binaries_url(parsed):
    binaries = parsed.get("Binaries", "")
    assert "%v" in binaries, "Binaries URL must contain %v version placeholder"
    assert "studfinder" in binaries.lower(), "Binaries URL must reference studfinder APK"
    assert "toadlyBroodle/StudFinderAndroid" in binaries


def test_fdroid_yaml_builds_block(parsed):
    builds = parsed.get("Builds", [])
    assert len(builds) >= 1, "Builds block required"
    build = builds[0]
    assert build.get("versionCode") == 15, f"versionCode must be 15, got {build.get('versionCode')}"
    assert build.get("commit") == "v15", f"commit must be v15, got {build.get('commit')}"
    assert "release" in (build.get("gradle") or []), "gradle must include 'release'"


def test_fdroid_yaml_no_antifeatures(parsed):
    af = parsed.get("AntiFeatures")
    assert af is None or af == [], (
        f"AntiFeatures must be absent or empty, got {af}"
    )


def test_fdroid_yaml_auto_update_mode(parsed):
    assert parsed.get("AutoUpdateMode") == "Version"


def test_fdroid_yaml_update_check_mode(parsed):
    assert parsed.get("UpdateCheckMode") == "Tags"


def test_fdroid_yaml_update_check_data(parsed):
    ucd = parsed.get("UpdateCheckData", "")
    assert "app/build.gradle" in ucd, "UpdateCheckData must reference app/build.gradle"
    assert "versionCode" in ucd


def test_fdroid_yaml_current_version(parsed):
    assert parsed.get("CurrentVersion") == "2.0"
    assert parsed.get("CurrentVersionCode") == 15


# SPEC 5.2 — fdroid lint passes

def test_fdroid_lint_passes():
    assert YAML_PATH.exists(), f"fdroid YAML missing at {YAML_PATH}"
    result = subprocess.run(
        ["fdroid", "lint", PACKAGE_ID],
        capture_output=True,
        text=True,
        cwd=str(FDROID_DIR),
    )
    assert result.returncode == 0, (
        f"fdroid lint failed (exit {result.returncode}):\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
