# OrangeCarrier Telegram Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Operational-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License">
</p>

A Python bot for real-time OrangeCarrier CDR monitoring and alerting via Telegram. 


**features?***
Monitors multiple accounts , Set it once and Runs forever , easy to edit if you want, A one-time funny unnecessary story intro cuz why not ? Terminal stays clean. Critical alerts are sent to a dedicated log channel , Instant CDR notifications sent to your designated Telegram chat.

### Tech Stack
*   **Python 3**
*   **`python-telegram-bot`**
*   **`httpx`**
*   **`beautifulsoup4`**

---

### Quick Start: All-in-One Command

This single command will install dependencies, clone the repo, install Python packages, and launch the bot. Designed for Termux but easily adaptable. ( i might upload a simplified version later cuz this one is fu*ked up ) 

```bash
pkg update && pkg upgrade -y && pkg install git python -y && git clone https://github.com/Reinhart-py/Orange-carrier.git && cd Orange-carrier && pip install -r requirements.txt && python run.py
```


**Configuration**

The bot uses a persistent orange_config.json file to store your credentials.

First Run: The command above will launch a setup TUI . You will be prompted to enter your BOT_TOKEN, CHAT_ID, optional LOG_CHAT_ID, and account details.

On Next Run: The bot will load the existing config and ask if you want to edit it (Edit? (y/N)). Pressing Enter will run the bot with the saved credentials.

------------------------------


**Operation**

The bot runs silently in the background after a brief cinematic intro. All operational logs and errors are sent to the LOG_CHAT_ID if configured.

To stop the bot, press Ctrl+C. ( it'll stop within few seconds with OLD school TV animation .


credit goes to me , your Reinhart 
