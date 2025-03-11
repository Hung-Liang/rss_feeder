# RSS Feeder

## 描述

這是一個簡單的 RSS 訂閱工具，可從來源擷取最新新聞，並將其發送到 Discord Webhook。

## 安裝

1. 克隆此存儲庫  
2. 新增 `config.py` 檔案，內容如下：

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

3. `configs` 陣列可擴充，以新增更多來源  
4. `web_hook` 是 Discord Webhook 的 URL  
5. `rss_url` 是 RSS 訂閱源的 URL  
6. `history_file` 是儲存新聞歷史記錄的檔案  
7. 需要安裝 Docker  

## 使用方式

```sh
chmod +x build_and_run.sh
./build_and_run.sh
```

## 支持我

<a href="https://www.buymeacoffee.com/hungliang" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
