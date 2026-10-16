# AdHost-TDB

Aggressive ad, tracker, telemetry and unwanted-domain blocklist intended for **NextDNS custom denylist** and other domain-list DNS blockers.

## NextDNS format

Use `hosts.txt` as the custom denylist source. It contains **one domain per line**, for example:

```text
ads.example.com
tracker.example.net
```

This is deliberately **not** an operating-system hosts file: do not add `0.0.0.0` or `127.0.0.1` prefixes. The generated file is a domain-only list.

Raw list URL:
`https://raw.githubusercontent.com/Kesitinh13524/AdHost-TDB/main/hosts.txt`

## Automatic refresh

GitHub Actions is scheduled daily at 19:17 UTC (02:17 in Vietnam, UTC+7). You can also run it manually from **Actions → Update NextDNS blocklist → Run workflow**.

The updater merges public lists, normalizes host-format and plain-domain entries into bare domains, validates domain syntax, deduplicates entries, applies `allowlist.txt`, and refuses to replace the output if the aggregate is unexpectedly small.

## Notes

- Aggressive lists can block legitimate sites or app functions. If a service stops working, remove its domain from the NextDNS denylist or add it to `allowlist.txt` and run the workflow again.
- No list blocks every ad; first-party ads may share domains with wanted content.
- The current `hosts.txt` is only a bootstrap seed. The full aggregate will be published after the first successful GitHub Actions run.
- A successful GitHub commit means the list was published, not that every domain has been manually tested in NextDNS.

## Sources

- HaGeZi DNS blocklists: https://github.com/hagezi/dns-blocklists
- StevenBlack hosts: https://github.com/StevenBlack/hosts
- AdAway hosts: https://adaway.org/hosts.txt

Upstream lists have their own licenses and terms. See [LICENSE-NOTICE.md](LICENSE-NOTICE.md).
