from pyrogram import Client, filters, enums
from config import ADMIN, ACCESS
from pyrogram.errors import ChatAdminRequired, FloodWait, MessageTooLong, UserIsBlocked, PeerIdInvalid, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated, ChatJoinRequest
from database import *

approve_text = "<b><a href='https://t.me/Yourresultsrobot?start=start'>Hᴇʟʟᴏ</a> {mention}👻, <a href='https://t.me/Yourresultsrobot?start=start'>Cʟɪᴄᴋ Mᴇ Tᴏ Cʟᴀɪᴍ Yᴏᴜʀ Fɪʟᴇ ɪɴ ʜɪɢʜ ϙᴜᴀʟɪᴛʏ ᴘʀɪɴᴛ</a></b>"
approve_photo = "https://telegra.ph/file/1532b9d30bb9df3df175c.jpg"

@Client.on_message(filters.command(["stats", "status"]) & filters.user(ADMIN))
async def get_stats(bot, message):
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')
    xx = all_users()
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️🙋‍♂️ Users :** `{xx}`")
    

@Client.on_chat_join_request()
async def accept_request(bot: Client, message):    
    user = message.from_user  
    try:        
        await add_user(user.id, bot, user)
        await bot.send_photo(
                message.from_user.id,
                photo=approve_photo,
                caption=approve_text.format(mention=message.from_user.mention),                
        )

    except UserIsBlocked:
        print("User blocked the bot")
    except PeerIdInvalid:
        print("Err")
    except Exception as e:
        print(f"#Error\n{str(e)}")

@Client.on_message(filters.command("start") & filters.private)                             
async def start_cmd(bot, msg):
    txt="hai This Bot Is Not Working Please Use Another Bot @YourResultsRobot"
    btn = InlineKeyboardMarkup([[
        InlineKeyboardButton("🤖 Use Other Bot", url="https://t.me/YourResultsRobot")
        ]])
    if msg.from_user.id != ADMIN:
        return await msg.reply_text(text=txt, reply_markup=btn, disable_web_page_preview = True)
    await start(bot, msg, cb=False)


@Client.on_callback_query(filters.regex("start"))
async def start(bot, msg, cb=True):   
    txt=f"hai This Bot Is Not Working Please Use Another Bot @YourResultsRobot</b>"                                     
    button = ([[
        InlineKeyboardButton("🤖 Use Other Bot", url="https://t.me/YourResultsRobot")
        ]])  
    if cb:
        await msg.message.edit(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview = True, parse_mode=enums.ParseMode.HTML)
    else:
        await msg.reply_text(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview = True, parse_mode=enums.ParseMode.HTML)


@Client.on_callback_query(filters.regex("help"))
async def help(bot, msg):
    txt = "just send a file and /rename <new name> with replayed your file\n\n"
    txt += "send photo to set thumbnail automatic \n"
    txt += "/view to see your thumbnail \n"
    txt += "/del to delete your thumbnail"
    button= [[        
        InlineKeyboardButton("🚫 Close", callback_data="del"),
        InlineKeyboardButton("⬅️ Back", callback_data="start") 
    ]]  
    await msg.message.edit(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview = True)


@Client.on_callback_query(filters.regex("about"))
async def about(bot, msg):
    me=await bot.get_me()     
    txt=f"<b>Bot Name: {me.mention}</b>"                 
    button= [[        
        InlineKeyboardButton("🚫 Close", callback_data="del"),
        InlineKeyboardButton("⬅️ Back", callback_data="start") 
    ]]  
    await msg.message.edit(text=txt, reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview = True, parse_mode=enums.ParseMode.HTML)


@Client.on_callback_query(filters.regex("del"))
async def closed(bot, msg):
    try:
        await msg.message.delete()
    except:
        return


