from flask import Flask, request

from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL

app = Flask(__name__)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)


@app.route("/webhook", methods=["POST"])
def index():
    req = request.get_json()
    if "message" in req:
        bot = TelegramBot()
        response = bot.prepare_response(req)
        bot.send_message(response)
    else:
        response = {}
    return response


if __name__ == "__main__":
    app.run(port=8080)
