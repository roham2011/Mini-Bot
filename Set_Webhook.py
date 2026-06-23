import requests

token = "1744473316:w5VeFENuKnbmKtWhmDfB0St5gOfcp3Y6_9g"
url = f"https://tapi.bale.ai/bot{token}/setWebhook"
# define your local host as url
webhook = "https://earliest-entities-arrived-sandwich.trycloudflare.com"


requests.post(url, data={"url": webhook})
