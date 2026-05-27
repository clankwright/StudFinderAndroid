"""Tests for Studfinder Android app source/resource files (SPEC 7.5 donate button)."""
from pathlib import Path

REPO = Path("/home/rob/Dev/android/Studfinder")
STRINGS_XML = REPO / "app/src/main/res/values/strings.xml"
ACTIVITY_KT = REPO / "app/src/main/java/org/bitanon/studfinder/StudFActivity.kt"


# SPEC 7.5: in-app donate button

def test_donate_lightning_string_defined():
    """strings.xml must define a donate_lightning string for the donate button label (SPEC 7.5)."""
    content = STRINGS_XML.read_text(encoding="utf-8")
    assert 'name="donate_lightning"' in content, (
        'donate_lightning string not defined in strings.xml — SPEC 7.5; '
        'used as the label for the donate button in the Instructions dialog'
    )


def test_donate_button_wired_in_instructions_dialog():
    """StudFActivity.kt must link the donate button to studfinderapp.com/#donate (SPEC 7.5)."""
    content = ACTIVITY_KT.read_text(encoding="utf-8")
    assert "studfinderapp.com/#donate" in content, (
        "studfinderapp.com/#donate not found in StudFActivity.kt — SPEC 7.5; "
        "the donate button in showInstructions() must open the website donate section"
    )


def test_donate_button_uses_donate_string():
    """showInstructions() must reference R.string.donate_lightning for the donate button (SPEC 7.5)."""
    content = ACTIVITY_KT.read_text(encoding="utf-8")
    assert "donate_lightning" in content, (
        "donate_lightning string reference not found in StudFActivity.kt — SPEC 7.5"
    )
