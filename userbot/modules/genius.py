#Developed by Oleh Polisan. get_args_split_by kanged from Friendly Telegram (https://gitlab.com/friendly-telegram/).
from userbot import BOTLOG, bot, BOTLOG_CHATID, CMD_HELP, GENIUS_API
from userbot.events import register
from userbot.utils import get_args_split_by
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
      await e.edit("**Searching for song **" + args[0] + "** by **" + args[1])
      song = genius.search_song(args[0], args[1])
      if song is None:
        await e.edit("**Can't find song **" + args[0] + "** by **" + args[1])
        return
      await e.edit("**Lyrics for: **" + args[1] + " - " + args[0] + " \n" + song.lyrics)
      
CMD_HELP.update({"lyrics": ["Lyrics",
    " - `.lyrics <song>, <author>`: Search lyrics in Genius platform\n"
    "You'll need an Genius api, which one you can get from https://genius.com/api-clients. \nIn APP WEBSITE URL type any url (such as http://example.com) and copy CLIENT ACCESS TOKEN to config.env file"]
})
