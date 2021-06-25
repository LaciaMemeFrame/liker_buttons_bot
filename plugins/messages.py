from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import configparser
import sys
import os

config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
db_url = config.get("pyrogram", "db_url")
connectDB = MongoClient(db_url)
createDB = connectDB.like_bot


@Client.on_message(filters.command(["start", "start@liker_button_bot"])
                   & filters.private)
async def start(client, message):
    await message.reply_text("Add me to the channel and give me permission to edit posts!")


@Client.on_message(filters.channel)
async def channel_message(client, message):
    if message.edit_date is None and message.via_bot is None:
        like_button = InlineKeyboardButton(f"❤️ 0", callback_data="like")
        dislike_button = InlineKeyboardButton(f"💔 0", callback_data="dislike")
        keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
        await message.edit_reply_markup(keyboard_like)