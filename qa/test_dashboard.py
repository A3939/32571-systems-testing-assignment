"""Offline checks: python -m unittest discover -s qa."""
import os
import unittest
from unittest.mock import patch
from reporting.dashboard import render, explanation


def row(status="Failed", alert=""):
    return dict(status=status, alert=alert, notes=["<script>unsafe</script>"],
                title="Example", expected="Expected behaviour", group="Login",
                case="T002", nodeid="tests/example.py::test_example", duration=1.2)


class DashboardTests(unittest.TestCase):
    def test_counts_and_escaping(self):
        page = render([row("Passed"), row("Failed"), row("Skipped")], "Offline test")
        for status in ("passed", "failed", "skipped"):
            self.assertIn(f'<strong class="{status}">1</strong>', page)
        self.assertNotIn("<script>unsafe</script>", page)
        self.assertIn("&lt;script&gt;unsafe&lt;/script&gt;", page)

    def test_lockout_is_review_hint_not_a_pass(self):
        item = row(alert="Your account has exceeded allowed number of login attempts.")
        self.assertIn("blocked", explanation(item)[0])
        self.assertEqual(item["status"], "Failed")

    def test_configured_credentials_are_redacted(self):
        with patch.dict(os.environ, {"TEST_PASSWORD": "secret-for-unit-test"}):
            item = row()
            item["notes"] = ["secret-for-unit-test"]
            page = render([item], "Offline test")
            self.assertNotIn("secret-for-unit-test", page)
            self.assertIn("[redacted]", page)

    def test_empty_run_is_not_a_success_claim(self):
        page = render([], "No tests selected")
        self.assertIn("0 selected scenarios", page)
        self.assertIn('<strong class="passed">0</strong>', page)
