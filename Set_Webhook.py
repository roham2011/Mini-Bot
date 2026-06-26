import requests

TOKEN = "1744473316:w5VeFENuKnbmKtWhmDfB0St5gOfcp3Y6_9g"
URL = f"https://tapi.bale.ai/bot{TOKEN}/setWebhook"


def set_webh(webhook):
    return requests.post(URL, data={"url": webhook})
