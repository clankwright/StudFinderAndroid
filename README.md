# StudFinder Android

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

Free, open-source, ad-free Android stud finder app. Uses the device magnetometer to detect metal screws/nails inside wall studs.

- No ads, no analytics, no crash reporting, no Google Play Services
- Fully offline — no network permissions
- Distributed via [F-Droid](https://f-droid.org) (submission in progress)
- Source available at [github.com/clankwright/StudFinderAndroid](https://github.com/clankwright/StudFinderAndroid)

## Screenshots

<p>
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/01-main.png" width="200" alt="Main screen with the magnetometer marker, Detect, Beeper, and sensitivity controls">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/02-ready.png" width="200" alt="Green LED while Detect is held and the magnetic field is stable">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/03-detecting.png" width="200" alt="Red LEDs when metal in a stud disturbs the magnetic field">
  <img src="fastlane/metadata/android/en-US/images/phoneScreenshots/04-instructions.png" width="200" alt="Instructions dialog">
</p>

## Build

```bash
./gradlew assembleDebug
```

Release builds require `app/release.keystore.properties` (gitignored) pointing at the signing keystore.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
