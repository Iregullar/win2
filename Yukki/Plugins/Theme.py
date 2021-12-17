from typing import Dict, List, Union

from pyrogram import Client, filters

from Yukki import BOT_USERNAME, MUSIC_BOT_NAME, app, db
from Yukki.Database import _get_theme, get_theme, save_theme
from Yukki.Decorators.permission import PermissionCheck

themes = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
    "Random",
]

themes2 = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
]

__MODULE__ = "Tema"
__HELP__ = """


/settheme
- Küçük resimler için bir tema ayarlayın.

/theme
- Sohbetiniz için Temayı kontrol edin.
"""


@app.on_message(
    filters.command(["settheme", f"settheme@{BOT_USERNAME}"]) & filters.group
)
async def settheme(_, message):
    usage = f"Bu bir tema değil.\n\nOnlardan birini seçin\n{' | '.join(themes)}\n\nRastgele tema seçimi elde etmek için 'Random' seçeneğini kullanın"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    theme = message.text.split(None, 1)[1].strip()
    if theme not in themes:
        return await message.reply_text(usage)
    note = {
        "theme": theme,
    }
    await save_theme(message.chat.id, "theme", note)
    await message.reply_text(f"Changed thumbnail theme to {theme}")


@app.on_message(filters.command("theme"))
@PermissionCheck
async def theme_func(_, message):
    await message.delete()
    _note = await get_theme(message.chat.id, "theme")
    if not _note:
        theme = "Random"
    else:
        theme = _note["theme"]
    await message.reply_text(
        f"**{MUSIC_BOT_NAME} Küçük Resimler Teması**\n\n**Geçerli Tema:-** {theme}\n\n**Kullanılabilir Temalar:-** {' | '.join(themes2)} \n\nTemayı değiştirmek için /settheme kullanın."
    )
