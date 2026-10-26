# Upstream source notices

AdHost-TDB aggregates third-party blocklists. Sources used by the daily `hosts.txt` generator include:

- HaGeZi DNS blocklists: https://github.com/hagezi/dns-blocklists
- StevenBlack/hosts: https://github.com/StevenBlack/hosts
- AdAway: https://adaway.org/hosts.txt

## Sources for hosts-selected-sources.txt

This file is a point-in-time hostname export from the seven filter archives supplied for this snapshot:

- StevenBlack hosts: https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
- HaGeZi Pro: https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt
- HaGeZi Multi: https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/multi.txt
- EasyList: https://easylist.to/easylist/easylist.txt
- AdGuard Android filter 11 optimized: https://filters.adtidy.org/android/filters/11_optimized.txt
- AdGuard uBlock filter 11: https://filters.adtidy.org/extension/ublock/filters/11.txt
- AdGuard uBlock filter 2: https://filters.adtidy.org/extension/ublock/filters/2.txt

The upstream lists retain their own licenses and attribution terms. HaGeZi publishes its lists under GNU GPL version 3 and requires a copy of that license to accompany redistribution; this repository includes [LICENSE-GPL-3.0.txt](LICENSE-GPL-3.0.txt). EasyList is dual licensed under GPL version 3 or later and CC BY-SA 3.0 or later. AdGuard filters are GPL-3.0-only. StevenBlack/hosts is MIT licensed. Please consult each upstream source for its current terms.

This list is provided without warranty and may contain false positives.
