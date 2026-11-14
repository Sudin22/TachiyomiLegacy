# TachiyomiLegacy

A legacy-format extension catalogue intended for testing with original Tachiyomi 0.15.3.

## Repository URL

`https://raw.githubusercontent.com/Sudin22/TachiyomiLegacy/main/index.min.json`

## Catalogue

- 1,284 archived extension metadata entries.
- 413 English entries.
- Includes **Tachiyomi: Asura Scans** (package `eu.kanade.tachiyomi.extension.en.asurascans`).
- Asura Scans APK v1.4.58 is mirrored locally at `apk/tachiyomi-en.asurascans-v1.4.58.apk`.
- Other APK references currently point to the archived source repository; they have not all been mirrored or individually tested.

## Compatibility and safety notes

The catalogue is converted from an archived 1.4.x-era extension index. This is a compatibility candidate for Tachiyomi 0.15.3, not a guarantee that every APK installs or that every website still works. Websites change, and some archived extensions may be broken or discontinued.

Install only extensions from repositories you trust. Extension APKs execute code on your device.

## Test Asura Scans

1. Remove and re-add the repository URL above, or refresh its index.
2. Find **Tachiyomi: Asura Scans** in Browse → Extensions.
3. Install it and check whether Android accepts the APK.
4. Open the installed source and test browsing and opening a chapter.

Report installation errors separately from source/network errors; they indicate different problems.
