from typing import Dict, List, Union

from Yukki import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "Bazı izinlere sahip yönetici olmam gerekiyor:\n"
                + "\n- **can_manage_voice_chats:** Sesli sohbetleri yönetmek için"
                + "\n- **can_delete_messages:** Botun Aranan Atıklarını silmek için"
                + "\n- **can_invite_users**: Asistanı sohbete davet etmek için."
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli izne sahip değilim."
                + "\n**Permission:** __SESLİ SOHBETLERİ YÖNET__"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli izne sahip değilim."
                + "\n**Permission:** __MESAJLARI SİL__"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli izne sahip değilim."
                + "\n**Permission:** __KULLANICILARI BAĞLANTI YOLUYLA DAVET ET__"
            )
            return
        return await mystic(_, message)

    return wrapper
