from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API
from userbot.events import register
from userbot.utils import get_args_split_by, escape_html
import lyricsgenius

@register(outgoing=True, pattern=r"^\.lyrics (.*)")
async def gen(e):
      genius = lyricsgenius.Genius(GENIUS_API)
      if GENIUS_API is None:
        await e.edit("**We don't support magic! No Genius API!**")
        return
      args = get_args_split_by(e.pattern_match.group(), ",")
      if len(args) != 2:
        await e.edit("**Syntax Error**")
        return
      try:
          song = await genius.search_song(args[0], args[1])
          e.edit(song)
          return
      except TypeError:
          # Song not found causes internal library error
          song = None
      if song is None:
        await e.edit("**Can't find song **" + args[0] + "** by **" + args[1])
        return
      await e.edit(escape_html(song.lyrics))
