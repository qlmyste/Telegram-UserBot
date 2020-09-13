# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import CONVERT_TOKEN, bot, CMD_HELP
from userbot.events import register
import os
from pdf2image import convert_from_path
import convertapi
from shutil import rmtree



@register(outgoing=True, pattern=r"^\.pdf2img$")
async def pdf(e):
  message = await e.get_reply_message()
  if message.file.mime_type == "application/pdf":
    file = message.document
    await e.edit("**Downloading...**")
    file = await bot.download_file(file, "file.pdf")
    if os.path.isdir("/root/Telegram-UserBot/files") is False:
      os.mkdir("/root/Telegram-UserBot/files")
    await e.edit("**Processing...**")  
    images_from_path = convert_from_path('/root/Telegram-UserBot/file.pdf', output_folder='/root/Telegram-UserBot/files/', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("/root/Telegram-UserBot/files/"):
      await e.client.send_file(e.chat_id, open('/root/Telegram-UserBot/files/' + filename, 'rb'), reply_to=message)
    rmtree("/root/Telegram-UserBot/files")
    os.remove(f"/root/Telegram-UserBot/file.pdf")
  else:
    await e.edit("`Not a pdf file. Aborting...`")
    return
@register(outgoing=True, pattern=r"^\.doc2pdf$")
async def doc(e):
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  message = await e.get_reply_message()
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or message.file.mime_type == "application/msword":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": #docx
      file = await bot.download_file(file, "file.docx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.docx' })
      os.remove('file.docx')
    if message.file.mime_type == "application/msword": #docx
        file = await bot.download_file(file, "file.doc")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.doc' })
        os.remove('file.doc')
    result.file.save('file.pdf')
    await e.edit("**Sending...**")
    await e.client.send_file(e.chat_id, f'file.pdf',reply_to=message)
    
    os.remove('file.pdf')
  else:
    await e.edit("`Not a doc/docx file. Aborting...`")
    return
@register(outgoing=True, pattern=r"^\.doc2img$")
async def doc_png(e):
  message = await e.get_reply_message()
  if CONVERT_TOKEN == False:
    await e.edit("**No converter API defined. Fill it in config.env file. Aborting...**")
    return
  convertapi.api_secret = CONVERT_TOKEN
  if message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or message.file.mime_type == "application/msword":
    file = message.document
    await e.edit("**Downloading...**")
    result = None
    if  message.file.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": #docx
      file = await bot.download_file(file, "file.docx")
      await e.edit("**Converting...**")
      result = convertapi.convert('pdf', { 'File': 'file.docx' })
      os.remove('file.docx')
    if message.file.mime_type == "application/msword": #docx
        file = await bot.download_file(file, "file.doc")
        await e.edit("**Converting...**")
        result = convertapi.convert('pdf', { 'File': 'file.doc' })
        os.remove('file.doc')
    result.file.save('file.pdf')
    if os.path.isdir("/root/Telegram-UserBot/files") is False:
      os.mkdir("/root/Telegram-UserBot/files")
    await e.edit("**Processing...**")
    images_from_path = convert_from_path('/root/Telegram-UserBot/file.pdf', output_folder='/root/Telegram-UserBot/files/', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("/root/Telegram-UserBot/files/"):
      await e.client.send_file(e.chat_id, open('/root/Telegram-UserBot/files/' + filename, 'rb'), reply_to=message)
    rmtree("/root/Telegram-UserBot/files")
    os.remove(f"/root/Telegram-UserBot/file.pdf")
    os.remove('file.docx')
  else:
    await e.edit("`Not a doc file. Aborting...`")
    return
