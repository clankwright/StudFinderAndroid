# studfinderapp.com TODO (handoff doc)

> Cross-cycle state. Every skill reads this on start and updates it on close. Three sections, in this order.

## In flight

<!-- Empty — no skill currently running. -->

## Just shipped (last cycle)

- 5.4: address linsui MR !39185 change requests (full commit SHA, subdir: app, delete UpdateCheckData); push to fork branch; 62→64 tests pass — by sst-dev-cycle at 2026-05-28T07:15:00Z
- 5.9: add AllowedAPKSigningKeys + Binaries %c assertions to test_fdroid_mr_yaml_in_source_branch; 62→62 tests pass — by sst-dev-cycle at 2026-05-27T23:30:00Z
- 5.8: decode+parse YAML content from GitLab API in test_fdroid_mr_yaml_in_source_branch; assert RepoType='git' and Repo=GITHUB_URL — by sst-dev-cycle at 2026-05-27T22:00:00Z
- 5.4 (proactive): added RepoType, Repo, WebSite to fdroid YAML; pushed to fork branch add-org.bitanon.studfinder; 3 new tests; 59→62 tests pass — by sst-dev-cycle at 2026-05-27T21:30:00Z
- 7.6: extended test_ua_routing_cta_divs_present to assert cta-ios + cta-desktop divs; 59→59 tests pass — by sst-dev-cycle at 2026-05-27T14:05:00Z
- 7.1+7.2+7.3+7.4: F-Droid badge (primary CTA), GitHub sideload link, UA routing (Android/iOS/desktop divs + navigator.userAgent IIFE), "why open source" marked complete; 8 new tests in test_html.py; 51→59 tests pass — by sst-dev-cycle at 2026-05-27T12:30:00Z
- 5.3: created branch add-org.bitanon.studfinder in fork, added YAML via GitLab API, opened MR !39185 to fdroid/fdroiddata; 5 new tests in test_fdroid_mr.py; 46→51 tests pass — by sst-dev-cycle at 2026-05-27T10:30:00Z
- 4.9: replace apksigner verify body with aapt dump badging + assert versionCode='15' in test_release_apk_versioncode_15; 46→46 tests pass — by sst-dev-cycle at 2026-05-28T00:00:00Z
- SPEC 4.6+4.7: built+signed release APK (assembleRelease with toadlybroodleKeyStore.jks); discovered actual cert SHA-256 e04d3854... (differs from MinimaList's older cert); corrected YAML + SPEC + tests; published studfinder-v15-release.apk to GitHub Release v15; 41→46 tests pass — by sst-dev-cycle at 2026-05-27T23:30:00Z
- SPEC 5.7: fix stale %v→%c in SPEC.md 4.7 parenthetical + 5.1 Binaries URL description; 41→41 tests pass — by sst-dev-cycle at 2026-05-27T23:00:00Z
- SPEC 5.6: fix Binaries %v→%c in fdroid YAML (versionCode-based URL matches tag v15 + planned APK filename); assert %c + deny %v in test; 41→41 tests pass — by sst-dev-cycle at 2026-05-27T22:00:00Z
- SPEC 5.1+5.2: drafted docs/fdroid/metadata/org.bitanon.studfinder.yml + categories config; fdroid lint passes; 25→41 tests pass — by sst-dev-cycle at 2026-05-27T21:00:00Z
- SPEC 1.1: rewrote landing-page copy with open-source+physical-tools lead, added "Why open source" section explaining F-Droid path; deployed to VPS; 21→25 tests pass — by sst-dev-cycle at 2026-05-27T20:00:00Z
- SPEC 4.8: replace tag_sha==head_sha with ancestor check in test_tag_v15_points_to_head; 20→21 tests pass — by sst-dev-cycle at 2026-05-27T19:00:00Z
- SPEC 4.5+4.2: created annotated git tag v15 at HEAD; fastlane metadata (title, short/full description, changelog/15.txt, 512×512 icon upscaled from xxxhdpi); phoneScreenshots/ dir created; 11→21 tests pass — by sst-dev-cycle at 2026-05-27T18:30:00Z
- SPEC 4.1+3.9+4.3+4.4: added Apache-2.0 LICENSE + README.md; removed org.gradle.java.home; upgraded Gradle 7.4→8.7 + AGP 7.3.1→8.2.2 + Kotlin 1.7.20→1.9.20; pinned buildToolsVersion "33.0.2"; bumped versionCode 14→15, versionName "1.13"→"2.0"; assembleDebug BUILD SUCCESSFUL with Java 21; 26→36 tests pass — by sst-dev-cycle at 2026-05-27T17:00:00Z
- SPEC 3.8: replaced storeFile rootProject.file("app/" + ...) with file() in app/build.gradle; documented correct storeFile format in REMOVED-CLOUD-SURFACE.md; 16 → 26 tests pass — by sst-dev-cycle at 2026-05-27T15:10:00Z

## Next up (queued for next cycle)

- [easy] Add Lightning donation address in website footer + in-app "About" screen link. Reason: SPEC 7.5. Blocked: need user's Lightning address (e.g. user@getalby.com or user@stacker.news) — not found in codebase; user must supply before this can ship.
- [medium] Add 4-6 affiliate product cards above the fold (Franklin ProSensor 710, Zircon HD55, magnetic, premium electronic) with UTM-tagged links + FTC disclosure. Reason: SPEC 1.3. Blocked on H1.1 (Amazon Associates signup in HUMAN.md).
- [medium] Smoke-test studfinder-v15-release.apk on a connected Android device via adb: `adb install -r app/build/outputs/apk/release/studfinder-v15-release.apk` (or pull from GitHub Release v15), then drive through `adb shell am start`/`input` to exercise launch → instructions screen → sensor-sweep activity → settings; assert (a) `adb logcat` contains no `AdMob`, `FirebaseApp`, or `GoogleAnalytics` lines during the run (greppable allowlist), (b) `dumpsys netstats detail` shows zero bytes for `org.bitanon.studfinder` over the run, (c) exit code 0 from `adb shell am force-stop`. Write a new `test_device_smoke.py` that runs against `ADB_SERIAL` env var (skip if unset so CI without a device stays green) and record outcome under a new SPEC 4.10 (file the sub-item when picking). Reason: gates F-Droid acceptance + verifies the Phase-3 strip on real hardware; emulator cannot exercise magnetometer/haptic. Requires a phone connected to the chain host via USB-debugging before this is picked.
