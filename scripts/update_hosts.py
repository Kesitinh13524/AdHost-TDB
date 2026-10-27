#!/usr/bin/env python3
"""Build a bare-domain denylist suitable for NextDNS custom denylist."""
from __future__ import annotations

import datetime as dt
import ipaddress
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "hosts.txt"
SOURCES_FILE = ROOT / "sources.json"
ALLOWLIST_FILE = ROOT / "allowlist.txt"
MIN_DOMAINS = int(os.environ.get("MIN_DOMAINS", "5000"))
TIMEOUT_SECONDS = 120
MAX_SOURCE_BYTES = 80 * 1024 * 1024
MAX_OUTPUT_BYTES = 90 * 1024 * 1024
DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$",
    re.IGNORECASE,
)


def load_allowlist() -> set[str]:
    result: set[str] = set()
    if not ALLOWLIST_FILE.exists():
        return result
    for raw in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines():
        item = raw.split("#", 1)[0].strip().lower().rstrip(".")
        if DOMAIN_RE.fullmatch(item):
            result.add(item)
    return result


def normalize_domain(value: str) -> str | None:
    value = value.strip().lower()
    # Ignore Adblock exception rules: they explicitly allow a domain.
    if value.startswith("@@"):
        return None
    # Accept simple Adblock rules such as ||ads.example.com^ and
    # ||tracker.example.net^$important, but not URL/path or regex rules.
    if value.startswith("||"):
        value = value[2:]
    elif value.startswith("|"):
        value = value[1:]
    value = re.split(r"[\^$]", value, maxsplit=1)[0].rstrip(".")
    if value.startswith("*."):
        value = value[2:]
    try:
        value = value.encode("idna").decode("ascii")
    except UnicodeError:
        return None
    if DOMAIN_RE.fullmatch(value):
        return value
    return None


def parse_domains(text: str, allowlist: set[str] | None = None) -> set[str]:
    allow = allowlist or set()
    domains: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        fields = line.split()
        if not fields:
            continue
        # Hosts format: IP address followed by one or more names.
        try:
            ipaddress.ip_address(fields[0])
            candidates = fields[1:]
        except ValueError:
            # Plain domain list (one domain per line); ignore arbitrary multi-field lines.
            candidates = fields if len(fields) == 1 else []
        for candidate in candidates:
            domain = normalize_domain(candidate)
            if domain and domain not in allow and not domain.endswith(".localhost"):
                domains.add(domain)
    return domains


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AdHost-TDB/1.0 (+https://github.com/Kesitinh13524/AdHost-TDB)"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        payload = response.read(MAX_SOURCE_BYTES + 1)
    if len(payload) > MAX_SOURCE_BYTES:
        raise RuntimeError("source exceeded 80 MiB safety limit")
    return payload.decode("utf-8", errors="replace")


def main() -> int:
    sources = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    allow = load_allowlist()
    merged: set[str] = set()
    successes: list[str] = []
    failures: list[str] = []
    for source in sources:
        name, url = source["name"], source["url"]
        try:
            domains = parse_domains(fetch(url), allow)
            if not domains:
                raise RuntimeError("no valid domains parsed")
            merged.update(domains)
            successes.append(f"{name}: {len(domains):,}")
            print(f"OK {name}: {len(domains):,} valid domains")
        except (OSError, urllib.error.URLError, UnicodeError, RuntimeError, TimeoutError) as exc:
            failures.append(f"{name}: {exc}")
            print(f"WARNING {name}: {exc}", file=sys.stderr)

    merged.difference_update(allow)
    if not successes:
        print("ERROR: every source failed; preserving previous list.", file=sys.stderr)
        return 1
    if len(merged) < MIN_DOMAINS:
        print(
            f"ERROR: only {len(merged):,} unique domains (minimum {MIN_DOMAINS:,}); "
            "preserving previous list.",
            file=sys.stderr,
        )
        return 1

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    header = [
        "# AdHost-TDB — NextDNS-compatible custom denylist",
        f"# Generated: {today} UTC",
        f"# Unique domains: {len(merged):,}",
        "# Format: one bare domain per line; no 0.0.0.0 or 127.0.0.1 prefix.",
        "# Sources: " + "; ".join(successes),
        "# Upstream false positives are possible. See README.md.",
        "",
    ]
    header.append(
        "# Large aggregates are split into sorted, non-overlapping hosts*.txt files."
    )
    header_text = "\n".join(header) + "\n"
    header_size = len(header_text.encode("utf-8"))
    output_paths: list[Path] = [OUTPUT]
    part_number = 1
    output_path = OUTPUT
    stream = output_path.open("w", encoding="utf-8", newline="\n")
    stream.write(header_text)
    bytes_written = header_size

    for domain in sorted(merged):
        line = domain + "\n"
        line_size = len(line.encode("ascii"))
        if bytes_written + line_size > MAX_OUTPUT_BYTES and bytes_written > header_size:
            stream.close()
            part_number += 1
            output_path = ROOT / f"hosts-part-{part_number:02d}.txt"
            output_paths.append(output_path)
            stream = output_path.open("w", encoding="utf-8", newline="\n")
            stream.write(header_text)
            bytes_written = header_size
        stream.write(line)
        bytes_written += line_size
    stream.close()

    active_outputs = set(output_paths)
    for stale_path in ROOT.glob("hosts-part-*.txt"):
        if stale_path not in active_outputs:
            stale_path.unlink()

    print(
        f"Wrote {len(merged):,} unique domains across {len(output_paths)} "
        "non-overlapping files."
    )
    for output_path in output_paths:
        print(f"Output: {output_path.name} ({output_path.stat().st_size:,} bytes)")
    if failures:
        print("Some upstream sources failed; successful sources passed validation.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
