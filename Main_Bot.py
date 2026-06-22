import requests
from flask import Flask


def set_webhook(url_token, webhook):
    """
    this function set new webhook for your bot
    """
    requests.post(url_token, data={"url": webhook})
