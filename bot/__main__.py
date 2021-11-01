import shutil, psutil
import signal
import os
import asyncio

from pyrogram import idle, filters, types, emoji
from pyrogram import idle
from sys import executable
from datetime import datetime
from pytz import timezone
from sys import executable
from quoters import Quote
import threading

from telegram import ParseMode, InlineKeyboardButton
from telegram.ext import Filters, InlineQueryHandler, MessageHandler, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from telegraph import Telegraph
from wserver import start_server_async
from bot import bot, app, dispatcher, updater, botStartTime, IGNORE_PENDING_REQUESTS, IS_VPS, PORT, alive, web, nox, OWNER_ID, AUTHORIZED_CHATS, telegraph_token, BOT_NO
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper import button_build
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, torrent_search, delete, speedtest, count, leech_settings, mediainfo, telegraph



# Current time in UTC
now_utc = datetime.now(timezone('UTC'))
print"(now_utc.strftime(format))

# Convert to Asia/Jakarta time zone
now_asia = now_utc.astimezone(timezone('Asia/Jakarta'))
print"(now_asia.strftime(format))

def stats(update, context):
    currentTime = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'<b>👴🏻 𝐖𝐚𝐤𝐭𝐮 𝐀𝐤𝐭𝐢𝐟 𝐁𝐨𝐭 ⌚️:</b> <code>{currentTime}</code>\n' \
            f'<b>💾 𝐓𝐨𝐭𝐚𝐥 𝐑𝐮𝐚𝐧𝐠 𝐃𝐢𝐬𝐤 💾:</b> <code>{total}</code>\n' \
            f'<b>📳 𝐒𝐮𝐝𝐚𝐡 𝐀𝐤𝐭𝐢𝐟 𝐃𝐚𝐫𝐢 🕐:{current}<code>\n' \
            f'<b>⌛️ 𝐓𝐞𝐫𝐩𝐚𝐤𝐚𝐢 ⌛️:</b> <code>{used}</code> ' \
            f'<b>🔋 𝐊𝐨𝐬𝐨𝐧𝐠 🔋:</b> <code>{free}</code>\n\n' \
            f'<b>🔺 𝐔𝐧𝐠𝐠𝐚𝐡𝐚𝐧:</b> <code>{sent}</code>\n' \
            f'<b>🔻 𝐔𝐧𝐝𝐮𝐡𝐚𝐧:</b> <code>{recv}</code>\n\n' \
            f'<b>🖥️ 𝐂𝐏𝐔:</b> <code>{cpuUsage}%</code> ' \
            f'<b>🧭 𝐑𝐀𝐌:</b> <code>{memory}%</code> ' \
            f'<b>🖫 𝐃𝐈𝐒𝐊:</b> <code>{disk}%</code>'
    sendMessage(stats, context.bot, update)
    
    
    def call_back_data(update, context):
    global main
    query = update.callback_query
    query.answer()
    main.delete()
    main = None


def start(update, context):
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("👨🏼‍✈️ 𝐏𝐞𝐦𝐢𝐥𝐢𝐤 🙈", "https://www.instagram.com/mimi.peri")
    buttons.buildbutton("🐊 𝐂𝐫𝐮𝐬𝐡 👩🏻", "https://www.instagram.com/zar4leola")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
This bot can mirror all your links to Google Drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
        sendMarkup(start_string, context.bot, update, reply_markup)
    else:
        sendMarkup(
            '𝐔𝐩𝐬! 𝐓𝐢𝐝𝐚𝐤 𝐌𝐞𝐦𝐢𝐥𝐢𝐤𝐢 𝐎𝐭𝐨𝐫𝐢𝐬𝐚𝐬𝐢 𝐑𝐞𝐬𝐦𝐢.\n𝐘𝐚𝐧𝐠 𝐒𝐀𝐁𝐀𝐑 𝐲𝐚 𝐁𝐨𝐬𝐪𝐮. \n<b>𝐇𝐚𝐫𝐢 𝐘𝐚𝐧𝐠 𝐁𝐞𝐫𝐚𝐭, 𝐔𝐧𝐭𝐮𝐤 𝐎𝐫𝐚𝐧𝐠 𝐘𝐚𝐧𝐠 𝐇𝐞𝐛𝐚𝐭.</b>.',
            context.bot,
            update,
            reply_markup,
        )


def restart(update, context):
    restart_message = sendMessage("𝐌𝐞𝐦𝐮𝐥𝐚𝐢 𝐮𝐥𝐚𝐧𝐠, 𝐇𝐚𝐫𝐚𝐩 𝐭𝐮𝐧𝐠𝐠𝐮!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    fs_utils.clean_all()
    alive.terminate()
    web.terminate()
    os.execl(executable, executable, "-m", "bot")


def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


def log(update, context):
    sendLogFile(context.bot, update)


help_string_telegraph = f'''<br>
<b>/{BotCommands.HelpCommand}</b>: To get this message
<br><br>
<b>/{BotCommands.MirrorCommand}</b> [download_url][magnet_link]: 𝐌𝐞𝐦𝐮𝐥𝐚𝐢 𝐌𝐢𝐫𝐫𝐨𝐫𝐢𝐧𝐠 𝐤𝐞 𝐆𝐃𝐫𝐢𝐯𝐞.
<br><br>
<b>/{BotCommands.TarMirrorCommand}</b> [download_url][magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫𝐢𝐧𝐠 𝐝𝐚𝐧 𝐮𝐧𝐠𝐠𝐚𝐡 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐚𝐫𝐬𝐢𝐩𝐤𝐚𝐧 (.𝐭𝐚𝐫) 𝐤𝐞 𝐯𝐞𝐫𝐬𝐢 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐧𝐲𝐚.
<br><br>
<b>/{BotCommands.ZipMirrorCommand}</b> [download_url][magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫𝐢𝐧𝐠 𝐝𝐚𝐧 𝐮𝐧𝐠𝐠𝐚𝐡 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐚𝐫𝐬𝐢𝐩𝐤𝐚𝐧 (.𝐳𝐢𝐩) 𝐤𝐞 𝐯𝐞𝐫𝐬𝐢 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐧𝐲𝐚.
<br><br>
<b>/{BotCommands.UnzipMirrorCommand}</b> [download_url][magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫𝐢𝐧𝐠 𝐝𝐚𝐧 𝐣𝐢𝐤𝐚 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐮𝐧𝐝𝐮𝐡 𝐚𝐝𝐚𝐥𝐚𝐡 𝐚𝐫𝐬𝐢𝐩 𝐣𝐞𝐧𝐢𝐬 𝐚𝐩𝐚 𝐩𝐮𝐧, 𝐦𝐞𝐧𝐠-𝐞𝐤𝐬𝐭𝐫𝐚𝐤𝐧𝐲𝐚 𝐤𝐞 𝐆𝐨𝐨𝐠𝐥𝐞 𝐃𝐫𝐢𝐯𝐞.
<br><br>
<b>/{BotCommands.QbMirrorCommand}</b> [magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫 𝐦𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐪𝐁𝐢𝐭𝐭𝐨𝐫𝐫𝐞𝐧𝐭, Use <b>/{BotCommands.QbMirrorCommand} s</b> 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐦𝐢𝐥𝐢𝐡 𝐟𝐢𝐥𝐞 𝐬𝐞𝐛𝐞𝐥𝐮𝐦 𝐦𝐞𝐧𝐠𝐮𝐧𝐝𝐮𝐡.
<br><br>
<b>/{BotCommands.QbTarMirrorCommand}</b> [magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫 𝐦𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐪𝐁𝐢𝐭𝐭𝐨𝐫𝐫𝐞𝐧𝐭 𝐝𝐚𝐧 𝐮𝐧𝐠𝐠𝐚𝐡 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐚𝐫𝐬𝐢𝐩𝐤𝐚𝐧 (.𝐭𝐚𝐫) 𝐤𝐞 𝐯𝐞𝐫𝐬𝐢 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐧𝐲𝐚.
<br><br>
<b>/{BotCommands.QbZipMirrorCommand}</b> [magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫 𝐦𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐪𝐁𝐢𝐭𝐭𝐨𝐫𝐫𝐞𝐧𝐭 𝐝𝐚𝐧 𝐮𝐧𝐠𝐠𝐚𝐡 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐚𝐫𝐬𝐢𝐩𝐤𝐚𝐧 (.𝐳𝐢𝐩) 𝐤𝐞 𝐯𝐞𝐫𝐬𝐢 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐧𝐲𝐚.
<br><br>
<b>/{BotCommands.QbUnzipMirrorCommand}</b> [magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐢𝐫𝐫𝐨𝐫 𝐦𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐪𝐁𝐢𝐭𝐭𝐨𝐫𝐫𝐞𝐧𝐭 𝐝𝐚𝐧 𝐣𝐢𝐤𝐚 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐮𝐧𝐝𝐮𝐡 𝐚𝐝𝐚𝐥𝐚𝐡 𝐚𝐫𝐬𝐢𝐩 𝐣𝐞𝐧𝐢𝐬 𝐚𝐩𝐚 𝐩𝐮𝐧, 𝐦𝐞𝐧𝐠-𝐞𝐤𝐬𝐭𝐫𝐚𝐤𝐧𝐲𝐚 𝐤𝐞 𝐆𝐨𝐨𝐠𝐥𝐞 𝐃𝐫𝐢𝐯𝐞.
<br><br>
<b>/{BotCommands.LeechCommand}</b> [download_url][magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐮𝐩𝐥𝐨𝐚𝐝 𝐤𝐞 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦, Use <b>/{BotCommands.LeechCommand} s</b> to select files before leeching
<br><br>
<b>/{BotCommands.TarLeechCommand}</b> [download_url][magnet_link]:  𝐌𝐮𝐥𝐚𝐢 𝐦𝐞𝐧𝐠𝐮𝐧𝐠𝐠𝐚𝐡 𝐤𝐞 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐝𝐞𝐧𝐠𝐚𝐧 𝐟𝐨𝐫𝐦𝐚𝐭 𝐬𝐞𝐛𝐚𝐠𝐚𝐢 (.𝐭𝐚𝐫)
<br><br>
<b>/{BotCommands.ZipLeechCommand}</b> [download_url][magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐞𝐧𝐠𝐮𝐧𝐠𝐠𝐚𝐡 𝐤𝐞 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐝𝐞𝐧𝐠𝐚𝐧 𝐟𝐨𝐫𝐦𝐚𝐭 𝐬𝐞𝐛𝐚𝐠𝐚𝐢 (.𝐳𝐢𝐩)
<br><br>
<b>/{BotCommands.UnzipLeechCommand}</b> [download_url][magnet_link]: 𝐌𝐮𝐥𝐚𝐢 𝐦𝐞𝐧𝐠𝐮𝐧𝐠𝐠𝐚𝐡 𝐤𝐞 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐝𝐚𝐧 𝐣𝐢𝐤𝐚 𝐟𝐢𝐥𝐞 𝐲𝐚𝐧𝐠 𝐝𝐢𝐮𝐧𝐝𝐮𝐡 𝐚𝐝𝐚𝐥𝐚𝐡 𝐚𝐫𝐬𝐢𝐩 𝐣𝐞𝐧𝐢𝐬 𝐚𝐩𝐚 𝐩𝐮𝐧, 𝐦𝐞𝐧𝐠-𝐞𝐤𝐬𝐭𝐫𝐚𝐤𝐧𝐲𝐚 𝐤𝐞 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦
<br><br>
<b>/{BotCommands.QbLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent, Use <b>/{BotCommands.QbLeechCommand} s</b> to select files before leeching
<br><br>
<b>/{BotCommands.QbTarLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent and upload it as (.tar)
<br><br>
<b>/{BotCommands.QbZipLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent and upload it as (.zip)
<br><br>
<b>/{BotCommands.QbUnzipLeechCommand}</b> [magnet_link]: Start leeching to Telegram using qBittorrent and if downloaded file is any archive, extracts it to Telegram
<br><br>
<b>/{BotCommands.CloneCommand}</b> [drive_url]: 𝐂𝐨𝐩𝐲 𝐟𝐢𝐥𝐞/𝐟𝐨𝐥𝐝𝐞𝐫 𝐊𝐞 𝐆𝐃𝐫𝐢𝐯𝐞
<br><br>
<b>/{BotCommands.CountCommand}</b> [drive_url]: 𝐌𝐞𝐧𝐠𝐡𝐢𝐭𝐮𝐠 𝐟𝐢𝐥𝐞/𝐟𝐨𝐥𝐝𝐞𝐫 𝐝𝐚𝐫𝐢 𝐆𝐃𝐫𝐢𝐯𝐞 𝐋𝐢𝐧𝐤𝐬
<br><br>
<b>/{BotCommands.DeleteCommand}</b> [drive_url]: Delete file from Google Drive (Only Owner & Sudo)
<br><br>
<b>/{BotCommands.WatchCommand}</b> [youtube-dl supported link]: Mirror through youtube-dl. Click <b>/{BotCommands.WatchCommand}</b> for more help
<br><br>
<b>/{BotCommands.TarWatchCommand}</b> [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading
<br><br>
<b>/{BotCommands.ZipWatchCommand}</b> [youtube-dl supported link]: Mirror through youtube-dl and zip before uploading
<br><br>
<b>/{BotCommands.LeechWatchCommand}</b> [youtube-dl supported link]: Leech through youtube-dl 
<br><br>
<b>/{BotCommands.LeechTarWatchCommand}</b> [youtube-dl supported link]: Leech through youtube-dl and tar before uploading 
<br><br>
<b>/{BotCommands.LeechZipWatchCommand}</b> [youtube-dl supported link]: Leech through youtube-dl and zip before uploading 
<br><br>
<b>/{BotCommands.LeechSetCommand}</b>: Leech Settings 
<br><br>
<b>/{BotCommands.SetThumbCommand}</b>: Reply photo to set it as Thumbnail
<br><br>
<b>/{BotCommands.CancelMirror}</b>: Reply to the message by which the download was initiated and that download will be cancelled
<br><br>
<b>/{BotCommands.CancelAllCommand}</b>: Cancel all running tasks
<br><br>
<b>/{BotCommands.ListCommand}</b> [search term]: Searches the search term in the Google Drive, If found replies with the link
<br><br>
<b>/{BotCommands.StatusCommand}</b>: Shows a status of all the downloads
<br><br>
<b>/{BotCommands.StatsCommand}</b>: Show Stats of the machine the bot is hosted on
'''
help = Telegraph(access_token=telegraph_token).create_page(
        title='Perintah Rumah Awan',
        author_name='Rumah Awan',
        author_url='https://t.me/awanmirrorbot1',
        html_content=help_string_telegraph,
    )["path"]

help_string = f'''
/{BotCommands.PingCommand}: 𝐏𝐞𝐫𝐢𝐤𝐬𝐚 𝐛𝐞𝐫𝐚𝐩𝐚 𝐉𝐮𝐦𝐥𝐚𝐡 𝐏𝐢𝐧𝐠 𝐛𝐨𝐭

/{BotCommands.AuthorizeCommand}: 𝐎𝐭𝐨𝐫𝐢𝐬𝐚𝐬𝐢 𝐨𝐛𝐫𝐨𝐥𝐚𝐧/𝐩𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐛𝐨𝐭 (𝐂𝐮𝐦𝐚 𝐛𝐢𝐬𝐚 𝐝𝐢𝐩𝐚𝐤𝐞 𝐨𝐥𝐞𝐡 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚 & 𝐒𝐮𝐝𝐨 𝐛𝐨𝐭)

/{BotCommands.UnAuthorizeCommand}: 𝐁𝐚𝐭𝐚𝐥𝐤𝐚𝐧 𝐎𝐭𝐨𝐫𝐢𝐬𝐚𝐬𝐢 𝐨𝐛𝐫𝐨𝐥𝐚𝐧/𝐩𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐤𝐚𝐧 𝐛𝐨𝐭 (𝐂𝐮𝐦𝐚 𝐛𝐢𝐬𝐚 𝐝𝐢𝐩𝐚𝐤𝐞 𝐨𝐥𝐞𝐡 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚 & 𝐒𝐮𝐝𝐨 𝐛𝐨𝐭)

/{BotCommands.AuthorizedUsersCommand}: 𝐓𝐚𝐦𝐩𝐢𝐥𝐤𝐚𝐧 𝐩𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐫𝐞𝐬𝐦𝐢 (𝐂𝐮𝐦𝐚 𝐛𝐢𝐬𝐚 𝐝𝐢𝐩𝐚𝐤𝐞 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚 & 𝐒𝐮𝐝𝐨)

/{BotCommands.AddSudoCommand}: 𝐓𝐚𝐦𝐛𝐚𝐡𝐤𝐚𝐧 𝐏𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐒𝐮𝐝𝐨 (𝐂𝐮𝐦𝐚 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚)

/{BotCommands.RmSudoCommand}: 𝐇𝐚𝐩𝐮𝐬 𝐏𝐞𝐧𝐠𝐠𝐮𝐧𝐚 𝐒𝐮𝐝𝐨 (𝐂𝐮𝐦𝐚 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚)

/{BotCommands.RestartCommand}: 𝐌𝐮𝐚𝐭 𝐮𝐥𝐚𝐧𝐠 𝐛𝐨𝐭

/{BotCommands.LogCommand}: 𝐃𝐚𝐩𝐚𝐭𝐤𝐚𝐧 𝐟𝐢𝐥𝐞 𝐥𝐨𝐠 𝐛𝐨𝐭. 𝐁𝐞𝐫𝐠𝐮𝐧𝐚 𝐮𝐧𝐭𝐮𝐤 𝐦𝐞𝐧𝐝𝐚𝐩𝐚𝐭𝐤𝐚𝐧 𝐥𝐚𝐩𝐨𝐫𝐚𝐧 𝐤𝐞𝐫𝐮𝐬𝐚𝐤𝐚𝐧

/{BotCommands.SpeedCommand}: 𝐏𝐞𝐫𝐢𝐤𝐬𝐚 𝐊𝐞𝐜𝐞𝐩𝐚𝐭𝐚𝐧 𝐈𝐧𝐭𝐞𝐫𝐧𝐞𝐭 𝐁𝐨𝐭

/{BotCommands.ShellCommand}: Run commands in Shell (𝐂𝐮𝐦𝐚 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚)

/{BotCommands.ExecHelpCommand}: Get help for Executor module (𝐂𝐮𝐦𝐚 𝐘𝐚𝐧𝐠 𝐏𝐮𝐧𝐲𝐚)

/{BotCommands.TsHelpCommand}: 𝐃𝐚𝐩𝐚𝐭𝐤𝐚𝐧 𝐛𝐚𝐧𝐭𝐮𝐚𝐧 𝐮𝐧𝐭𝐮𝐤 𝐦𝐨𝐝𝐮𝐥 𝐩𝐞𝐧𝐜𝐚𝐫𝐢𝐚𝐧 𝐓𝐨𝐫𝐫𝐞𝐧𝐭
'''

def bot_help(update, context):
    button = button_build.ButtonMaker()
    button.buildbutton("Other Commands", f"https://telegra.ph/{help}")
    reply_markup = InlineKeyboardMarkup(button.build_menu(1))
    sendMarkup(help_string, context.bot, update, reply_markup)

'''
botcmds = [
        (f'{BotCommands.HelpCommand}','Get Detailed Help'),
        (f'{BotCommands.MirrorCommand}', 'Start Mirroring'),
        (f'{BotCommands.TarMirrorCommand}','Start mirroring and upload as .tar'),
        (f'{BotCommands.ZipMirrorCommand}','Start mirroring and upload as .zip'),
        (f'{BotCommands.UnzipMirrorCommand}','Extract files'),
        (f'{BotCommands.QbMirrorCommand}','Start Mirroring using qBittorrent'),
        (f'{BotCommands.QbTarMirrorCommand}','Start mirroring and upload as .tar using qb'),
        (f'{BotCommands.QbZipMirrorCommand}','Start mirroring and upload as .zip using qb'),
        (f'{BotCommands.QbUnzipMirrorCommand}','Extract files using qBitorrent'),
        (f'{BotCommands.CloneCommand}','Copy file/folder to Drive'),
        (f'{BotCommands.CountCommand}','Count file/folder of Drive link'),
        (f'{BotCommands.DeleteCommand}','Delete file from Drive'),
        (f'{BotCommands.WatchCommand}','Mirror Youtube-dl support link'),
        (f'{BotCommands.TarWatchCommand}','Mirror Youtube playlist link as .tar'),
        (f'{BotCommands.ZipWatchCommand}','Mirror Youtube playlist link as .zip'),
        (f'{BotCommands.CancelMirror}','Cancel a task'),
        (f'{BotCommands.CancelAllCommand}','Cancel all tasks'),
        (f'{BotCommands.ListCommand}','Searches files in Drive'),
        (f'{BotCommands.StatusCommand}','Get Mirror Status message'),
        (f'{BotCommands.StatsCommand}','Bot Usage Stats'),
        (f'{BotCommands.PingCommand}','Ping the Bot'),
        (f'{BotCommands.RestartCommand}','Restart the bot [owner/sudo only]'),
        (f'{BotCommands.LogCommand}','Get the Bot Log [owner/sudo only]'),
        (f'{BotCommands.TsHelpCommand}','Get help for Torrent search module')
    ]
'''

def main():
    current = now_asia.strftime(format)
    fs_utils.start_cleanup()
    if IS_VPS:
        asyncio.get_event_loop().run_until_complete(start_server_async(PORT))
    # Check if the bot is restarting
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text("𝐁𝐞𝐫𝐡𝐚𝐬𝐢𝐥 𝐦𝐞𝐦𝐮𝐥𝐚𝐢 𝐮𝐥𝐚𝐧𝐠, 𝐒𝐞𝐦𝐮𝐚 𝐓𝐮𝐠𝐚𝐬 𝐃𝐢𝐛𝐚𝐭𝐚𝐥𝐤𝐚𝐧!", chat_id, msg_id)
        os.remove(".restartmsg")
    elif OWNER_ID:
        try:
            text = "<b>𝐁𝐨𝐭 𝐇𝐢𝐝𝐮𝐩 𝐊𝐞𝐦𝐛𝐚𝐥𝐢! 𝐊𝐢𝐭𝐚 𝐌𝐮𝐥𝐚𝐢 𝐃𝐚𝐫𝐢 𝐍𝐎𝐋 𝐘𝐚 𝐌𝐚𝐬 𝐞</b>"
            bot.sendMessage(chat_id=OWNER_ID, text=text, parse_mode=ParseMode.HTML)
            if AUTHORIZED_CHATS:
                for i in AUTHORIZED_CHATS:
                    bot.sendMessage(chat_id=i, text=text, parse_mode=ParseMode.HTML)
        except Exception as e:
            LOGGER.warning(e)
    # bot.set_my_commands(botcmds)
    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    del_data_msg = CallbackQueryHandler(call_back_data, pattern="stats_close")
    dispatcher.add_handler(del_data_msg)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

app.start()
main()
idle()
