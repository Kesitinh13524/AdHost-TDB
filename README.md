# AdHost-TDB

A single merged, deduplicated domain denylist for **NextDNS custom denylist** and compatible DNS blockers.

## Output format

`hosts.txt` is intentionally a **plain domain list**: one domain per line, no IP address prefix, no duplicate domains. The generator converts standard hosts-file lines and plain domain feeds into lowercase ASCII domains, validates syntax, removes duplicates, and applies `allowlist.txt`.

Example:

```text
ad.doubleclick.net
doubleclick.net
tracker.example.net
```

Raw URL:
https://raw.githubusercontent.com/Kesitinh13524/AdHost-TDB/main/hosts.txt

## Aggregated sources

The daily generator merges these 37 upstream feeds where available:

- HaGeZi Multi Ultimate
- 1Hosts Xtra
- OISD Big domains
- hBlock domains
- Lightswitch05 Ads & Tracking Extended
- StevenBlack Unified Hosts
- AdAway
- GoodbyeAds
- anti-AD
- NoTracking hostnames
- jdlingyu/ad-wars
- tiuxo/hosts ads
- AnudeepND adservers
- Re-Malwack Aggressive aggregate (1M+ domains)
- Re-Malwack Default aggregate
- BlocklistProject Ads
- BlocklistProject Tracking
- Vietnamese hostsVN and its ad-server feed
- AdGuard Mobile Ads and Mobile Spyware hosts
- PolishFilters KADhosts
- FadeMind Spam and anti-popads
- Yoyo ad servers
- SomeoneWhoCares hosts
- Perflyst Smart TV and Android tracking
- NextDNS native tracking domains (Xiaomi, Apple, Alexa)
- DandelionSprout Anti-Malware hosts
- Firebog Easylist and AdGuardDNS hosts
- FadeMind Additional Risks
- Android app ads hosts
- DataMaster Android AdBlock hosts

These lists overlap by design; the generator stores each valid domain only once. Sources may change, become unavailable, or contain false positives. Some upstream lists include malware, phishing, telemetry, and tracking domains in addition to advertising domains. This is an aggressive combined list, so legitimate app/site features may occasionally be blocked.

## Automatic updates

GitHub Actions is scheduled daily at 19:17 UTC (02:17 in Vietnam, UTC+7). You can also run it manually from **Actions → Update NextDNS blocklist → Run workflow**.

The workflow runs parser tests, downloads the feeds, validates the aggregate, and commits `hosts.txt` only if it passes the minimum-size safety check. If every source fails or the result is unexpectedly small, the previous list is preserved.

**Bootstrap note:** until the first successful workflow run completes, `hosts.txt` contains only a small starter list. Check the [Actions page](https://github.com/Kesitinh13524/AdHost-TDB/actions) for the first successful run before relying on the full aggregate.

## False positives

If a wanted site or app stops working, identify the blocked domain in NextDNS logs and add that exact domain to `allowlist.txt`, then run the workflow again. Keep allowlist entries specific rather than allowlisting an entire large provider domain.

## Upstream licenses

This repository aggregates third-party feeds. Refer to each source's repository and license for its redistribution terms. See [LICENSE-NOTICE.md](LICENSE-NOTICE.md).
