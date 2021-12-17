from inspect import getfullargspec

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import (ASSID, ASSISTANT_PREFIX, ASSNAME, BOT_ID, BOT_USERNAME,
                   LOG_GROUP_ID, MUSIC_BOT_NAME, SUDOERS, app, userbot)
from Yukki.Database import (approve_pmpermit, disapprove_pmpermit,
                            is_pmpermit_approved)

__MODULE__ = "Asistan"
__HELP__ = f"""

**Not:**
- Sadece Yardımcı Kullanıcıları için



{ASSISTANT_PREFIX[0]}block [ Kullanıcı Mesajına Yanıt Ver ] 
- Kullanıcıyı Asistan Hesabından engeller.

{ASSISTANT_PREFIX[0]}unblock [ Kullanıcı Mesajına Yanıt Ver ] 
- Kullanıcının Asistan Hesabından engelini kaldırır.

{ASSISTANT_PREFIX[0]}approve [ Kullanıcı Mesajına Yanıt Ver ] 
- Kullanıcıyı DM için onaylar.

{ASSISTANT_PREFIX[0]}disapprove [ Kullanıcı Mesajına Yanıt Verme ] 
- Kullanıcıyı DM için onaylamaz.

{ASSISTANT_PREFIX[0]}pfp [ Fotoğrafa Yanıtla ] 
- Yardımcı hesap fotoğraf'ını değiştirir.

{ASSISTANT_PREFIX[0]}bio [Bio metini] 
- Asistan Hesabının Biyografisini değiştirir.

"""

flood = {}


@userbot.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
async def awaiting_message(_, message):
    user_id = message.from_user.id
    if await is_pmpermit_approved(user_id):
        return
    async for m in userbot.iter_history(user_id, limit=6):
        if m.reply_markup:
            await m.delete()
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 5:
        await message.reply_text("Spam Algılandı. Kullanıcı Engellendi")
        await userbot.send_message(
            LOG_GROUP_ID,
            f"**Asistanda Spam Algılama Bloğu**\n\n- **Engellenen Kullanıcı:** {message.from_user.mention}\n- **Kullanıcı Kimliğ:** {message.from_user.id}",
        )
        return await userbot.block_user(user_id)
    results = await userbot.get_inline_bot_results(
        BOT_ID, f"permit_to_pm {user_id}"
    )
    await userbot.send_inline_bot_result(
        user_id,
        results.query_id,
        results.results[0].id,
        hide_via=True,
    )


@userbot.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def pm_approve(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Onaylamak için bir kullanıcının mesajına yanıt verin."
        )
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        return await eor(message, text="Kullanıcı pm'ye zaten onaylandı")
    await approve_pmpermit(user_id)
    await eor(message, text="Kullanıcı pm'ye onaylandı")


@userbot.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def pm_disapprove(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Onaylamamak için bir kullanıcının mesajına yanıt verin."
        )
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await eor(message, text="Kullanıcı pm'ye zaten onaylanmadı")
        async for m in userbot.iter_history(user_id, limit=6):
            if m.reply_markup:
                try:
                    await m.delete()
                except Exception:
                    pass
        return
    await disapprove_pmpermit(user_id)
    await eor(message, text="Kullanıcı pm'ye onaylanmadı")


@userbot.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def block_user_func(_, message):
    if not message.reply_to_message:
        return await eor(message, text="Engellenecek bir kullanıcının mesajını yanıtla.")
    user_id = message.reply_to_message.from_user.id
    await eor(message, text="Kullanıcı başarıyla engellendi")
    await userbot.block_user(user_id)


@userbot.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def unblock_user_func(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Engelini kaldırmak için bir kullanıcının mesajına yanıt verin."
        )
    user_id = message.reply_to_message.from_user.id
    await userbot.unblock_user(user_id)
    await eor(message, text="Kullanıcının Engelini Başarıyla kaldırdı")


    
@userbot.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def set_pfp(_, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="Fotoğraf Başarıyla değiştirdi.") 
    photo = await message.reply_to_message.download()
    try: 
        await userbot.set_profile_photo(photo=photo)   
        await eor(message, text="Successfully Changed PFP.")
    except Exception as e:
        await eor(message, text=e)
    
    
@userbot.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def set_bio(_, message):
    if len(message.command) == 1:
        return await eor(message , text="Bio olarak ayarlamak için biraz metin verin.") 
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try: 
            await userbot.update_profile(bio=bio) 
            await eor(message , text="Biyo değiştirildi.") 
        except Exception as e:
            await eor(message , text=e) 
    else:
        return await eor(message , text="Bio olarak ayarlamak için biraz metin verin.") 

flood2 = {}

@app.on_callback_query(filters.regex("pmpermit"))
async def pmpermit_cq(_, cq):
    user_id = cq.from_user.id
    data, victim = (
        cq.data.split(None, 2)[1],
        cq.data.split(None, 2)[2],
    )
    if data == "approve":
        if user_id != ASSID:
            return await cq.answer("Bu Düğme Sizin İçin Değil")
        await approve_pmpermit(int(victim))
        return await app.edit_inline_text(
            cq.inline_message_id, "Kullanıcı Pm'ye Onaylandı."
        )

    if data == "block":
        if user_id != ASSID:
            return await cq.answer("Bu Düğme Sizin İçin Değil")
        await cq.answer()
        await app.edit_inline_text(
            cq.inline_message_id, "Kullanıcıyı başarıyla engelledi."
        )
        await userbot.block_user(int(victim))
        return await userbot.send(
            DeleteHistory(
                peer=(await userbot.resolve_peer(victim)),
                max_id=0,
                revoke=False,
            )
        )

    if user_id == ASSID:
        return await cq.answer("Diğer Kişi İçin.")

    if data == "to_scam_you":
        async for m in userbot.iter_history(user_id, limit=6):
            if m.reply_markup:
                await m.delete()
        await userbot.send_message(user_id, "Engellendi, Git başkasını kandır.")
        await userbot.send_message(
            LOG_GROUP_ID,
            f"**Asistanda Aldatmaca Bloğu**\n\n- **Engellenen Kullanıcı:** {cq.from_user.mention}\n- **Kullanıcı Kimliği:** {user_id}",
        )
        await userbot.block_user(user_id)
        await cq.answer()
    if data == "for_pro":
        async for m in userbot.iter_history(user_id, limit=6):
            if m.reply_markup:
                await m.delete()
        await userbot.send_message(user_id, f"Engellendi, Promosyon Yok.")
        await userbot.send_message(
            LOG_GROUP_ID,
            f"**Asistanda Promosyon Bloğu**\n\n- **Engellenen Kullanıcı:** {cq.from_user.mention}\n- **Kullanıcı Kimliği:** {user_id}",
        )
        await userbot.block_user(user_id)
        await cq.answer()
    elif data == "approve_me":
        await cq.answer()
        if str(user_id) in flood2:
            flood2[str(user_id)] += 1
        else:
            flood2[str(user_id)] = 1
        if flood2[str(user_id)] > 5:
            await userbot.send_message(
                user_id, "SPAM ALGILANDI, KULLANICI ENGELLENDİ."
            )
            await userbot.send_message(
                LOG_GROUP_ID,
                f"**Asistanda Spam Algılama Bloğu**\n\n- **Engellenen Kullanıcı:** {cq.from_user.mention}\n- **Kullanıcı Kimliği:** {user_id}",
            )
            return await userbot.block_user(user_id)
        await userbot.send_message(
            user_id,
            "Şu anda meşgulüm, sizi kısa süre içinde onaylayacağım, SPAM yapmayın.",
        )


async def pmpermit_func(answers, user_id, victim):
    if user_id != ASSID:
        return
    caption = f"Merhaba, ben {ASSNAME}, Ne için buradasın? 5'ten fazla mesaj gönderirseniz engellenirsiniz."
    audio_markup2 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=f"Grubunuza {MUSIC_BOT_NAME} Ekle",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Seni Aldatmak İçin",
                    callback_data=f"pmpermit to_scam_you a",
                ),
                InlineKeyboardButton(
                    text="Tanıtım için", callback_data=f"pmpermit for_pro a"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Beni onayla", callback_data=f"pmpermit approve_me a"
                ),
                InlineKeyboardButton(
                    text="Onayla", callback_data=f"pmpermit approve {victim}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "Engelle ve Sil", callback_data="pmpermit block {victim}"
                )
            ],
        ]
    )
    answers.append(
        InlineQueryResultArticle(
            title="do_not_click_here",
            reply_markup=audio_markup2,
            input_message_content=InputTextMessageContent(caption),
        )
    )
    return answers


@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.split()[0] == "permit_to_pm":
            user_id = query.from_user.id
            victim = text.split()[1]
            answerss = await pmpermit_func(answers, user_id, victim)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )
    except:
        return


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
