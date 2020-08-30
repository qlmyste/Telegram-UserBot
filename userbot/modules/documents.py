# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import bot, CMD_HELP
from userbot.events import register
import os
from pdf2image import convert_from_path
from docx2pdf import convert

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
  message = await e.get_reply_message()
  if message.file.mime_type == "application/doc" or message.file.mime_type == "application/docx":
    file = message.document
    await e.edit("**Downloading...**")
    file = await bot.download_file(file, "file.docx")
    await e.edit("**Converting...**")
    convert("file.docx", "output.pdf")
    await e.edit("**Sending...**")
    await e.client.send_file(e.chat_id, f'output.pdf',reply_to=message)
    os.remove('file.docx')
    os.remove('output.pdf')
  else:
    await e.edit("`Not a doc file. Aborting...`")
    return
@register(outgoing=True, pattern=r"^\.doc2pdf$")
async def doc_png(e):
  message = await e.get_reply_message()
  if message.file.mime_type == "application/doc" or message.file.mime_type == "application/docx":
    file = message.document
    await e.edit("**Downloading...**")
    file = await bot.download_file(file, "file.docx")
    await e.edit("**Converting...**")
    convert("file.docx", "output.pdf")
    if os.path.isdir("/root/Telegram-UserBot/files") is False:
      os.mkdir("/root/Telegram-UserBot/files")
    await e.edit("**Processing...**")
    images_from_path = convert_from_path('/root/Telegram-UserBot/output.pdf', output_folder='/root/Telegram-UserBot/files/', fmt='png')
    await e.edit("**Sending...**")
    for filename in os.listdir("/root/Telegram-UserBot/files/"):
      await e.client.send_file(e.chat_id, open('/root/Telegram-UserBot/files/' + filename, 'rb'), reply_to=message)
      rmtree("/root/Telegram-UserBot/files")
      os.remove(f"/root/Telegram-UserBot/output.pdf")
      os.remove('file.docx')
  else:
    await e.edit("`Not a doc file. Aborting...`")
    return
