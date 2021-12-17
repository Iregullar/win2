import os

import speedtest
import wget
from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import BOT_ID, SUDOERS, app

__MODULE__ = "Hız Testi"
__HELP__ = """

/speedtest 
- Sunucu Gecikmesini ve Hızını kontrol edin.

"""


def bytes(size: float) -> str:
    """boyutu insanlaştırın"""
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


@app.on_message(filters.command("speedtest") & ~filters.edited)
async def statsguwid(_, message):
    m = await message.reply_text("Çalışma Hızı testi")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("İndirme Hız Testi Çalıştırılıyor")
        test.download()
        m = await m.edit("Yükleme Hızı Testini Çalıştırılıyor")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        return await m.edit(e)
    m = await m.edit("Hız Testi Sonuçlarını Paylaşma")
    path = wget.download(result["share"])

    output = f"""**Hız testi Sonuçları**
    
<u>**İstemci:**</u>
**__Site:__** {result['client']['isp']}
**__Ülke:__** {result['client']['country']}
  
<u>**Sunucu:**</u>
**__İsim:__** {result['server']['name']}
**__Ülke:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Gecikme:__** {result['server']['latency']}  
**__Ping:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
