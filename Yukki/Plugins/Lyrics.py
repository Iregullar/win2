import re
import os

import lyricsgenius
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch

from Yukki import MUSIC_BOT_NAME, app

__MODULE__ = "Şarkı Sözleri"
__HELP__ = """

/Lyrics [Müzik Adı]
- Web'de belirli Müzik için Şarkı Sözlerini arar.

**Not**:
Şarkı sözlerinin satır içi düğmesinde bazı hatalar var. Sonuçların sadece %50'sini arar. Bunun yerine, çalınan herhangi bir müzik için şarkı sözleri istiyorsanız komutu kullanabilirsiniz.

"""


@app.on_callback_query(filters.regex(pattern=r"lyrics"))
async def lyricssex(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    try:
        id, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Hata Oluştu\n**Olası sebep şunlar olabilir**:{e}"
        )
    url = f"https://www.youtube.com/watch?v={id}"
    print(url)
    try:
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = result["title"]
    except Exception as e:
        return await CallbackQuery.answer(
            "Ses bulunamadı. Youtube sorunları.", show_alert=True
        )
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    t = re.sub(r"[^\w]", " ", title)
    y.verbose = False
    S = y.search_song(t, get_full_info=False)
    if S is None:
        return await CallbackQuery.answer(
            "Şarkı sözleri bulunamadı:p", show_alert=True
        )
    await CallbackQuery.message.delete()
    userid = CallbackQuery.from_user.id
    usr = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    xxx = f"""
**Şarkı Sözleri Arama {MUSIC_BOT_NAME} Tarafından Desteklenmektedir**

**Tarafından Arandı:-** {usr}
**Aranan Şarkı:-** __{title}__

**Şarkı Sözleri Bulundu:-** __{S.title}__
**Sanatçı:-** {S.artist}

**__Sözler:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await CallbackQuery.message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n\n`Lyrics`",
            quote=False,
        )
        os.remove(filename)
    else:
        await CallbackQuery.message.reply_text(xxx)


@app.on_message(filters.command("lyrics"))
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Kullanım:**\n\n/lyrics [Müzik Adı]")
    m = await message.reply_text("Şarkı Sözleri Aranıyor")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("Şarkı sözleri bulunamadı:p")
    xxx = f"""
**Şarkı Sözleri Arama {MUSIC_BOT_NAME} Tarafından Desteklenmektedir**

**Aranan Şarkı:-** __{query}__
**Şarkı Sözleri Bulundu:-** __{S.title}__
**Sanatçı:-** {S.artist}

**__Sözler:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n\n`Lyrics`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)
    
