import requests

TOKEN = "1744473316:V8sHnllCPQBKHRSHDMCi6IDvRmrKIOSQqas"
URL = f"https://tapi.bale.ai/bot{TOKEN}/setWebhook"


def set_webh(webhook):
    return requests.post(URL, data={"url": webhook})
