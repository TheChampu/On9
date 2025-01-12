import os

API_ID = os.getenv("API_ID", "29893020") # Get it from my.telegram.org
API_HASH = os.getenv("API_HASH", "28e79037f0b334ef0503466c53f08af5") # Get it from my.telegram.org
SESSION = os.getenv("SESSION", "BQHIIZwAeiOpebTn0fnJIVq4MyS13vemdF8pn_tsVjU24aqtfAf2fiEyrinCkfEDTMT-RAqi5ccu3ezTfNjd0XzkH0TgF3D2HHma8C7SV7vPN0kt_jJDmyWwZEYidAS3aeEowCbapwfqx6f1i5gGMipvwMwd6GRt8CrC_ezUZlQKmLVDYhT0gksAVaHOd7-oxcqSLnmCgIrIeeUzEfaIEkX46Sn9AQ-waAKUWm_p96Y45eaL56oZv1HuQGdMzj-1pYhCDPFGZ_tOklh6keNjahVhQulk5mYQ19WzZTN-_Fekz3KmWczUq6S4oKz36eB5wZ8AV9pO8buBvsEosEtRWQmbq2fDagAAAAGTViY_AA") # Pyrogram Session String (Run session.py to get)
GENAI_API_KEY = os.getenv("GENAI_API_KEY") # Get it from https://makersuit.google.com/
TG_NAME = os.getenv("TG_NAME", "Champu") # Your Telegram Name (Needed if you wanna use One9word plugins)
DEPLOY_HOOK = os.getenv("DEPLOY_HOOK") # Get it from render.com if you are hosting this bot to RENDER 
PREFIX = os.getenv("PREFIX", ".") # Command Prefix 
ADMIN = int(os.getenv("ADMIN", 6399386263)) # Owner User_ID
