"""Tests for index.html changes (SPEC 0.2): broken store badges removed, F-Droid/GitHub CTA added."""
import re

HTML_PATH = "/home/rob/Dev/websites/studfinderapp.com/public_html/index.html"


def read_html():
    with open(HTML_PATH) as f:
        return f.read()


def test_no_itunes_links():
    html = read_html()
    assert "linkmaker.itunes.apple.com" not in html, "iTunes badge still present"
    assert "a9k3m.app.goo.gl" not in html, "Dead Firebase dynamic link still present"


def test_no_google_play_links():
    html = read_html()
    assert "play.google.com/store/apps/details?id=org.bitanon.studfinder" not in html, (
        "Google Play badge still present"
    )
    assert "en_app_rgb_wo_60.png" not in html, "Google Play badge image still present"


def test_no_try_free_try_premium_tables():
    html = read_html()
    assert "Try free" not in html, '"Try free" table still present'
    assert "Try premium" not in html, '"Try premium" table still present'


def test_github_cta_present():
    html = read_html()
    assert "github.com/toadlyBroodle/StudFinderAndroid" in html, (
        "GitHub repo link not found"
    )


def test_fdroid_cta_text_present():
    html = read_html()
    lower = html.lower()
    assert "f-droid" in lower or "fdroid" in lower, "No F-Droid reference found"
    assert "open-source" in lower or "open source" in lower, "No open-source mention found"
