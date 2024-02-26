import time
import os
from pyrogram import Client, filters
from config import CAPTION, DESTINATION_CHANNEL, SOURCE_CHANNEL, DOWNLOAD_LOCATION
from main.utils import progress_message, humanbytes
import telegraph 


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
        cap = f"**{old_name}**"

    dir = os.listdir(DOWNLOAD_LOCATION)
    if len(dir) == 0:
        file_thumb = await bot.download_media(media.thumbs[0].file_id)
        og_thumbnail = file_thumb
    else:
        try:
            og_thumbnail = f"{DOWNLOAD_LOCATION}/thumbnail.jpg"
        except Exception as e:
            print(e)        
            og_thumbnail = None
        
    await sts.edit("Trying to Uploading")    
    
    try:
        await bot.send_document(chat_id=DESTINATION_CHANNEL, document=downloaded, thumb=og_thumbnail, caption=cap)        
    except Exception as e:  
        return await sts.edit(f"Error {e}")                                              
    try:
        if file_thumb:
            os.remove(file_thumb)
        os.remove(downloaded)      
    except:
        pass
    await sts.delete()
