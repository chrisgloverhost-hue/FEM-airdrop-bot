import logging
import threading
from datetime import datetime

import telegram
from pymongo import ReturnDocument
from web3 import Web3


from telegram import (
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ConversationHandler,
    Filters,
    MessageHandler,
)
from utils.bot_status import get_bot_status, set_bot_status
from utils.keyboard import create_markup, get_reply_keyboard_markup
from utils.message_strings import *
from utils.jokes import getJoke
from utils.states import *
from utils import mongo
from utils.payout import broadcast_payout, prepare_payout

from multicolorcaptcha import CaptchaGenerator
from bson.json_util import dumps
from utils.tempdata import (
    getCaptchaData,
    getUserInfo,
    updateCaptchaData,
    updateUserInfo,
)

PAYOUT_LOCK = threading.Lock()
logger = logging.getLogger(__name__)


def submit_details(update, context):
    if not FEM_APP_LINK:
        update.message.reply_text("The FEM app download link is not configured yet.")
        return ConversationHandler.END
    update.message.reply_text(
        text=PROCEED_MESSAGE, parse_mode=telegram.ParseMode.MARKDOWN
    )
    update.message.reply_text(
        text='Please click on "Submit Details" to proceed',
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=create_markup([["Submit Details"], ["Cancel"]]),
    )
    return FOLLOW_TELEGRAM


def follow_twitter(update, context):
    user = update.effective_user
    if getUserInfo(user.id) == False:
        return startAgain(update, context)
    updateUserInfo(user.id, "fem_app_task_claimed", True)
    updateUserInfo(user.id, "telegram_task_claimed", True)
    update.message.reply_text(
        text=FOLLOW_TWITTER_TEXT, parse_mode=telegram.ParseMode.MARKDOWN
    )
    update.message.reply_text(
        text="Type in *your X username* to proceed",
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=create_markup([["Cancel"]]),
    )
    return SUBMIT_ADDRESS


def maxNumberReached(update, context):
    update.message.reply_text(
        "Hey! Thanks for your interest, but it seems that the maximum number of users has been reached."
    )
    return ConversationHandler.END


def botStopped(update, context):
    update.message.reply_text(
        "The airdrop has been completed. Thanks for you interest."
    )
    return ConversationHandler.END


def botPaused(update, context):
    update.message.reply_text(
        "The airdrop has been temporarily paused, please try again later",
        reply_markup=ReplyKeyboardMarkup([["/start"]]),
    )
    return ConversationHandler.END


def follow_telegram(update, context):
    update.message.reply_text(
        text=MAKE_SURE_TELEGRAM, parse_mode=telegram.ParseMode.MARKDOWN
    )
    update.message.reply_text(
        text='Please click on "Done" to proceed',
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=create_markup([["Done"], ["Cancel"]]),
    )

    return FOLLOW_TWITTER


def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text("Goodbye!", reply_markup=create_markup([["/start"]]))
    return ConversationHandler.END


def startAgain(update, context) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text(
        "An error occured, please start the bot again.",
        reply_markup=create_markup([["/start"]]),
    )
    return ConversationHandler.END


cancelHandler = MessageHandler(Filters.regex("^Cancel$"), cancel)


def loopAnswer(update, context):
    user = update.message.from_user
    info = mongo.getUserInfo(user.id)
    message = update.message.text
    reply = ""
    if message == "💰 Balance":
        refbal = "{:,.2f}".format(info["refCount"] * REFERRAL_REWARD)
        if refbal == "":
            refbal = "0"
        reply = BALANCE_TEXT.replace("IARTBALANCE", AIRDROP_AMOUNT).replace(
            "REFERRALBALANCE", refbal
        )

    if message == "ℹ️ Airdrop Info":
        reply = PROCEED_MESSAGE

    if message == "💸 Withdrawal":
        reply = WITHDRAWAL_TEXT

    if message == "🔗 Ref Link":
        reply = f"""
Here is *your referral link*
[https://t.me/{context.bot.username}?start={user.id}](https://t.me/{context.bot.username}?start={user.id})
"""

    if message == "Quit Airdrop":
        update.message.reply_text(
            "Are you sure want to quit the Airdrop? All your data will be deleted",
            reply_markup=create_markup([["YES"], ["NO"]]),
        )
        return SUREWANTTO

    if message == "💾 My Data":
        name = str(info["name"])
        refbal = "{:,.2f}".format(info["refCount"] * REFERRAL_REWARD)
        balance = BALANCE_TEXT.replace("IARTBALANCE", AIRDROP_AMOUNT).replace(
            "REFERRALBALANCE", refbal
        )
        refferals = str(info["refCount"])
        bep20Address = str(info["bep20"])
        twitterUsername = str(info["twitter_username"])
        tiktokUsername = str(info.get("tiktok_username", ""))
        reply = f"""
Name: {name}
Referrals: {refferals}
{AIRDROP_NETWORK} address: {bep20Address}
X Username: {twitterUsername}
TikTok Username: {tiktokUsername}
Balance: {balance}
"""
    if reply == "":
        joke = getJoke()
        joke = joke.split("  -")
        reply = f"""
I'm not sure what you meant, but here is a joke for you!
> {joke[0]}
- {joke[1]}
"""
    update.message.reply_text(
        reply,
        reply_markup=get_reply_keyboard_markup(),
        parse_mode=telegram.ParseMode.MARKDOWN,
    )
    return LOOP


def sureWantTo(update, context):
    user = update.message.from_user
    message = update.message.text
    if message == "YES":
        update.message.reply_text("Goodbye!", reply_markup=create_markup([["/start"]]))
        mongo.users.delete_one({"userId": user.id})
        return ConversationHandler.END

    if message == "NO":
        update.message.reply_text(
            "Oh thanks god, I thought I lost you",
            reply_markup=get_reply_keyboard_markup(),
        )
        return LOOP


def getName(user):
    first = user["first_name"]
    last = user["last_name"]
    if last == None:
        last = ""
    if first == None:
        first = ""
    return str(first + " " + last).strip()


def checkCaptcha(update, context):
    user = update.message.from_user
    text = update.message.text

    if getCaptchaData(user.id) != text:
        update.message.reply_text("Invalid captcha!")
        return generateCaptcha(update, context)
    else:
        NAME = getName(user)
        update.message.reply_text(
            text="Correct!", parse_mode=telegram.ParseMode.MARKDOWN
        )
        update.message.reply_text(
            text=WELCOME_MESSAGE.replace("NAME", NAME),
            reply_markup=create_markup([["🚀 Join Airdrop"]]),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        updateCaptchaData(user.id, True)
        return PROCEED


def generateCaptcha(update, context):
    user = update.message.from_user
    CAPCTHA_SIZE_NUM = 2
    generator = CaptchaGenerator(CAPCTHA_SIZE_NUM)
    captcha = generator.gen_captcha_image(difficult_level=3)
    image = captcha["image"]
    characters = captcha["characters"]
    updateCaptchaData(user.id, characters)
    filename = f"{user.id}.png"
    image.save(filename, "png")
    photo = open(filename, "rb")
    update.message.reply_photo(photo)
    update.message.reply_text("Please type in the numbers on the image")
    return CAPTCHASTATE


def submit_address(update, context):
    user = update.message.from_user
    if getUserInfo(user.id) == False:
        return startAgain(update, context)

    updateUserInfo(user.id, "twitter_username", update.message.text.strip())
    updateUserInfo(user.id, "x_follow_task_claimed", True)
    update.message.reply_text(
        text=SUBMIT_TIKTOK_TEXT,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=create_markup([["Cancel"]]),
    )
    return SUBMIT_TIKTOK


def submit_tiktok(update, context):
    user = update.message.from_user
    if getUserInfo(user.id) == False:
        return startAgain(update, context)

    updateUserInfo(user.id, "tiktok_username", update.message.text.strip())
    updateUserInfo(user.id, "tiktok_follow_task_claimed", True)
    updateUserInfo(user.id, "tiktok_like_task_claimed", True)
    update.message.reply_text(
        text=SUBMIT_BEP20_TEXT,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=create_markup([["Cancel"]]),
    )
    return END_CONVERSATION


def start(update, context):
    user = update.message.from_user
    updateCaptchaData(user.id, False)

    refferal = update.message.text.replace("/start", "").strip()
    if refferal != "" and refferal != user.id and "ref" not in getUserInfo(user.id):
        updateUserInfo(user.id, "ref", refferal)
        print("Using refferal")
    else:
        updateUserInfo(user.id, "ref", False)

    NAME = getName(user)

    if mongo.getUserInfo(user.id) != "":
        update.message.reply_text(
            text="It seems like you have already joined!",
            reply_markup=get_reply_keyboard_markup(),
        )
        return LOOP

    count = mongo.users.count_documents({})
    if count >= MAX_USERS:
        return maxNumberReached(update, context)

    if get_bot_status() == "STOPPED":
        return botStopped(update, context)

    if get_bot_status() == "PAUSED":
        return botPaused(update, context)

    if CAPTCHA_ENABLED == "YES" and getCaptchaData(user.id) != True:
        return generateCaptcha(update, context)
    else:
        update.message.reply_text(
            text=WELCOME_MESSAGE.replace("NAME", NAME),
            reply_markup=create_markup([["🚀 Join Airdrop"]]),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
    return PROCEED


def end_conversation(update, context):
    user = update.message.from_user
    if getUserInfo(user.id) == False:
        return startAgain(update, context)

    wallet = update.message.text.strip()
    if not Web3.is_address(wallet):
        update.message.reply_text("Enter a valid FEM EVM wallet address (0x followed by 40 hex characters).")
        return END_CONVERSATION
    wallet = Web3.to_checksum_address(wallet)
    existing_wallet = mongo.users.find_one({"bep20": {"$regex": f"^{wallet}$", "$options": "i"}})
    if existing_wallet:
        update.message.reply_text("That wallet is already registered for this airdrop.")
        return END_CONVERSATION

    updateUserInfo(user.id, "bep20", wallet)
    updateUserInfo(user.id, "chatId", update.effective_chat.id)
    updateUserInfo(user.id, "userId", user.id)
    updateUserInfo(user.id, "name", getName(user))
    updateUserInfo(user.id, "username", user.username)
    updateUserInfo(user.id, "payout_status", "pending_review")
    updateUserInfo(user.id, "application_submitted_at", datetime.utcnow())
    mongo.users.insert_one(getUserInfo(user.id))
    url = f"https://t.me/{context.bot.username}?start={user.id}"

    # check refferal
    # if USERINFO[user.id]["ref"] != False:
    # refferal = USERINFO[user.id]["ref"]
    # info = getUserInfo(int(refferal))
    # print("Referall step 1")
    # print(refferal)
    # print(info)
    # if info != "":
    # if str(user.id) in info["refList"]:
    # info["refCount"] += 1
    # info["refList"].append(str(user.id))
    # users.update({"userId": refferal}, info)
    # print("Updated refferal")

    update.message.reply_text(
        JOINED.replace("REPLACEME", url),
        reply_markup=get_reply_keyboard_markup(),
    )
    return LOOP


def _is_private_admin(update):
    user = update.effective_user
    return (
        update.effective_chat.type == "private"
        and ADMIN_USERNAME
        and user
        and user.username == ADMIN_USERNAME
    )


def _admin_denied(update):
    update.effective_message.reply_text("Admin command not authorized.")


def getPendingPayouts(update, context):
    if not _is_private_admin(update):
        return _admin_denied(update)

    pending = mongo.users.find(
        {
            "$or": [
                {"payout_status": {"$exists": False}},
                {"payout_status": {"$in": [None, "pending_review", "failed", "processing"]}},
            ]
        }
    ).limit(50)
    entries = []
    for participant in pending:
        entries.append(
            "ID: {user_id} | status: {status}\nWallet: {wallet}\nX: {x}\nTikTok: {tiktok}".format(
                user_id=participant.get("userId"),
                status=participant.get("payout_status", "pending_review"),
                wallet=participant.get("bep20", "missing"),
                x=participant.get("twitter_username", "not provided"),
                tiktok=participant.get("tiktok_username", "not provided"),
            )
        )
        entries[-1] += (
            "\nTask claims: FEM app={app}, Telegram={telegram}, X={x_follow}, "
            "TikTok follow={tiktok_follow}, TikTok likes={tiktok_likes}".format(
                app="yes" if participant.get("fem_app_task_claimed") else "no",
                telegram="yes" if participant.get("telegram_task_claimed") else "no",
                x_follow="yes" if participant.get("x_follow_task_claimed") else "no",
                tiktok_follow="yes" if participant.get("tiktok_follow_task_claimed") else "no",
                tiktok_likes="yes" if participant.get("tiktok_like_task_claimed") else "no",
            )
        )
    update.effective_message.reply_text(
        "No participants need review." if not entries else "\n\n".join(entries)
    )


def _publish_payout(update, participant):
    transaction_hash = participant["payout_tx_hash"]
    tx_link = f"{FEM_TX_EXPLORER_URL}{transaction_hash}" if FEM_TX_EXPLORER_URL else transaction_hash
    update.bot.send_message(
        chat_id=_announcement_chat_id(),
        text=(
            "FEM airdrop payout sent\n"
            f"Amount: {FEM_REWARD_AMOUNT} FEM\n"
            f"Wallet: {participant['bep20']}\n"
            f"Transaction: {tx_link}"
        ),
    )
    mongo.users.update_one(
        {"userId": participant["userId"]},
        {"$set": {"announcement_status": "announced", "announced_at": datetime.utcnow()}},
    )


def _announcement_chat_id():
    chat_id = FEM_ANNOUNCEMENT_CHAT_ID
    return int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id


def announceUpdate(update, context):
    if not _is_private_admin(update):
        return _admin_denied(update)
    if not FEM_ANNOUNCEMENT_CHAT_ID:
        update.effective_message.reply_text(
            "Set FEM_ANNOUNCEMENT_CHAT_ID and make the bot an admin in the group first."
        )
        return

    message = update.effective_message.text.partition(" ")[2].strip()
    if not message:
        update.effective_message.reply_text("Usage: /announce <message>")
        return
    if len(message) > 4096:
        update.effective_message.reply_text("Announcement must be 4096 characters or fewer.")
        return

    try:
        update.bot.send_message(chat_id=_announcement_chat_id(), text=message)
    except Exception as error:
        logger.error("Group announcement failed (%s)", type(error).__name__)
        update.effective_message.reply_text("Could not post the announcement; check bot permissions.")
        return
    update.effective_message.reply_text("Announcement posted to the campaign group.")


def approvePayout(update, context):
    if not _is_private_admin(update):
        return _admin_denied(update)
    if len(context.args) != 1 or not context.args[0].isdigit():
        update.effective_message.reply_text("Usage: /approve <telegram_user_id>")
        return
    if not FEM_ANNOUNCEMENT_CHAT_ID:
        update.effective_message.reply_text(
            "Set FEM_ANNOUNCEMENT_CHAT_ID and make the bot an admin in that group before approving payouts."
        )
        return

    user_id = int(context.args[0])
    with PAYOUT_LOCK:
        participant = mongo.users.find_one({"userId": user_id})
        if not participant:
            update.effective_message.reply_text("Participant not found.")
            return
        if participant.get("payout_status") == "paid":
            update.effective_message.reply_text(
                f"Already paid: {participant.get('payout_tx_hash', 'transaction hash unavailable')}"
            )
            return
        if not participant.get("bep20"):
            update.effective_message.reply_text("Participant has no saved FEM wallet.")
            return

        raw_transaction = participant.get("payout_raw_transaction")
        transaction_hash = participant.get("payout_tx_hash")
        if participant.get("payout_status") != "processing":
            participant = mongo.users.find_one_and_update(
                {
                    "userId": user_id,
                    "$or": [
                        {"payout_status": {"$exists": False}},
                        {"payout_status": {"$in": [None, "pending_review", "failed"]}},
                    ],
                },
                {"$set": {"payout_status": "processing", "payout_started_at": datetime.utcnow()}},
                return_document=ReturnDocument.AFTER,
            )
            if not participant:
                update.effective_message.reply_text("Payout is already being processed or completed.")
                return

        if not raw_transaction or not transaction_hash:
            try:
                raw_transaction, transaction_hash = prepare_payout(participant["bep20"])
            except Exception as error:
                logger.error(
                    "FEM payout preparation failed for user %s (%s)",
                    user_id,
                    type(error).__name__,
                )
                mongo.users.update_one(
                    {"userId": user_id, "payout_status": "processing"},
                    {
                        "$set": {
                            "payout_status": "pending_review",
                            "payout_error": type(error).__name__,
                        }
                    },
                )
                update.effective_message.reply_text(
                    "Payout not submitted due to an RPC or configuration error. Check Railway logs."
                )
                return
            mongo.users.update_one(
                {"userId": user_id, "payout_status": "processing"},
                {
                    "$set": {
                        "payout_raw_transaction": raw_transaction,
                        "payout_tx_hash": transaction_hash,
                    }
                },
            )

        try:
            broadcast_payout(raw_transaction, transaction_hash)
        except RuntimeError as error:
            if str(error) == "FEM payout transaction reverted on chain":
                mongo.users.update_one(
                    {"userId": user_id},
                    {
                        "$set": {"payout_status": "failed", "payout_error": str(error)},
                        "$unset": {"payout_raw_transaction": ""},
                    },
                )
                update.effective_message.reply_text("The transaction reverted. Review and retry approval.")
            else:
                logger.error("FEM payout is unresolved for user %s (%s)", user_id, type(error).__name__)
                update.effective_message.reply_text(
                    f"Payout is still processing. Retry /approve {user_id} to check/rebroadcast the same transaction."
                )
            return
        except Exception as error:
            logger.error("FEM payout is unresolved for user %s (%s)", user_id, type(error).__name__)
            update.effective_message.reply_text(
                f"Payout is still processing. Retry /approve {user_id} to check/rebroadcast the same transaction."
            )
            return

        mongo.users.update_one(
            {"userId": user_id},
            {
                "$set": {
                    "payout_status": "paid",
                    "payout_paid_at": datetime.utcnow(),
                    "announcement_status": "pending",
                },
                "$unset": {"payout_raw_transaction": ""},
            },
        )
        participant["payout_tx_hash"] = transaction_hash
        try:
            _publish_payout(update, participant)
        except Exception as error:
            logger.error("Payout announcement failed for user %s (%s)", user_id, type(error).__name__)
            update.effective_message.reply_text(
                f"Paid {FEM_REWARD_AMOUNT} FEM. Announcement failed; /retryannouncements can retry it. Transaction: {transaction_hash}"
            )
            return
        update.effective_message.reply_text(
            f"Paid {FEM_REWARD_AMOUNT} FEM to {participant['bep20']} and announced transaction {transaction_hash}."
        )


def retryPayoutAnnouncements(update, context):
    if not _is_private_admin(update):
        return _admin_denied(update)
    pending = mongo.users.find(
        {"payout_status": "paid", "announcement_status": {"$ne": "announced"}}
    ).limit(100)
    sent = 0
    for participant in pending:
        try:
            _publish_payout(update, participant)
            sent += 1
        except Exception as error:
            logger.error(
                "Payout announcement retry failed for user %s (%s)",
                participant.get("userId"),
                type(error).__name__,
            )
    update.effective_message.reply_text(f"Posted {sent} payout announcement(s).")


# Admin commands
def getList(update, context):
    user = update.message.from_user
    if user.username != ADMIN_USERNAME:
        return
    list = mongo.users.find({})

    with open("users.json", "w") as file:
        file.write("[")
        for document in list:
            file.write(dumps(document))
            file.write(",")
        file.write("]")
    with open("users.json", "r") as file:
        update.message.reply_document(document=file, filename="list.json")


def getStats(update, context):
    user = update.message.from_user
    if user.username != ADMIN_USERNAME:
        return
    list = mongo.users.find({})
    refes = mongo.users.count_documents({"ref": {"$ne": False}})
    user_count = mongo.users.count_documents({})
    reply = f"""
Currently there are *{user_count} users* joined the airdrop!
Currently there are *{refes} users* joined by referrals
A total of *{"{:,.2f}".format(float(AIRDROP_AMOUNT.replace(",",""))*user_count)} {COIN_SYMBOL}* will be distributed as participation rewards
A total of *{"{:,.2f}".format(REFERRAL_REWARD*refes)} {COIN_SYMBOL}* referral rewards will be distributed
"""
    update.message.reply_text(reply, parse_mode=telegram.ParseMode.MARKDOWN)


def setStatus(update, context):
    user = update.message.from_user
    if user.username != ADMIN_USERNAME:
        return
    arg = context.args[0]
    if arg == "stop":
        set_bot_status("STOPPED")
        update.message.reply_text("Airdrop stopped")
    if arg == "pause":
        set_bot_status("PAUSED")
        update.message.reply_text("Airdrop paused")
    if arg == "start":
        set_bot_status("ON")
        update.message.reply_text("Airdrop started")


# ----------------
