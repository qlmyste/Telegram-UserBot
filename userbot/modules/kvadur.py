import asyncio
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from math import sqrt
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
        a = integ[0]
        b = integ[1]
        c = integ[2]
        D = b*b - 4*a*c
        x1 = (-b - sqrt(D))/2*a
        x2 = (-b + sqrt(D))/2*a
        await kvad.edit("`\n**Result: **\n`\n`D = `f"{D}"`\n **x1 = ** `f"{x1}"`, "**x2 = ** `f"{x2}"`")
      else:
        await kvad.edit("``` Give a numbers to evaluate. ```")
        return

