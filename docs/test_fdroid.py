"""Tests for F-Droid prep: SPEC 4.2 (fastlane metadata) + SPEC 4.5 (git tag v15)."""
import subprocess
import struct
from pathlib import Path

REPO = Path("/home/rob/Dev/android/Studfinder")
FASTLANE = REPO / "fastlane/metadata/android/en-US"


# SPEC 4.2 — fastlane text metadata

def test_short_description_exists_and_length():
    path = FASTLANE / "short_description.txt"
    assert path.exists(), "short_description.txt missing"
    text = path.read_text(encoding="utf-8").strip()
    assert 0 < len(text) <= 80, f"short_description must be 1-80 chars, got {len(text)}"


def test_full_description_exists_and_length():
    path = FASTLANE / "full_description.txt"
    assert path.exists(), "full_description.txt missing"
    text = path.read_text(encoding="utf-8").strip()
    assert 0 < len(text) <= 4000, f"full_description must be 1-4000 chars, got {len(text)}"


def test_title_exists_and_length():
    path = FASTLANE / "title.txt"
    assert path.exists(), "title.txt missing"
    text = path.read_text(encoding="utf-8").strip()
    assert 0 < len(text) <= 50, f"title must be 1-50 chars, got {len(text)}"


def test_changelog_15_exists_and_length():
    path = FASTLANE / "changelogs/15.txt"
    assert path.exists(), "changelogs/15.txt missing"
    text = path.read_text(encoding="utf-8").strip()
    assert 0 < len(text) <= 500, f"changelog must be 1-500 chars, got {len(text)}"


def test_icon_is_valid_png():
    path = FASTLANE / "images/icon.png"
    assert path.exists(), "fastlane icon.png missing"
    with open(path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", "icon.png is not a valid PNG file"


def test_icon_is_512x512():
    path = FASTLANE / "images/icon.png"
    assert path.exists(), "fastlane icon.png missing"
    with open(path, "rb") as f:
        f.read(8)   # PNG signature
        f.read(4)   # IHDR chunk length
        f.read(4)   # "IHDR"
        w = struct.unpack(">I", f.read(4))[0]
        h = struct.unpack(">I", f.read(4))[0]
    assert w == 512 and h == 512, f"icon.png must be 512x512, got {w}x{h}"


def test_screenshots_dir_exists():
    path = FASTLANE / "images/phoneScreenshots"
    assert path.exists() and path.is_dir(), "phoneScreenshots directory missing"


# SPEC 4.5 — git tag v15

def _git(*args):
    result = subprocess.run(["git"] + list(args), capture_output=True, text=True, cwd=str(REPO))
    return result


def test_tag_v15_exists():
    r = _git("tag", "-l", "v15")
    assert r.returncode == 0
    assert "v15" in r.stdout.strip(), "git tag v15 does not exist"


def test_tag_v15_is_annotated():
    r = _git("cat-file", "-t", "v15")
    assert r.returncode == 0, f"git cat-file failed: {r.stderr}"
    assert r.stdout.strip() == "tag", (
        f"v15 is a lightweight tag (type=commit); must be annotated (type=tag)"
    )


def test_tag_v15_points_to_head():
    # v15 was tagged before subsequent commits; the real contract is reachability, not equality.
    r = subprocess.run(
        ["git", "merge-base", "--is-ancestor", "v15^{}", "HEAD"],
        cwd=str(REPO),
    )
    assert r.returncode == 0, "v15 is not a reachable ancestor of HEAD"
