import requests
from flask import Flask, request

token = "1744473316:w5VeFENuKnbmKtWhmDfB0St5gOfcp3Y6_9g"
url = f"https://tapi.bale.ai/bot{token}/setWebhook"
# define your local host as url
webhook = ""


def set_webhook(url_token, webhook):
    """
    this function set new webhook for your bot
    """
    requests.post(url_token, data={"url": webhook})


bot_app = Flask(__name__)


@bot_app.route("/")
def main():
    return "OK"


@bot_app.route("/webhook", methods=["POST"])
def webhook():

    data = requests.json
    print(data)

    return "OK"


if __name__ == "__main__":
    bot_app.run(host=5000, debug=True)
