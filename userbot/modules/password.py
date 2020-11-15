# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments
import string, random
import re

@register(outgoing=True, pattern="^.password(?: |$)(.*)")
async def password(e):
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  query = e.pattern_match.group(1)
  size = re.findall(r'\d+', query)
  print(size[0])
