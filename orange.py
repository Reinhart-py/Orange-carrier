#!/usr/bin/env python3
import os
import json
import asyncio
import logging
import sys
import threading
import time
import re
from typing import List, Dict, Any, Optional

import httpx
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

CONFIG_FILE = "orange_config.json"
STOP_EVENT = threading.Event()

def display_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    header = f"""
\x1b[38;5;208m   ___                 __         __  __                       
\x1b[38;5;208m  / _ \___ ___________/ /_  ___ _/ /_/ /  __ _  ___ ____ ____  
\x1b[38;5;208m / // / _ `/ __/ __/ _  / / _ `/ __/ _ \/  ' \/ _ `/ _ `/ -_) 
\x1b[38;5;208m/____/\_,_/_/ /_/  \_,_/  \_, /_/\__/_//_/_/_/\_,_/\_, /\__/  
\x1b[38;5;208m                        /___/                    /___/       

\x1b[38;5;226m                 Made by \x1b[1mReinhart aka kiri\x1b[0m
\x1b[38;5;123m              Telegram: \x1b[4m\x1b]8;;tg://openmessage?user_id=1354754957\x07tg://openmessage?user_id=1354754957\x1b]8;;\x07\x1b[0m
\x1b[38;5;117m              Portfolio: \x1b[4m\x1b]8;;https://reinhart.pages.dev/\x07https://reinhart.pages.dev/\x1b]8;;\x07\x1b[0m
\x1b[38;5;208m{'─' * 60}\x1b[0m
"""
    sys.stdout.write(header)
    sys.stdout.flush()

def visible_len(s: str) -> int:
    return len(re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', s))

def ui_thread_manager():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\x1b[?25l")
    
    story = [
        "", "", "", "",
        "\x1b[3mYour bot is running in the background...\x1b[0m",
        "\x1b[3m...but while you wait, let me tell you a story.\x1b[0m",
        "", "",
        "\x1b[38;5;220mA mom visits her son for dinner...",
        "...who lives with a girl as a roommate.",
        "",
        "During the meal, his mother couldn't help but notice",
        "how pretty his roommate was.",
        "",
        "She had long been suspicious of a relationship between the two,",
        "and this only made her more curious.",
        "",
        "Over the course of the evening, watching them interact,",
        "she started to wonder if there was more between them.",
        "",
        "\x1b[38;5;198mReading his mom's thoughts, the son volunteered,",
        "'\x1b[3mI know what you must be thinking,'\x1b[0m",
        "'\x1b[3mbut I assure you, we are just roommates.'\x1b[0m",
        "", "",
        "About a week later, his roommate came to him saying,",
        "'\x1b[3mEver since your mother came to dinner,'\x1b[0m",
        "'\x1b[3mI've been unable to find the silver plate.'\x1b[0m",
        "'\x1b[3mYou don't suppose she took it, do you?'\x1b[0m",
        "",
        "He said, 'Well I doubt it, but I'll email her just to be sure!'",
        "He sat down and wrote:",
        "",
        "\x1b[38;5;117mDear Mom,",
        "After your visit, the silver plate has been missing.",
        "",
        "I'm not saying you DID take the silver plate,",
        "and I'm not saying you DIDN'T take it...",
        "...but the fact remains that it has been missing since you were here.",
        "",
        "Love, your Son.\x1b[0m",
        "", "",
        "Several days later, he received an email from his mother.",
        "It read:",
        "",
        "\x1b[38;5;201mDear Son,",
        "",
        "I'm not saying that you DO sleep with your roommate,",
        "and I'm not saying that you DON'T sleep with her...",
        "",
        "...but the fact remains that if she was sleeping in her \x1b[1mOWN\x1b[0m\x1b[38;5;201m bed,",
        "...she would have found the silver plate by now, under her pillow.",
        "",
        "Love, Mom.\x1b[0m",
        "", "",
        "\x1b[38;5;226m***** The End *****\x1b[0m",
        "",
        "\x1b[3mHope you enjoyed the story.\x1b[0m",
        "\x1b[3mWill see ya next time.\x1b[0m",
    ]
    
    width, height = os.get_terminal_size()
    on_screen_lines = []
    
    while story and not STOP_EVENT.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if not on_screen_lines or on_screen_lines[-1]['y'] < height - 2:
            on_screen_lines.append({'text': story.pop(0), 'y': height})
        
        active_lines = []
        for line_info in on_screen_lines:
            y_pos = line_info['y']
            if y_pos > -2:
                padding = " " * int((width - visible_len(line_info['text'])) / 2)
                sys.stdout.write(f"\x1b[{y_pos};1H{padding}{line_info['text']}\x1b[0m")
                line_info['y'] -= 1
                active_lines.append(line_info)
        
        on_screen_lines = active_lines
        sys.stdout.flush()
        time.sleep(0.7)

    display_header()
    header_height = "\n".join(sys.stdout.getvalue().splitlines()).count('\n') if hasattr(sys.stdout, 'getvalue') else 12

    runners = ["🏃", "🏃💨", "💨🏃"]
    i = 0
    while not STOP_EVENT.is_set():
        runner = runners[i % len(runners)]
        line = f"  \x1b[38;5;46m{runner}\x1b[0m Bot is running... (Press Ctrl+C to exit)"
        sys.stdout.write(f"\x1b[{header_height + 2};1H\x1b[K{line}")
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1

    sys.stdout.write("\x1b[?25h")

def tv_shut_off_animation():
    width, height = os.get_terminal_size()
    mid_y = height // 2
    for i in range(width // 2):
        line = " " * i + "█" * (width - 2 * i) + " " * i
        sys.stdout.write(f"\x1b[{mid_y};1H{line}")
        sys.stdout.flush()
        time.sleep(0.005)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for i in range(mid_y):
        sys.stdout.write(f"\x1b[{i};1H" + " " * width)
        sys.stdout.write(f"\x1b[{height - i};1H" + " " * width)
        sys.stdout.flush()
        time.sleep(0.01)
    
    sys.stdout.write(f"\x1b[{mid_y};{width // 2}H·")
    sys.stdout.flush()
    time.sleep(0.2)
    os.system('cls' if os.name == 'nt' else 'clear')

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("orange-bot")

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_config(config):
    with open(CONFIG_FILE, 'w') as f: json.dump(config, f, indent=2)

def setup_wizard():
    print("\n\x1b[38;5;11mFirst run or busted config. Let's get you set up.\x1b[0m")
    token = input("Enter BOT_TOKEN: ").strip()
    chat_id = input("Enter main CHAT_ID (for CDRs): ").strip()
    log_chat_id = input("Enter LOG_CHAT_ID (optional, for errors/status): ").strip()
    accounts = []
    print("\nEnter accounts. Press Enter on an empty email to finish.")
    while True:
        email = input(f"  Account {len(accounts) + 1} Email: ").strip()
        if not email: break
        password = input(f"  Account {len(accounts) + 1} Password: ").strip()
        accounts.append({"email": email, "password": password})
    
    config = {"BOT_TOKEN": token, "CHAT_ID": chat_id, "LOG_CHAT_ID": log_chat_id, "ACCOUNTS": accounts}
    save_config(config)
    print("\n\x1b[38;5;46mConfig locked in. Booting up...\x1b[0m")
    time.sleep(1)
    return config

def extract_token_from_html(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    inp = soup.find("input", {"name": "_token"})
    return inp["value"] if inp and inp.get("value") else None

async def fetch_cdr_for_account(client: httpx.AsyncClient, email: str, password: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    r = await client.get("https://www.orangecarrier.com/login")
    token = extract_token_from_html(r.text)
    payload = {"email": email, "password": password}
    if token: payload["_token"] = token

    r2 = await client.post("https://www.orangecarrier.com/login", data=payload, follow_redirects=True)
    if not ("logout" in r2.text.lower() or "dashboard" in r2.text.lower()) and r2.url.path.endswith("/login"):
        raise Exception(f"Login failed for {email}. Check credentials.")

    api_resp = await client.get("https://www.orangecarrier.com/CDR/mycdrs?start=0&length=50")
    if api_resp.status_code != 200: return results
    
    j = api_resp.json()
    data = j.get("data") or j.get("aaData", [])
    seen_ids_this_run = set()
    for row in data:
        if isinstance(row, list):
            cli, to_num, time_str, duration, call_type = (str(row[i]) if i < len(row) else "" for i in range(5))
        elif isinstance(row, dict):
            cli, to_num, time_str, duration, call_type = (str(row.get(k,"")) for k in ["cli","to","time","duration","type"])
        else: continue
        
        uid = f"{email}_{cli}_{time_str}"
        if uid not in seen_ids_this_run:
            results.append({"id": uid, "cli": cli, "to": to_num, "time": time_str, "duration": duration, "type": call_type, "account": email})
            seen_ids_this_run.add(uid)
    return results

async def send_log(app: Application, log_chat_id: Optional[int], message: str):
    if not log_chat_id: return
    try: await app.bot.send_message(chat_id=log_chat_id, text=message, parse_mode="Markdown")
    except Exception: pass

async def send_record_to_telegram(app: Application, chat_id: int, rec: Dict[str, Any]):
    text = (f"👤 **Account:** `{rec.get('account')}`\n"
            f"📞 **CLI:** `{rec.get('cli')}`\n"
            f"➡️ **To:** `{rec.get('to')}`\n"
            f"⏱️ **Time:** `{rec.get('time')}`\n"
            f"⏳ **Duration:** `{rec.get('duration')}`\n"
            f"📌 **Type:** `{rec.get('type')}`")
    await app.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

async def account_worker(app: Application, acc: Dict[str, str], chat_id: int, log_chat_id: Optional[int], seen_ids: set):
    email, password = acc.get("email"), acc.get("password")
    if not email or not password: return

    async with httpx.AsyncClient(timeout=30.0, headers={"User-Agent": "Mozilla/5.0"}) as client:
        while not STOP_EVENT.is_set():
            try:
                records = await fetch_cdr_for_account(client, email, password)
                for rec in records:
                    if rec["id"] not in seen_ids:
                        seen_ids.add(rec["id"])
                        await send_record_to_telegram(app, chat_id, rec)
            except Exception as e:
                await send_log(app, log_chat_id, f"🚨 **WORKER ERROR** for `{email}`:\n`{e}`")
            await asyncio.sleep(10)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Bot is operational. CDRs are being monitored.")

def main():
    display_header()
    cfg = load_config()
    if cfg:
        print("\x1b[38;5;220mExisting config found. \x1b[0m")
        action = input("Edit? (y/N): ").lower().strip()
        if action == 'y': 
            display_header()
            cfg = setup_wizard()
    else:
        cfg = setup_wizard()

    BOT_TOKEN = cfg.get("BOT_TOKEN")
    CHAT_ID = int(cfg["CHAT_ID"]) if cfg.get("CHAT_ID", "").lstrip('-').isdigit() else None
    LOG_CHAT_ID = int(cfg["LOG_CHAT_ID"]) if cfg.get("LOG_CHAT_ID", "").lstrip('-').isdigit() else None
    ACCOUNTS = cfg.get("ACCOUNTS", [])

    if not all([BOT_TOKEN, CHAT_ID, ACCOUNTS]):
        print("\x1b[38;5;196mCritical config missing. Can't run. Fix orange_config.json.\x1b[0m")
        return

    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).setLevel(logging.CRITICAL + 1)

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))

    seen_ids = set()

    async def post_init(_: Application):
        await send_log(app, LOG_CHAT_ID, "✅ **Bot Started**\nMonitoring for new CDRs...")
        for acc in ACCOUNTS:
            asyncio.create_task(account_worker(app, acc, CHAT_ID, LOG_CHAT_ID, seen_ids))
    app.post_init = post_init
    
    animation_thread = threading.Thread(target=ui_thread_manager, daemon=True)
    animation_thread.start()

    try:
        app.run_polling(drop_pending_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        STOP_EVENT.set()
        animation_thread.join(timeout=2)
        
        tv_shut_off_animation()
        
        loop = asyncio.get_event_loop()
        shutdown_task = send_log(app, LOG_CHAT_ID, "🛑 **Bot Shutting Down**")
        if loop.is_running() and not loop.is_closed():
            loop.run_until_complete(shutdown_task)

        display_header()
        print("\n\x1b[38;5;196mBot stopped. Cya.\x1b[0m")

if __name__ == "__main__":
    main()