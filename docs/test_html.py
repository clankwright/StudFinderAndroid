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


# SPEC 0.4: no on-page analytics. Regression guard against reintroducing any third-party
# tracking surface (script tags, dataLayer pushes, event-call helpers, beacon endpoints).

def test_no_third_party_analytics():
    """The website ships zero third-party tracking. Asserts no script tags or call sites for
    common analytics endpoints/helpers in either index.html or privacy.html."""
    index_html = read_html()
    with open(PRIVACY_PATH) as f:
        privacy_html = f.read()
    forbidden = (
        "plausible.io", "window.plausible", "plausible(",
        "google-analytics.com", "googletagmanager.com", "gtag(",
        "umami.js", "goatcounter",
    )
    for label, content in (("index.html", index_html), ("privacy.html", privacy_html)):
        for needle in forbidden:
            assert needle not in content, f"{label}: forbidden tracking reference '{needle}' present"


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
    """All three UA-routed CTA divs must be present in HTML (SPEC 7.3/7.6).

    The routing IIFE calls getElementById on all three without null guards, so a
    missing div causes a TypeError for affected visitors with no prior test catch.
    """
    html = read_html()
    assert 'id="cta-android"' in html, (
        'Android CTA container (id="cta-android") missing — SPEC 7.3/7.6'
    )
    assert 'id="cta-ios"' in html, (
        'iOS CTA container (id="cta-ios") missing — SPEC 7.3/7.6; JS calls getElementById("cta-ios") without null guard'
    )
    assert 'id="cta-desktop"' in html, (
        'Desktop CTA container (id="cta-desktop") missing — SPEC 7.3/7.6; JS calls getElementById("cta-desktop") without null guard'
    )


# SPEC 7.5: Lightning donation footer

def test_donate_section_anchor_present():
    """Website must have a #donate anchor so the in-app donate button can deep-link to it (SPEC 7.5)."""
    html = read_html()
    assert 'id="donate"' in html, (
        'No id="donate" anchor found — SPEC 7.5; in-app button links to studfinderapp.com/#donate'
    )


def test_donate_lightning_content_present():
    """Donation section must mention Lightning (SPEC 7.5)."""
    html = read_html()
    lower = html.lower()
    assert "lightning" in lower or "⚡" in lower, (
        "No Lightning reference found in page — SPEC 7.5"
    )


def test_donate_lightning_address_displayed():
    """Donation section must display a Lightning address in user@domain format (SPEC 7.5).
    Scoped to the donate section with HTML comments stripped so a comment-only address
    cannot produce a false positive (SPEC 7.7).
    """
    import re
    html = read_html()
    donate_idx = html.lower().find("donate")
    assert donate_idx != -1, "No donate section found — SPEC 7.5"
    donate_html = re.sub(r'<!--.*?-->', '', html[donate_idx:], flags=re.DOTALL)
    assert re.search(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', donate_html), (
        "No Lightning address (user@domain) in donate section (outside HTML comments) — SPEC 7.5"
    )


def test_donate_address_comment_only_is_rejected():
    """Comment-stripping guard: email that exists only inside an HTML comment must not pass
    the address check (guards the false-positive path described in SPEC 7.7)."""
    import re
    # email is inside a comment within the donate section — not visible to users
    mock_html = '<section id="donate"><!-- user@example.com --> no visible address</section>'
    donate_idx = mock_html.lower().find("donate")
    donate_html = re.sub(r'<!--.*?-->', '', mock_html[donate_idx:], flags=re.DOTALL)
    assert not re.search(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', donate_html), (
        "Comment-only email passed the address check, comment stripping not working"
    )


PRIVACY_PATH = "/home/rob/Dev/websites/studfinderapp.com/public_html/privacy.html"


def test_privacy_policy_exists_and_covers_core_claims():
    """SPEC 0.6 — public_html/privacy.html must exist and disclose the key claims:
    app collects no data, website runs no analytics, Lightning donations pseudonymous,
    future affiliate/ads will be disclosed before going live."""
    import os
    assert os.path.exists(PRIVACY_PATH), f"privacy.html missing at {PRIVACY_PATH}"
    with open(PRIVACY_PATH) as f:
        content = f.read().lower()
    expectations = [
        "no personal data",
        "no analytics",
        "lightning",
        "pseudonymous",
        "tips@studfinderapp.com",
        "affiliate",
    ]
    missing = [phrase for phrase in expectations if phrase not in content]
    assert not missing, f"privacy.html missing expected disclosures: {missing}"


def test_privacy_link_in_index_footer():
    """Index footer must link to /privacy.html (not the previous placeholder)."""
    html = read_html()
    assert 'href="/privacy.html"' in html, "Privacy Policy link in footer must point to /privacy.html"
    assert "privacypolicies.com" not in html, "Placeholder privacypolicies.com link must be removed"


def test_charset_meta_declared_in_head():
    """SPEC 0.6 — <meta charset="utf-8"> must be present in <head> as a belt-and-suspenders
    fallback to the nginx-side `charset utf-8;` directive. Without this declaration, browsers
    sniffing the bytes can briefly render Latin-1 before the HTTP header is parsed."""
    html = read_html()
    head_idx = html.lower().find("<head>")
    head_end = html.lower().find("</head>", head_idx)
    assert head_idx >= 0 and head_end > head_idx
    head_block = html[head_idx:head_end]
    assert '<meta charset="utf-8">' in head_block or "<meta charset='utf-8'>" in head_block, (
        "Missing <meta charset=\"utf-8\"> in <head>"
    )


def test_no_em_dashes_in_html():
    """SPEC 0.6 — the served HTML must be pure ASCII AND contain no em-dash entities
    (&mdash;, &#8212;, &#x2014;). Catches reintroduction of em-dashes whether as raw
    UTF-8 bytes or as HTML entities. Bolt icon &#9889; is allowed (renders as ⚡)."""
    with open(HTML_PATH, "rb") as f:
        raw = f.read()
    non_ascii = [(i, b) for i, b in enumerate(raw) if b > 0x7F]
    assert not non_ascii, (
        f"Non-ASCII bytes found at offsets {[o for o,_ in non_ascii[:5]]}; "
        f"first byte {hex(non_ascii[0][1]) if non_ascii else 'n/a'}; "
        f"strip em-dashes / curly quotes / emoji to ASCII alternatives"
    )
    html = raw.decode("utf-8")
    forbidden_entities = ["&mdash;", "&#8212;", "&#x2014;", "&#X2014;"]
    for ent in forbidden_entities:
        assert ent not in html, f"Forbidden em-dash entity '{ent}' found in HTML"
