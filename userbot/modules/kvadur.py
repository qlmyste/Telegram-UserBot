import asyncio
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.kvadur(?: |$)(.*)")
async def evaluate(kvad):
      if kvad.pattern_match.group(1):
        expression = kvad.pattern_match.group(1)
        await kvad.edit(expression)
      else:
        await kvad.edit("``` Give a numbers to evaluate. ```")
        return
