import json
import sys

import os
import feedparser
import pytz
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


def load_processed(history_file):
    """Load the processed entries from the history file.

    Args:
        history_file (str): The path to the history file.

    Returns:
        set: The set of processed entry IDs.
    """
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return set(json.load(f))
    return set()


def save_processed(processed, history_file):
    """Save the processed entries to the history file.

    Args:
        processed (set): The set of processed entry IDs.
        history_file (str): The path to the history file.
    """
    with open(history_file, "w") as f:
        json.dump(list(processed), f)


def remove_old_processed(processed):
    """Remove old entries from the processed set.

    Args:
        processed (set): The set of processed entry IDs.

    Returns:
        set: The updated set of processed entry IDs.
    """
    if len(processed) > 100:
        processed = processed[-50:]
    return processed


def fetch_rss(rss_url):
    """Fetch the RSS feed and return the entries.

    Args:
        rss_url (str): The URL of the RSS feed.

    Returns:
        list: The list of entries in the RSS feed.
    """
    return feedparser.parse(rss_url).entries


def keep_recent_entries(entries, n=10):
    """Keep only the most recent entries.

    Args:
        entries (list): The list of entries.
        n (int): The number of entries to keep.

    Returns:
        list: The most recent entries.
    """
    results = entries[:n] if len(entries) > n else entries
    return list(reversed(results))


def send_to_discord(entry, webhook_url, retries=0):
    """Send the entry to Discord using a webhook.

    Args:
        entry (dict): The entry to send.
        webhook_url (str): The URL of the Discord webhook.
        retries (int): The number of retries.
    """
    data = {
        "content": f"[{entry.title}]({entry.link})",
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Posted to Discord successfully.")
    else:
        print(f"Failed to post to Discord: {response.status_code}")
        if retries < 5:
            print("Retrying...")
            send_to_discord(entry, webhook_url, retries + 1)


def rss_feeder(webhook_url, rss_url, history_file):
    """Fetch the RSS feed and send new entries to Discord.

    Args:
        webhook_url (str): The URL of the Discord webhook.
        rss_url (str): The URL of the RSS feed.
        history_file (str): The path to the history file.
    """
    processed = load_processed(history_file)
    new_processed = set()
    entries = fetch_rss(rss_url)
    entries = keep_recent_entries(entries, 10)

    for entry in entries:
        entry_id = entry.get("guid", entry.link)
        if entry_id not in processed:
            send_to_discord(entry, webhook_url)
            new_processed.add(entry_id)

    processed.update(new_processed)
    processed = remove_old_processed(processed)
    save_processed(processed, history_file)


if __name__ == "__main__":
    webhook_url = sys.argv[1]
    rss_url = sys.argv[2]
    history_file = sys.argv[3]
    timezone = pytz.timezone('Asia/Taipei')

    scheduler = BlockingScheduler(timezone=timezone)
    scheduler.add_job(
        rss_feeder, "cron", args=[webhook_url, rss_url, history_file], minute=0
    )
    # run every 3 minutes for testing
    # scheduler.add_job(
    #     rss_feeder,
    #     "cron",
    #     args=[webhook_url, rss_url, history_file],
    #     minute="*/3",
    # )
    scheduler.start()
