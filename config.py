from pathlib import Path

# token of bale bot
TOKEN = "1744473316:V8sHnllCPQBKHRSHDMCi6IDvRmrKIOSQqas"

# bale API
URL = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

# ip port in flask 
PORT = 5010

# Main Flask addres
MAIN_ROUTE = "/webhook"

# addres test 
TEST_ROUTE = "/test/<name>"

# addres host
HOST = "127.0.0.1"

# import URL from tunneled Host
Global_URL = Path("runtime/tunnel_url.txt").read_text().strip()

# set route for set webhook
Webhook_URL = f"{Global_URL}{MAIN_ROUTE}"

# Data base URL
DATABASE_URL = "sqlite:///database/RAG.db"

# state of debug mode in falsk
DEBUG = True

