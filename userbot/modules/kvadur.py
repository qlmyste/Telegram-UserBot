import asyncio
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.kvadur(?: |$)(.*)")
async def evaluate(kvad):
      if query.pattern_match.group(1):
        expression = query.pattern_match.group(1)
        await query.edit(expression)
      else:
        await query.edit("``` Give a numbers to evaluate. ```")
        return
