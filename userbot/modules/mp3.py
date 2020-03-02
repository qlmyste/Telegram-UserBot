from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments
import os
from io import BytesIO
@register(outgoing=True, pattern=r"^\.mp3$")
async def mp3(e):
  message = await e.get_reply_message()
  file = message.audio or message.voice
  if not file:
      await e.edit("**Bot doesn't support magic! Use voice message.**")
      return
  await e.edit("**Downloading...**")
  file = BytesIO()
  file.name = "voice.mp3"
  file = await bot.download_file(file)
  await e.edit("**Sending...**")
  await e.client.send_file(e.chat_id,
                           file,
                           reply_to=message)
  os.remove(f'voice.mp3')
  CMD_HELP.update({
    ".mp3":
    "Convert a voice message to a mp3 and send it."
})
