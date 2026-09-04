# Aven Android

Android companion app for Mark-1/Aven.

## What this first Android build does

- Kotlin + Jetpack Compose UI
- Gemini chat over HTTPS
- API key entered by the user and encrypted with Android Keystore
- Local lightweight chat memory
- Microphone permission entry point (voice pipeline comes next)
- Reuses the Mark-1 prompt as an Android app asset

## Security

The APK does **not** contain a Gemini API key. Each user enters their own key on-device. Do not put a real API key in source control, Gradle files, resources, or GitHub Actions logs.

For a production public app, a backend proxy with server-side quota/rate-limit controls is safer than shipping direct client-side API access.

## Build

Open `android/` in Android Studio and let Gradle sync. Then select an emulator or Android phone and run the `app` configuration.

For a release build, use **Build > Generate Signed App Bundle / APK** in Android Studio.

## Current scope

The Windows Python app still contains desktop-only controls. Those are intentionally not copied into the Android module because Android permissions and APIs differ from Windows desktop automation.
