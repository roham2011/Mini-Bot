from pathlib import Path

# token of bale bot
TOKEN = "1744473316:V8sHnllCPQBKHRSHDMCi6IDvRmrKIOSQqas"

# bale API
URL = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

# ip port in flask 
APP_PORT = 5026

# Main Flask addres
MAIN_ROUTE = "/webhook"

# addres test 
TEST_ROUTE = "/test/<name>"

# addres host
HOST = "127.0.0.1"

# import URL from tunneled Host
TUNNEL_URL_FILE = Path("runtime/tunnel_url.txt")

if TUNNEL_URL_FILE.exists():
    Global_URL = TUNNEL_URL_FILE.read_text().strip()
else:
    Global_URL = ""


# set route for set webhook
Webhook_URL = f"{Global_URL}{MAIN_ROUTE}"

# Data base URL
DATABASE_URL = "sqlite:///database/RAG.db"

# state of debug mode in falsk
DEBUG = True

