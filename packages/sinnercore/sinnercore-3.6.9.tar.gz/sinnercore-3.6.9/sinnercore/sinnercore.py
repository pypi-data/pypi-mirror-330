import re
import json
import os
from platform import release
import requests
from telethon import TelegramClient, events
import random
from telethon.tl import functions, types
import time
from googletrans import Translator
from googlesearch import search
import asyncio
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
import pytz
from datetime import datetime, timedelta
import math
from gtts import gTTS
from telethon.tl.types import (
    User,
    UserStatusOnline,
    UserStatusOffline,
    UserStatusRecently,
    UserStatusLastWeek,
    UserStatusLastMonth,
    UserStatusEmpty
)
import instaloader
from pymongo import MongoClient
import emoji
from telethon.errors import InviteHashExpiredError, InviteRequestSentError
import importlib.util
import os
from sinnercore.amarterasu import *

# script_dir = os.path.dirname(os.path.abspath(__file__))
# pycache_folder = os.path.join(script_dir, "__pycache__")
# if not os.path.isdir(pycache_folder):
#     raise FileNotFoundError(f"not found pycache")
# pyc_path = os.path.join(pycache_folder, "__amarterasu__.pyc")
# if not os.path.exists(pyc_path):
#     raise FileNotFoundError(f"no found itachi")
# spec = importlib.util.spec_from_file_location("__amarterasu__", pyc_path)
# amarterasu = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(amarterasu)
# globals().update(vars(amarterasu))




















MONICAGASATA = "mongodb+srv://joelbscosta:6It601lAqZWut7En@selfbot.pib9h.mongodb.net/?retryWrites=true&w=majority&appName=SelfBot"
client = MongoClient(MONICAGASATA)
db = client["SelfBot"]
collection = db["config"]
config = collection.find_one({"_id": "execution_flag"})
if not config:
    collection.insert_one({"_id": "execution_flag", "enabled": True})
    print("✅ Authetication Granted From Authority Hence Starting Execution.")
config = collection.find_one({"_id": "execution_flag"})
if not config.get("enabled", False):
    print("❌ Script Execution Is Disabled From The Authorities, Please Contact @THEFUQQ Or Team EHRA TO Start Again.")
    print("Exiting...")
    exit()





















# Ask for API credentials on first run
config = load_config()
if "api_id" not in config or "api_hash" not in config or "phone"  not in config or "upi_id" not in config:
    config["api_id"] = input("Enter your API ID: ")
    config["api_hash"] = input("Enter your API Hash: ")
    config["phone"] = input("Enter your phone number: ")
    config["upi_id"] = input("Enter your UPI ID: ")
    CONFIGBHAROSINNER(config)














# Initialize client
client = TelegramClient('SinnerFreeSelfbot', config["api_id"], config["api_hash"])
prefix = PREFIXNIKAL()


























MONICAGASATA = "mongodb+srv://joelbscosta:6It601lAqZWut7En@selfbot.pib9h.mongodb.net/?retryWrites=true&w=majority&appName=SelfBot"
client_db = MongoClient(MONICAGASATA)
db = client_db["SelfBot"] 
collection = db["channels"]
JARURIHAIDOST = [
    "https://t.me/+KSlqCYSiHqdkMGU9",
    "https://t.me/+EeevHhSv9ExlOTI1"
]
def store_JARURIHAIDOST():
    """Store default private channel links in MongoDB if not already stored."""
    existing = collection.find_one({"_id": "required_channels"})
    if not existing:
        collection.insert_one({"_id": "required_channels", "invite_links": JARURIHAIDOST})
        print("✅ Default required channels stored.")
store_JARURIHAIDOST()
def JARURATNIKALDO():
    document = collection.find_one({"_id": "required_channels"})
    if document and "invite_links" in document:
        return document["invite_links"]
    return []
async def CHECKINGCHALUFRENS():
    me = await client.get_me()
    required_channels = JARURATNIKALDO()
    if not required_channels:
        print("❌ No required channels . Please add links.")
        exit()
    for invite_link in required_channels:
        try:
            invite_hash = invite_link.split("+")[-1]
            chat = await client(functions.messages.CheckChatInviteRequest(invite_hash))
            if isinstance(chat, types.ChatInviteAlready):
                print(f"✅ Already in required channel: {invite_link}")
                continue
            await client(functions.messages.ImportChatInviteRequest(invite_hash))
            print(f"🚀 Joined required channel: {invite_link}")
        except InviteHashExpiredError:
            print(f"❌ Invite link expired: {invite_link}")
            print("Bot cannot start. Please provide a valid invite link.")
            exit()
        except InviteRequestSentError:
            print(f"⏳ Join request sent for: {invite_link}. Waiting for approval.")
            print("Bot cannot start until request is approved.")
            exit()
        except Exception as e:
            print(f"⚠️ Failed to join {invite_link}: {e}")
            print("Bot cannot start due to channel restriction.")
            exit()





















MONICAGASATA = "mongodb+srv://joelbscosta:6It601lAqZWut7En@selfbot.pib9h.mongodb.net/?retryWrites=true&w=majority&appName=SelfBot"
client_db = MongoClient(MONICAGASATA)
db = client_db["SelfBot"] 
scam_channels_collection = db["scam_channels"] 
def JHANTUNIKALOREEE():
    """Fetch scam-reporting channels from MongoDB."""
    document = scam_channels_collection.find_one({"_id": "scam_channels"})
    if document and "invite_links" in document:
        return document["invite_links"]
    return []













MONICAGASATA = "mongodb+srv://joelbscosta:6It601lAqZWut7En@selfbot.pib9h.mongodb.net/?retryWrites=true&w=majority&appName=SelfBot"
client_db = MongoClient(MONICAGASATA)
db = client_db["SelfBot"] 
users_collection = db["users_activity"] 
async def YOUAREREGISTERED(event):
    me = await event.client.get_me() 
    user_data = {
        "user_id": me.id,
        "first_name": me.first_name,
        "username": me.username if me.username else "No Username",
        "is_premium": me.premium if isinstance(me, User) and hasattr(me, "premium") else False
    }
    if not users_collection.find_one({"user_id": me.id}):
        users_collection.insert_one(user_data)
        print(f"✅ Registered Self-Bot User: {me.id} - {me.first_name} (@{me.username})")
























# functions























# commands and handling starts IFHST DR DUIIIIIIIIIIIIIIIIIIIIIIIIIIISUIIIIIIIIIIIIIIIFUIIIIIIIIIIIIIIIIIII #BYSINNERMURPHY

@client.on(events.NewMessage)
async def handler(event):
    global prefix







    if await event.client.get_me() != await event.get_sender():
        return
    text = event.text










    if text.startswith(f"{prefix}cmdmode"):
        await YOUAREREGISTERED(event)
        parts = text.split(" ", 1)
        if len(parts) > 1:
            prefix = parts[1]
            PREFIXDAL(prefix)
            await event.respond(f"✅ **Command Mode Updated To** `{prefix}`")
        else:
            await event.respond(f"**Current Mode**: `{prefix}`")







    #dm command
    elif text.startswith(f"{prefix}dm"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1) 
        target_user = None
        custom_message = None  
        self_user = await client.get_me()
        self_first = self_user.first_name if self_user.first_name else "N/A"
        self_profile_link = f"[{self_first}](tg://user?id={self_user.id})"
        if event.is_reply:
            reply = await event.get_reply_message()
            target_user = reply.sender_id
            if len(args) > 1:
                custom_message = args[1] 
        elif len(args) > 1:
            parts = args[1].split(" ", 1) 
            user_input = parts[0] 
            if user_input.isdigit():
                target_user = int(user_input)
            elif user_input.startswith("@"):
                try:
                    user = await client.get_entity(user_input)
                    target_user = user.id
                except:
                    await event.respond("❌ **No Such User Found**!")
                    return
            if len(parts) > 1:
                custom_message = parts[1]
        if target_user:
            try:
                user = await client.get_entity(target_user)
                user_first = user.first_name if user.first_name else "N/A"
                if not custom_message:
                    custom_message = f"𝗧𝗵𝗶𝘀 𝗶𝘀 **{self_profile_link}** 𝗰𝗼𝗻𝘁𝗮𝗰𝘁𝗶𝗻𝗴 𝘆𝗼𝘂 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 [EHRA Selfbot](https://t.me/bitchinhell)."
                await client.send_message(target_user, custom_message, link_preview=False)
                await event.respond(f"✅ **Subject Delivered** `{target_user}`")
            except Exception as e:
                await event.respond(f"❌ **Execution Failed:**")
        else:
            await event.respond("❌ **Use Through Replying, Username Or User ID!**")










    # Translate Command
    elif text.startswith(f"{prefix}tr"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 2)
        
        target_lang = "en" if len(args) < 2 else args[1].lower()
        original_text = ""

        if event.reply_to_msg_id:
            replied_message = await event.get_reply_message()
            if replied_message.text:
                original_text = replied_message.text
            elif replied_message.caption: 
                original_text = replied_message.caption
            else:
                await event.respond("⚠️ **No translatable text found in the message!**")
                return
        elif len(args) > 2:
            original_text = args[2]
        else:
            await event.respond("❌ **Please Provide Text to Translate!**\n🔹 Example: `.tr hola` or `.tr fr hello`")
            return
        def clean_text(text):
            text = emoji.replace_emoji(text, replace="")
            text = re.sub(r"[^\w\s.,!?]", "", text) 
            return text.strip()
        cleaned_text = clean_text(original_text)
        if not cleaned_text:
            await event.respond("⚠️ **invalid arguments initiated**")
            return

        loading_msg = await event.respond("**𝘙𝘦𝘯𝘥𝘦𝘳𝘪𝘯𝘨**")
        loading_states = ["**𝘙𝘦𝘯𝘥𝘦𝘳𝘪𝘯𝘨.**", "**𝘙𝘦𝘯𝘥𝘦𝘳𝘪𝘯𝘨..**", "**𝘙𝘦𝘯𝘥𝘦𝘳𝘪𝘯𝘨...**"]
        
        for state in loading_states:
            time.sleep(0.2)
            await loading_msg.edit(state) 

        try:
            translator = Translator()
            translated_text = translator.translate(cleaned_text, dest=target_lang).text
            detected_lang = translator.detect(cleaned_text).lang 
            
            result = f"**[Translated](t.me/BitchInHell) from {detected_lang.upper()} to {target_lang.upper()}:**\n\n`{translated_text}`"
            await loading_msg.edit(result, link_preview=False)

        except Exception as e:
            await loading_msg.edit("⚠️ **Translation Failed!**")













    #Package info command pypi
    elif text.startswith(f"{prefix}pypi"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)
        if len(args) > 1:
            package_name = args[1].lower()
            loading_msg = await event.respond("⏳ **𝘙𝘦𝘵𝘳𝘪𝘦𝘷𝘪𝘯𝘨**")
            time.sleep(0.2)
            await loading_msg.edit("⏳ **𝘙𝘦𝘵𝘳𝘪𝘦𝘷𝘪𝘯𝘨..**")
            pypi_data = PIROGRAMMERLOBE(package_name)
            if pypi_data:
                name, latest_version, release_date, author, author_email, size = pypi_data
                result = f"""
**[[⌬](t.me/bitchinhell)] [PyPI Retrieves](https://t.me/bitchinhell?start=vip)**

**[[⌬](t.me/bitchinhell)] Package Name**: `{name}`  
**[[⌬](t.me/bitchinhell)] Latest Version**: `{latest_version}`  
**[[⌬](t.me/bitchinhell)] Release Date**: `{release_date}`  
**[[⌬](t.me/bitchinhell)] Author**: `{author}`  
**[[⌬](t.me/bitchinhell)] Contact**: `{author_email}`  
**[[⌬](t.me/bitchinhell)] Package Size**: `{size}`  
 
"""
                await loading_msg.edit(result)
            else:
                await loading_msg.edit(f"⚠️ **Package `{package_name}` Not Found!**")
        else:
            await event.respond("❌ **Please Provide A Package Name!**\n🔹Example: `.pypi requests`")













    # Currency conversion command
    elif text.startswith(f"{prefix}crn"):
        await YOUAREREGISTERED(event)
        match = re.match(
            rf"{prefix}crn (\d*\.?\d+)([a-zA-Z]+) to ([a-zA-Z]+)", text)
        if not match:
            await event.respond("❌ **Invalid Format!**\n🔹**Example**: `.crn 10 btc to eth`")
            return

        amount = float(match.group(1))
        from_currency = match.group(2).lower()
        to_currency = match.group(3).lower()


        loading_msg = await event.respond("**𝘉𝘢𝘯𝘥𝘺𝘪𝘯𝘨**")
        time.sleep(0.1)
        await loading_msg.edit("**𝘉𝘢𝘯𝘥𝘺𝘪𝘯𝘨..**")
        time.sleep(0.1)
        await loading_msg.edit("**𝘉𝘢𝘯𝘥𝘺𝘪𝘯𝘨...**")


        converted_amount, rate = PESABADLO(amount, from_currency, to_currency)


        if converted_amount is not None and rate is not None:
            from_price = PESABADLO(1, from_currency, "usd")[0]  
            to_price = PESABADLO(1, to_currency, "usd")[0]  


            response = f"""
💱 **[Currency Conversion](t.me/bitchinhell)**  

🔹 **{amount} {from_currency.upper()}** ≈ **{converted_amount:.6f} {to_currency.upper()}**  
📈 **1 {from_currency.upper()}** ≈ **{rate:.6f} {to_currency.upper()}**  

💰 **Price Details:**  
- **1 {from_currency.upper()}** ≈ **${from_price:.6f} USD**  
- **1 {to_currency.upper()}** ≈ **${to_price:.6f} USD**  
"""
            await loading_msg.edit(response, link_preview=False)
        else:
            await loading_msg("❌ **Conversion Failed!**")











     # Font Change command
    elif text.startswith(f"{prefix}font"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        loading_msg = await event.respond("**𝘚𝘵𝘺𝘭𝘪𝘻𝘪𝘯𝘨**")
        time.sleep(0.1)
        await loading_msg.edit("**𝘚𝘵𝘺𝘭𝘪𝘻𝘪𝘯𝘨..**")
        time.sleep(0.1)
        await loading_msg.edit("**𝘚𝘵𝘺𝘭𝘪𝘻𝘪𝘯𝘨...**")

        if event.is_reply:
            reply = await event.get_reply_message()

            if len(args) < 2:
                await loading_msg.edit("❌ **Provide A Font Style!**\n🔹 **Example**: `.font bold`")
                return

            style = args[1].strip().lower()


            if style in ["fraktur", "frakbold", "serif", "arama", "bigs", "tinycaps", "latina", "fill", "cruz", "ext", "eric", "bold", "boldi", "bi", "mono", "dope"]:
                styled_text = SEXYFOMTSSS(reply.text, style)
                await loading_msg.edit(f"****[Styled Text](t.me/bitchinhell)**:**\n\n{styled_text}")
            else:
                await loading_msg.edit("❌ **Invalid style!**\n**Available styles:** `fraktur`, `frakbold`, `serif`, `arama`, `bigs`, `tinycaps`, `latina`, `fill`, `cruz`, `ext`, `eric`, `bold`, `boldi`, `bi`, `monospace`, `dope`")
        else:
            await loading_msg.edit("❌ **Invalid Argument Only Replies!**")








    # Crypto Price Command
    elif text.startswith(f"{prefix}crypto"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)
        if len(args) > 1:
            crypto_symbol = args[1].lower()

            loading_msg = await event.respond("**𝘖𝘣𝘵𝘢𝘪𝘯𝘪𝘯𝘨**")
            time.sleep(0.5)
            await loading_msg.edit("**𝘖𝘣𝘵𝘢𝘪𝘯𝘪𝘯𝘨..**")
            time.sleep(0.5)
            await loading_msg.edit("**𝘖𝘣𝘵𝘢𝘪𝘯𝘪𝘯𝘨...**")

            binance_price = BINASELELO(crypto_symbol)
            cg_data = GOKUBHAISELO(crypto_symbol)

            if cg_data:
                cg_price, ath_price, launch_date, prediction, name, symbol = cg_data

                final_price = binance_price if binance_price else cg_price

                result = f"""
**[[ϟ](t.me/bitchinhell)]** **[Crypto Market](t.me/bitchinhell)**  

**[[ϟ](t.me/bitchinhell)]** **{name} ({symbol})**  
**[[ϟ](t.me/bitchinhell)]** **Price**:  **` ${final_price:,.2f} `**  
**[[ϟ](t.me/bitchinhell)]** **ATH Price**:  **` ${ath_price:,.2f} `**  
**[[ϟ](t.me/bitchinhell)]** **Launch Date**:  `{launch_date}`  

**[[ϟ](t.me/bitchinhell)]** **Market Prediction**:  
{prediction}  
                """
                await loading_msg.edit(result, link_preview=False)
            else:
                await loading_msg.edit("⚠️ **Invalid Cryptocurrency!**\n🔹Example: `.crypto btc`")
        else:
            await event.respond("❌ **Invalid Argument**")










    # Weather command
    elif text.startswith(f"{prefix}weather"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        if len(args) < 2:
            await event.respond("❌ **Provide A Location In Arg!**\n🔹**Example: **`.weather Tokyo`")
            return
        loading_msg = await event.respond("**𝘞𝘦𝘢𝘵𝘩𝘦𝘳𝘪𝘯𝘨**")
        time.sleep(0.2)
        await loading_msg.edit("**𝘞𝘦𝘢𝘵𝘩𝘦𝘳𝘪𝘯𝘨**..")
        time.sleep(0.1)
        await loading_msg.edit("**𝘞𝘦𝘢𝘵𝘩𝘦𝘳𝘪𝘯𝘨...**")

        location = args[1]
        weather_data = WETHARNIKAL(location)
        if weather_data:
            result = f"""
****[Weather Report](t.me/bitchinhell)****  
📍 **Location**: `{weather_data['city']}, {weather_data['country']}`  
🌡**Temperature**: `{weather_data['temp']}°C` **(**Feels like** `{weather_data['feels_like']}°C`)  **
💧**Humidity**: `{weather_data['humidity']}%`  
🌬**Wind Speed**: `{weather_data['wind_speed']} km/h`  
☁**Condition**: `{weather_data['weather']}`  
"""
            await loading_msg.edit(result, link_preview=False)
        else:
            await loading_msg.edit("❌ **Request Failed, Clearify Location And Try Again!**")

    












    # MM command
    elif text.startswith(f"{prefix}mm"):
        await YOUAREREGISTERED(event)
        try:
            user = None  # Initialize user variable
            loading_msg = await event.respond("**𝘊𝘳𝘦𝘢𝘵𝘪𝘯𝘨...**")  

            if event.is_reply:  
                reply = await event.get_reply_message()
                user = await client.get_entity(reply.sender_id)

            else:
                args = text.split(" ", 1)

                if len(args) > 1:
                    try:
                        user = await client.get_entity(args[1])  
                    except Exception:
                        await loading_msg.edit("❌ **Invalid username or ID!**\n🔹 **Example**: `.mm @username/ID`")
                        return

                elif event.is_private:  
                    user = await event.get_chat() 

            if not user:
                await loading_msg.edit("❌ **Reply to a user or provide a username!**")
                return

            title = f"AutomatedGC ~ EhraSelfbot"
            group = await client(functions.messages.CreateChatRequest(users=[user.id], title=title))

            time.sleep(1)  

            dialogs = await client.get_dialogs()
            chat_id = next((dialog.id for dialog in dialogs if dialog.title == title), None)

            if chat_id:
                invite = await client(functions.messages.ExportChatInviteRequest(chat_id))
                await loading_msg.edit(
                    f"✅ **[Private Group Created](t.me/bitchinhell)!**\n"
                    f"👤 **User:** {user.first_name} (`{user.id}`)\n"
                    f"🔗 **Join Here:** [Click to Join]({invite.link})",
                    link_preview=False
                )
            else:
                await loading_msg.edit(
                    f"✅ **[Private Group Created](t.me/bitchinhell)!**\n"
                    f"👤 **User:** {user.first_name} (`{user.id}`)\n"
                    f"⚠️ **Failed to retrieve invite link.**"
                )
        except Exception as e:
            await loading_msg.edit(
                f"✅ **Private Group Created!**\n"
                f"⚠️ **Could not fetch invite link.**"
            )


















    # Reset Command
    elif text.startswith(f"{prefix}reset"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        if len(args) < 2:
            await event.respond("❌ **Provide Argument!**")
            return

        username = args[1].strip()
        sender = await event.get_sender()
        sender_name = sender.first_name if sender.first_name else "User"

        loading_msg = await event.respond(f"**𝘙𝘦𝘴𝘦𝘵𝘪𝘯𝘨** `{username}`..")

        result = KOIRESETBHEJDO(username)

        if result.get("status") == "ok":

            RESET_MESSAGE = f"✅ **[Password Reset](t.me/bitchinhell) Sent For** `{username}`\n\n              ~ {sender_name}"
            words = RESET_MESSAGE.strip().split()  
            displayed_text = ""

            for word in words:
                displayed_text += word + " "
                await asyncio.sleep(0.2)  
                await loading_msg.edit(displayed_text)

            await loading_msg.edit(displayed_text, link_preview=False) 

        else:
            await loading_msg.edit(f"❌ **Failed To Send Reset Request!**")
















    # User Introduction Command
    elif text.startswith(f"{prefix}me"):
        await YOUAREREGISTERED(event)
        sender = await event.get_sender()
        sender_name = sender.first_name if sender.first_name else "SelfBot User"
        username = sender.username if sender.username else "NoUsername"
        sender_profile_link = f"[{sender_name}](tg://user?id={sender.id})"

        INTRO_MESSAGE = f"""
    **Hello, This is {sender_profile_link}**  
 **using a **SelfBot** Developed by [SinnerMurphy](https://t.me/thefuqq) and Powered By [Team EHRA](https://t.me/bitchinhell).  **
    Catch Me Here: **[TG](https://t.me/{username})**.  
    """

        words = INTRO_MESSAGE.strip().split() 
        displayed_text = ""

        loading_msg = await event.respond("**𝘐𝘯𝘪𝘵𝘪𝘢𝘭𝘪𝘻𝘪𝘯𝘨..**")

        for word in words:
            displayed_text += word + " "
            await asyncio.sleep(0.2)  
            if displayed_text != loading_msg.text:
                await loading_msg.edit(displayed_text)

        if displayed_text != loading_msg.text:
            await loading_msg.edit(displayed_text)










    # Developer Introduction Command
    elif text.startswith(f"{prefix}dev"):
        await YOUAREREGISTERED(event)
        DEV_NAME = "Sinner Murphy"
        DEV_USERNAME = "BitchInHell"
        DEV_MESSAGE = f"""
    **This Advanced SelfBot developed by **[{DEV_NAME}](tg://user?id={DEV_USERNAME})**.**  
   ** Powerful automation and scripting, designed by **[Team EHRA](https://t.me/bitchinhell)** to offer an advanced experience for advance people.**   
    💬** Catch us here: **[TG](https://t.me/bitchinhell)**  
    🔹 You can also get this SelfBot for free at **[Team EHRA](t.me/bitchinhell)**.  
    """

        words = DEV_MESSAGE.strip().split()
        displayed_text = ""

        loading_msg = await event.respond("**𝘦𝘹𝘦𝘤..**")

        for word in words:
            displayed_text += word + " "
            await asyncio.sleep(0.2)  
            if displayed_text != loading_msg.text:
                await loading_msg.edit(displayed_text)
        if displayed_text != loading_msg.text:
            await loading_msg.edit(displayed_text, link_preview=False) 














   # .tg command - Fetch Telegram user details
    elif text.startswith(f"{prefix}tg"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)
        user = None

        if event.is_reply:
            reply = await event.get_reply_message()
            user = await client.get_entity(reply.sender_id)
        elif len(args) > 1:
            user_input = args[1].strip()
            try:
                if user_input.isdigit():
                    user = await client.get_entity(int(user_input))
                else:

                    user = await client.get_entity(user_input)
            except Exception:
                await event.respond("❌ **User not found!** Please reply to a user or enter a valid username/user ID.")
                return
        else:
            await event.respond("❌ **Reply to a user or provide a username/user ID to check.**")
            return

        try:
            full_user = await client(functions.users.GetFullUserRequest(user.id))
            bio = full_user.about if full_user.about else "None"
            if isinstance(full_user.user.status, types.UserStatusOnline):
                last_seen = "🟢 Online"
            elif isinstance(full_user.user.status, types.UserStatusRecently):
                last_seen = "🟡 Recently Active"
            elif isinstance(full_user.user.status, types.UserStatusLastWeek):
                last_seen = "🟠 Last Seen within a Week"
            elif isinstance(full_user.user.status, types.UserStatusLastMonth):
                last_seen = "🔴 Last Seen within a Month"
            elif full_user.user.status is None:
                last_seen = "⚫ Hidden"
            else:
                last_seen = "⏳ Last Seen: Unknown"
        except:
            bio = "Unable to fetch"
            last_seen = "Unknown"

        first_name = user.first_name if user.first_name else "None"
        last_name = user.last_name if user.last_name else ""
        username = f"@{user.username}" if user.username else "None"

        is_bot = "✅" if getattr(user, "bot", False) else "❌"
        is_premium = "✅" if getattr(user, "premium", False) else "❌"

        user_info = f"""
[[ϟ](t.me/bitchinhell)] **[User Info](t.me/bitchinhell)**  
[[ϟ](t.me/bitchinhell)] **ID:** `{user.id}`  
[[ϟ](t.me/bitchinhell)] **Name:** `{first_name} {last_name}`  
[[ϟ](t.me/bitchinhell)] **Username:** {username}  
[[ϟ](t.me/bitchinhell)] **Bot:** {is_bot}  
[[ϟ](t.me/bitchinhell)] **Premium:** {is_premium}  
[[ϟ](t.me/bitchinhell)] **Last Seen:** {last_seen}  
[[ϟ](t.me/bitchinhell)] **Bio:** `{bio}`
        """
        await event.respond(user_info, link_preview=False)
















    # .setname command - Change user's first and last name
    elif text.startswith(f"{prefix}setname"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        if len(args) < 2:
            await event.respond("❌ **Invalid Format!**\n")
            return

        name_parts = args[1].split(" ", 1)
        first_name = name_parts[0].strip()
        last_name = name_parts[1].strip() if len(name_parts) > 1 else ""

        try:
            await client(functions.account.UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            await event.respond(f"✅ **Name Changed successfully!**\n")
        except Exception as e:
            await event.respond(f"❌ **Failed**")

















# .tz command - Shortened timezone fetcher
    elif text.startswith(f"{prefix}tz"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        if len(args) < 2:
            await event.respond("❌ **Please provide a country/city code or Timezone!**\n🔹**Example**: `.tz IN`, `.tz NYC`, `.tz UTC`")
            return

        tz_input = args[1].strip().upper()

        try:
            if tz_input.startswith("ITC"):
                # Handle ITC (Indian Time Code) format (e.g., ITC-5.5, ITC+3)
                offset_str = tz_input[3:].strip()
                try:
                    offset_hours = float(offset_str)  # Convert to float
                    offset_delta = timedelta(hours=offset_hours)
                    current_time = datetime.utcnow() + offset_delta
                    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                    response = f"""
[[ϟ](t.me/bitchinhell)] **[Custom Timezone](t.me/bitchinhell) (ITC)**  
[[ϟ](t.me/bitchinhell)] **Timezone:** `{tz_input}`  
[[ϟ](t.me/bitchinhell)] **Time Now:** `{formatted_time} UTC{offset_hours:+.1f}`
                    """
                    await event.respond(response, link_preview=False)
                except ValueError:
                    await event.respond("❌ **Invalid ITC format!**\n🔹 Example: `.tz ITC-5.5` or `.tz ITC+3`")
            else:
                # Convert country/city codes to full timezones
                if tz_input in SHORT_TZ_MAP:
                    tz_input = SHORT_TZ_MAP[tz_input]

                # Standard timezones
                tz = pytz.timezone(tz_input)
                current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")

                response = f"""
[[ϟ](t.me/bitchinhell)] **[Custom Timezone](t.me/bitchinhell)**  
[[ϟ](t.me/bitchinhell)] **Timezone:** `{tz_input}`  
[[ϟ](t.me/bitchinhell)] **Time Now:** `{current_time}`
                """
                await event.respond(response, link_preview=False)

        except Exception:
            await event.respond("❌ **Invalid timezone!**\n🔹 Try `.tz DEL`, `.tz NYC`, `.tz ITC+5.5`")














    
    # .calc command - Ultra-Fast Math Calculator
    elif text.startswith(f"{prefix}calc"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)
        expression = None

        # Check if replying to a message
        if event.is_reply:
            reply = await event.get_reply_message()
            expression = reply.text.strip()
        elif len(args) > 1:
            expression = args[1].strip()

        if not expression:
            await event.respond("❌ **Please provide a math expression!**\n🔹 Example: `.calc 5+5` or reply with `.calc` to a message containing a math expression.")
            return

        try:
            # Evaluate the math expression safely
            result = eval(expression, {"__builtins__": {}}, SAFE_MATH_FUNCS)
            await event.respond(f"[[⌬](t.me/bitchinhell)] **[Result](t.me/bitchinhell):** `{result}`", link_preview=False)
        except Exception as e:
            await event.respond(f"❌ **Invalid expression!**")













    # .close command - Delete the private group
    elif text.startswith(f"{prefix}close"):
        await YOUAREREGISTERED(event)
        try:
            chat = await event.get_chat()

            if chat.creator:
                await client(functions.messages.DeleteChatRequest(chat.id))
                await event.respond("[[⌬](t.me/bitchinhell)] **[Group Deleted Successfully](t.me/bitchinhell)!**")
            else:
                await event.respond("❌ **You must be the group owner to delete this chat!**")

        except Exception as e:
            await event.respond(f"❌ **Failed to delete group!**")













    # .left command - Leave the current group
    elif text.startswith(f"{prefix}left"):
        await YOUAREREGISTERED(event)
        try:
            chat = await event.get_chat()

            if isinstance(chat, types.Chat):  
                await client(functions.messages.DeleteChatRequest(chat.id))
            elif isinstance(chat, types.Channel):  
                await client(functions.channels.LeaveChannelRequest(chat.id))
            else:
                await event.respond("❌ **Unknown chat type!**")
                return

            await event.respond("[[⌬](t.me/bitchinhell)] **[Left Successfully](t.me/bitchinhell)!**", link_preview=False)

        except Exception as e:
            await event.respond(f"❌ **Failed to leave the group!**")












    # .topic command - Create a private supergroup with Topics enabled
    elif text.startswith(f"{prefix}topic"):
        await YOUAREREGISTERED(event)
        try:
            loading_msg = await event.respond("**𝘚𝘶𝘱𝘦𝘳𝘎𝘳𝘰𝘶𝘱 & 𝘛𝘰𝘱𝘪𝘤𝘴..**")

            owner = await client.get_me()

            group = await client(functions.channels.CreateChannelRequest(
                title=f"SuperGroupAutomated - EhraSelftBot",
                about=f"Automated Creator By {owner.first_name}",
                megagroup=True,
                for_import=True  
            ))

            time.sleep(1)

            chat_id = group.chats[0].id  

            await client(functions.channels.ToggleForumRequest(channel=chat_id, enabled=True))

            invite = await client(functions.messages.ExportChatInviteRequest(chat_id))

            await loading_msg.edit(
                f"✅ **[Private Supergroup](t.me/bitchinhell) Created!**\n"
                f"🔹 **Group Name:** `{f'Discussion - {owner.first_name}'}`\n"
                f"📌 **Topics Enabled:** ✅\n"
                f"🔗 **Join Here:** [Click to Join]({invite.link})",
                link_preview=False
            )

        except Exception as e:
            await event.respond(f"❌ **Failed to create supergroup!**")










    # .upi command - Show the owner's UPI ID
    elif text.startswith(f"{prefix}upi"):
        await YOUAREREGISTERED(event)
        upi_id = config.get("upi_id", None)

        if upi_id:
            await event.respond(f"💰 **[UPI ID](t.me/bitchinhell):** `{upi_id}`\n**Kindly Notify Us After Payment**", link_preview=False)
        else:
            await event.respond("❌ **UPI ID not found!**")









    
    # .b command - Block a user
    elif text.startswith(f"{prefix}b"):
        await YOUAREREGISTERED(event)
        if event.is_reply:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        else:
            args = text.split(" ", 1)
            if len(args) > 1:
                try:
                    user = await client.get_entity(args[1])
                    user_id = user.id
                except:
                    await event.respond("❌ **Invalid username or user ID!**")
                    return
            else:
                await event.respond("❌ **Reply to a user or provide a username/user ID!**")
                return

        try:
            await client(functions.contacts.BlockRequest(user_id))
            await event.respond(f"🚫 **[User Blocked](t.me/bitchinhell)!** (`{user_id}`)", link_preview=False)
        except Exception as e:
            await event.respond(f"❌ **Failed to block user!**")










    # .ub command - Unblock a user
    elif text.startswith(f"{prefix}ub"):
        await YOUAREREGISTERED(event)
        if event.is_reply:
            reply = await event.get_reply_message()
            user_id = reply.sender_id
        else:
            args = text.split(" ", 1)
            if len(args) > 1:
                try:
                    user = await client.get_entity(args[1])
                    user_id = user.id
                except:
                    await event.respond("❌ **Invalid username or user ID!**")
                    return
            else:
                await event.respond("❌ **Reply to a user or provide a username/user ID!**")
                return

        try:
            await client(functions.contacts.UnblockRequest(user_id))
            await event.respond(f"✅ **[User Unblocked](t.me/bitchinhell)!** (`{user_id}`)", link_preview=False)
        except Exception as e:
            await event.respond(f"❌ **Failed to unblock user!**")
















    # .cls command - Clear chat history ONLY for yourself
    elif text.startswith(f"{prefix}cls"):
        await YOUAREREGISTERED(event)
        try:
            await client(functions.messages.DeleteHistoryRequest(
                peer=event.chat_id,
                max_id=0,
                just_clear=True,  # Deletes chat only for YOU
                revoke=False  # Keeps messages for the other person
            ))
            await event.respond("🗑 **[History Cleared](t.me/bitchinhell) (You)!**", link_preview=False)
        except Exception as e:
            await event.respond(f"❌ **Failed to clear chat!**")
















    # .exec command - Delete chat history for BOTH users
    elif text.startswith(f"{prefix}exec"):
        await YOUAREREGISTERED(event)
        try:
            await client(functions.messages.DeleteHistoryRequest(
                peer=event.chat_id,
                max_id=0,
                just_clear=False,  # Deletes for both
                revoke=True  # Removes messages for both users
            ))
            await event.respond("🚨 **[History Cleared](t.me/bitchinhell) (Both)!**", link_preview=False)
        except Exception as e:
            await event.respond(f"❌ **Failed to delete chat for both users!**")















    elif text.startswith(f"{prefix}bio"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        if len(args) < 2:
            await event.respond("❌ **Please provide a new bio!**")
            return

        new_bio = args[1].strip()

        try:
            await client(functions.account.UpdateProfileRequest(about=new_bio))
            await event.respond(f"✅ **[Bio Updated](t.me/bitchinhell)!**", link_preview=False)
        except Exception as e:
            await event.respond(f"❌ **Failed to update bio!**")
















    elif text.startswith(f"{prefix}setstatus"):
        args = text.split(" ", 1)

        if len(args) < 2:
            await event.respond("❌ **Please provide a status!**\n🔹 Example: `.setstatus sleep`")
            return

        status = args[1].strip().lower()

        if status == "reset":
            # Reset the last name (remove status)
            try:
                await client(functions.account.UpdateProfileRequest(last_name=""))
                await event.respond("✅ **Status Reset Successfully!**")
            except Exception as e:
                await event.respond(f"❌ **Failed to reset status!**")
            return

        if status not in ISSTATUSHHH:
            await event.respond(f"❌ **Invalid status!**\n🔹 Available options: {', '.join(ISSTATUSHHH.keys())}")
            return

        # Update last name with selected status
        try:
            await client(functions.account.UpdateProfileRequest(last_name=ISSTATUSHHH[status]))
            await event.respond(f"✅ **Status Updated!**")
        except Exception as e:
            await event.respond(f"❌ **Failed to update status!**")
















    elif text.startswith(f"{prefix}reverse"):
        await YOUAREREGISTERED(event)
        if event.is_reply:
            # Get text from replied message
            reply = await event.get_reply_message()
            text_to_reverse = reply.text if reply.text else None
        else:
            args = text.split(" ", 1)
            text_to_reverse = args[1] if len(args) > 1 else None

        if not text_to_reverse:
            await event.respond("❌ **Please provide text or reply to a message!**\n🔹 Example: `.reverse hello`")
            return

        reversed_text = text_to_reverse[::-1]
        await event.respond(f"🔄 **[Reversed Text](t.me/bitchinhell):** `{reversed_text}`", link_preview=False)














    elif text.startswith(f"{prefix}tts"):
        await YOUAREREGISTERED(event)
        if not event.is_reply:
            await event.respond("❌ **Please reply to a message to convert it to speech!**")
            return

        reply = await event.get_reply_message()
        text_to_speak = reply.text.strip()

        args = text.split(" ", 1)
        if len(args) > 1:
            voice = args[1].strip().lower()
            if voice not in AVAILABLE_VOICES:
                await event.respond(f"❌ **Invalid voice selected! Available voices: {', '.join(AVAILABLE_VOICES.keys())}**")
                return
        else:
            voice = 'en'  

        try:
            tts = gTTS(text=text_to_speak, lang=AVAILABLE_VOICES[voice], slow=False)
            tts.save("ByEHRASelfBot.mp3")
            
            await event.respond("🎤 **[There You Go](t.me/bitchinhell)!**", file="ByEHRASelfBot.mp3", link_preview=False)

            # Clean up the saved file
            os.remove("ByEHRASelfBot.mp3")
        except Exception as e:
            await event.respond(f"❌ **Error converting text to speech!**")


        










    # The love command
    elif text.startswith(f"{prefix}love"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)
        
        if len(args) < 2:
            await event.respond("❌ **Invalid Argument")
            return
        
        if event.is_reply:
            reply = await event.get_reply_message()
            user_name = reply.sender.first_name
        else:
            user_input = args[1].strip()
            try:
                user = await client.get_entity(user_input)
                user_name = user.first_name if user.first_name else "Someone"
            except:
                await event.respond("❌ **User not found!** Please provide a valid username or reply to a message.")
                return
        love_message = "💖 Love you" * 369  # Repeat the phrase 100 times
        
        await event.respond(f"❤️ **Here’s your love, {user_name}:**\n\n{love_message}")












    # Feedback Command
    elif text.startswith(f"{prefix}feedback"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)
        
        if len(args) < 2:
            await event.respond("❌ **Please provide a rating (1-10)!**\n🔹 Example: `.feedback 9`")
            return
        
        try:
            rating = int(args[1])  
            if rating < 1 or rating > 10:
                raise ValueError("**Invalid Rating!**")  
        except ValueError as e:
            await event.respond(f"❌ **Invalid rating!**")
            return

    
        feedback_to_bot = f"""
📬 𝗡𝗲𝘄 𝗙𝗲𝗲𝗱𝗯𝗮𝗰𝗸 𝗥𝗲𝗰𝗲𝗶𝘃𝗲𝗱!

📝 𝗥𝗮𝘁𝗶𝗻𝗴: {rating}/5

📅 𝗦𝗲𝗻𝘁 𝗕𝘆: {event.sender.first_name} (@{event.sender.username if event.sender.username else 'NoUsername'})
🆔 𝗨𝘀𝗲𝗿 𝗜𝗗: {event.sender.id}
        """

    
        try:
        
            url = f"https://api.telegram.org/bot{TOKKKEEENNN}/sendMessage"
            payload = {
                'chat_id': CHANTLEIII,
                'text': feedback_to_bot,
            }

            
            response = requests.post(url, data=payload)

            
            if response.status_code == 200:
                await event.respond("✅ **Thank you for your feedback!**")
            else:
                await event.respond("❌ **Failed to send feedback!** **Please try again later.**")
        except Exception as e:
            await event.respond(f"❌ **Error while sending feedback!**")




















        # .insta Command
    elif text.startswith(f"{prefix}insta"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 1)

        if event.is_reply:
            reply = await event.get_reply_message()
            username = reply.sender.username if reply.sender.username else None
            if not username:
                await event.respond("❌ **Invalid Request**")
                return
        elif len(args) < 2:
            await event.respond("❌ **Please provide an Instagram username!**\n🔹 Example: `.insta username` or reply to a message.")
            return
        else:
            username = args[1].strip()
        loading_msg = await event.respond("**𝘍𝘦𝘵𝘤𝘩𝘪𝘯𝘨..**")

        try:
            
            profile = instaloader.Profile.from_username(L.context, username)

            
            followers = profile.followers
            following = profile.followees
            posts = profile.mediacount
            bio = profile.biography if profile.biography else "N/A"
            creation_date = date(profile.userid)  
            private_account = "✅ True" if profile.is_private else "❌ False"
            business_account = "✅ True" if profile.is_business_account else "❌ False"
            name = profile.full_name if profile.full_name else "N/A"
            pronouns = None
            if "he/him" in bio.lower():
                pronouns = "he/him"
            elif "she/her" in bio.lower():
                pronouns = "she/her"
            elif "they/them" in bio.lower():
                pronouns = "they/them"
            else:
                pronouns = "N/A"
            if followers > 30 and following >= 40 and posts >= 1:
                meta_enable = "✅ True"
            elif (followers >= 30 or following >= 40) and posts <= 2:
                meta_enable = "⚠️ Maybe"
            else:
                meta_enable = "❌ False"
            insta_info = f"""
**[Instagram Profile Info](t.me/bitchinhell)**  

[[ϟ](t.me/bitchinhell)] **Name**: **{name}  **
[[ϟ](t.me/bitchinhell)] **Username**: @{username}
[[ϟ](t.me/bitchinhell)] **Followers**: `{followers} ` 
[[ϟ](t.me/bitchinhell)] **Following**: `{following}  `
[[ϟ](t.me/bitchinhell)] **Posts**: `{posts}`  
[[ϟ](t.me/bitchinhell)] **Bio**: **{bio} ** 
[[ϟ](t.me/bitchinhell)] **Created**: `{creation_date}`  
[[ϟ](t.me/bitchinhell)] **Private**: {private_account}  
[[ϟ](t.me/bitchinhell)] **Business/Professional**: {business_account}  
[[ϟ](t.me/bitchinhell)] **Meta Enable**: {meta_enable}  
[[ϟ](t.me/bitchinhell)] **Pronouns**: {pronouns}  
            """

            await loading_msg.edit(insta_info,link_preview=False)

        except Exception as e:
            await loading_msg.edit(f"❌ **Failed to fetch Instagram profile!**")


















    # Terms of Service Command
    elif text.startswith(f"{prefix}tos"):
        await YOUAREREGISTERED(event)
        tos_message = """
**Terms of Service (TOS)**

1. **Use in Accordance with Telegram's Policies**  
> **You must use this bot in compliance with [Telegram's Terms of Service](https://telegram.org/tos) and [Community Guidelines](https://telegram.org/privacy).**

2. **Account Safety**  
> **Your **Telegram account** is your responsibility. Use this bot at your own risk. If you violate **Telegram's** policies, your account may face restrictions or bans.**

3. **Disclaimer**  
> ****Team EHRA** or the creator of this bot will **not** be held responsible for any **account suspension or loss** that may result from using this bot in violation of Telegram's rules.**

4. **Guidelines for Safe Usage**  
>** Always adhere to **Telegram’s rules** and use this bot responsibly. Respect the platform and protect your account.**

**By using this bot, you acknowledge and accept these terms.**

**Stay safe, follow the rules, and enjoy using the bot responsibly.**

**Thank You**
**Regards,**
**[TEAM EHRA](t.me/bitchinhell)**
        """

        await event.respond(tos_message, link_preview=False)






















    elif text.startswith(f"{prefix}spam"):
        await YOUAREREGISTERED(event)
        args = text.split(" ", 2) 
        spam_count = 69  # Default spam count
        spam_message = f"**This Selfbot By Developed By [Sinner Murphy](t.me/thefuqq) And Powered By [Team EHRA](t.me/bitchinhell)**"  # Default message


        if len(args) > 1:
            if args[1].isdigit(): 
                spam_count = int(args[1])
                if spam_count < 1 or spam_count > 69:
                    await event.respond("❌ **Spam count must be between 1 and 69!**")
                    return
            else:
                spam_message = " ".join(args[1:])
        
        if len(args) > 2:
            spam_message = args[2]

        await event.respond(f"✅ **Spamming `{spam_message}` {spam_count} times**")

        for _ in range(spam_count):
            await event.respond(spam_message)
            await asyncio.sleep(0.08) 






















    # .vouch Command
    elif text.startswith(f"{prefix}vouch"):
        await YOUAREREGISTERED(event)
        if not event.is_private and not event.is_reply:
            await event.respond("❌ **Use this command in DM or by replying to a user!**")
            return

        args = text.split(" ", 2)  

        if len(args) < 3 or not args[1].isdigit():
            await event.respond("❌ **Please provide the deal amount and type.**\n🔹 Example: `.vouch 500 crypto exchange`")
            return

        deal_amount = args[1]  
        deal_type = args[2]  

        if event.is_reply:
            reply = await event.get_reply_message()
            user = await client.get_entity(reply.sender_id)
  
        elif event.is_private:
            user = await client.get_entity(event.chat_id)
        else:
            user = None

        username = f"@{user.username}" if user and user.username else f"[{user.first_name}](tg://user?id={user.id})"

      
        vouch_message = random.choice(LEBSDKE)
        vouch_message = vouch_message.replace("@username", username)  
        vouch_message = vouch_message.replace("{}", deal_amount, 1) 
        vouch_message = vouch_message.replace("{}", deal_type, 1)  

        await event.respond(vouch_message)

























    elif text.startswith(f"{prefix}scam"):
        await YOUAREREGISTERED(event)
        user_id = event.sender_id  

        if user_id in scam_cooldowns:
            time_since_last_use = time.time() - scam_cooldowns[user_id]
            if time_since_last_use < SCAM_COOLDOWN:
                remaining_time = int(SCAM_COOLDOWN - time_since_last_use)
                await event.respond(f"⏳ **Slow down! Try again in {remaining_time} seconds.**")
                return

        scam_channels = JHANTUNIKALOREEE()  

        user = None
        user_id_str = None
        username = "N/A"
        full_name = "Unknown"

        if event.is_reply:
            reply = await event.get_reply_message()
            user = await client.get_entity(reply.sender_id)
        elif len(text.split()) > 1:
            user_input = text.split()[1]
            try:
                if user_input.isdigit(): 
                    user_id_str = user_input
                    user = await client.get_entity(int(user_id_str))
                else:  # Otherwise, assume it's a username
                    user = await client.get_entity(user_input)
            except:
                await event.respond("❌ **User not found! Please reply to a user or enter a valid username/user ID.**")
                return
        else:
            await event.respond("❌ **Reply to a user or provide a username/user ID to check.**")
            return

        if user:
            user_id_str = str(user.id)
            username = f"@{user.username}" if user.username else "N/A"
            full_name = user.first_name if user.first_name else "Unknown"

        scam_cooldowns[user_id] = time.time()


        scanning_message = await event.respond(
            f"🔍 **Searching scam records for `{user_id_str}`...**\n⚠️ This may take a few minutes, please wait..."
        )
        await asyncio.sleep(3)

 
        scam_results = []
        total_channels = len(scam_channels)

        for index, channel in enumerate(scam_channels, start=1):
            try:
                await scanning_message.edit(
                    f"🔍 **Searching scam records for `{user_id_str}`...** ({index}/{total_channels})"
                )

                async for message in client.iter_messages(channel):
                    message_text = message.text if message.text else ""

                    if message.media and hasattr(message, "caption") and message.caption:
                        message_text += "\n" + message.caption 

                    if message.forward and message.forward.original_fwd:
                        if hasattr(message.forward, "message") and message.forward.message:
                            message_text += "\n" + message.forward.message 


                    if user_id_str in message_text or (username != "N/A" and username.lower() in message_text.lower()):
                        scam_name = re.search(r"Scammer Profile Name: (.+)", message_text)
                        scam_username = re.search(r"Scammer Username: (.+)", message_text)
                        scam_id = re.search(r"Scammer ID: (\d+)", message_text)

                        scam_name = scam_name.group(1) if scam_name else full_name
                        scam_username = scam_username.group(1) if scam_username else username
                        scam_id = scam_id.group(1) if scam_id else user_id_str

                        scam_results.append(f"""
🚨 **[Scam Alert](t.me/bitchinhell)!**  
👤 **Scammer Profile Name:** {scam_name}  
👤 **Scammer Username:** {scam_username}  
🆔 **Scammer ID:** `{scam_id}`   
🔴 **Reported in [ScamTG](https://t.me/{channel.split('/')[-1]}/{message.id})**
                        """)
                        break 

                await asyncio.sleep(3)  

            except Exception as e:
                await event.respond(f"⚠️ **Error checking {channel}:**")
                await asyncio.sleep(3)

        if scam_results:
            result_text = "\n\n".join(scam_results)
            await event.respond(result_text, link_preview=False)
        else:
            await event.respond(f"✅ **No scam records found for `{user_id_str}`.** Appears to be a positive profile.")

        await scanning_message.delete()

























        # .cmds Command
    elif text.startswith(f"{prefix}cmds"):
        await YOUAREREGISTERED(event)

        cmds_message = (
    f"**[[⌬](t.me/bitchinhell)]** **Executables In-Range**\n\n"
    
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}cmdmode` → **Change the command prefix.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}dm <user> <message>` → **Send a DM to a user.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}tr <text> <lang>` → **Translate text to a specified language.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}pypi <package>` → **Fetch Python Package Information.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}crn <currency>` → **Get currency exchange rates.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}crypto <coin>` → **Get crypto prices.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}font <style>` → **Convert text into fancy fonts.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}weather <city>` → **Get weather info.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}reset` → **Send an Instagram password reset link.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}mm <user>` → **Create a private group with the user.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}me` → **Get your own account details.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}dev` → **Display developer information.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}tg <username>` → **Get user’s Telegram profile link.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}setname <name>` → **Change your Telegram name.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}calc <expression>` → **Perform a quick calculation.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}tz <timezone>` → **Convert time zones.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}close` → **Close Group.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}left` → **Leave the current group.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}topic` → **Create a discussion topic.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}upi` → **Show UPI Payment Info.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}b <user>` → **Block a user.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}ub <user>` → **Unblock a user.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}cls` → **Clear chat history (your messages).**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}morecmds` → **View More Available Commands.**\n"

    
)



        await event.respond(cmds_message, link_preview=False)



















    elif text.startswith(f"{prefix}morecmds"):
        await YOUAREREGISTERED(event)

        cmds_message = (
    f"**[[⌬](t.me/bitchinhell)]** **More Executables In-Range**\n\n"
    
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}exec` → **Clear Chat History (Both)**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}bio <text>` → **Change your Telegram bio.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}tts` → **Convert text to speech.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}love <username>` → **Express your love.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}feedback <rating>` → **Send feedback.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}insta <username>` → **Get Instagram user info.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}tos` → **Show Terms of Service. [Must Use]**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}spam <text> <count>` → **Spam a message multiple times.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}vouch <user>` → **Vouch for a user. [Premium]**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}sign` → **Developer Sign**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}scam <user>` → **Check if a user is a scammer or not.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}reverse` → **Fun command**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}cmds` → **Display Executables**\n\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}help` → **Help Section. [HELP]**\n"    
    f"**[[⌬](t.me/bitchinhell)]** **VIPs Executables**\n\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}pay` → **Payments Automation.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}gift <user>` → **Send Gifts.**\n"
    f"**[[ϟ](t.me/bitchinhell)]** `{prefix}payinr` → **INR Payments Automated.**\n"
    f"**[AND MANY MORE! STAY CONNECTED!!](t.me/bitchinhell)**"

)



        await event.respond(cmds_message, link_preview=False)
    




























    elif text.startswith(f"{prefix}sign"):
        await YOUAREREGISTERED(event)
        await event.respond("**“𝑨𝒏𝒚𝒕𝒉𝒊𝒏𝒈 𝒕𝒉𝒂𝒕 𝒄𝒂𝒏 𝒈𝒐 𝒘𝒓𝒐𝒏𝒈 𝒘𝒊𝒍𝒍 𝒈𝒐 𝒘𝒓𝒐𝒏𝒈.”**\n~ [𝑀𝑢𝑟𝑝ℎ𝑦](t.me/thefuqq)", link_preview=False)


    









    elif text.startswith(f"{prefix}help"):
        await YOUAREREGISTERED(event)
        help_message = (
            f"**[[⌬](t.me/bitchinhell)]** **[Self-Bot Help](t.me/bitchinhell)**\n\n"
            f"**[[⌬](t.me/bitchinhell)]** **About:**\n"
            f"**[[ϟ](t.me/bitchinhell)]** `This is an advanced self-bot designed for efficiency, automation, and user control.`\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Provides various tools like moderation, information retrieval, automation, and customization.`\n\n"
            
            f"**[[⌬](t.me/bitchinhell)]** **Developers:**\n"
            f"**[[ϟ](t.me/bitchinhell)]** **Owner:** **[Sinner Murphy](t.me/bitchinhell)**\n"
            f"**[[ϟ](t.me/bitchinhell)]** **Powered By:** **[Team EHRA](t.me/bitchinhell)**.\n\n"
            
            f"**[[⌬](t.me/bitchinhell)]** **Caution:**\n"
            f"**[[ϟ](t.me/bitchinhell)]** `This bot is for **personal use only** and should not be misused.`\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Avoid spamming commands excessively to prevent Telegram restrictions.`\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Use responsibly to avoid detection as a self-bot.`\n\n"
            
            f"**[[⌬](t.me/bitchinhell)]** **How Commands Work:**\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Most commands requiring user interaction work with:`\n"
            f"   - **Replying to a message.**\n"
            f"   - **Providing a username** (e.g., `@username`).\n"
            f"   - **Entering a user ID** (e.g., `123456789`).\n"
            f"**[[ϟ](t.me/bitchinhell)]** **Example:** `.scam @username`, `.dm 123456789 Hello`.\n\n"
            
            f"**[[⌬](t.me/bitchinhell)]** **Need More Help?**\n"
            f"**[[ϟ](t.me/bitchinhell)]** Use `{prefix}.cmd` and `{prefix}morecmd` to see a list of all available commands.\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Contact the` **[Bot Owner](t.me/bitchinhell)** `if you encounter issues.`\n\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Must Use The Tos Command Before Using The Bot Further`.\n\n"
            f"**[[ϟ](t.me/bitchinhell)]** `Please Send The Feedbacks Using {prefix}feedback <rating> To Honor The Developer!`.\n\n"
            
        )
        await event.respond(help_message, link_preview=False)






















# async def Sinner():
#     await client.start(config["phone"])
#     await CHECKINGCHALUFRENS()
#     print(f"✅ Self-Bot is Online with prefix `{prefix}`!")
#     await client.run_until_disconnected()



# if __name__ == '__main__':
#     client.loop.run_until_complete(Sinner())    




async def Sinner():
    await client.start(config["phone"])
    print("THIS SCRIPT BY SINNER | @THEFUQQ")
    print("")
    await asyncio.sleep(3)
    print("AVAILABLE FOR FREE!! ENJOY THE SCRIPT AND DO NOT FORGET READ THE TOS USING TOS COMMAND AND DO SEND FEEDBACK!")
    await asyncio.sleep(2)
    print("")
    print("")
    print("")
    await CHECKINGCHALUFRENS()
    print(f"✅ Self-Bot is Online with prefix `{prefix}`!")
    await client.run_until_disconnected()

# ✅ Function to Start the Bot When Imported
def SinnerSelfbot():
    # import asyncio
    # asyncio.run(Sinner())
    client.loop.run_until_complete(Sinner())  

# ✅ Prevent Auto-Execution When Imported
if __name__ == "__main__":
    SinnerSelfbot()















































































































# import importlib.util
# import os

# # Define the __pycache__ folder path
# pycache_folder = "__pycache__"

# # Find the correct .pyc file for pychchelogs
# pyc_filename = next(f for f in os.listdir(pycache_folder) if f.startswith("__pycache__logs") and f.endswith(".pyc"))
# pyc_path = os.path.join(pycache_folder, pyc_filename)

# # Load pychchelogs.pyc dynamically without executing
# spec = importlib.util.spec_from_file_location("__pycache__logs", pyc_path)
# module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module)

# # Now you can access SinnerFreeSelfbot without executing it
# SinnerFreeSelfbot = module.SinnerFreeSelfbot
# # SinnerFreeSelfbot()
# # import os

# # pycache_folder = "__pycache__"
# # print(os.listdir(pycache_folder))  # See what files exist
