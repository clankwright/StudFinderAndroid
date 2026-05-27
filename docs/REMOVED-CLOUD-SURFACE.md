# Removed Cloud Surface — StudFinderAndroid

Documents every proprietary/network dependency removed from the app in Phase 3, mirroring MinimaList's log format. Goal: zero anti-features, `AntiFeatures: []` in the fdroiddata YAML.

## Summary

All AdMob, Firebase, and Google Play Services dependencies have been removed. The app is fully offline; it requires only the device magnetometer (compass sensor). F-Droid anti-feature status: none.

## Phase 3.1 — AdMob removed

- Deleted `app/src/main/java/org/bitanon/studfinder/AdMob.kt`
- Removed all `AdMob` call sites from `StudFActivity.kt` (init, banner show/hide, interstitial trigger)
- Removed `com.google.android.gms:play-services-ads:21.4.0` from `app/build.gradle`
- Removed `com.google.android.gms.ads.APPLICATION_ID` meta-data from manifest
- Removed `com.google.android.gms.ads.AdActivity` declaration from manifest

Audit (run `scripts/verify_cloud_strip.sh`): PASS — `grep -rn 'AdMob\|gms\.ads\|ca-app-pub-' app/src` returns nothing.

## Phase 3.2 — Firebase removed

- Deleted `app/src/main/java/org/bitanon/studfinder/Firebase.kt`
- Removed all Firebase/Crashlytics call sites from `StudFActivity.kt`
- Removed `id 'com.google.gms.google-services'` and `id 'com.google.firebase.crashlytics'` plugins from `app/build.gradle`
- Removed `platform('com.google.firebase:firebase-bom:31.1.1')`, `firebase-crashlytics-ktx`, and `firebase-analytics-ktx` deps
- Deleted `app/google-services.json`

Audit: PASS — `grep -rn 'Firebase\|firebase' app/src app/build.gradle` returns nothing.

## Phase 3.3 — Network permissions removed

- Removed `android.permission.INTERNET` from `AndroidManifest.xml`
- Removed `android.permission.ACCESS_NETWORK_STATE` from `AndroidManifest.xml`
- `WAKE_LOCK` retained (screen must stay on during detection)

App is now fully offline. Qualifies for F-Droid `NoAnti-Features`.

## Phase 3.4 — GMS version meta-data removed

- Removed `com.google.android.gms.version` meta-data from `AndroidManifest.xml`

## Phase 3.5 — Signing rewired to shared toadlybroodle keystore

Replaced the old `extras/key-signing/keyStoreCreds.properties` signing config with a load of `app/release.keystore.properties` (gitignored), mirroring MinimaList's pattern.

**Keystore**: `~/Dev/dev-creds/toadlybroodleKeyStore.jks`
**Cert SHA-256**: `e04d3854fc1245e27b826feaa30298bda89a4c0528a2a0b7ddbc23ad60a72fd4`
(derived by running `apksigner verify --print-certs studfinder-v15-release.apk` on the Phase 4.6 build; note: the `toadlybroodleKeyStore.jks` key is distinct from the cert used by MinimaList's earlier APKs, which were signed with a prior keystore no longer in dev-creds)

The signing block in `app/build.gradle` is gated on `app/release.keystore.properties` existence so contributors without the keystore can still run `./gradlew assembleDebug` without error.

**`storeFile` format**: `app/release.keystore.properties` must set `storeFile` to the keystore path. Both absolute paths (e.g. `/home/rob/Dev/dev-creds/toadlybroodleKeyStore.jks`) and paths relative to the `app/` module directory (e.g. `../dev-creds/toadlybroodleKeyStore.jks`) work — `app/build.gradle` resolves the value with `file(storeFile)`, which handles absolute paths correctly. The old `rootProject.file("app/" + storeFile)` pattern (Phase 3.5 original) only accepted relative paths and silently broke for absolute paths.

Trade-off: breaks signature continuity for any device with a prior Play Store sideload of `org.bitanon.studfinder` (Play Store listing is suspended — no active install funnel). Gains consistency across toadlyBroodle's F-Droid catalog; the pre-known cert digest is already referenced in the fdroiddata YAML (`AllowedAPKSigningKeys:`).

The legacy `extras/key-signing/` directory (original 2022 Studfinder cert + `keyStoreCreds.properties`) is left in place — gitignored, harmless archive in case signature continuity is ever wanted.

Gitignore additions: `*.jks`, `*.keystore`, `*.keystore.properties`, `*.apk`

## Phase 3.6 — Final reverse-grep audit

Command: `grep -rEi 'firebase|gms|admob|crashlytics|ca-app-pub' app/src app/build.gradle app/src/main/AndroidManifest.xml`

Result: **no matches** (exit 0). All 16 `scripts/verify_cloud_strip.sh` checks pass.

## Phase 3.7 — Clean Gradle debug build

Command: `./gradlew clean assembleDebug`

Result: **BUILD SUCCESSFUL** — zero unresolved references.

Note: Gradle 7.4's bundled Groovy ASM does not support Java 21 class files (major version 65). Fixed by adding `org.gradle.java.home=/usr/lib/jvm/java-17-openjdk-amd64` to `gradle.properties` to pin the Gradle daemon JDK to JDK 17 on this build machine. SPEC 4.3 should upgrade the Gradle wrapper to a version with full Java 21 support when doing F-Droid build-server compatibility work.
