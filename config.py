from os import environ

API_ID = int(environ.get("API_ID", "977080"))
API_HASH = environ.get("API_HASH", "0c20c4265501492a1513f91755acd42b")
BOT_TOKEN = environ.get("BOT_TOKEN", "6113221657:AAGezKFTnAYwOyUNMX1FwLtPMVcybouxOH8")
ADMIN = int(environ.get("ADMIN", "399726799"))          
CAPTION = environ.get("CAPTION", "")
DESTINATION_CHANNEL = int(environ.get("DESTINATION_CHANNEL", "-1001919589838"))
SOURCE_CHANNEL = int(environ.get("SOURCE_CHANNEL", "-1001960862288"))
DB_URL  = environ.get("DB_URL","mongodb+srv://abcd:abcd@cluster0.jmkqvnb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") # ⚠️ Required

# for thumbnail ( back end is MrMKN brain 😉)
DOWNLOAD_LOCATION = "./DOWNLOADS"

ACCESS = [""]
