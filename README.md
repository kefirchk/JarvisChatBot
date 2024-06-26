## GUIDE

---

### Installing requirements

---

***Step 1:***

    pip install -r requirements.txt

***Step 2:***

Create a **.env** file in the project directory and fill it with your data:
    
    TELEGRAM_BOT_TOKEN         - your Telegram bot token
    OPENAI_API_TOKEN           - your token received from OpenAI
    ASSISTANT_ID               - assistant id of OpenAI
    DB_HOST                    - ip address of your database
    DB_PORT                    - port of database
    DB_USER                    - user name (owner) of database
    DB_PASS                    - password for access to database
    DB_NAME                    - database name
    AMPLITUDE_API_KEY          - api key for amplitude analytics
    REDIS_HOST                 - ip address for Redis
    REDIS_PORT                 - port for Redis
    REDIS_PASS                 - password for Redis

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

### Deploying a bot via Docker

---

    docker build -t jarvis_telegram_bot .          # Explanations below
    docker-compose up -d redis                     # Deploy Redis, Posgres and Telegram bot (Jarvis)

###### Explanation:

**docker build**:

This part of the command tells Docker to build (create) the image based on the instructions in the Dockerfile.

**-t jarvis_telegram_bot**:

The -t (or --tag) option specifies a tag for the image being created.
A tag consists of a name and, optionally, a version in the format name:tag.
In this case, the image will be called "*jarvis_telegram_bot*". If a version
(tag) is not specified, Docker defaults to the "_latest_" tag.

**.** (dot):

This part specifies the build context. The dot denotes the current directory,
meaning Docker will look for the Dockerfile and all necessary files in the
current directory to create the image.    

---

### Author

---
_Designed by Alexei Klimovich, 2024_
