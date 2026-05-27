#!/usr/bin/env bash
# Tests that app/build.gradle uses app/release.keystore.properties (gated on
# file existence) and that .gitignore covers key/apk artifacts.

set -e
PASS=0
FAIL=0
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

check() {
    local label="$1"
    shift
    if "$@" &>/dev/null; then
        echo "PASS: $label"
        PASS=$((PASS + 1))
    else
        echo "FAIL: $label"
        FAIL=$((FAIL + 1))
    fi
}

check_absent() {
    local label="$1"
    shift
    if "$@" &>/dev/null; then
        echo "FAIL: $label (pattern found, should be absent)"
        FAIL=$((FAIL + 1))
    else
        echo "PASS: $label"
        PASS=$((PASS + 1))
    fi
}

# 3.5a: build.gradle references app/release.keystore.properties
check "build.gradle references app/release.keystore.properties" \
    grep -q "app/release.keystore.properties" "$ROOT/app/build.gradle"

# 3.5b: old extras/key-signing path removed from build.gradle
check_absent "old extras/key-signing path absent from build.gradle" \
    grep -q "extras/key-signing" "$ROOT/app/build.gradle"

# 3.5c: build.gradle has an existence check gating the signing block
check "build.gradle gates signing on file existence" \
    grep -qE "\.exists\(\)" "$ROOT/app/build.gradle"

# 3.5d: .gitignore covers *.jks
check ".gitignore covers *.jks" grep -q "\*\.jks" "$ROOT/.gitignore"

# 3.5e: .gitignore covers *.keystore.properties
check ".gitignore covers *.keystore.properties" grep -q "\*\.keystore\.properties" "$ROOT/.gitignore"

# 3.5f: .gitignore covers *.apk
check ".gitignore covers *.apk" grep -q "\*\.apk" "$ROOT/.gitignore"

# 3.5g: app/release.keystore.properties is NOT committed (should not exist or be gitignored)
check_absent "app/release.keystore.properties not tracked by git" \
    git -C "$ROOT" ls-files --error-unmatch "app/release.keystore.properties"

# 3.8a: storeFile must NOT use rootProject.file("app/" + ...) — breaks absolute paths
check_absent "storeFile does not use rootProject.file(\"app/\" + ...) concatenation" \
    grep -qE 'rootProject\.file\("app/" \+' "$ROOT/app/build.gradle"

# 3.8b: storeFile must use file() so absolute and relative paths both resolve correctly
check "storeFile uses file() for absolute/relative path resolution" \
    grep -qE "storeFile file\(" "$ROOT/app/build.gradle"

# 3.8c: REMOVED-CLOUD-SURFACE.md documents the correct storeFile format
check "REMOVED-CLOUD-SURFACE.md documents file() storeFile format" \
    grep -q "file(storeFile)" "$ROOT/docs/REMOVED-CLOUD-SURFACE.md"

echo ""
echo "Signing config: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
