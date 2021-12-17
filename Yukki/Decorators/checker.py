from Yukki import BOT_USERNAME, LOG_GROUP_ID, app
from Yukki.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "Bu Sohbet Grubunda __Anonim bir Yönetici__ sizsiniz!\nYönetici Haklarından Kullanıcı Hesabına geri dönün."
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"**Kara Listeye Alınmış Sohbet**\n\nSohbetiniz Sudo Kullanıcıları tarafından kara listeye alındı.Herhangi bir __SUDO KULLANICISINDAN__ beyaz listeye almasını isteyin.\nSudo Kullanıcı Listesini Kontrol Edin [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"Botu Bakım altında. Rahatsızlıktan dolayı özür dilerim!"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**Yasaklı kullanıcı**\n\nİkisini birden kullanman yasaklandı.Herhangi bir __SUDO KULLANICISINDAN __ unban'ı kaldırmasını isteyin.\nSudo Kullanıcı Listesini Kontrol Edin [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        blacklisted_chats_list = await blacklisted_chats()
        if CallbackQuery.message.chat.id in blacklisted_chats_list:
            return await CallbackQuery.answer(
                "Kara Listeye Alınmış Sohbet", show_alert=True
            )
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOG_GROUP_ID):
                return await CallbackQuery.answer(
                    "Bot Bakım altında. Rahatsızlıktan dolayı özür dilerim!",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "Yasaklı Kullanıcı", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
