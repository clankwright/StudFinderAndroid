"""Tests for F-Droid submission MR (SPEC 5.3).

Verifies that toadlyBroodle/fdroiddata has an open (or merged) MR to
fdroid/fdroiddata adding metadata/org.bitanon.studfinder.yml, and that the
source branch in the fork contains the linted YAML.
"""
import os
import subprocess
from pathlib import Path

import pytest
import yaml

GITLAB_TOKEN_FILE = Path.home() / ".config/gitlab-fdroid.token"
FORK_ID = 82491652          # toadlyBroodle/fdroiddata
UPSTREAM_ID = 36528         # fdroid/fdroiddata
PACKAGE_ID = "org.bitanon.studfinder"
YAML_PATH_IN_REPO = f"metadata/{PACKAGE_ID}.yml"
LOCAL_YAML = Path("/home/rob/Dev/android/Studfinder/docs/fdroid/metadata") / f"{PACKAGE_ID}.yml"


def _token() -> str:
    assert GITLAB_TOKEN_FILE.exists(), f"GitLab token file missing: {GITLAB_TOKEN_FILE}"
    return GITLAB_TOKEN_FILE.read_text().strip()


def _gl_get(path: str) -> dict | list:
    """GET from GitLab API, return parsed JSON."""
    import urllib.request, json as _json
    url = f"https://gitlab.com/api/v4{path}"
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": _token()})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return _json.loads(resp.read())


def _find_studfinder_mr() -> dict:
    """Return the studfinder MR from the upstream fdroiddata project (cross-project MRs live in the target)."""
    mrs = _gl_get(
        f"/projects/{UPSTREAM_ID}/merge_requests"
        f"?state=all&search={PACKAGE_ID}&per_page=20"
    )
    matches = [
        m for m in mrs
        if PACKAGE_ID in m.get("title", "") or PACKAGE_ID in m.get("source_branch", "")
    ]
    return matches[0] if matches else {}


# ── SPEC 5.3 local checks ────────────────────────────────────────────────────

def test_local_yaml_still_valid():
    """The local linted YAML must still parse cleanly (regression guard)."""
    assert LOCAL_YAML.exists(), f"Local YAML missing: {LOCAL_YAML}"
    data = yaml.safe_load(LOCAL_YAML.read_text())
    assert data.get("License") == "Apache-2.0"
    assert data.get("AuthorName") == "toadlyBroodle"


# ── SPEC 5.3 GitLab checks ───────────────────────────────────────────────────

def test_fdroid_mr_exists():
    """An open or merged MR must exist from fork to fdroid/fdroiddata for the studfinder YAML."""
    mr = _find_studfinder_mr()
    assert mr, (
        f"No MR for {PACKAGE_ID} found in fdroid/fdroiddata "
        f"(cross-project MR from toadlyBroodle/fdroiddata)"
    )


def test_fdroid_mr_state_open_or_merged():
    """The studfinder MR must be in 'opened' or 'merged' state (not closed/abandoned)."""
    mr = _find_studfinder_mr()
    assert mr, f"No MR for {PACKAGE_ID} found"
    assert mr["state"] in ("opened", "merged"), (
        f"Expected state opened or merged, got '{mr['state']}' (MR !{mr['iid']})"
    )


def test_fdroid_mr_description_cites_source_repo():
    """MR description must mention the GitHub source repo URL."""
    mr = _find_studfinder_mr()
    assert mr, f"No MR for {PACKAGE_ID} found"
    desc = mr.get("description", "")
    assert "StudFinderAndroid" in desc or "toadlyBroodle" in desc, (
        f"MR description does not mention the source repo:\n{desc[:500]}"
    )


def test_fdroid_mr_yaml_in_source_branch():
    """The MR's source branch in the fork must contain metadata/org.bitanon.studfinder.yml."""
    mr = _find_studfinder_mr()
    assert mr, f"No MR for {PACKAGE_ID} found"
    branch = mr["source_branch"]
    encoded_path = YAML_PATH_IN_REPO.replace("/", "%2F")
    file_info = _gl_get(
        f"/projects/{FORK_ID}/repository/files/{encoded_path}?ref={branch}"
    )
    assert "file_name" in file_info, (
        f"YAML not found in branch '{branch}': {file_info.get('message', '')}"
    )
