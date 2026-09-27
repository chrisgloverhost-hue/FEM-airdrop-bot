import os
import pickle


COIN_SYMBOL = os.environ["COIN_SYMBOL"]
COIN_NAME = os.environ["COIN_NAME"]
FEM_REWARD_AMOUNT = os.environ.get("FEM_REWARD_AMOUNT", "40")
AIRDROP_AMOUNT = "{:,.2f}".format(float(FEM_REWARD_AMOUNT))
AIRDROP_DATE = os.environ["AIRDROP_DATE"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
AIRDROP_NETWORK = os.environ["AIRDROP_NETWORK"]
REFERRAL_REWARD = float(os.environ["REFERRAL_REWARD"])
COIN_PRICE = os.environ["COIN_PRICE"]
WEBSITE_URL = os.environ["WEBSITE_URL"]
MONGO_URI = os.environ.get("MONGO_URI", "")
MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "")
MONGO_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "")
MONGO_IP = os.environ.get("MONGO_INITDB_IP", "")
MONGO_PORT = os.environ.get("MONGO_INITDB_PORT", "27017")
EXPLORER_URL = os.environ["EXPLORER_URL"]
ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]

TWITTER_LINKS = os.environ["TWITTER_LINKS"]
TIKTOK_LINKS = os.environ["TIKTOK_LINKS"]
TELEGRAM_LINKS = os.environ["TELEGRAM_LINKS"]
TELEGRAM_CHAT_IDS = [
    chat_id.strip()
    for chat_id in os.environ.get("TELEGRAM_CHAT_IDS", "").split(",")
    if chat_id.strip()
]
FEM_APP_LINK = os.environ.get("FEM_APP_LINK", "")
TIKTOK_VIDEO_LINKS = os.environ.get("TIKTOK_VIDEO_LINKS", "")
FEM_DECIMALS = int(os.environ.get("FEM_DECIMALS", "18"))
FEM_RPC_URL = os.environ.get("FEM_RPC_URL", "")
FEM_CHAIN_ID = int(os.environ.get("FEM_CHAIN_ID") or "0")
FEM_PAYOUT_PRIVATE_KEY = os.environ.get("FEM_PAYOUT_PRIVATE_KEY", "")
FEM_PAYOUT_ENABLED = os.environ.get("FEM_PAYOUT_ENABLED", "NO")
FEM_ANNOUNCEMENT_CHAT_ID = os.environ.get("FEM_ANNOUNCEMENT_CHAT_ID", "")
FEM_ANNOUNCEMENT_PRIVACY = os.environ.get("FEM_ANNOUNCEMENT_PRIVACY", "user").lower()
FEM_TX_EXPLORER_URL = os.environ.get("FEM_TX_EXPLORER_URL", "")
MAX_USERS = int(os.environ["MAX_USERS"])
MAX_REFS = int(os.environ["MAX_REFS"])
CAPTCHA_ENABLED = os.environ["CAPTCHA_ENABLED"]

if FEM_ANNOUNCEMENT_PRIVACY not in {"user", "minimal", "full"}:
    raise ValueError("FEM_ANNOUNCEMENT_PRIVACY must be user, minimal, or full")

TWITTER_LINKS = [link.strip() for link in TWITTER_LINKS.split(",") if link.strip()]
if not TWITTER_LINKS:
    raise ValueError("TWITTER_LINKS must contain at least one X profile URL")
TIKTOK_LINKS = [link.strip() for link in TIKTOK_LINKS.split(",") if link.strip()]
if not TIKTOK_LINKS:
    raise ValueError("TIKTOK_LINKS must contain at least one TikTok profile URL")
TIKTOK_VIDEO_LINKS = [
    link.strip()
    for link in TIKTOK_VIDEO_LINKS.split(",")
    if link.strip()
]
if not TIKTOK_VIDEO_LINKS:
    raise ValueError("TIKTOK_VIDEO_LINKS must contain at least one TikTok video URL")
if not FEM_APP_LINK:
    raise ValueError("FEM_APP_LINK must contain the official FEM app download URL")
TELEGRAM_LINKS = TELEGRAM_LINKS.split(",")
TWITTER_LINKS = "\n".join(TWITTER_LINKS)
TIKTOK_LINKS = "\n".join(TIKTOK_LINKS)
TIKTOK_VIDEO_LINKS = "\n".join(TIKTOK_VIDEO_LINKS)
TELEGRAM_LINKS = "\n".join(TELEGRAM_LINKS)
STATUS_PATH = "./conversationbot/botconfig.p"
