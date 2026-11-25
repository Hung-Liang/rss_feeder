import json
import os
import tempfile
import unittest
from unittest import mock

import feedparser

import rss_feeder


def make_entries(ids):
    # fetch_rss returns newest first, like a real feed
    return [
        feedparser.FeedParserDict(guid=i, link=f"https://example.com/{i}", title=i)
        for i in reversed(ids)
    ]


class RssFeederDedupeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.history = os.path.join(self.tmp.name, "history.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_feeder(self, ids, send_result=True):
        with mock.patch.object(rss_feeder, "fetch_rss", return_value=make_entries(ids)), \
                mock.patch.object(rss_feeder, "send_to_discord", return_value=send_result) as send:
            rss_feeder.rss_feeder("webhook", "rss", self.history)
        return [call.args[0].guid for call in send.call_args_list]

    def test_each_id_sent_once_and_history_bounded(self):
        sent = []
        for run in range(15):
            ids = [f"id-{run}-{i}" for i in range(10)]
            sent += self.run_feeder(ids)
            # the same feed again must not resend anything
            self.assertEqual(self.run_feeder(ids), [])
            with open(self.history) as f:
                self.assertLessEqual(len(json.load(f)), 10)
        self.assertEqual(len(sent), 150)
        self.assertEqual(len(set(sent)), 150)

    def test_failed_send_is_retried_next_run(self):
        ids = ["a", "b"]
        self.assertEqual(self.run_feeder(ids, send_result=False), ["a", "b"])
        self.assertEqual(self.run_feeder(ids), ["a", "b"])
        self.assertEqual(self.run_feeder(ids), [])

    def test_empty_fetch_keeps_history(self):
        self.run_feeder(["a"])
        with open(self.history) as f:
            before = f.read()
        self.assertEqual(self.run_feeder([]), [])
        with open(self.history) as f:
            self.assertEqual(f.read(), before)


class SendToDiscordTest(unittest.TestCase):
    entry = feedparser.FeedParserDict(title="t", link="https://example.com/t")

    @mock.patch.object(rss_feeder.time, "sleep")
    @mock.patch.object(rss_feeder.requests, "post")
    def test_retries_on_exception_then_fails(self, post, sleep):
        post.side_effect = rss_feeder.requests.ConnectionError()
        self.assertFalse(rss_feeder.send_to_discord(self.entry, "webhook"))
        self.assertEqual(post.call_count, 6)
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [1, 2, 4, 8, 16])
        self.assertEqual(post.call_args.kwargs["timeout"], 10)

    @mock.patch.object(rss_feeder.time, "sleep")
    @mock.patch.object(rss_feeder.requests, "post")
    def test_success_after_retry(self, post, sleep):
        post.side_effect = [mock.Mock(status_code=429), mock.Mock(status_code=204)]
        self.assertTrue(rss_feeder.send_to_discord(self.entry, "webhook"))


if __name__ == "__main__":
    unittest.main()
