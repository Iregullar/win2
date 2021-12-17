from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import (_get_authusers, delete_authuser, get_authuser,
                            get_authuser_count, get_authuser_names,
                            save_authuser)
from Yukki.Decorators.admins import AdminActual
from Yukki.Utilities.changers import (alpha_to_int, int_to_alpha,
                                      time_to_seconds)

__MODULE__ = "Auth Kullanıcıları"
__HELP__ = """

**Not:**
-Auth kullanıcıları Yönetici Hakları olmadan bile Sesli Sohbetleri atlayabilir, duraklatabilir, durdurabilir, devam ettirebilir.


/auth [Kullanıcı Adı veya Mesaja Cevap Verme] 
- Grubun kimlik doğrulama listesine bir kullanıcı ekleyin.

/unauth [Kullanıcı Adı veya Mesaja Cevap Verme] 
- Bir kullanıcıyı grubun kimlik doğrulama listesinden kaldırın.

/authusers 
- Grubun kimlik listesini kontrol edin.
"""


@app.on_message(filters.command("auth") & filters.group)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Bir kullanıcının mesajına cevap verin veya KullanıcıAdı/Kullanıcı_id verin."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0
        for smex in _check:
            count += 1
        if int(count) == 20:
            return await message.reply_text(
                "Grup Yetkili Kullanıcılar Listenizde yalnızca 20 Kullanıcınız olabilir."
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            await message.reply_text(
                f"Bu grubun Yetkili Kullanıcılar Listesine eklendi."
            )
            return
        else:
            await message.reply_text(f"Zaten Yetkili Kullanıcılar Listesinde.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(
            "Grup Yetkili Kullanıcılar Listenizde yalnızca 20 Kullanıcınız olabilir."
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"Bu grubun Yetkili Kullanıcılar Listesine eklendi."
        )
        return
    else:
        await message.reply_text(f"Zaten Yetkili Kullanıcılar Listesinde.")


@app.on_message(filters.command("unauth") & filters.group)
@AdminActual
async def whitelist_chat_func(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Bir kullanıcının mesajına cevap verin veya KullanıcıAdı/Kullanıcı_id verin."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if deleted:
            return await message.reply_text(
                f"Bu Grubun Yetkili Kullanıcılar Listesinden kaldırıldı."
            )
        else:
            return await message.reply_text(f"Not an Authorised User.")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"Bu Grubun Yetkili Kullanıcılar Listesinden kaldırıldı."
        )
    else:
        return await message.reply_text(f"Yetkili bir Kullanıcı Değil.")


@app.on_message(filters.command("authusers") & filters.group)
async def authusers(_, message: Message):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(
            f"Bu Grupta Yetkili Kullanıcı Yok.\n\nAuth kullanıcılarını /auth ile ekleyin ve /unauth ile kaldırın."
        )
    else:
        j = 0
        m = await message.reply_text(
            "Yetkili Kullanıcılar Getiriliyor... Lütfen Bekleyin"
        )
        msg = f"**Yetkili Kullanıcı Listesi[AUL]:**\n\n"
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            user_name = _note["auth_name"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}➤ {user}[`{user_id}`]\n"
            msg += f"    ┗ Tarafından eklendi:- {admin_name}[`{admin_id}`]\n\n"
        await m.edit_text(msg)
