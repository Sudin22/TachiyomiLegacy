#!/usr/bin/env python3
"""Mirror legacy Tachiyomi APKs and icons into this repository.

The legacy index stores APK filenames (not absolute URLs). Tachiyomi resolves
those filenames beneath the repository's /apk/ directory and discovers icons
from /icon/<package>.png.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import json
import os
import time

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.min.json"
SOURCE = "https://raw.githubusercontent.com/deeplyarnab/mihon-extensions/repo"
HEADERS = {"User-Agent": "TachiyomiLegacy-asset-mirror/1.0"}
WORKERS = 16
RETRIES = 4


def fetch(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(RETRIES):
        try:
            request = Request(url, headers=HEADERS)
            with urlopen(request, timeout=90) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {url}")
                data = response.read()
            if not data:
                raise RuntimeError(f"Empty response: {url}")
            temporary = destination.with_suffix(destination.suffix + ".tmp")
            temporary.write_bytes(data)
            temporary.replace(destination)
            return
        except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
            last_error = exc
            if attempt + 1 < RETRIES:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to mirror {url}: {last_error}")


def main() -> None:
    entries = json.loads(INDEX.read_text(encoding="utf-8"))
    tasks = {}
    for entry in entries:
        package = entry["pkg"]
        apk_value = entry["apk"]
        filename = Path(urlparse(apk_value).path).name
        if not filename.endswith(".apk"):
            raise ValueError(f"Invalid APK reference for {package}: {apk_value}")
        entry["apk"] = filename
        tasks[f"apk/{filename}"] = f"{SOURCE}/apk/{filename}"
        tasks[f"icon/{package}.png"] = f"{SOURCE}/icon/{package}.png"

    failures = []
    completed = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(fetch, url, ROOT / relative): (relative, url)
            for relative, url in tasks.items()
        }
        for future in as_completed(futures):
            relative, url = futures[future]
            try:
                future.result()
                completed += 1
                if completed % 100 == 0:
                    print(f"Mirrored {completed}/{len(futures)} assets")
            except Exception as exc:
                failures.append(f"{relative}: {exc}")

    if failures:
        print("\n".join(failures))
        raise SystemExit(f"{len(failures)} asset downloads failed; index was not rewritten")

    INDEX.write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Successfully mirrored {len(entries)} APKs and {len(entries)} icons.")


if __name__ == "__main__":
    main()
