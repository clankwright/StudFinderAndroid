# studfinderapp.com TODO (handoff doc)

> Cross-cycle state. Every skill reads this on start and updates it on close. Three sections, in this order.

## In flight

<!-- Empty — no skill currently running. -->

## Just shipped (last cycle)

- 6.2: at-wall hands-on verification on OnePlus CPH2647 — coin calibration triggered red-LED sequence, wall sweep located studs as expected, beeper + sensitivity slider behaved per instructions — by user (manual physical test) at 2026-05-28T21:00:00Z
- 6.1+6.3+6.4+6.5: device smoke-test on OnePlus CPH2647 (Android 16); install via /data/local/tmp, launch StudFActivity, force-stop; logcat allowlist clean (0 AdMob/Firebase/Crashlytics/GoogleAnalytics/gms.ads/ca-app-pub hits across 29k lines); netstats UID 10408 absent (zero bytes); airplane-mode relaunch clean; Phase 7.5 SUPPORT button confirmed firing ACTION_VIEW to studfinderapp.com/#donate (Brave opened the page); new docs/test_device_smoke.py (5 tests, ADB_SERIAL-gated); 71→76 tests pass with device / 71+5 skipped without — by manual (direct on-device session) at 2026-05-28T20:30:00Z
- 7.7: fix test_donate_lightning_address_displayed to strip HTML comments + scope to donate section; add comment-only rejection guard; 70→71 tests pass — by sst-dev-cycle at 2026-05-28T10:00:00Z
- 7.5: Lightning donation footer (website #donate section + lightning: link) + donate button in app Instructions dialog; 64→70 tests pass — by sst-dev-cycle at 2026-05-28T09:30:00Z
- 5.4: address linsui MR !39185 change requests (full commit SHA, subdir: app, delete UpdateCheckData); push to fork branch; 62→64 tests pass — by sst-dev-cycle at 2026-05-28T07:15:00Z
- 5.9: add AllowedAPKSigningKeys + Binaries %c assertions to test_fdroid_mr_yaml_in_source_branch; 62→62 tests pass — by sst-dev-cycle at 2026-05-27T23:30:00Z
- 5.8: decode+parse YAML content from GitLab API in test_fdroid_mr_yaml_in_source_branch; assert RepoType='git' and Repo=GITHUB_URL — by sst-dev-cycle at 2026-05-27T22:00:00Z
- 5.4 (proactive): added RepoType, Repo, WebSite to fdroid YAML; pushed to fork branch add-org.bitanon.studfinder; 3 new tests; 59→62 tests pass — by sst-dev-cycle at 2026-05-27T21:30:00Z
- 7.6: extended test_ua_routing_cta_divs_present to assert cta-ios + cta-desktop divs; 59→59 tests pass — by sst-dev-cycle at 2026-05-27T14:05:00Z
- 7.1+7.2+7.3+7.4: F-Droid badge (primary CTA), GitHub sideload link, UA routing (Android/iOS/desktop divs + navigator.userAgent IIFE), "why open source" marked complete; 8 new tests in test_html.py; 51→59 tests pass — by sst-dev-cycle at 2026-05-27T12:30:00Z
- 5.3: created branch add-org.bitanon.studfinder in fork, added YAML via GitLab API, opened MR !39185 to fdroid/fdroiddata; 5 new tests in test_fdroid_mr.py; 46→51 tests pass — by sst-dev-cycle at 2026-05-27T10:30:00Z
## Next up (queued for next cycle)

- [easy] Fix UTF-8 mojibake on studfinderapp.com. Served HTML body uses valid UTF-8 (em-dashes encoded as `e2 80 94`, apostrophes as `e2 80 99`) but the response carries `Content-Type: text/html` with no `charset=utf-8`, and `public_html/index.html` has no `<meta charset>` in `<head>` — browsers fall back to Latin-1 and render `â€"` / `â€™` for the em-dashes and curly quotes. Two-part fix in one commit: (a) add `<meta charset="utf-8">` immediately after `<head>` in `/home/rob/Dev/websites/studfinderapp.com/public_html/index.html` (HTML-side belt-and-suspenders); (b) add `charset utf-8;` to the nginx server block for `studfinderapp.com` in `/etc/nginx/sites-available/default` on the VPS (around line 115) — canonical fix that makes the response header `Content-Type: text/html; charset=utf-8`; reload nginx (`sudo nginx -t && sudo systemctl reload nginx`); scp updated index.html to VPS. Acceptance: `curl -sI https://studfinderapp.com/ | grep -i content-type` reports `text/html; charset=utf-8` AND a new test `test_html.py::test_charset_meta_declared_in_head` asserts `<meta charset="utf-8">` is present in `public_html/index.html`. Reason: discovered 2026-05-28 during SPEC 6.4 device verification — the SUPPORT button correctly opened studfinderapp.com but the body text rendered mangled characters in Brave on Android 16; SEO impact (Google may downrank pages with display errors) and trust-tax on the donate page (mojibake undermines the "professional ad-free app" message). [no SPEC ID needed — site hygiene; file as 0.6 in Phase 0 when picking.]
- [medium] Add 4-6 affiliate product cards above the fold (Franklin ProSensor 710, Zircon HD55, magnetic, premium electronic) with UTM-tagged links + FTC disclosure. Reason: SPEC 1.3. Blocked on H1.1 (Amazon Associates signup in HUMAN.md).
