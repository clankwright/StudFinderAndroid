#!/usr/bin/env bash
# Tests for Phase 4 F-Droid preparation: LICENSE, Gradle hygiene, version bump.
# Exits 0 if all pass, non-zero if any fail.

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

# 4.1: LICENSE file exists and README.md has license badge
check "LICENSE file exists at repo root" test -f "$ROOT/LICENSE"
check "LICENSE file contains Apache-2.0 identifier" grep -q "Apache License" "$ROOT/LICENSE"
check "README.md exists at repo root" test -f "$ROOT/README.md"
check "README.md has license badge" grep -q "license" "$ROOT/README.md"

# 3.9: org.gradle.java.home machine-specific path removed from gradle.properties
check_absent "org.gradle.java.home removed from gradle.properties" \
    grep -q "org.gradle.java.home" "$ROOT/gradle.properties"

# 4.3: buildToolsVersion pinned in app/build.gradle
check "buildToolsVersion pinned in app/build.gradle" \
    grep -q "buildToolsVersion" "$ROOT/app/build.gradle"

# 3.9/4.3: Gradle wrapper upgraded to 7.6+ (no longer 7.4)
check "Gradle wrapper is 7.6+ or 8.x+" \
    grep -qE "gradle-(7\.[6-9]|[89]\.[0-9])" "$ROOT/gradle/wrapper/gradle-wrapper.properties"
check_absent "Gradle wrapper is no longer 7.4" \
    grep -q "gradle-7\.4-" "$ROOT/gradle/wrapper/gradle-wrapper.properties"

# 4.4: versionCode bumped to 15
check "versionCode is 15 in app/build.gradle" \
    grep -q "versionCode 15" "$ROOT/app/build.gradle"

# 4.4: versionName bumped to 2.0
check "versionName is 2.0 in app/build.gradle" \
    grep -q 'versionName "2.0"' "$ROOT/app/build.gradle"

echo ""
echo "F-Droid prep: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
