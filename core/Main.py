from flask import Flask, request
from .logic import handle_messages
from utils.Set_Webhook import set_webh
from database.db import SessionLocal
from config import Webhook_URL , DEBUG , PORT

app = Flask(__name__)

set_webh(Webhook_URL)

@app.route("/webhook", methods=["POST"])
def webhook():
    """this function Handle Bale webhook requests."""
    update = request.get_json(silent=True) or {}

    print("New Data:", update)

    text = None
    bale_user_id = None
    first_name = None

    if "message" in update:
        text = update["message"].get("text")
        bale_user_id = update["message"]["from"]["id"]
        first_name = update["message"]["from"].get("first_name")
    
    if "callback_query" in update:
        text = update["callback_query"].get("data")
        bale_user_id = update["callback_query"]["from"]["id"]
        first_name = update["callback_query"]["from"].get("first_name")

    if text is None or bale_user_id is None:
        return "ok"

    print("User:", bale_user_id)
    print("Text:", text)
    
    with SessionLocal() as session :
        try:
            handle_messages(
            session=session,
            command=text,
            bale_user_id=bale_user_id,
            first_name=first_name,
        )
            
        except Exception :
            session.rollback()
            raise
    return "OK", 200

@app.route("/test/<name>")
def test_webhook(name: str):
    """Test route."""
    return f"Hello {name}, webhook is OK!"


if __name__ == "__main__":
   app.run(host="127.0.0.1", port=PORT, debug=DEBUG)
