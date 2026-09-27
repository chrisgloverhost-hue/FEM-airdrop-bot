from utils.env import *


if COIN_PRICE == "0":
    SYMBOL = ""
else:
    SYMBOL = f"\n⭐️ 1 {COIN_SYMBOL} = {COIN_PRICE}"
if EXPLORER_URL != "":
    EXPLORER_URL = f"\nContract: {EXPLORER_URL}"
if WEBSITE_URL != "":
    WEBSITE_URL = f"\nWebsite: {WEBSITE_URL}"
WELCOME_MESSAGE = f"""
Hello, NAME! I am your friendly {COIN_NAME} Airdrop bot
{SYMBOL}
🔸For Joining - Get {AIRDROP_AMOUNT} {COIN_SYMBOL}
⭐️ For each referral - Get {"{:,.2f}".format(REFERRAL_REWARD)} {COIN_SYMBOL}

📘By Participating you are agreeing to the {COIN_NAME} (Airdrop) Program Terms and Conditions. Please see pinned post for more information.
Click "🚀 Join Airdrop" to proceed"""
tasks = ""

PROCEED_MESSAGE = f"""
🔹 Airdrop Reward = *{AIRDROP_AMOUNT} {COIN_SYMBOL}*
🔹 Extra reward per referral = *{"{:,.2f}".format(REFERRAL_REWARD)} {COIN_SYMBOL}* (max {MAX_REFS}){SYMBOL}

📢 Airdrop Rules

✏️ Mandatory Tasks:
- Join our telegram channels
- Follow our X (Twitter) page
- Follow our TikTok page

NOTE: Users found Cheating would be disqualified & banned immediately.

Airdrop Date: *{AIRDROP_DATE}*{EXPLORER_URL}
{WEBSITE_URL}
"""

MAKE_SURE_TELEGRAM = f"""
Do no forget to join our Telegram channel
{TELEGRAM_LINKS}
"""

FOLLOW_TWITTER_TEXT = f"""
🔹 Follow our X (Twitter) page
{TWITTER_LINKS}

Type in *your X username* to proceed
"""

SUBMIT_TIKTOK_TEXT = f"""
🔹 Follow our TikTok page
{TIKTOK_LINKS}

Type in *your TikTok username* to proceed
"""


SUBMIT_BEP20_TEXT = f"""
Type in *your Wallet Address*

Please make sure your wallet supports the *{AIRDROP_NETWORK}*
"""

JOINED = f"""
Thank you!
Rewards would be sent out automatically to your {AIRDROP_NETWORK} address on the {AIRDROP_DATE}

Don't forget to:
🔸 Stay in the telegram channels
🔸 Follow all the social media channels for the updates

Your personal referral link (+{"{:,.2f}".format(REFERRAL_REWARD)} {COIN_SYMBOL} for each referral)
REPLACEME
"""

WITHDRAWAL_TEXT = f"""
Withdrawals would be sent out automatically to your {AIRDROP_NETWORK} address on the {AIRDROP_DATE}
NOTE: Users found Cheating would be disqualified & banned immediately."""

BALANCE_TEXT = f"""
{COIN_NAME} Airdrop Balance: *IARTBALANCE*
Referral Balance: *REFERRALBALANCE*
"""
