# AdHost-TDB

A single merged, deduplicated domain denylist for **NextDNS custom denylist** and compatible DNS blockers.

## Output format

`hosts.txt` is intentionally a **plain domain list**: one domain per line, no IP address prefix, no duplicate domains. The generator converts standard hosts-file lines and plain domain feeds and simple Adblock domain rules into lowercase ASCII domains, validates syntax, removes duplicates, and applies `allowlist.txt`.

Example:

```text
ad.doubleclick.net
doubleclick.net
tracker.example.net
```

Raw URL:
https://raw.githubusercontent.com/Kesitinh13524/AdHost-TDB/main/hosts.txt

## Aggregated sources

The daily generator merges these 45 upstream feeds where available:

- HaGeZi Pop-Up Ads domains
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
- HaGeZi native trackers for Xiaomi, Samsung, Apple, Amazon, OPPO/Realme, Vivo, and Huawei
- HaGeZi referral and affiliate trackers

These lists overlap by design; the generator stores each valid domain only once. Sources may change, become unavailable, or contain false positives. Some upstream lists include malware, phishing, telemetry, and tracking domains in addition to advertising domains. This is an aggressive combined list, so legitimate app/site features may occasionally be blocked.

## Automatic updates

GitHub Actions is scheduled daily at 19:17 UTC (02:17 in Vietnam, UTC+7). You can also run it manually from **Actions → Update NextDNS blocklist → Run workflow**.

The workflow runs parser tests, downloads the feeds, validates the aggregate, and commits `hosts.txt` only if it passes the minimum-size safety check. If every source fails or the result is unexpectedly small, the previous list is preserved.

**Current aggregate:** `hosts.txt` has been populated with 74,512 unique domains from the ad, pop-up, referral, mobile, Smart TV, and native-device tracker feeds collected in this update. The scheduled workflow will refresh it from the 45 configured upstream sources when a run completes successfully. Check the [Actions page](https://github.com/Kesitinh13524/AdHost-TDB/actions) for update status.

## False positives

If a wanted site or app stops working, identify the blocked domain in NextDNS logs and add that exact domain to `allowlist.txt`, then run the workflow again. Keep allowlist entries specific rather than allowlisting an entire large provider domain.

## Upstream licenses

This repository aggregates third-party feeds. Refer to each source's repository and license for its redistribution terms. See [LICENSE-NOTICE.md](LICENSE-NOTICE.md).


## User-selected snapshot list

[hosts-selected-sources.txt](https://raw.githubusercontent.com/Kesitinh13524/AdHost-TDB/main/hosts-selected-sources.txt) is a static, sorted plain-domain export from the seven filter archives supplied for this snapshot. It contains 283,247 unique hostnames from 536,386 source entries.

| Source | Host entries | Archive metadata updated (UTC) |
| --- | ---: | --- |
| StevenBlack hosts | 71,476 | 2026-10-19 04:43:12 |
| HaGeZi Pro | 202,297 | 2026-10-19 05:18:04 |
| HaGeZi Multi | 166,141 | 2026-10-19 05:17:45 |
| EasyList | 41,832 | 2026-10-26 07:45:41 |
| AdGuard Android filter 11 optimized | 930 | 2026-10-26 09:33:40 |
| AdGuard uBlock filter 11 | 929 | 2026-10-26 09:50:59 |
| AdGuard uBlock filter 2 | 52,781 | 2026-10-26 09:53:25 |

The export contains hostname entries decoded from each archive's domain trie, one lowercase hostname per line. See [LICENSE-NOTICE.md](LICENSE-NOTICE.md) for upstream attribution and license information.
