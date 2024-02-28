import time
import os
from pyrogram import Client, filters
from config import CAPTION, DESTINATION_CHANNEL, SOURCE_CHANNEL, DOWNLOAD_LOCATION
from main.utils import progress_message, humanbytes
import telegraph
import requests

@Client.on_message(filters.chat(SOURCE_CHANNEL) & (filters.document | filters.audio | filters.video))
async def rename_file(bot, msg):
    media = msg.document or msg.audio or msg.video
    old_name = media.file_name
    if not media.file_size < 2 * 1024 * 1024 * 1024:
        await msg.reply_text("File is larger than 2GB and won't be processed.")
        return
    sts = await msg.reply_text("Task added in pending...")
    await sts.edit("downloading started...")
    downloaded = await bot.download_media(media, file_name=old_name)
    filesize = humanbytes(media.file_size)

    if CAPTION:
        try:
            cap = CAPTION.format(file_name=old_name, file_size=filesize)
        except Exception as e:
            return await sts.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
    else:
        cap = f"**@noisemovies {old_name}**"

    og_thumbnail = None
    if media.thumbs is not None and len(media.thumbs) > 0:
        file_thumb = await bot.download_media(media.thumbs[0].file_id)
        og_thumbnail = file_thumb

    await sts.edit("Trying to Uploading")

    try:
        thumb_url = "https://telegra.ph/file/dca389b38e62071a5c9b3.jpg"
        thumb_file_path = os.path.join(DOWNLOAD_LOCATION, "custom_thumbnail.jpg")
        response = requests.get(thumb_url)
        if response.status_code == 200:
            with open(thumb_file_path, 'wb') as f:
                f.write(response.content)

        if og_thumbnail:
            thumb_path = thumb_file_path
        else:
            thumb_path = None

        await bot.send_document(chat_id=DESTINATION_CHANNEL, document=downloaded, thumb=thumb_path, caption=cap)
    except Exception as e:
        return await sts.edit(f"Error {e}")
    finally:
        if og_thumbnail:
            os.remove(thumb_file_path)
        os.remove(downloaded)
    await sts.delete()
