#!/usr/bin/env bash
# Verifies that cloud surface (AdMob, Firebase, GMS) has been stripped.
# Exits 0 if clean, non-zero if any banned symbol is found.

set -e
PASS=0
FAIL=0
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

check() {
    local label="$1"
    shift
    if "$@" &>/dev/null; then
        echo "FAIL: $label"
        FAIL=$((FAIL + 1))
    else
        echo "PASS: $label"
        PASS=$((PASS + 1))
    fi
}

# 3.1: No AdMob symbols in app/src
check "no AdMob class references" grep -rn "AdMob" "$ROOT/app/src"
check "no gms.ads imports" grep -rn "gms\.ads\|gms/ads" "$ROOT/app/src"
check "no ca-app-pub" grep -rn "ca-app-pub-" "$ROOT/app/src"
check "no AdActivity in manifest" grep -n "AdActivity" "$ROOT/app/src/main/AndroidManifest.xml"
check "no gms.ads.APPLICATION_ID in manifest" grep -n "gms\.ads\.APPLICATION_ID" "$ROOT/app/src/main/AndroidManifest.xml"
check "no play-services-ads in app/build.gradle" grep -n "play-services-ads" "$ROOT/app/build.gradle"

# 3.2: No Firebase symbols in app/src or build files
check "no Firebase class in app/src" grep -rn "Firebase\|firebase" "$ROOT/app/src"
check "no google-services plugin in app/build.gradle" grep -n "com.google.gms.google-services" "$ROOT/app/build.gradle"
check "no crashlytics plugin in app/build.gradle" grep -n "com.google.firebase.crashlytics" "$ROOT/app/build.gradle"
check "no firebase-bom in app/build.gradle" grep -n "firebase-bom" "$ROOT/app/build.gradle"
check "no firebase deps in app/build.gradle" grep -n "firebase-crashlytics-ktx\|firebase-analytics-ktx" "$ROOT/app/build.gradle"
check "no google-services in root build.gradle" grep -n "google-services\|firebase-crashlytics-gradle" "$ROOT/build.gradle"
check "no google-services.json" test -f "$ROOT/app/google-services.json"

# 3.3: No network permissions in manifest
check "no INTERNET permission in manifest" grep -n "android.permission.INTERNET" "$ROOT/app/src/main/AndroidManifest.xml"
check "no ACCESS_NETWORK_STATE in manifest" grep -n "ACCESS_NETWORK_STATE" "$ROOT/app/src/main/AndroidManifest.xml"

# 3.4: No gms.version meta-data
check "no gms.version in manifest" grep -n "com.google.android.gms.version" "$ROOT/app/src/main/AndroidManifest.xml"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
