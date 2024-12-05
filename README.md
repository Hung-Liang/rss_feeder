# RSS Feeder

## Description

This is a simple RSS feeder that fetches the latest news from the source and send requests to Discord webhook.

## Installation

- Clone the repository
- add `config.py` file with the following content:

```python
configs = [
    {
        "web_hook": "",
        "rss_url": "",
        "history_file": "",
    },
    {
        "web_hook": "",
        "rss_url": "",
        "history_file": "",
    },
]

```

- the configs list can be extended to add more sources
- `web_hook` is the discord webhook url
- `rss_url` is the rss feed url
- `history_file` is the file that stores the history of the news
- require docker installed on your machine

## Usage

- chmod +x build_and_run.sh
- ./build_and_run.sh
  
## Support me

<a href="https://www.buymeacoffee.com/hungliang" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
