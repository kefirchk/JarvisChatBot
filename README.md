## GUIDE

---

### Installing requirements

---

***Step 1:***

    pip install -r requirements.txt

***Step 2:***

Create a **.env** file in the project directory and fill it with your data:
    
    TELEGRAM_BOT_TOKEN         - your Telegram bot token
    OPENAI_API_TOKEN             - your token received from OpenAI
    ASSISTANT_ID               - assistant id of OpenAI
    DB_HOST                    - ip address of your database
    DB_PORT                    - port of database
    DB_USER                    - user name (owner) of database
    DB_PASS                    - password for access to database
    DB_NAME                    - database name

***Step 3:***

You can create a virtual environment.

###### *Linux / macOS:*

    python3 -m venv venv
    source venv/bin/activate

###### *Windows:*

    python -m venv venv
    source venv/Scripts/activate

---

### Launch

---

    python bot.py

**P.S.** If you have message *"Unfortunately, using a chatbot is prohibited in your region :("* turn on VPN

---

### Author

---
_Designed by Alexei Klimovich, 2024_
