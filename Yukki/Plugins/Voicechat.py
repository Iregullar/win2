import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from config import get_queue
from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app, db_mem, userbot
from Yukki.Database import get_active_chats, is_active_chat
from Yukki.Decorators.checker import checker, checkerCB
from Yukki.Inline import primary_markup

from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)

loop = asyncio.get_event_loop()

__MODULE__ = "Katıl/Ayrıl"
__HELP__ = """

**Not:**
Sadece Yardımcı Kullanıcıları için


/joinassistant [Sohbet Kullanıcı Adı veya Sohbet id]
- Asistanı Gruba Ekler.

/leaveassistant [Sohbet Kullanıcı Adı veya Sohbet id]
- Asistan gruptan ayrılacak.

/leavebot [Sohbet Kullanıcı Adı veya Sohbet id]
- Bot özel sohbeti bırakacak.

"""



@app.on_callback_query(filters.regex("pr_go_back_timer"))
async def pr_go_back_timer(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            buttons = primary_markup(videoid, user_id, dur_left, duration_min)
            await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
             
    
    

@app.on_callback_query(filters.regex("timer_checkup_markup"))
async def timer_checkup_markup(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            return await CallbackQuery.answer(
                f"Remaining {dur_left} out of {duration_min} Mins.",
                show_alert=True,
            )
        return await CallbackQuery.answer(f"Çalmıyor.", show_alert=True)
    else:
        return await CallbackQuery.answer(
            f"Etkin Sesli Sohbet Yok", show_alert=True
        )


@app.on_message(filters.command("queue"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("Lütfen Bekleyin... Sıraya Alıyorum..")
        dur_left = db_mem[message.chat.id]["left"]
        duration_min = db_mem[message.chat.id]["total"]
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit(f"Sırada Hiçbir Şey Yok")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        ### Results
        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**Sıraya Alınmış Liste**\n\n"
        msg += "**Şu Anda Yürütülüyor:**"
        msg += "\n▶️" + current_playing[:30]
        msg += f"\n   ╚Tarafından:- {user_name}"
        msg += f"\n   ╚Süre:- Remaining `{dur_left}` out of `{duration_min}` Dakika."
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**Sıradaki:**"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n⏸️{name}"
                msg += f"\n   ╠Süre : {dur}"
                msg += f"\n   ╚Tarafından istenen : {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption=f"**çıktı:**\n\n`Sıraya Alınmış Liste`",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"Sırada Hiçbir Şey Yok")


@app.on_message(filters.command("activevc") & filters.user(SUDOERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**Hata:-** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Özel Grup"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("Etkin Sesli Sohbet Yok")
    else:
        await message.reply_text(
            f"**Etkin Sesli Sohbetler:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command("joinassistant") & filters.user(SUDOERS))
async def basffy(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Kullanım:**\n/joinassistant [Sohbet Kullanıcı Adı veya Sohbet Kimliği]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.join_chat(chat)
    except Exception as e:
        await message.reply_text(f"Başarısız\n**Olası sebep olabilir**:{e}")
        return
    await message.reply_text("Katıldı.")


@app.on_message(filters.command("leavebot") & filters.user(SUDOERS))
async def baaaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Kullanım:**\n/leavebot [Sohbet Kullanıcı Adı veya Sohbet Kimliği]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Başarısız\n**Olası sebep olabilir**:{e}")
        print(e)
        return
    await message.reply_text("Bot sohbeti başarıyla bıraktı")


@app.on_message(filters.command("leaveassistant") & filters.user(SUDOERS))
async def baujaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Kullanım:**\n/leave [Sohbet Kullanıcı Adı veya Sohbet Kimliği]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Başarısız\n**Olası sebep olabilir**:{e}")
        return
    await message.reply_text("Left.")
