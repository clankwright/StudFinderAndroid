# studfinderapp.com TODO (handoff doc)

> Cross-cycle state. Every skill reads this on start and updates it on close. Three sections, in this order.

## In flight

<!-- Empty — no skill currently running. -->

## Just shipped (last cycle)

- 0.6 + SPEC 7.5 re-routed: stripped all em-dashes (7) from `public_html/index.html` → ASCII-clean; added `<meta charset="utf-8">` to `<head>`; added `charset utf-8;` to studfinderapp.com nginx block in `/home/rob/Dev/botlab.dev/botlab_nginx_config` (synced from VPS first, then edited locally + pushed back); added `/.well-known/lnurlp/` + `/lnurlp/` proxy_pass blocks to the same nginx block; swapped LN address `rob@botlab.dev` → `sf@studfinderapp.com` (LNBits paylink id `TWmbXp`, same wallet as id `a6Vcvc`; UPDATE-fixed `domain` column from `sf@studfinderapp.com` typo to `studfinderapp.com` so metadata identifier reads correctly); kept the ⚡ icon on the Lightning link via HTML entity `&#9889;` (renders as bolt, keeps source ASCII); scp'd HTML to VPS with timestamped backup; nginx -t + reload clean. Verified: `Content-Type: text/html; charset=utf-8`; 0 non-ASCII bytes in served body; `studfinderapp.com/.well-known/lnurlp/sf` returns valid LNURL-pay JSON with identifier `sf@studfinderapp.com`; `botlab.dev/.well-known/lnurlp/rob` still works (legacy unaffected). Added 2 tests: `test_charset_meta_declared_in_head`, `test_no_em_dashes_in_html`; 27→29 tests in test_html.py; 71→73 full suite. Also synced all other ~/Dev nginx configs (akiya, csvagent already byte-identical; satring + clankfeed source-of-truth via symlink) — by manual (direct edit + VPS push) at 2026-05-28T22:30:00Z
- H7.1 closed + SPEC 7.5 refined: swapped placeholder `toadlybroodle@stacker.news` → live `rob@botlab.dev` in `public_html/index.html` (href + visible text); scp'd to VPS with timestamped backup; curl confirms served page now shows `lightning:rob@botlab.dev`; 4 donate-tests still green; LNBits paylink consolidation (rob@satring.com + tob@botlab.dev → rob@botlab.dev id a6Vcvc) confirmed live on both botlab.dev and satring.com /.well-known/lnurlp/ paths — by manual (direct edit + VPS push) at 2026-05-28T21:30:00Z
- 6.2: at-wall hands-on verification on OnePlus CPH2647 — coin calibration triggered red-LED sequence, wall sweep located studs as expected, beeper + sensitivity slider behaved per instructions — by user (manual physical test) at 2026-05-28T21:00:00Z
- 6.1+6.3+6.4+6.5: device smoke-test on OnePlus CPH2647 (Android 16); install via /data/local/tmp, launch StudFActivity, force-stop; logcat allowlist clean (0 AdMob/Firebase/Crashlytics/GoogleAnalytics/gms.ads/ca-app-pub hits across 29k lines); netstats UID 10408 absent (zero bytes); airplane-mode relaunch clean; Phase 7.5 SUPPORT button confirmed firing ACTION_VIEW to studfinderapp.com/#donate (Brave opened the page); new docs/test_device_smoke.py (5 tests, ADB_SERIAL-gated); 71→76 tests pass with device / 71+5 skipped without — by manual (direct on-device session) at 2026-05-28T20:30:00Z
- 7.7: fix test_donate_lightning_address_displayed to strip HTML comments + scope to donate section; add comment-only rejection guard; 70→71 tests pass — by sst-dev-cycle at 2026-05-28T10:00:00Z
- 7.5: Lightning donation footer (website #donate section + lightning: link) + donate button in app Instructions dialog; 64→70 tests pass — by sst-dev-cycle at 2026-05-28T09:30:00Z
- 5.4: address linsui MR !39185 change requests (full commit SHA, subdir: app, delete UpdateCheckData); push to fork branch; 62→64 tests pass — by sst-dev-cycle at 2026-05-28T07:15:00Z
- 5.9: add AllowedAPKSigningKeys + Binaries %c assertions to test_fdroid_mr_yaml_in_source_branch; 62→62 tests pass — by sst-dev-cycle at 2026-05-27T23:30:00Z
- 5.8: decode+parse YAML content from GitLab API in test_fdroid_mr_yaml_in_source_branch; assert RepoType='git' and Repo=GITHUB_URL — by sst-dev-cycle at 2026-05-27T22:00:00Z
- 5.4 (proactive): added RepoType, Repo, WebSite to fdroid YAML; pushed to fork branch add-org.bitanon.studfinder; 3 new tests; 59→62 tests pass — by sst-dev-cycle at 2026-05-27T21:30:00Z
## Next up (queued for next cycle)

- [medium] Add 4-6 affiliate product cards above the fold (Franklin ProSensor 710, Zircon HD55, magnetic, premium electronic) with UTM-tagged links + FTC disclosure. Reason: SPEC 1.3. Blocked on H1.1 (Amazon Associates signup in HUMAN.md).
