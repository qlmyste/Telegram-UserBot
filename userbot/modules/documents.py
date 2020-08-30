# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import bot, CMD_HELP
from userbot.events import register
import os, docx2pdf
from pdf2image import convert_from_path

@register(outgoing=True, pattern=r"^\.pdf2png$")
async def pdf(e):
  message = await e.get_reply_message()
  print (message.file.mime_type)
