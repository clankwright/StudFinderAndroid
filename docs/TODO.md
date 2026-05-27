# studfinderapp.com TODO (handoff doc)

> Cross-cycle state. Every skill reads this on start and updates it on close. Three sections, in this order.

## In flight

<!-- Empty — no skill currently running. -->

## Just shipped (last cycle)

- 7.5: Lightning donation footer (website #donate section + lightning: link) + donate button in app Instructions dialog; 64→70 tests pass — by sst-dev-cycle at 2026-05-28T09:30:00Z
- 5.4: address linsui MR !39185 change requests (full commit SHA, subdir: app, delete UpdateCheckData); push to fork branch; 62→64 tests pass — by sst-dev-cycle at 2026-05-28T07:15:00Z
- 5.9: add AllowedAPKSigningKeys + Binaries %c assertions to test_fdroid_mr_yaml_in_source_branch; 62→62 tests pass — by sst-dev-cycle at 2026-05-27T23:30:00Z
- 5.8: decode+parse YAML content from GitLab API in test_fdroid_mr_yaml_in_source_branch; assert RepoType='git' and Repo=GITHUB_URL — by sst-dev-cycle at 2026-05-27T22:00:00Z
- 5.4 (proactive): added RepoType, Repo, WebSite to fdroid YAML; pushed to fork branch add-org.bitanon.studfinder; 3 new tests; 59→62 tests pass — by sst-dev-cycle at 2026-05-27T21:30:00Z
- 7.6: extended test_ua_routing_cta_divs_present to assert cta-ios + cta-desktop divs; 59→59 tests pass — by sst-dev-cycle at 2026-05-27T14:05:00Z
- 7.1+7.2+7.3+7.4: F-Droid badge (primary CTA), GitHub sideload link, UA routing (Android/iOS/desktop divs + navigator.userAgent IIFE), "why open source" marked complete; 8 new tests in test_html.py; 51→59 tests pass — by sst-dev-cycle at 2026-05-27T12:30:00Z
- 5.3: created branch add-org.bitanon.studfinder in fork, added YAML via GitLab API, opened MR !39185 to fdroid/fdroiddata; 5 new tests in test_fdroid_mr.py; 46→51 tests pass — by sst-dev-cycle at 2026-05-27T10:30:00Z
- 4.9: replace apksigner verify body with aapt dump badging + assert versionCode='15' in test_release_apk_versioncode_15; 46→46 tests pass — by sst-dev-cycle at 2026-05-28T00:00:00Z
- SPEC 4.6+4.7: built+signed release APK (assembleRelease with toadlybroodleKeyStore.jks); discovered actual cert SHA-256 e04d3854... (differs from MinimaList's older cert); corrected YAML + SPEC + tests; published studfinder-v15-release.apk to GitHub Release v15; 41→46 tests pass — by sst-dev-cycle at 2026-05-27T23:30:00Z

## Next up (queued for next cycle)

- [easy] [should-fix] 7.7 `docs/test_html.py:259` — scope email regex to donate section and strip HTML comments to close false-positive path — review of 72e88a5
- [medium] Add 4-6 affiliate product cards above the fold (Franklin ProSensor 710, Zircon HD55, magnetic, premium electronic) with UTM-tagged links + FTC disclosure. Reason: SPEC 1.3. Blocked on H1.1 (Amazon Associates signup in HUMAN.md).
- [medium] Smoke-test studfinder-v15-release.apk on a connected Android device via adb: `adb install -r app/build/outputs/apk/release/studfinder-v15-release.apk` (or pull from GitHub Release v15), then drive through `adb shell am start`/`input` to exercise launch → instructions screen → sensor-sweep activity → settings; assert (a) `adb logcat` contains no `AdMob`, `FirebaseApp`, or `GoogleAnalytics` lines during the run (greppable allowlist), (b) `dumpsys netstats detail` shows zero bytes for `org.bitanon.studfinder` over the run, (c) exit code 0 from `adb shell am force-stop`. Write a new `test_device_smoke.py` that runs against `ADB_SERIAL` env var (skip if unset so CI without a device stays green) and record outcome under a new SPEC 4.10 (file the sub-item when picking). Reason: gates F-Droid acceptance + verifies the Phase-3 strip on real hardware; emulator cannot exercise magnetometer/haptic. Requires a phone connected to the chain host via USB-debugging before this is picked.
