FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends tmux\
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py config.py rss_feeder.py ./
# COPY /configs /app/configs


CMD ["python", "main.py"]

