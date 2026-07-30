from pathlib import Path

# token of bale bot
TOKEN = "1744473316:V8sHnllCPQBKHRSHDMCi6IDvRmrKIOSQqas"

# bale API
URL = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

# import URL from tunneled Host
Global_URL = Path("tunnel_url.txt").read_text().strip()

# set route for set webhook
Webhook_URL = f"{Global_URL}/webhook"

# Data base URL
DATABASE_URL = "sqlite:///RAG.db"
