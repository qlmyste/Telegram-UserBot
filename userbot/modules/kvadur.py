import asyncio
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
import re
@register(outgoing=True, pattern="^.kvadur(?: |$)(.*)")
async def evaluate(kvad):
      if kvad.pattern_match.group(1):
        expression = kvad.pattern_match.group(1)
        numbers = re.findall(r'\b\d+\b', 'he33llo 42 I\'ma 32 string 30')
        await kvad.edit(numbers.groups())
      else:
        await kvad.edit("``` Give a numbers to evaluate. ```")
        return

