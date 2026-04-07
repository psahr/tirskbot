FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

RUN pip install --no-cache-dir -r requirements.txt

ENV TELEGRAM_BOT_TOKEN=""

CMD ["python", "bot.py"]
