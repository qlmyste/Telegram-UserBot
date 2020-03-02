from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments

@register(outgoing=True, pattern=r"^\.mp3$")
async def mp3(e):
  message = await e.get_reply_message()
  file = message.audio or message.voice
  if not file:
      await e.edit("**No audio file specified**", delete_in=3)
      return
  file = await bot.download_file(file)
  await e.edit(file)
