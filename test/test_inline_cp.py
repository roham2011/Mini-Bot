from utils.send_message import post_message

CHAT_ID = 812398278

form = (
    "چه زمانی؟\n"
    "چی اتفاقی افتاد؟\n"
    "چه چیزی باعثش شد؟\n"
    "نتیجه چه بود؟"
)

payload = {
    "chat_id": CHAT_ID,
    "text": "فرم توضیحات گزارش:\n\n" + form,
    "reply_markup": {
        "inline_keyboard": [
            [
                {
                    "text": "📋 کپی فرم",
                    "copy_text": {
                        "text": form
                    }
                }
            ]
        ]
    }
}

response = post_message(payload)

print(response.status_code)
print(response.text)