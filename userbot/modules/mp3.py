from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments
import os

@register(outgoing=True, pattern=r"^\.mp3$")
async def mp3(e):
  message = await e.get_reply_message()
  file = message.audio or message.voice
  if not file:
      await e.edit("**Bot doesn't support magic! Use voice message.**", delete_in=3)
      return
  file = await bot.download_file(file)
    await e.client.send_file(e.chat.id,
                              f'voice.mp3',
                              reply_to=reply_message)
  os.remove(f'voice.mp3')
  CMD_HELP.update({
    ".mp3":
    "Convert a voice message to a mp3 and send it."
})
