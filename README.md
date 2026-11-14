# Tachiyomi Legacy Bridge (experimental)

This repository contains an experimental legacy-format catalogue test for the original Tachiyomi app.

## Test repository URL

After GitHub Pages is enabled for this repository, the intended URL is:

`https://sudin22.github.io/TachiyomiLegacy/index.min.json`

Until Pages is enabled and deployed, use the raw file URL:

`https://raw.githubusercontent.com/Sudin22/TachiyomiLegacy/main/index.min.json`

## Important compatibility warning

This is a metadata-format experiment only. It does not convert, patch, or downgrade APK binaries. A current Keiyoushi extension may require a newer extension library than original Tachiyomi supports. A catalogue entry appearing does not prove that its APK will install, load, or run.

The sample entry is AHottie, based on metadata visible in Keiyoushi's public catalogue. Test only if you trust the extension publisher and understand that extensions execute code in the app.

## Files

- `index.min.json`: one-entry legacy catalogue sample.
- `convert_keiyoushi.py`: experimental converter for a downloaded Keiyoushi `index.json`.
