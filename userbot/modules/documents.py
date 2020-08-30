# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import bot, CMD_HELP
from userbot.events import register
import os, docx2pdf
from pdf2image import convert_from_path

@register(outgoing=True, pattern=r"^\.pdf2img$")
async def pdf(e):
  message = await e.get_reply_message()
  test = message.file.mime_type == "application/pdf"
  print(test)
  if message.file.mime_type == "application/pdf":
    file = message.document
    file = await bot.download_file(file, "file.pdf")
    if os.path.isdir("/root/Telegram-UserBot/files") is False:
      os.mkdir("/root/Telegram-UserBot/files")
    images_from_path = convert_from_path('/root/Telegram-UserBot/file.pdf', output_folder='/root/Telegram-UserBot/files/', fmt='png')
    for filename in os.listdir("/root/Telegram-UserBot/files/"):
      await e.client.send_file(e.chat_id, open('/root/Telegram-UserBot/files/' + filename, 'rb'), reply_to=message)
    
