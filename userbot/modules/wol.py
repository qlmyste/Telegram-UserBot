from userbot.events import register
from userbot import MAC_ADDRESS as MAC

@register(outgoing=True, pattern=r"^\.boot$")
async def boot(bt):
    if MAC is None:
      await bt.edit("**We don't support magic! No API Code! Take it from audiotag.info**")
      return
    
    
