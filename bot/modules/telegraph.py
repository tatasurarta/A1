import os
import traceback

from pyrogram import filters
from pyrogram.types import Message
from telegraph import upload_file

from bot import app, dispatcher, telegraph
from telegram.ext import CommandHandler

@app.on_message(filters.command(['tgm']))
async def tgm(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("Reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4"),
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.reply("Not supported!")
        return
    download_location = await client.download_media(
        message=message.reply_to_message,
        file_name="root/downloads/",
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        await message.reply(
            f"**link : **[telegraph](https://telegra.ph{response[0]})",
            disable_web_page_preview=True,
        )
    finally:
        os.remove(download_location)

@app.on_message(filters.command(['tgt']))
async def tgt(_, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("𝐁𝐚𝐥𝐚𝐬 𝐤𝐞 𝐩𝐞𝐬𝐚𝐧 𝐭𝐞𝐤𝐬 🙃")

    if len(message.command) < 2:
        return await message.reply("**😑𝐆𝐮𝐧𝐚𝐤𝐚𝐧:**\n /tgt [𝐣𝐮𝐝𝐮𝐥 𝐭𝐞𝐤𝐬]")

    page_name = message.text.split(None, 1)[1]
    page = telegraph.create_page(page_name, html_content=reply.text.html)
    return await message.reply(
        f"**link : **[telegraph]({page['url']})",
        disable_web_page_preview=True,
    )
        
        
TGM_HANDLER = CommandHandler("tgm", tgm)
TGT_HANDLER = CommandHandler("tgt", tgt)

dispatcher.add_handler(TGM_HANDLER)
dispatcher.add_handler(TGT_HANDLER)
