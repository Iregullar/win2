import asyncio
import importlib
import os
import re

from config import LOG_GROUP_ID
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from Yukki import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME,
                   BOT_USERNAME, SUDOERS, app, db, userbot)
from Yukki.Core.Logger.Log import (startup_delete_last, startup_edit_last,
                                   startup_send_new)
from Yukki.Core.PyTgCalls.Yukki import run
from Yukki.Database import get_active_chats, get_sudoers, remove_active_chat
from Yukki.Inline import private_panel
from Yukki.Plugins import ALL_MODULES
from Yukki.Utilities.inline import paginate_modules

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
    with console.status(
        "[magenta] Winamp Müzik Botunu Açıyorum...",
    ) as status:
        console.print("┌ [red]MongoDB önbelleğini temizliyorum...")
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            console.print("[red] Mongo DB temizlenirken hata oluştu.")
        console.print("└ [green]MongoDB Başarıyla Temizlendi!\n\n")
        ____ = await startup_send_new("Tüm Eklentileri İçe Aktarıyorum...")
        status.update(
            status="[bold blue]Eklentiler için Tarama", spinner="earth"
        )
        await asyncio.sleep(1.7)
        console.print("{} Eklentileri bulundu".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Eklentileri içe Aktarma...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        await asyncio.sleep(1.2)
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "Yukki.Plugins." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f">> [bold cyan]Başarıyla içe aktarıldı: [green]{all_module}.py"
            )
            await asyncio.sleep(0.2)
        console.print("")
        _____ = await startup_edit_last(____, "Sonuçlandırılıyor...")
        status.update(
            status="[bold blue]İçe aktarma Tamamlandı!",
        )
        await asyncio.sleep(2.4)
        await startup_delete_last(_____)
    console.print(
        "[bold green]⚡Tebrikler!! Winamp Müzik Botu başarıyla başladı!⚡\n"
    )
    try:
        await app.send_message(
            LOG_GROUP_ID,
            "<b>⚡Tebrikler!! Müzik Botu başarıyla başladı!⚡</b>",
        )
    except Exception as e:
        print(
            "Bot günlük Kanalına erişemedi. Botunuzu günlük kanalınıza eklediğinizden ve yönetici olarak tanıttığınızdan emin olun!"
        )
        console.print(f"\n[red]Durdurma Botu")
        return
    a = await app.get_chat_member(LOG_GROUP_ID, BOT_ID)
    if a.status != "yönetici":
        print("Logger Kanalında Botu Yönetici Olarak Tanıtın")
        console.print(f"\n[red]Durdurma Botu")
        return
    try:
        await userbot.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Asistan başarıyla başladı!</b>",
        )
    except Exception as e:
        print(
            "Yardımcı Hesap günlük Kanalına erişemedi. Botunuzu günlük kanalınıza eklediğinizden ve yönetici olarak tanıttığınızdan emin olun!"
        )
        console.print(f"\n[red]Durdurma Botu")
        return
    try:
        await userbot.join_chat("WinampMuzikDestek")
    except:
        pass
    console.print(f"\n┌[red] Bot olarak başladı! {BOT_NAME}!")
    console.print(f"├[green] ID :- {BOT_ID}!")
    console.print(f"├[red] Asistan olarak başladı! {ASSNAME}!")
    console.print(f"└[green] ID :- {ASSID}!")
    await run()
    console.print(f"\n[red]Durdurma Botu")


home_text_pm = f"""⚡ Merhaba 🖤 [ ](https://www.burn-soft.ru/wp-content/uploads/2015/07/Programma-Winamp-1024x1024.jpg)

⚡ Benim adım {BOT_NAME} Bot ⚡.

💡 Bazı kullanışlı özelliklere sahip Telegram Sesli Sohbet Sesiyim.

⚡ **Geliştiricim <3  [Pratheek](http://t.me/OrmanCocuklariylaMucadele)**

💭 Tüm komutlarımı ile kullanılabilirsin: / """


@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await app.send_message(message.chat.id, text, reply_markup=keyboard)


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name[0] == "s":
            sudoers = await get_sudoers()
            text = "**__Yardımcı Kullanıcıları Bot Listesi:-__**\n\n"
            j = 0
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = (
                        user.first_name if not user.mention else user.mention
                    )
                except Exception:
                    continue
                text += f"➤ {kullanıcı}\n"
                j += 1
            if j == 0:
                await message.reply_text("Yardım Kullanıcısı Yok")
            else:
                await message.reply_text(text)
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            m = await message.reply_text("🔎 Bilgi Alınıyor!")
            query = (str(name)).replace("bilgi_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**Video Parça Bilgileri**__

❇️**Başlık:** {title}

⏳**Süreli:** {duration} Dakika
👀**Görünümler:** `{views}`
⏰**Yayın Saati:** {published}
🎥**Kanal Adı:** {channel}
📎**Kanal Linki:** [Visit From Here]({channellink})
🔗**Video Linki:** [Link]({link})

⚡️ __Arama {BOT_NAME} Tarafından Desteklenmektedir__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Youtube Videosunu İzle", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Kapat", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
    out = private_panel()
    return await message.reply_text(
        home_text_pm,
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """⚡️ Merhaba {first_name}⚡️,
        
Daha fazla bilgi için düğmelere tıklayın.

Tüm komutlarım ile kullanabilirsin: /
""".format(
            first_name=name
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("shikhar"))
async def shikhar(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""⚡️ Merhaba {query.from_user.first_name},
    
Daha fazla bilgi için düğmelere tıklayın.

Tüm komutlarım ile kullanabilirsin: /
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "İşte yardım için", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Geri", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="🔄 Kapat", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
