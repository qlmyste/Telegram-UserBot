# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments
import string, random
import re
from password_generator import PasswordGenerator

@register(outgoing=True, pattern="^.password(?: |$)(.*)")
async def password(e):
  query = e.pattern_match.group(1)
  size = re.findall(r'\d+', query)
  pwo = PasswordGenerator()
  pwo.minlen = int(size[0])
  pwo.maxlen = int(size[0])
  passw = pwo.generate()
  await e.edit(f"`{passw}`")
