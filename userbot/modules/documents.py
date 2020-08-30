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
    file = message.file
    file = await bot.download_file(file, "file.pdf")
    
    
