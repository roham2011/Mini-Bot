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
├── Main_Bot.py          # Flask + Webhook
├── Set_Webhook.py       # Set Webhook
├── requirements.txt
├── README.md            # About project
├── .gitignore
│
├── Pata_Base/
│   ├── __init__.py
│   ├── database.py      # SQLite functions
│   └── RAG.db
```   
## Run
After Clone Repo :
bash >> python3 Main_Bot.py

## Author
"Roham"
