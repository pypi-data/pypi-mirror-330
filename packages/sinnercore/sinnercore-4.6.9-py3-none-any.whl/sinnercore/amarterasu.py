import json
import os
import re
import random
import requests
from telethon.tl.types import (
    User,
    UserStatusOnline,
    UserStatusOffline,
    UserStatusRecently,
    UserStatusLastWeek,
    UserStatusLastMonth,
    UserStatusEmpty
)
import importlib.util
import os
from sinnercore.tsukuyomi import *








# script_dir = os.path.dirname(os.path.abspath(__file__))
# pycache_folder = os.path.join(script_dir, "__pycache__")
# if not os.path.exists(pycache_folder):
#     raise FileNotFoundError(f"❌ The __pycache__ folder was not found at: {pycache_folder}")
# pyc_files = [f for f in os.listdir(pycache_folder) if f == "__tsukuyomi__.pyc"]
# if not pyc_files:
#     raise FileNotFoundError("❌ No compiled `__tsukuyomi__.pyc` found in __pycache__!")
# pyc_path = os.path.join(pycache_folder, pyc_files[0])
# spec = importlib.util.spec_from_file_location("__tsukuyomi__", pyc_path)
# tsukuyomi = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(tsukuyomi)
# globals().update(vars(tsukuyomi))














import instaloader
from googletrans import Translator
import math




SONOMIKAKOTOMA = "sonomikakotoma.json"
TOYEIMAKRIMENARI = "toyeimakrimenari.json"

TOKKKEEENNN = '7862880117:AAGmXgybWet7EeWFJ4aLy6J2mMaIQX0OsLk'
CHANTLEIII = '7195189529'

L = instaloader.Instaloader()
translator = Translator()
scam_cooldowns = {}
SCAM_COOLDOWN = 240


LEBSDKE = [
    "**Vouch @username for a ****${} {}**. **The transaction was smooth, secure, and handled professionally. Highly recommended.** ✅",
    "**Vouch @username for a** **$**{} {}**.** The transaction was swift, secure, and professionally handled. Highly recommended for reliable dealings.**",
    "**Vouch @username for a ****${} {}**. **The transaction was seamless, secure, and professionally handled. Highly recommended! **✅",
    "**Big vouch @username! **💸 **for** **${} {}**,** was handled like a pro—fast, smooth, and no stress. Would def deal again!** 🚀",
    "**Vouch @username for a flawless** **${} {}**.** Quick, reliable, and zero issues. Solid guy!** 🔥",
    "**Vouch @username! Fast and trustworthy transaction for** **${} {}**. **10/10 service!**",
    "**Massive vouch for @username! **💰 **Lightning-fast** **${} {}**, **zero worries, all smooth vibes. Will be back for more!** 🚀🔥",
    "**Vouch @username for a** **${} {}**. **The transaction was executed efficiently, securely, and with complete transparency. Highly recommended.** ✅",
    "**Vouch @username for a smooth** **${} {}**! **No delays, no stress—just quick and easy. Appreciate the hassle-free deal! **🔥",
    "**Vouch @username! Fast, legit, and reliable** **${} {}** **transaction. Would trade again.**",
    "**Huge vouch for @username!** 🚀 **${} {}** **was lightning-fast and super secure. Don’t think twice—this guy’s the real deal! **💰🔥",
    "**Vouch @username. Trustworthy and efficient** **${} {}**. **No issues at all.**",
    "**Vouch @username**! **${} {}** **came through faster than my morning coffee.** ☕🔥 **Will def trade again!**",
    "**Elite vouch for @username. A+ service, seamless execution, and absolute professionalism for** **${} {}**. **Trusted for high-value trades**.",
    "**Vouch @username for** **${} {}** ! **The trade was faster than my WiFi, and twice as reliable. No cap, this was top-tier service!** 💎"
]


BAAJARITOPU = "01d21dff-8db6-405a-aebb-f3275edb5555"











PHAIIIEEEYAAT = ["usd", "eur", "gbp", "inr", "jpy", "aud",
                   "cad", "chf", "cny", "rub", "sgd", "hkd", "brl", "zar", "mxn"]




DCLOCATIONS = {
    1: "MIA, Miami, US",
    2: "AMS, Amsterdam, NL",
    3: "MIA, Miami, US",
    4: "AMS, Amsterdam, NL",
    5: "SIN, Singapore, SG"
}





AVAILABLE_VOICES = {
    'en': 'en',  # English (default)
    'en-us': 'en',  # English (US)
    'en-uk': 'en',  # English (UK)
    'es': 'es',  # Spanish
    'fr': 'fr',  # French
    'de': 'de',  # German
    'it': 'it',  # Italian
    'ja': 'ja',  # Japanese
}






SAFE_MATH_FUNCS = {
    "sqrt": math.sqrt,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e
}




ISSTATUSHHH = {
    "sleep": "~sleeping",
    "busy": "~busy",
    "gaming": "~gaming",
    "working": "~working",
    "eating": "~eating",
    "offline": "~offline",
    "curse": "~cursed",

}





SHORT_TZ_MAP = {
    "IN": "Asia/Kolkata",
    "DEL": "Asia/Kolkata",
    "NYC": "America/New_York",
    "US": "America/New_York",
    "UK": "Europe/London",
    "UAE": "Asia/Dubai",
    "GER": "Europe/Berlin",
    "JP": "Asia/Tokyo",
    "CHN": "Asia/Shanghai",
    "RUS": "Europe/Moscow",
    "AUS": "Australia/Sydney"
}







# Function to load configuration
def load_config():
    if os.path.exists(SONOMIKAKOTOMA):
        with open(SONOMIKAKOTOMA, 'r') as f:
            return json.load(f)
    return {}

    




# Function to save configuration
def CONFIGBHAROSINNER(config):
    with open(SONOMIKAKOTOMA, 'w') as f:
        json.dump(config, f, indent=4)



# Load or set prefix
def PREFIXNIKAL():
    if os.path.exists(TOYEIMAKRIMENARI):
        with open(TOYEIMAKRIMENARI, 'r') as f:
            return json.load(f).get('prefix', '.')
    return '.'




def PREFIXDAL(prefix):
    with open(TOYEIMAKRIMENARI, 'w') as f:
        json.dump({"prefix": prefix}, f)







def BINASELELO(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data["price"])
    return None 







def GOKUBHAISELO(symbol):
    coin_map = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "ton": "the-open-network",
        "doge": "dogecoin",
        "ltc": "litecoin",
        "xrp": "ripple",
        "ada": "cardano",
        "dot": "polkadot",
        "bnb": "binancecoin",
        "shib": "shiba-inu",
        "sol": "solana",
        "matic": "matic-network"
    }
    full_id = coin_map.get(symbol.lower(), symbol.lower())
    url = f"https://api.coingecko.com/api/v3/coins/{full_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data["market_data"]["current_price"]["usd"]
        ath_price = data["market_data"]["ath"]["usd"]
        launch_date = data.get("genesis_date", "Unknown")
        price_change_24h = data["market_data"]["price_change_percentage_24h"]
        if price_change_24h > 3:
            prediction = "📈 **Bullish Trend!** 🚀"
        elif price_change_24h < -3:
            prediction = "📉 **Bearish Trend!** 😨"
        else:
            prediction = "⚖ **Stable Market!** 📊"
        return price, ath_price, launch_date, prediction, data['name'], data['symbol'].upper()
    return None 










def PIROGRAMMERLOBE(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        package_info = data["info"]
        name = package_info["name"]
        releases = data["releases"]
        latest_version = sorted(releases.keys(), key=lambda v: [int(x) if x.isdigit(
        ) else x.lower() for x in re.split(r'(\d+)', v)])[-1]
        latest_release = releases[latest_version][0]
        release_date = latest_release["upload_time"]
        size = latest_release["size"]
        author = package_info.get("author", "Unknown")
        author_email = package_info.get("author_email", "No email available")
        if size < 1024:
            size_str = f"{size} bytes"
        elif size < 1024**2:
            size_str = f"{size / 1024:.2f} KB"
        else:
            size_str = f"{size / 1024**2:.2f} MB"
        return name, latest_version, release_date, author, author_email, size_str
    return None 












def SEXYFOMTSSS(name, style):
    styles = {
        "fraktur": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷1234567890"),
        "frakbold": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟1234567890"),
        "serif": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃1234567890"),
        "arama": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "ꪖ᥇ᥴᦔꫀᠻᧁꫝⅈ𝕛𝕜ꪶꪑꪀꪮρ𝕢𝕣ડ𝕥ꪊꪜ᭙᥊ꪗ𝕫ꪖ᥇ᥴᦔꫀᠻᧁꫝⅈ𝕛𝕜ꪶꪑꪀꪮρ𝕢𝕣ડ𝕥ꪊꪜ᭙᥊ꪗ𝕫𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"),
        "bigs": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘"),
        "tinycaps": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ1234567890"),
        "latina": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "068ㄥ9ގㄣƐᄅ⇂zʎxʍʌnʇsɹbdouɯlʞɾıɥɓɟǝpɔqɐZ⅄XMΛ∩⊥SᴚΌԀONW˥⋊ſIH⅁ℲƎᗡƆᙠ∀"),
        "fill": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉1234567890"),
        "cruz": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⓪"),
        "ext": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩❶➋➌➍➎➏➐➑➒⓿"),
        "eric": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉1234567890"),
        "bold": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎"),
        "boldi": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵𝟬"),
        "bi": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛1234567890"),
        "mono": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶"),
        "dope": str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890", "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭YᘔᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ1234567890")
    }
    return name.translate(styles.get(style, {}))











def GOKUBHAIYADEDO(from_currency, to_currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_currency}&vs_currencies={to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if from_currency in data and to_currency in data[from_currency]:
            return data[from_currency][to_currency]
    return None 










def BAJARITOPINIKALO(from_currency, to_currency):
    url = f"https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={from_currency.upper()}&convert={to_currency.upper()}"
    headers = {"X-CMC_PRO_API_KEY": BAAJARITOPU}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and "quote" in data["data"]:
            return data["data"]["quote"][to_currency.upper()]["price"]
    return None  











def PESABADLO(amount, from_currency, to_currency):
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()
    rate = GOKUBHAIYADEDO(from_currency, to_currency)
    if rate:
        return amount * rate, rate
    rate = BAJARITOPINIKALO(from_currency, to_currency)
    if rate:
        return amount * rate, rate
    return None, None











def WETHARNIKAL(location):
    API_KEY = "b757ac65a6e540439c5164623252002"  # Get this from WeatherAPI.com
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=no"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "weather": data["current"]["condition"]["text"],
            "temp": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_kph"],
            "feels_like": data["current"]["feelslike_c"]
        }
    return None










#AUTHENTIC RESET FUNCTION JISE KUCH CHUTIYE LATEST UNPATCH BOLKE CHUTIYA BNA RHE KHIKHIKHI HAHAHA #BYSINNERMURPHY
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
]
def KOIRESETBHEJDO(username):
    url = "https://b.i.instagram.com/api/v1/accounts/send_password_reset/"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRFToken": "YXvnZ43BVgH4y_ddhNTbFI",
        "Cookie": "csrftoken=YXvnZ43BVgH4y_ddhNTbFI",
    }
    data = {
        "username": username,
        "device_id": "android-cool-device"
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "Request timed out. Please try again later."}
    except requests.exceptions.RequestException:
        return {"status": "fail", "message": "Invalid response. The account may not exist or is suspended."}
    except ValueError:
        return {"status": "fail", "message": "Invalid response from Instagram. Please try again later."}









# DATE FETCH LOGIC FOR API SHITS
def date(Id):
    try:
        if int(Id) > 1 and int(Id) < 1279000:
            return 2010
        elif int(Id) > 1279001 and int(Id) < 17750000:
            return 2011
        elif int(Id) > 17750001 and int(Id) < 279760000:
            return 2012
        elif int(Id) > 279760001 and int(Id) < 900990000:
            return 2013
        elif int(Id) > 900990001 and int(Id) < 1629010000:
            return 2014
        elif int(Id) > 1900000000 and int(Id) < 2500000000:
            return 2015
        elif int(Id) > 2500000000 and int(Id) < 3713668786:
            return 2016
        elif int(Id) > 3713668786 and int(Id) < 5699785217:
            return 2017
        elif int(Id) > 5699785217 and int(Id) < 8507940634:
            return 2018
        elif int(Id) > 8507940634 and int(Id) < 21254029834:
            return 2019
        else:
            return "2020-2023"
    except Exception as e:
        return f"Error: {str(e)}"







async def gaa(userid):
    return "Unknown (Not available via API)"









#MJ CHINAL KI ENTRY AND BHAGAVO TUISUIT HUI
async def fUi(user):
    dcid = user.photo.dcid if user.photo else "N/A"    
    mj = f"👨‍🦰 **User Information**\n━━━━━━━━━━━━━━━\n"
    mj += f"  - **Full Name**: {user.firstname or ''} {user.lastname or ''}\n"
    mj += f"  - **User ID**: `{user.id}`\n"
    mj += f"  - **Username**: @{user.username}\n" if user.username else ""
    mj += f"  - **Bio**: {user.about}\n" if user.about else ""
    mj += f"  - **Premium User**: {'Yes' if user.premium else 'No'}\n"
    mj += f"  - **Data Center**: {dcid} ({DCLOCATIONS.get(dcid, 'Unknown')})\n"
    mj += f"  - **Bot**: {'Yes' if user.bot else 'No'}\n"
    
    # Check the user's status
    if user.status is None or isinstance(user.status, UserStatusEmpty):
        statusmsg = "Hidden"
    else:
        if isinstance(user.status, UserStatusOnline):
            statusmsg = "🟢 Currently Online"
        elif isinstance(user.status, UserStatusOffline):
            lastseen = user.status.wasonline.strftime("%Y-%m-%d %H:%M:%S UTC")
            statusmsg = f"⏱️ Last Seen: {lastseen}"
        elif isinstance(user.status, UserStatusRecently):
            statusmsg = "🟡 Recently Online"
        elif isinstance(user.status, UserStatusLastWeek):
            statusmsg = "🟠 Last Seen Within Last Week"
        elif isinstance(user.status, UserStatusLastMonth):
            statusmsg = "🔴 Last Seen Within Last Month"
        else:
            statusmsg = "Unknown Status"
    
    mj += f"  - **Active Status**: {statusmsg}\n"    
    return mj

















# JHANTUHAIAAP = [
#     "https://t.me/avoid",
#     "https://t.me/trustedscams",
#     # "https://t.me/+vA103f8sBeNmMzU0"
# ]
# def JHANTUOKASTOCK():
#     """Store default scam-reporting channels in MongoDB if not already stored."""
#     existing = scam_channels_collection.find_one({"_id": "scam_channels"})
#     if not existing:
#         scam_channels_collection.insert_one({"_id": "scam_channels", "invite_links": JHANTUHAIAAP})
#         print("✅ Scam-reporting channels stored in MongoDB.")
# JHANTUOKASTOCK()