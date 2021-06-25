from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pymongo import MongoClient
from throttling.throtling import isFlood
import configparser
import sys
import os

config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
db_url = config.get("pyrogram", "db_url")
connectDB = MongoClient(db_url)
createDB = connectDB.like_bot


@Client.on_callback_query()
async def callback(client, callback):
    if callback.message:
        if callback.message.edit_date > 1624648602:
            db = createDB[f"{callback.message.message_id}"]
            flood = await isFlood(callback)
            if callback.data == "like" and flood != False:
                user = db.find_one({"USER_ID": f"{callback.from_user.id}"})
                if user:
                    if user["CLICKER"] == "LIKE":
                        db.delete_one({"USER_ID": f"{callback.from_user.id}"})
                        like_button = InlineKeyboardButton(
                            f"❤️ {int(callback.message.reply_markup.inline_keyboard[0][0].text.split(' ')[1]) - 1}",
                            callback_data="like")
                        dislike_button = InlineKeyboardButton(f"{callback.message.reply_markup.inline_keyboard[0][1].text}",
                                                              callback_data="dislike")
                        keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                        await callback.message.edit_reply_markup(keyboard_like)
                    else:
                        await callback.answer("limit")
                else:
                    db.insert_one({"USER_ID": f"{callback.from_user.id}", "CLICKER": "LIKE"}).inserted_id
                    like_button = InlineKeyboardButton(
                        f"❤️ {int(callback.message.reply_markup.inline_keyboard[0][0].text.split(' ')[1]) + 1}",
                        callback_data="like")
                    dislike_button = InlineKeyboardButton(
                        f"{callback.message.reply_markup.inline_keyboard[0][1].text}", callback_data="dislike")
                    keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                    await callback.message.edit_reply_markup(keyboard_like)
                    await callback.answer("Ok")

            elif callback.data == "dislike" and flood != False:
                user = db.find_one({"USER_ID": f"{callback.from_user.id}"})
                if user:
                    if user["CLICKER"] == "DISLIKE":
                        db.delete_one({"USER_ID": f"{callback.from_user.id}"})
                        like_button = InlineKeyboardButton(
                            f"{callback.message.reply_markup.inline_keyboard[0][0].text}",
                            callback_data="like")
                        dislike_button = InlineKeyboardButton(
                            f"💔 {int(callback.message.reply_markup.inline_keyboard[0][1].text.split(' ')[1]) - 1}",
                            callback_data="dislike")
                        keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                        await callback.message.edit_reply_markup(keyboard_like)
                    else:
                        await callback.answer("limit")
                else:
                    db.insert_one({"USER_ID": f"{callback.from_user.id}", "CLICKER": "DISLIKE"}).inserted_id
                    like_button = InlineKeyboardButton(
                        f"{callback.message.reply_markup.inline_keyboard[0][0].text}",
                        callback_data="like")
                    dislike_button = InlineKeyboardButton(
                        f"💔 {int(callback.message.reply_markup.inline_keyboard[0][1].text.split(' ')[1]) + 1}",
                        callback_data="dislike")
                    keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                    await callback.message.edit_reply_markup(keyboard_like)
                    await callback.answer("Ok")
            elif flood == False:
                await callback.answer("No flood pls")
        else:
            await callback.answer("None")
    elif callback.id:
        db = createDB[f"{callback.inline_message_id}"]
        flood = await isFlood(callback)
        if callback.data == "like" and flood != False:
            user = db.find_one({"USER_ID": f"{callback.from_user.id}"})
            likes_dislikes = db.find_one({"INLINE_MESSAGE": "TRUE"})
            if likes_dislikes is None:
                db.insert_one({"INLINE_MESSAGE": "TRUE", "LIKES": "0", "DISLIKES": "0"}).inserted_id
                likes_dislikes = db.find_one({"INLINE_MESSAGE": "TRUE"})
            else:
                likes_dislikes = db.find_one({"INLINE_MESSAGE": "TRUE"})
            if user:
                if user["CLICKER"] == "LIKE":
                    db.delete_one({"USER_ID": f"{callback.from_user.id}"})
                    like_button = InlineKeyboardButton(
                        f"❤️ {int(likes_dislikes['LIKES']) - 1}",
                        callback_data="like")
                    dislike_button = InlineKeyboardButton(f"💔 {likes_dislikes['DISLIKES']}",
                                                          callback_data="dislike")
                    keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                    db.delete_one({"INLINE_MESSAGE": "TRUE"})
                    db.insert_one({"INLINE_MESSAGE": "TRUE", "LIKES": f"{int(likes_dislikes['LIKES']) - 1}", "DISLIKES": f"{likes_dislikes['DISLIKES']}"}).inserted_id
                    await client.edit_inline_reply_markup(callback.inline_message_id, keyboard_like)
                else:
                    await callback.answer("limit")
            else:
                db.insert_one({"USER_ID": f"{callback.from_user.id}", "CLICKER": "LIKE"}).inserted_id
                like_button = InlineKeyboardButton(
                    f"❤️ {int(likes_dislikes['LIKES']) + 1}",
                    callback_data="like")
                dislike_button = InlineKeyboardButton(
                    f"💔 {likes_dislikes['DISLIKES']}", callback_data="dislike")
                keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                db.delete_one({"INLINE_MESSAGE": "TRUE"})
                db.insert_one({"INLINE_MESSAGE": "TRUE", "LIKES": f"{int(likes_dislikes['LIKES']) + 1}",
                               "DISLIKES": f"{likes_dislikes['DISLIKES']}"}).inserted_id
                await client.edit_inline_reply_markup(callback.inline_message_id, keyboard_like)
                await callback.answer("Ok")

        elif callback.data == "dislike" and flood != False:
            user = db.find_one({"USER_ID": f"{callback.from_user.id}"})
            likes_dislikes = db.find_one({"INLINE_MESSAGE": "TRUE"})
            if likes_dislikes is None:
                db.insert_one({"INLINE_MESSAGE": "TRUE", "LIKES": "0", "DISLIKES": "0"}).inserted_id
                likes_dislikes = db.find_one({"INLINE_MESSAGE": "TRUE"})
            else:
                likes_dislikes = db.find_one({"INLINE_MESSAGE": "TRUE"})
            if user:
                if user["CLICKER"] == "DISLIKE":
                    db.delete_one({"USER_ID": f"{callback.from_user.id}"})
                    like_button = InlineKeyboardButton(
                        f"❤️ {likes_dislikes['LIKES']}",
                        callback_data="like")
                    dislike_button = InlineKeyboardButton(f"💔 {int(likes_dislikes['DISLIKES']) - 1}",
                                                          callback_data="dislike")
                    keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                    db.delete_one({"INLINE_MESSAGE": "TRUE"})
                    db.insert_one({"INLINE_MESSAGE": "TRUE", "LIKES": f"{likes_dislikes['LIKES']}",
                                   "DISLIKES": f"{int(likes_dislikes['DISLIKES']) - 1}"}).inserted_id
                    await client.edit_inline_reply_markup(callback.inline_message_id, keyboard_like)
                else:
                    await callback.answer("limit")
            else:
                db.insert_one({"USER_ID": f"{callback.from_user.id}", "CLICKER": "DISLIKE"}).inserted_id
                like_button = InlineKeyboardButton(
                    f"❤️ {likes_dislikes['LIKES']}",
                    callback_data="like")
                dislike_button = InlineKeyboardButton(
                    f"💔 {int(likes_dislikes['DISLIKES']) + 1}", callback_data="dislike")
                keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
                db.delete_one({"INLINE_MESSAGE": "TRUE"})
                db.insert_one({"INLINE_MESSAGE": "TRUE", "LIKES": f"{likes_dislikes['LIKES']}",
                               "DISLIKES": f"{int(likes_dislikes['DISLIKES']) + 1}"}).inserted_id
                await client.edit_inline_reply_markup(callback.inline_message_id, keyboard_like)
                await callback.answer("Ok")
        elif flood == False:
            await callback.answer("No flood pls")

@Client.on_inline_query()
async def inline_query(client, query):
    like_button = InlineKeyboardButton(f"❤️ 0", callback_data="like")
    dislike_button = InlineKeyboardButton(f"💔 0", callback_data="dislike")
    keyboard_like = InlineKeyboardMarkup([[like_button, dislike_button]])
    if len(query.query) > 0:
        await client.answer_inline_query(inline_query_id=query.id, results=[InlineQueryResultArticle(title="Like ❤️",
                                                                           input_message_content=
                                                                           InputTextMessageContent(message_text=f"{query.query}"),
                                                                           reply_markup=keyboard_like)])
    else:
        await client.answer_inline_query(inline_query_id=query.id, results=[InlineQueryResultArticle(title="Write text message️",
                                                                                                     input_message_content=
                                                                                                     InputTextMessageContent(
                                                                                                         message_text="Write text message️"))])

