# studfinderapp.com TODO (handoff doc)

> Cross-cycle state. Every skill reads this on start and updates it on close. Three sections, in this order.

## In flight

<!-- Empty — no skill currently running. -->

## Just shipped (last cycle)

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
- 4.9: replace apksigner verify body with aapt dump badging + assert versionCode='15' in test_release_apk_versioncode_15; 46→46 tests pass — by sst-dev-cycle at 2026-05-28T00:00:00Z

## Next up (queued for next cycle)

- [medium] Add 4-6 affiliate product cards above the fold (Franklin ProSensor 710, Zircon HD55, magnetic, premium electronic) with UTM-tagged links + FTC disclosure. Reason: SPEC 1.3. Blocked on H1.1 (Amazon Associates signup in HUMAN.md).
