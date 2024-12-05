import hashlib
import subprocess
import time

from config import configs


def generate_session_name(rss_url, webhook_url):
    """Generate a unique session name based on the RSS URL.

    Args:
        rss_url (str): The URL of the RSS feed.
        webhook_url (str): The URL of the Discord webhook.

    Returns:
        str: The generated session name
    """
    hashed = (
        hashlib.md5(rss_url.encode()).hexdigest()[:8]
        + hashlib.md5(webhook_url.encode()).hexdigest()[:8]
    )

    return f"rss_feeder_{hashed}"


def start_tmux_session(rss_url, webhook_url, history_file):
    """Start a tmux session with the RSS feeder.

    Args:
        rss_url (str): The URL of the RSS feed.
        webhook_url (str): The URL of the Discord webhook.
        history_file (str): The path to the history file.
    """
    session_name = generate_session_name(rss_url, webhook_url)

    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0:
        print(f"Session {session_name} already exists. Skipping...")
        return

    log_file = f"/var/log/{session_name}.log"
    subprocess.Popen(
        [
            "tmux",
            "new",
            "-d",
            "-s",
            session_name,
            "bash",
            "-c",
            (
                "python rss_feeder.py"
                f" {webhook_url} {rss_url} {history_file} > {log_file} 2>&1"
            ),
        ]
    )
    print(f"Started tmux session {session_name} with log: {log_file}")


if __name__ == "__main__":
    while True:
        for config in configs:
            webhook_url = config["web_hook"]
            rss_url = config["rss_url"]
            history_file = config["history_file"]

            start_tmux_session(rss_url, webhook_url, history_file)
        time.sleep(3600)
