import asyncio
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
import re
@register(outgoing=True, pattern="^.kvadur(?: |$)(.*)")
async def evaluate(kvad):
      if kvad.pattern_match.group(1):
        expression = kvad.pattern_match.group(1)
        l = len(expression)
        integ = []
        i = 0
        while i < l:
            s_int = ''
            a = expression[i]
            while '0' <= a <= '9':
                s_int += a
                i += 1
                if i < l:
                    a = expression[i]
                else:
                    break
            i += 1
            if s_int != '':
              integ.append(int(s_int))
        m = integ[0] + 3
        await kvad.edit("Test")
      else:
        await kvad.edit("``` Give a numbers to evaluate. ```")
        return
