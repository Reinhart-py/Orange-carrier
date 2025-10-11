# OrangeCarrier Tg bot

A Python bot for real-time OrangeCarrier CDR monitoring and alerting via Telegram. Built to run silently .

### Features

*   **⚡️ Asynchronous Core:** Monitors multiple accounts without breaking a sweat.
*   **💾 Persistent Config:** Set it once. Runs forever. Edit on the fly.
*   **🎬 Cinematic UI:** A one-time story intro and a silent, animated running status.
*   **🤫 Silent Operation:** Terminal stays clean. Critical alerts are sent to a dedicated log channel.
*   **🚀 Real-time Alerts:** Instant CDR notifications sent to your designated Telegram chat.

### Tech Stack

*   **Python 3**
*   **`python-telegram-bot`**
*   **`httpx`**
*   **`BeautifulSoup4`**

### Setup

Get it running in three steps.

1️⃣ **Clone the repo:**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name```


2️⃣**Install the goods**

code
```Bash
pip install python-telegram-bot httpx beautifulsoup4```

3️⃣**Fire it up**:
code
```Bash
python your_script_name.py```





**Configuration**

On the first run, the script will launch a setup wizard to create your orange_config.json. You'll be prompted for your bot token, chat IDs, and account credentials. ( log group is optional)

On subsequent runs, it will use the saved config and give you the option to edit. All business happens in the background.
To stop the bot, press Ctrl+C.
