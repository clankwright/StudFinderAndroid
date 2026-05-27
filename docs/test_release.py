"""Tests for release APK build (SPEC 4.6) + GitHub Release publish (SPEC 4.7)."""
import json
import subprocess
from pathlib import Path

REPO = Path("/home/rob/Dev/android/Studfinder")
APK_PATH = REPO / "studfinder-v15-release.apk"
APKSIGNER = "/home/rob/Android/Sdk/build-tools/34.0.0/apksigner"
AAPT = "/home/rob/Android/Sdk/build-tools/34.0.0/aapt"
EXPECTED_CERT_SHA256 = "e04d3854fc1245e27b826feaa30298bda89a4c0528a2a0b7ddbc23ad60a72fd4"
GITHUB_REPO = "toadlyBroodle/StudFinderAndroid"
RELEASE_TAG = "v15"
EXPECTED_APK_FILENAME = "studfinder-v15-release.apk"


# SPEC 4.6 — build + sign release APK

def test_release_apk_exists():
    """Release APK must exist at project root after assembleRelease + rename."""
    assert APK_PATH.exists(), f"APK not found at {APK_PATH} — run ./gradlew assembleRelease"


def test_release_apk_cert_sha256_matches():
    """APK must be signed with the shared toadlybroodle cert (SHA-256 pre-known from MinimaList)."""
    assert APK_PATH.exists(), f"APK not found; build it first (SPEC 4.6)"
    result = subprocess.run(
        [APKSIGNER, "verify", "--print-certs", str(APK_PATH)],
        capture_output=True, text=True, check=True,
    )
    output = result.stdout.lower()
    assert EXPECTED_CERT_SHA256 in output, (
        f"Expected cert SHA-256 {EXPECTED_CERT_SHA256} not found in apksigner output:\n{result.stdout}"
    )


def test_release_apk_versioncode_15():
    """APK must carry versionCode 15 (the F-Droid debut version)."""
    assert APK_PATH.exists(), f"APK not found; build it first (SPEC 4.6)"
    result = subprocess.run(
        [AAPT, "dump", "badging", str(APK_PATH)],
        capture_output=True, text=True, check=True,
    )
    assert "versionCode='15'" in result.stdout, (
        f"Expected versionCode='15' in aapt dump badging output:\n{result.stdout[:500]}"
    )


# SPEC 4.7 — GitHub Release

def test_github_release_v15_exists():
    """GitHub Release v15 must exist at github.com/toadlyBroodle/StudFinderAndroid."""
    result = subprocess.run(
        ["gh", "release", "view", RELEASE_TAG, "--repo", GITHUB_REPO, "--json", "tagName"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"GitHub Release {RELEASE_TAG} not found: {result.stderr.strip()}"
    )
    data = json.loads(result.stdout)
    assert data.get("tagName") == RELEASE_TAG, f"Expected tagName={RELEASE_TAG}, got {data}"


def test_github_release_v15_apk_attached():
    """GitHub Release v15 must have studfinder-v15-release.apk as an asset."""
    result = subprocess.run(
        ["gh", "release", "view", RELEASE_TAG, "--repo", GITHUB_REPO, "--json", "assets"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Failed to fetch release: {result.stderr.strip()}"
    data = json.loads(result.stdout)
    asset_names = [a["name"] for a in data.get("assets", [])]
    assert EXPECTED_APK_FILENAME in asset_names, (
        f"Expected {EXPECTED_APK_FILENAME} in release assets, got: {asset_names}"
    )
