import os
import pickle


COIN_SYMBOL = os.environ["COIN_SYMBOL"]
COIN_NAME = os.environ["COIN_NAME"]
AIRDROP_AMOUNT = os.environ["AIRDROP_AMOUNT"]
AIRDROP_AMOUNT = "{:,.2f}".format(float(AIRDROP_AMOUNT))
AIRDROP_DATE = os.environ["AIRDROP_DATE"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
AIRDROP_NETWORK = os.environ["AIRDROP_NETWORK"]
REFERRAL_REWARD = float(os.environ["REFERRAL_REWARD"])
COIN_PRICE = os.environ["COIN_PRICE"]
WEBSITE_URL = os.environ["WEBSITE_URL"]
MONGO_USER = os.environ["MONGO_INITDB_ROOT_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
MONGO_IP = os.environ["MONGO_INITDB_IP"]
MONGO_PORT = os.environ["MONGO_INITDB_PORT"]
EXPLORER_URL = os.environ["EXPLORER_URL"]
ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]

TWITTER_LINKS = os.environ["TWITTER_LINKS"]
TIKTOK_LINKS = os.environ["TIKTOK_LINKS"]
TELEGRAM_LINKS = os.environ["TELEGRAM_LINKS"]
MAX_USERS = int(os.environ["MAX_USERS"])
MAX_REFS = int(os.environ["MAX_REFS"])
CAPTCHA_ENABLED = os.environ["CAPTCHA_ENABLED"]

TWITTER_LINKS = [link.strip() for link in TWITTER_LINKS.split(",") if link.strip()]
if not TWITTER_LINKS:
    raise ValueError("TWITTER_LINKS must contain at least one X profile URL")
TIKTOK_LINKS = [link.strip() for link in TIKTOK_LINKS.split(",") if link.strip()]
if not TIKTOK_LINKS:
    raise ValueError("TIKTOK_LINKS must contain at least one TikTok profile URL")
TELEGRAM_LINKS = TELEGRAM_LINKS.split(",")
TWITTER_LINKS = "\n".join(TWITTER_LINKS)
TIKTOK_LINKS = "\n".join(TIKTOK_LINKS)
TELEGRAM_LINKS = "\n".join(TELEGRAM_LINKS)
STATUS_PATH = "./conversationbot/botconfig.p"
