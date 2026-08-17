from flask import Flask, request
from core.logic import command_handler
from utils.Set_Webhook import set_webh
from database.db import SessionLocal
from config import Webhook_URL , DEBUG , APP_PORT , MAIN_ROUTE , TEST_ROUTE , HOST

app = Flask(__name__)

set_webh(Webhook_URL)

@app.route(MAIN_ROUTE, methods=["POST"])
def webhook():
    """this function Handle Bale webhook requests."""
    update = request.get_json(silent=True) or {}

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

    
    with SessionLocal() as session :
        try:
            command_handler(
            session=session,
            text=text,
            bale_user_id=bale_user_id,
            first_name=first_name,
            update_id=update["update_id"],
        )
            session.commit()
        except Exception :
            session.rollback()
            raise
    return "OK", 200

@app.route(TEST_ROUTE)
def test_webhook(name: str):
    """Test route."""
    return f"Hello {name}, webhook is OK!"


if __name__ == "__main__":
   app.run(host=HOST, port=APP_PORT, debug=DEBUG)
