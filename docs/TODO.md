# studfinderapp.com TODO (handoff doc)

> Cross-cycle state. Every skill reads this on start and updates it on close. Three sections, in this order.

## In flight

<!-- Empty — no skill currently running. -->

## Just shipped (last cycle)

- SPEC 3.5+3.6+3.7: rewired app/build.gradle signing to shared toadlybroodle keystore (gated on app/release.keystore.properties existence), extended .gitignore (*.jks/*.keystore/*.keystore.properties/*.apk), created docs/REMOVED-CLOUD-SURFACE.md, all 16 cloud-strip + 7 signing-config checks pass, assembleDebug BUILD SUCCESSFUL with JDK 17 pin in gradle.properties — by sst-dev-cycle at 2026-05-27T08:00:00Z
- SPEC 3.1+3.2+3.3+3.4: deleted AdMob.kt + Firebase.kt, stripped all call sites from StudFActivity.kt + StudFView.kt, removed Firebase/AdMob plugins and deps from build.gradle, deleted google-services.json, removed INTERNET/ACCESS_NETWORK_STATE permissions and all GMS meta-data from manifest; all 16 strip-audit checks pass; `./gradlew clean assembleDebug` succeeds — by sst-dev-cycle at 2026-05-27T06:00:00Z
- SPEC 0.4+0.5: added Plausible analytics (outbound-links extension, F-Droid-badge-click event, stub fn) to index.html; updated sitemap.xml lastmod to 2026-05-27; deployed to VPS; GSC ownership confirmed via DNS TXT record — by sst-dev-cycle at 2026-05-27T05:00:00Z
- SPEC 0.1+0.2+0.3: confirmed studfinderapp.com is live on user's VPS (nginx, Let's Encrypt, web root `/var/www/studfinderapp.com`); documented DNS/TLS/hosting in SPEC; removed broken iTunes + Google Play badges from index.html; added F-Droid/GitHub CTA; marked 0.3 resolved (no migration needed) — by sst-dev-cycle at 2026-05-27T13:30:00Z
- Switched signing target from the legacy 2022 Studfinder keystore (`extras/key-signing/keystore.jks`) to the shared toadlybroodle keystore (`~/Dev/dev-creds/toadlybroodleKeyStore.jks`) — same cert MinimaList's F-Droid release uses (SHA-256 `b800dcf0a7725e2f71987c40d979757acd328a23de2e93a7efc0e400aeb2db69`). Trade-off accepted: breaks signature continuity for prior Play Store sideloads (Play Store listing is suspended anyway), gains consistency across toadlyBroodle's F-Droid catalog and reuses MinimaList's pre-known cert digest in the fdroiddata YAML. Updated SPEC 3.5 (rewire to shared keystore via `app/release.keystore.properties` pattern + extend `.gitignore`), 4.6 (verify post-build digest matches pre-known value as sanity check), 4.7 (APK naming `studfinder-v%v-release.apk` mirrors MinimaList), 5.1 (YAML mirrors MinimaList structure with pre-known `AllowedAPKSigningKeys`). — by manual at 2026-05-27.
- Switched F-Droid distribution from F-Droid-key path to reproducible-builds-with-developer-signing. Added SPEC 4.6 (build+sign+verify cert SHA-256), 4.7 (publish signed APK as GitHub Release), expanded 5.1 with `Binaries:` + `AllowedAPKSigningKeys:` YAML fields. — by manual at 2026-05-27.
- Moved Android source from `C:\Users\rob\Dev\android\Studfinder2023` to `~/Dev/android/Studfinder2023` (432MB, includes `.git` with full history) — by manual at 2026-05-27.
- Repositioned SPEC: open-source F-Droid Android app is the main value-add; website is the discovery + monetization layer. Re-ordered phases — Phase 3 (cloud-strip mirroring MinimaList), Phase 4 (repo hygiene), Phase 5 (F-Droid submission), Phase 6 (device QA), Phase 7 (website→F-Droid routing), Phase 8 (SEO push), Phase 9 (PWA demoted to iOS-only fallback), Phase 10 (email list). Removed paid Pro tier (incompatible with FOSS); replaced with Lightning donation jar. — by manual at 2026-05-27.
- Moved website files from `C:\Users\rob\Dev\websites\studfinderapp.com` to `~/Dev/websites/studfinderapp.com` (14MB cPanel backup; site code in `public_html/`) — by manual at 2026-05-27.

## Next up (queued for next cycle)

- [easy] [should-fix] 3.8 fix `app/build.gradle:17` storeFile path: replace `rootProject.file("app/" + storeFile)` with `file(storeFile)` so absolute keystore paths work; update `REMOVED-CLOUD-SURFACE.md` with correct storeFile format — review of 7463e01
- [easy] [should-fix] 3.9 when SPEC 4.3 runs: remove `gradle.properties` `org.gradle.java.home` machine-specific JDK path and upgrade Gradle wrapper to 8.x+ (Java-21-compatible) so F-Droid's build server doesn't fail — review of 7463e01
- [medium] Build + sign release APK with shared keystore; rename to `studfinder-v15-release.apk`; sanity-verify signing cert SHA-256 matches the pre-known `b800dcf0a7725e2f71987c40d979757acd328a23de2e93a7efc0e400aeb2db69`. Reason: SPEC 4.6 — verifies the keystore wiring is correct and produces the digest the fdroiddata YAML already expects.
- [medium] Publish `studfinder-v15-release.apk` as GitHub Release artifact attached to tag `v15`. Reason: SPEC 4.7 — F-Droid `Binaries:` URL target.
- [medium] Rewrite landing-page copy: lead with the F-Droid open-source app + physical-tools angle. Reason: SPEC 1.1 — kicks off the affiliate pivot in parallel with F-Droid prep.
- [easy] Sign up for Amazon Associates (US + OneLink for UK/CA/AU). Reason: SPEC 1.2.
- [medium] Add 4-6 affiliate product cards above the fold (Franklin ProSensor 710, Zircon HD55, magnetic, premium electronic) with UTM-tagged links + FTC disclosure. Reason: SPEC 1.3.
