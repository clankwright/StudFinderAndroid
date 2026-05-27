"""Device smoke-test (SPEC 6.1, 6.3, 6.4) — verifies the release APK installs,
launches, runs offline, makes zero network calls, and logs no AdMob/Firebase/
GoogleAnalytics/Crashlytics surfaces on a real Android device.

Gated by ADB_SERIAL env var so CI without a device stays green:
    ADB_SERIAL=<serial> pytest docs/test_device_smoke.py
"""
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

import pytest

REPO = Path("/home/rob/Dev/android/Studfinder")
APK_PATH = REPO / "studfinder-v15-release.apk"
PACKAGE = "org.bitanon.studfinder"
ACTIVITY = f"{PACKAGE}/.StudFActivity"
DEVICE_TMP_APK = "/data/local/tmp/studfinder-smoke.apk"
SERIAL = os.environ.get("ADB_SERIAL")
FORBIDDEN_LOGCAT = [
    "AdMob",
    "FirebaseApp",
    "Crashlytics",
    "GoogleAnalytics",
    "ca-app-pub",
    "gms.ads",
]


def _device_available():
    if not SERIAL:
        return False
    if shutil.which("adb") is None:
        return False
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    return f"{SERIAL}\tdevice" in result.stdout


pytestmark = pytest.mark.skipif(
    not _device_available(),
    reason="ADB_SERIAL unset or device not connected",
)


def _adb(*args, check=True, capture=True):
    cmd = ["adb", "-s", SERIAL, *args]
    return subprocess.run(cmd, check=check, capture_output=capture, text=True)


@pytest.fixture(scope="module")
def smoke_run(tmp_path_factory):
    """Install APK, capture logcat + netstats around a launch/force-stop cycle."""
    assert APK_PATH.exists(), f"Release APK not found at {APK_PATH}"
    workdir = tmp_path_factory.mktemp("smoke")

    # Disable adb-install verifier so a non-Play-signed APK can land; restore in teardown.
    prior_verifier = _adb(
        "shell", "settings", "get", "global", "verifier_verify_adb_installs",
    ).stdout.strip()
    _adb("shell", "settings", "put", "global", "verifier_verify_adb_installs", "0")

    try:
        # Remove any prior install (signature might not match → INSTALL_FAILED_UPDATE_INCOMPATIBLE).
        _adb("shell", "pm", "uninstall", PACKAGE, check=False)

        # Push to /data/local/tmp + pm install (bypasses Play Protect path).
        _adb("push", str(APK_PATH), DEVICE_TMP_APK)
        install = _adb("shell", "pm", "install", "-r", DEVICE_TMP_APK)
        assert "Success" in install.stdout, (
            f"install failed: stdout={install.stdout!r} stderr={install.stderr!r}"
        )

        netstats_before = workdir / "netstats-before.txt"
        netstats_before.write_text(
            _adb("shell", "dumpsys", "netstats", "detail").stdout
        )

        _adb("logcat", "-c")
        logcat_path = workdir / "logcat.txt"
        logcat_fh = open(logcat_path, "w")
        logcat_proc = subprocess.Popen(
            ["adb", "-s", SERIAL, "logcat"],
            stdout=logcat_fh,
            stderr=subprocess.DEVNULL,
        )

        try:
            _adb("shell", "am", "start", "-n", ACTIVITY)
            time.sleep(3)
            stop = _adb("shell", "am", "force-stop", PACKAGE, check=False)
        finally:
            logcat_proc.terminate()
            try:
                logcat_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logcat_proc.kill()
            logcat_fh.close()

        netstats_after = workdir / "netstats-after.txt"
        netstats_after.write_text(
            _adb("shell", "dumpsys", "netstats", "detail").stdout
        )

        pkg_dump = _adb("shell", "dumpsys", "package", PACKAGE).stdout
        uid_match = re.search(r"appId=(\d+)", pkg_dump)
        uid = int(uid_match.group(1)) if uid_match else None

        yield {
            "logcat": logcat_path,
            "netstats_before": netstats_before,
            "netstats_after": netstats_after,
            "uid": uid,
            "stop_returncode": stop.returncode,
        }
    finally:
        if prior_verifier and prior_verifier != "0":
            _adb(
                "shell", "settings", "put", "global",
                "verifier_verify_adb_installs", prior_verifier,
                check=False,
            )


def test_package_installed(smoke_run):
    result = _adb("shell", "pm", "list", "packages", PACKAGE)
    assert f"package:{PACKAGE}" in result.stdout


def test_app_uid_resolved(smoke_run):
    assert smoke_run["uid"] is not None, "Could not parse appId from dumpsys package"


def test_logcat_no_forbidden_surfaces(smoke_run):
    """Phase 3 strip verification on real hardware: no AdMob/Firebase/GA log lines."""
    logcat = smoke_run["logcat"].read_text()
    failures = []
    for tag in FORBIDDEN_LOGCAT:
        hits = [line for line in logcat.splitlines() if tag in line]
        if hits:
            failures.append(f"{tag}: {len(hits)} match(es); first: {hits[0][:200]}")
    assert not failures, "Forbidden cloud surfaces present in logcat:\n" + "\n".join(failures)


def test_netstats_zero_bytes_for_app(smoke_run):
    """SPEC 6.3 contract: app makes zero network calls.

    netstats detail records a `uid=<N>` row only for UIDs that transferred bytes.
    Absent UID = zero bytes. Browser-side traffic from the donate intent lands
    under the browser's UID, not the app's.
    """
    uid = smoke_run["uid"]
    assert uid is not None
    after = smoke_run["netstats_after"].read_text()
    rows = [line for line in after.splitlines() if f"uid={uid}" in line]
    assert not rows, (
        f"UID {uid} ({PACKAGE}) appears in netstats — app issued network calls:\n"
        + "\n".join(rows[:5])
    )


def test_force_stop_returns_zero(smoke_run):
    """SPEC 6.4 — am force-stop must exit 0."""
    assert smoke_run["stop_returncode"] == 0
