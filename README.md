# Introduction_MINI_PROJECT
Build and development telegram/bale(ir-messenger) bot .

## Requirments
Python 3.11+
...

** for more , read requirments.txt **

## Features
- Set WebHook in Bale or Telegram
- the Prog Send Welcome , Apout and Status Messege
- Prog Connect User Questions to LLM AI and Receive Response From LLM
- save data from users and use in next response (Same as RAG)
- SQLite database support

## Project Structure
```text
MINI-PROJS_Private/
│
├── Main_Bot.py              # Flask + Webhook
├── Set_Webhook.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── db.py                # Connect to DB
│   ├── models.py            # Class tables
│   ├── crud.py              # DB statment
│   └── RAG.db
│
├── handlers/
│   ├── __init__.py
│   ├── report.py
│   └── chat.py
│
└── utils/
    ├── __init__.py
    └── send_message.py
```   
## Run
After Clone Repo :
bash >> python3 Main_Bot.py

## Author
"Roham"
