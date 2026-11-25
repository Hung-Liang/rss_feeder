import time
import traceback

import rss_feeder
from config import configs


if __name__ == "__main__":
    while True:
        for config in configs:
            # One broken feed must not stop the others; the traceback goes to docker logs
            try:
                rss_feeder.rss_feeder(
                    config["web_hook"], config["rss_url"], config["history_file"]
                )
            except Exception:
                traceback.print_exc()
        time.sleep(3600)
