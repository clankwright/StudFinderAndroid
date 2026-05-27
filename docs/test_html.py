"""Tests for studfinderapp.com website changes (SPEC 0.2, 0.4, 0.5)."""
import re
import xml.etree.ElementTree as ET

HTML_PATH = "/home/rob/Dev/websites/studfinderapp.com/public_html/index.html"
SITEMAP_PATH = "/home/rob/Dev/websites/studfinderapp.com/public_html/sitemap.xml"


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


# SPEC 0.4: Plausible analytics

def test_plausible_script_present():
    html = read_html()
    assert "plausible.io/js/script" in html, "Plausible script tag not found in <head>"
    assert 'data-domain="studfinderapp.com"' in html, "Plausible data-domain not set to studfinderapp.com"


def test_plausible_outbound_links_extension():
    html = read_html()
    assert "outbound-links" in html, (
        "Plausible outbound-links extension missing — needed for automatic affiliate-click tracking in Phase 1"
    )


def test_plausible_stub_defined():
    html = read_html()
    assert "window.plausible" in html, (
        "Plausible queue stub not defined — custom events will silently fail before the script loads"
    )


def test_fdroid_badge_click_event():
    html = read_html()
    assert (
        "plausible('F-Droid-badge-click')" in html
        or 'plausible("F-Droid-badge-click")' in html
    ), "F-Droid-badge-click event not wired to the primary download button"


# SPEC 0.5: Sitemap lastmod

def test_sitemap_lastmod_updated():
    tree = ET.parse(SITEMAP_PATH)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    lastmods = [url.find("sm:lastmod", ns).text for url in tree.findall("sm:url", ns)]
    assert lastmods, "No <lastmod> entries found in sitemap.xml"
    assert all("2023" not in d for d in lastmods), (
        f"sitemap.xml still has stale 2023 lastmod: {lastmods}"
    )


def test_sitemap_root_url_present():
    tree = ET.parse(SITEMAP_PATH)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [url.find("sm:loc", ns).text for url in tree.findall("sm:url", ns)]
    assert any("studfinderapp.com" in loc for loc in locs), (
        "Root URL studfinderapp.com not present in sitemap.xml"
    )


# SPEC 1.1: Rewrite landing-page copy

def test_lead_physical_tools_angle():
    """Lead copy must mention physical tools as a complement to the app."""
    html = read_html()
    lower = html.lower()
    assert "physical" in lower and ("tool" in lower or "finder" in lower), (
        "Lead copy missing physical tools angle"
    )
    # The SPEC lead: phones can't replace physical tools in all cases
    assert "when phones can" in lower or "phone" in lower, (
        "No mention of phone limitations relative to physical tools"
    )


def test_why_open_source_section_present():
    """A 'Why open source' section heading must be present."""
    html = read_html()
    lower = html.lower()
    assert "why open source" in lower or "why open-source" in lower, (
        "No 'Why open source' section heading found"
    )


def test_why_open_source_explains_fdroid_path():
    """The Why-open-source section must explain the F-Droid distribution path."""
    html = read_html()
    lower = html.lower()
    # Must mention: no ads + no tracking + F-Droid
    assert "no ads" in lower or "ad-free" in lower, (
        "Why-open-source section missing 'no ads' claim"
    )
    assert "no tracking" in lower or "no analytics" in lower, (
        "Why-open-source section missing 'no tracking' claim"
    )
    # F-Droid already tested by test_fdroid_cta_text_present, but confirm it's
    # in the context of the why-open-source explanation
    assert "source on github" in lower or "github.com/toadlybroodle" in lower.replace(" ", ""), (
        "Why-open-source section missing GitHub source link"
    )


def test_how_it_works_preserved():
    """The 'How it works' educational section must be intact."""
    html = read_html()
    lower = html.lower()
    assert "how it works" in lower, "'How it works' section missing"
    assert "magnetometer" in lower, "Magnetometer explanation missing from How-it-works"
    assert "detect" in lower, "Detection instructions missing from How-it-works"


# SPEC 7.1: F-Droid badge as primary CTA

def test_fdroid_badge_image_present():
    """Official F-Droid badge image must be present (SPEC 7.1)."""
    html = read_html()
    assert "f-droid.org/badge/get-it-on.png" in html, (
        "Official F-Droid badge image (f-droid.org/badge/get-it-on.png) not found — SPEC 7.1"
    )


def test_fdroid_listing_link_present():
    """Link to the F-Droid app listing must be present (SPEC 7.1)."""
    html = read_html()
    assert "f-droid.org/packages/org.bitanon.studfinder" in html, (
        "F-Droid listing URL (f-droid.org/packages/org.bitanon.studfinder) not found — SPEC 7.1"
    )


# SPEC 7.2: Secondary GitHub sideload / build-from-source link

def test_github_releases_sideload_link_present():
    """GitHub releases page link must be present as a secondary install option (SPEC 7.2)."""
    html = read_html()
    assert "github.com/toadlyBroodle/StudFinderAndroid/releases" in html, (
        "GitHub releases sideload link missing — SPEC 7.2"
    )


def test_sideload_or_source_label_present():
    """The secondary GitHub link must be labelled as a sideload/source option (SPEC 7.2)."""
    html = read_html()
    lower = html.lower()
    assert (
        "sideload" in lower
        or "build from source" in lower
        or "apk" in lower
    ), "Secondary GitHub link has no sideload/APK/build-from-source label — SPEC 7.2"


# SPEC 7.3: UA-based CTA routing

def test_ua_routing_script_present():
    """A JS script must detect the user agent and route Android/iOS/desktop CTAs (SPEC 7.3)."""
    html = read_html()
    assert "navigator.userAgent" in html or "navigator.useragent" in html.lower(), (
        "No navigator.userAgent UA-detection script found — SPEC 7.3"
    )


def test_ua_routing_detects_android():
    """UA routing must branch on Android (SPEC 7.3)."""
    html = read_html()
    assert re.search(r"[Aa]ndroid", html), (
        "UA routing script does not check for Android — SPEC 7.3"
    )


def test_ua_routing_detects_ios():
    """UA routing must branch on iOS/iPhone (SPEC 7.3)."""
    html = read_html()
    assert re.search(r"[Ii][Pp]hone|[Ii][Pp]ad|iOS", html), (
        "UA routing script does not check for iPhone/iPad/iOS — SPEC 7.3"
    )


def test_ua_routing_cta_divs_present():
    """HTML must contain separate CTA containers for Android and non-Android visitors (SPEC 7.3)."""
    html = read_html()
    assert "cta-android" in html or "id=\"android" in html or "class=\"android" in html, (
        "No Android-specific CTA container (id/class containing 'android') found — SPEC 7.3"
    )
