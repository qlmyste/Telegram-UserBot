# Module developed by Oleh Polisan
# You can use this file without any permission.
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.utils import parse_arguments
import string, random

@register(outgoing=True, pattern="^.password(?: |$)(.*)")
async def pass(e):
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  query = await e.pattern_match.group(1)
  print(query)
