import requests
from config import URL


def post_message(payload):

    print("Sending payload:")
    print(payload)

    response = requests.post(
        URL,
        json=payload
    )

    print("Bale Status Code:", response.status_code)
    print("Bale Response:")
    print(response.text)

    return response 

def send_message(chat_id: int, text: str):
    """this function sends message to user."""
    print("send_start_menu called:", chat_id)

    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    post_message(payload)

