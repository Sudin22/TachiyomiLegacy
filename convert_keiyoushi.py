#!/usr/bin/env python3
"""Experimental Keiyoushi index.json -> legacy Tachiyomi index.min.json converter.

Run:
  python convert_keiyoushi.py
  python convert_keiyoushi.py ./index.json --out index.min.json

This converts catalogue metadata only. It does not patch or downgrade APKs.
"""
import argparse
import json
import urllib.request
from pathlib import Path

UPSTREAM = "https://raw.githubusercontent.com/keiyoushi/extensions/repo/index.json"

def extension_entries(document):
    if isinstance(document, list):
        return document
    if isinstance(document, dict):
        for key in ("extensions", "extensionList", "list"):
            value = document.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                nested = value.get("extensions") or value.get("list")
                if isinstance(nested, list):
                    return nested
    raise ValueError("Could not find an extension array in the input JSON")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="Local Keiyoushi index.json; omit to download it")
    parser.add_argument("--out", default="index.min.json")
    args = parser.parse_args()

    if args.input:
        document = json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:
        request = urllib.request.Request(
            UPSTREAM, headers={"User-Agent": "TachiyomiLegacyBridge/0.1"}
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            document = json.loads(response.read().decode("utf-8"))

    converted, skipped = [], []
    for entry in extension_entries(document):
        try:
            resources = entry.get("resources") or {}
            apk_url = resources.get("apkUrl") or entry.get("apk")
            required = ("name", "packageName", "versionCode", "versionName")
            if not all(entry.get(field) not in (None, "") for field in required) or not apk_url:
                raise ValueError("missing required field")

            sources = []
            languages = []
            for source in entry.get("sources") or []:
                source_id = source.get("id")
                source_name = source.get("name")
                base_url = source.get("homeUrl")
                if source_id in (None, "") or not source_name or not base_url:
                    continue
                language = source.get("language") or "all"
                # Convert IDs to integers exactly (Python integers preserve 64-bit values).
                sources.append({
                    "name": source_name,
                    "lang": language,
                    "id": int(source_id),
                    "baseUrl": base_url,
                })
                languages.append(language)

            warning = str(entry.get("contentWarning") or "").upper()
            converted.append({
                "name": entry["name"],
                "pkg": entry["packageName"],
                "apk": apk_url,
                "lang": languages[0] if languages else "all",
                "code": int(entry["versionCode"]),
                "version": entry["versionName"],
                "nsfw": 1 if "NSFW" in warning else 0,
                "sources": sources,
            })
        except Exception as error:
            skipped.append({
                "name": entry.get("name", "<unknown>"),
                "reason": str(error),
            })

    Path(args.out).write_text(
        json.dumps(converted, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    if skipped:
        Path(args.out + ".skipped.json").write_text(
            json.dumps(skipped, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(f"Wrote {len(converted)} entries; skipped {len(skipped)}.")

if __name__ == "__main__":
    main()
