# AdHost-TDB

One logical, deduplicated domain denylist for **Adblocker app** and compatible DNS blockers. When needed, GitHub stores it as several smaller, non-overlapping files.

## Output format

`hosts.txt` is the first shard of a **plain domain list**: one lowercase domain per line, with no IP address prefix. The generator converts standard hosts-file lines, plain domain feeds, and simple Adblock domain rules; validates hostnames; removes duplicates; and applies `allowlist.txt`. If the combined output grows beyond the safe GitHub file size, it creates `hosts-part-02.txt` and later parts. Import every generated shard; no hostname is repeated between files.

Example:

```text
ad.doubleclick.net
doubleclick.net
tracker.example.net
```

Raw URLs (import both; the shards contain no duplicate domains):
- [hosts.txt](https://raw.githubusercontent.com/Kesitinh13524/AdHost-TDB/main/hosts.txt)
- [hosts-part-02.txt](https://raw.githubusercontent.com/Kesitinh13524/AdHost-TDB/main/hosts-part-02.txt)

## Aggregated sources

The daily generator merges these 70 upstream feeds where available:

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
- BlocklistProject Lists: all 25 published host lists (Abuse, Adobe, Ads, Basic, Crypto, Drugs, Facebook, Fortnite, Fraud, Gambling, Malware, Phishing, Piracy, Porn, Ransomware, Redirect, Scam, Smart TV, TikTok, Torrent, Tracking, Twitter, Vaping, WhatsApp, and YouTube), plus Porn Alpha
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
- HaGeZi TIF threat-intelligence domains

These lists overlap by design; the generator stores each valid domain only once across all output parts. Sources may change, become unavailable, or contain false positives. Some upstream lists include malware, phishing, telemetry, and tracking domains. The complete BlocklistProject set also includes social-media and content categories such as adult content, drugs, gambling, and piracy, so importing every part may block those services as well.

## weekly updates


The workflow runs parser tests, downloads the feeds, validates the aggregate, and commits all generated host-list parts only if the aggregate passes the minimum-size safety check. If every source fails or the result is unexpectedly small, the previous list is preserved.

**Current aggregate:** The generated `hosts*.txt` files together form one deduplicated set. Import every part listed in the repository; the latest successful workflow reports the host count and source health. Check the [Actions page](https://github.com/Kesitinh13524/AdHost-TDB/actions) for update status.

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
