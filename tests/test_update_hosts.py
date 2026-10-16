import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import update_hosts


class ParserTests(unittest.TestCase):
    def test_hosts_format_becomes_bare_domains(self):
        text = "0.0.0.0 ads.example.com tracker.example.net\n127.0.0.1 one.example.org\n"
        self.assertEqual(
            update_hosts.parse_domains(text),
            {"ads.example.com", "tracker.example.net", "one.example.org"},
        )

    def test_nextdns_plain_domain_format(self):
        self.assertEqual(
            update_hosts.parse_domains("ads.example.com\ntracker.example.net\n"),
            {"ads.example.com", "tracker.example.net"},
        )

    def test_comments_duplicates_and_case(self):
        text = "# comment\nADS.EXAMPLE.COM\nads.example.com.\n"
        self.assertEqual(update_hosts.parse_domains(text), {"ads.example.com"})

    def test_allowlist_and_invalid_lines(self):
        allow = {"safe.example.com"}
        text = "safe.example.com\ninvalid domain line\n-bad.example\nvalid.example.net\n"
        self.assertEqual(update_hosts.parse_domains(text, allow), {"valid.example.net"})

    def test_adblock_domain_rules_and_exceptions(self):
        text = "||ads.example.com^\n||tracker.example.net^$important\n@@||safe.example.org^\n"
        self.assertEqual(
            update_hosts.parse_domains(text),
            {"ads.example.com", "tracker.example.net"},
        )

    def test_idn_normalization(self):
        self.assertEqual(update_hosts.normalize_domain("bücher.example"), "xn--bcher-kva.example")


if __name__ == "__main__":
    unittest.main()
