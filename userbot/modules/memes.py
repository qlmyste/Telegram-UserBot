# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#
""" Userbot module for having some fun with people. """

import asyncio
import random
import re
import time
import os

from collections import deque

import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon import types, utils

from cowpy import cow

from userbot import CMD_HELP
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.modules import speech

from os import environ
# ================= CONSTANT =================
METOOSTR = [
    "Me too thanks",
    "Haha yes, me too",
    "Same lol",
    "Me irl",
    "Same here",
    "Haha yes",
    "Me rn",
]

ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
             [
                 " ̍",
                 " ̎",
                 " ̄",
                 " ̅",
                 " ̿",
                 " ̑",
                 " ̆",
                 " ̐",
                 " ͒",
                 " ͗",
                 " ͑",
                 " ̇",
                 " ̈",
                 " ̊",
                 " ͂",
                 " ̓",
                 " ̈́",
                 " ͊",
                 " ͋",
                 " ͌",
                 " ̃",
                 " ̂",
                 " ̌",
                 " ͐",
                 " ́",
                 " ̋",
                 " ̏",
                 " ̽",
                 " ̉",
                 " ͣ",
                 " ͤ",
                 " ͥ",
                 " ͦ",
                 " ͧ",
                 " ͨ",
                 " ͩ",
                 " ͪ",
                 " ͫ",
                 " ͬ",
                 " ͭ",
                 " ͮ",
                 " ͯ",
                 " ̾",
                 " ͛",
                 " ͆",
                 " ̚",
             ],
             [
                 " ̕",
                 " ̛",
                 " ̀",
                 " ́",
                 " ͘",
                 " ̡",
                 " ̢",
                 " ̧",
                 " ̨",
                 " ̴",
                 " ̵",
                 " ̶",
                 " ͜",
                 " ͝",
                 " ͞",
                 " ͟",
                 " ͠",
                 " ͢",
                 " ̸",
                 " ̷",
                 " ͡",
             ]]

EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

INSULT_STRINGS = [
    "Owww ... Such a stupid idiot.",
    "Don't drink and type.",
    "I think you should go home or better a mental asylum.",
    "Command not found. Just like your brain.",
    "Do you realize you are making a fool of yourself? Apparently not.",
    "You can type better than that.",
    "Bot rule 544 section 9 prevents me from replying to stupid humans like you.",
    "Sorry, we do not sell brains.",
    "Believe me you are not normal.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
    "Zombies eat brains... you're safe.",
    "You didn't evolve from apes, they evolved from you.",
    "Come back and talk to me when your I.Q. exceeds your age.",
    "I'm not saying you're stupid, I'm just saying you've got bad luck when it comes to thinking.",
    "What language are you speaking? Cause it sounds like bullshit.",
    "Stupidity is not a crime so you are free to go.",
    "You are proof that evolution CAN go in reverse.",
    "I would ask you how old you are but I know you can't count that high.",
    "As an outsider, what do you think of the human race?",
    "Brains aren't everything. In your case they're nothing.",
    "Ordinarily people live and learn. You just live.",
    "I don't know what makes you so stupid, but it really works.",
    "Keep talking, someday you'll say something intelligent! (I doubt it though)",
    "Shock me, say something intelligent.",
    "Your IQ's lower than your shoe size.",
    "Alas! Your neurotransmitters are no more working.",
    "Are you crazy you fool.",
    "Everyone has the right to be stupid but you are abusing the privilege.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.",
    "You should try tasting cyanide.",
    "Your enzymes are meant to digest rat poison.",
    "You should try sleeping forever.",
    "Pick up a gun and shoot yourself.",
    "You could make a world record by jumping from a plane without parachute.",
    "Stop talking BS and jump in front of a running bullet train.",
    "Try bathing with Hydrochloric Acid instead of water.",
    "Try this: if you hold your breath underwater for an hour, you can then hold it forever.",
    "Go Green! Stop inhaling Oxygen.",
    "God was searching for you. You should leave to meet him.",
    "give your 100%. Now, go donate blood.",
    "Try jumping from a hundred story building but you can do it only once.",
    "You should donate your brain seeing that you never used it.",
    "Volunteer for target in an firing range.",
    "Head shots are fun. Get yourself one.",
    "You should try swimming with great white sharks.",
    "You should paint yourself red and run in a bull marathon.",
    "You can stay underwater for the rest of your life without coming back up.",
    "How about you stop breathing for like 1 day? That'll be great.",
    "Try provoking a tiger while you both are in a cage.",
    "Have you tried shooting yourself as high as 100m using a canon.",
    "You should try holding TNT in your mouth and igniting it.",
    "Try playing catch and throw with RDX its fun.",
    "I heard phogine is poisonous but i guess you wont mind inhaling it for fun.",
    "Launch yourself into outer space while forgetting oxygen on Earth.",
    "You should try playing snake and ladders, with real snakes and no ladders.",
    "Dance naked on a couple of HT wires.",
    "Active Volcano is the best swimming pool for you.",
    "You should try hot bath in a volcano.",
    "Try to spend one day in a coffin and it will be yours forever.",
    "Hit Uranium with a slow moving neutron in your presence. It will be a worthwhile experience.",
    "You can be the first person to step on sun. Have a try.",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNS_STR = [
    "Runs to Thanos..",
    "Runs far, far away from earth..",
    "Running faster than Bolt coz i'mma userbot !!",
    "Runs to Marie..",
    "This Group is too cancerous to deal with.",
    "Cya bois",
    "Kys",
    "I go away",
    "I am just walking off, coz me is too fat.",
    "I Fugged off!",
    "Will run for chocolate.",
    "I run because I really like food.",
    "Running...\nbecause dieting is not an option.",
    "Wicked fast runnah",
    "If you wanna catch me, you got to be fast...\nIf you wanna stay with me, you got to be good...\nBut if you wanna pass me...\nYou've got to be kidding.",
    "Anyone can run a hundred meters, it's the next forty-two thousand and two hundred that count.",
    "Why are all these people following me?",
    "Are the kids still chasing me?",
    "Running a marathon...there's an app for that.",
]

CHASE_STR = [
    "Where do you think you're going?",
    "Huh? what? did they get away?",
    "ZZzzZZzz... Huh? what? oh, just them again, nevermind.",
    "Get back here!",
    "Not so fast...",
    "Look out for the wall!",
    "Don't leave me alone with them!!",
    "You run, you die.",
    "Jokes on you, I'm everywhere",
    "You're gonna regret that...",
    "You could also try /kickme, I hear that's fun.",
    "Go bother someone else, no-one here cares.",
    "You can run, but you can't hide.",
    "Is that all you've got?",
    "I'm behind you...",
    "You've got company!",
    "We can do this the easy way, or the hard way.",
    "You just don't get it, do you?",
    "Yeah, you better run!",
    "Please, remind me how much I care?",
    "I'd run faster if I were you.",
    "That's definitely the droid we're looking for.",
    "May the odds be ever in your favour.",
    "Famous last words.",
    "And they disappeared forever, never to be seen again.",
    "\"Oh, look at me! I'm so cool, I can run from a bot!\" - this person",
    "Yeah yeah, just tap /kickme already.",
    "Here, take this ring and head to Mordor while you're at it.",
    "Legend has it, they're still running...",
    "Unlike Harry Potter, your parents can't protect you from me.",
    "Fear leads to anger. Anger leads to hate. Hate leads to suffering. If you keep running in fear, you might "
    "be the next Vader.",
    "Multiple calculations later, I have decided my interest in your shenanigans is exactly 0.",
    "Legend has it, they're still running.",
    "Keep it up, not sure we want you here anyway.",
    "You're a wiza- Oh. Wait. You're not Harry, keep moving.",
    "NO RUNNING IN THE HALLWAYS!",
    "Hasta la vista, baby.",
    "Who let the dogs out?",
    "It's funny, because no one cares.",
    "Ah, what a waste. I liked that one.",
    "Frankly, my dear, I don't give a damn.",
    "My milkshake brings all the boys to yard... So run faster!",
    "You can't HANDLE the truth!",
    "A long time ago, in a galaxy far far away... Someone would've cared about that. Not anymore though.",
    "Hey, look at them! They're running from the inevitable banhammer... Cute.",
    "Han shot first. So will I.",
    "What are you running after, a white rabbit?",
    "As The Doctor would say... RUN!",
]

HELLOSTR = [
    "Hi !",
    "‘Ello, gov'nor!",
    "What’s crackin’?",
    "‘Sup, homeslice?",
    "Howdy, howdy ,howdy!",
    "Hello, who's there, I'm talking.",
    "You know who this is.",
    "Yo!",
    "Whaddup.",
    "Greetings and salutations!",
    "Hello, sunshine!",
    "Hey, howdy, hi!",
    "What’s kickin’, little chicken?",
    "Peek-a-boo!",
    "Howdy-doody!",
    "Hey there, freshman!",
    "I come in peace!",
    "Ahoy, matey!",
    "Hiya!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{hits} {victim} with a {item}.",
    "{hits} {victim} in the face with a {item}.",
    "{hits} {victim} around a bit with a {item}.",
    "{throws} a {item} at {victim}.",
    "grabs a {item} and {throws} it at {victim}'s face.",
    "{hits} a {item} at {victim}.", "{throws} a few {item} at {victim}.",
    "grabs a {item} and {throws} it in {victim}'s face.",
    "launches a {item} in {victim}'s general direction.",
    "sits on {victim}'s face while slamming a {item} {where}.",
    "starts slapping {victim} silly with a {item}.",
    "pins {victim} down and repeatedly {hits} them with a {item}.",
    "grabs up a {item} and {hits} {victim} with it.",
    "starts slapping {victim} silly with a {item}.",
    "holds {victim} down and repeatedly {hits} them with a {item}.",
    "prods {victim} with a {item}.",
    "picks up a {item} and {hits} {victim} with it.",
    "ties {victim} to a chair and {throws} a {item} at them.",
    "{hits} {victim} {where} with a {item}.",
    "ties {victim} to a pole and whips them {where} with a {item}."
    "gave a friendly push to help {victim} learn to swim in lava.",
    "sent {victim} to /dev/null.", "sent {victim} down the memory hole.",
    "beheaded {victim}.", "threw {victim} off a building.",
    "replaced all of {victim}'s music with Nickelback.",
    "spammed {victim}'s email.", "made {victim} a knuckle sandwich.",
    "slapped {victim} with pure nothing.",
    "hit {victim} with a small, interstellar spaceship.",
    "quickscoped {victim}.", "put {victim} in check-mate.",
    "RSA-encrypted {victim} and deleted the private key.",
    "put {victim} in the friendzone.",
    "slaps {victim} with a DMCA takedown request!"
]

ITEMS = [
    "cast iron skillet",
    "large trout",
    "baseball bat",
    "cricket bat",
    "wooden cane",
    "nail",
    "printer",
    "shovel",
    "pair of trousers",
    "CRT monitor",
    "diamond sword",
    "baguette",
    "physics textbook",
    "toaster",
    "portrait of Richard Stallman",
    "television",
    "mau5head",
    "five ton truck",
    "roll of duct tape",
    "book",
    "laptop",
    "old television",
    "sack of rocks",
    "rainbow trout",
    "cobblestone block",
    "lava bucket",
    "rubber chicken",
    "spiked bat",
    "gold block",
    "fire extinguisher",
    "heavy rock",
    "chunk of dirt",
    "beehive",
    "piece of rotten meat",
    "bear",
    "ton of bricks",
]

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls",
]

HIT = [
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "bashes",
]

WHERE = ["in the chest", "on the head", "on the butt", "on the crotch"]

# ===========================================


@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
async def univsaye(cowmsg):
    """ For .cowsay module, userbot wrapper for cow which says things. """
    if environ.get("isSuspended") == "True":
        return
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$")
async def kek(keks):
    """ Check yourself ;)"""
    if environ.get("isSuspended") == "True":
        return
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@register(outgoing=True, pattern=r"^.coinflip (.*)")
async def coin(event):
    if environ.get("isSuspended") == "True":
        return
    r = random.choice(["heads", "tails"])
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r == "heads":
        if input_str == "heads":
            await event.edit(
                "The coin landed on: **Heads**.\nYou were correct.")
        elif input_str == "tails":
            await event.edit(
                "The coin landed on: **Heads**.\nYou weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Heads**.")
    elif r == "tails":
        if input_str == "tails":
            await event.edit(
                "The coin landed on: **Tails**.\nYou were correct.")
        elif input_str == "heads":
            await event.edit(
                "The coin landed on: **Tails**.\nYou weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Tails**.")


@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
async def who(event):
    """ slaps a user, or get slapped if not a reply. """
    if environ.get("isSuspended") == "True":
        return
    replied_user = await get_user_from_event(event)
    if replied_user:
        replied_user = replied_user[0]
    else:
        await event.edit("`I can't slap nothing !!`")
    caption = await slap(replied_user, event)
    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.edit(caption)

    except BaseException:
        await event.edit(
            "`Can't slap this person, need to fetch some sticks and stones !!`"
        )


async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    if environ.get("isSuspended") == "True":
        return
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)
    where = random.choice(WHERE)

    caption = "..." + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw, where=where)

    return caption


@register(outgoing=True, pattern="^.decide(?: |$)(.*)")
async def decide(event):
    if environ.get("isSuspended") == "True":
        return
    decision = event.pattern_match.group(1).lower()
    message_id = None
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if not decision:
        r = requests.get("https://yesno.wtf/api").json()
    else:
        try:
            options = ["yes", "no", "maybe"]
            if decision not in options:
                await event.edit("`Available decisions:` *yes*, *no*, *maybe*")
                return
            r = requests.get(f"https://yesno.wtf/api?force={decision}").json()
        except Excepption as err:
            await event.edit(f"`Error:` {str(err)}")
            return
    await event.client.send_message(event.chat_id,
                                    str(r["answer"]).upper(),
                                    reply_to=message_id,
                                    file=r["image"])
    await event.delete()


@register(outgoing=True, pattern="^.fp$")
async def facepalm(e):
    """ Facepalm  🤦‍♂ """
    if environ.get("isSuspended") == "True":
        return
    await e.edit("🤦‍♂")


@register(outgoing=True, pattern="^.cry$")
async def cry(e):
    """ y u du dis, i cry everytime !! """
    if environ.get("isSuspended") == "True":
        return
    await e.edit(random.choice(CRI))


@register(outgoing=True, pattern="^.insult$")
async def insult(e):
    """ I make you cry !! """
    if environ.get("isSuspended") == "True":
        return
    await e.edit(random.choice(INSULT_STRINGS))


@register(outgoing=True, pattern="^.cp(?: |$)(.*)")
async def copypasta(cp_e):
    """ Copypasta the famous meme """
    if environ.get("isSuspended") == "True":
        return
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await cp_e.edit("`😂🅱️IvE👐sOME👅text👅for✌️Me👌tO👐MAkE👀iT💞funNy!💦`")
        return

    reply_text = random.choice(EMOJIS)
    # choose a random character in the message to be substituted with 🅱️
    b_char = random.choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += random.choice(EMOJIS)
        elif owo in EMOJIS:
            reply_text += owo
            reply_text += random.choice(EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += owo.upper()
            else:
                reply_text += owo.lower()
    reply_text += random.choice(EMOJIS)
    await cp_e.edit(reply_text)


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
async def vapor(vpr):
    """ Vaporize everything! """
    if environ.get("isSuspended") == "True":
        return
    reply_text = list()
    textx = await vpr.get_reply_message()
    message = vpr.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await vpr.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await vpr.edit("".join(reply_text))


@register(outgoing=True, pattern="^.str(?: |$)(.*)")
async def stretch(stret):
    """ Stretch it."""
    if environ.get("isSuspended") == "True":
        return
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await stret.edit("`GiiiiiiiB sooooooomeeeeeee teeeeeeext!`")
        return

    count = random.randint(3, 10)
    reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                        message)
    await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    if environ.get("isSuspended") == "True":
        return
    reply_text = list()
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(0, 3):
            randint = random.randint(0, 2)

            if randint == 0:
                charac = charac.strip() + \
                    random.choice(ZALG_LIST[0]).strip()
            elif randint == 1:
                charac = charac.strip() + \
                    random.choice(ZALG_LIST[1]).strip()
            else:
                charac = charac.strip() + \
                    random.choice(ZALG_LIST[2]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))


@register(outgoing=True, pattern="^.hi$")
async def hoi(hello):
    """ Greet everyone! """
    if environ.get("isSuspended") == "True":
        return
    await hello.edit(random.choice(HELLOSTR))


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
async def faces(owo):
    """ UwU """
    if environ.get("isSuspended") == "True":
        return
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU no text given! `")
        return

    reply_text = re.sub(r"(r|l)", "w", message)
    reply_text = re.sub(r"(R|L)", "W", reply_text)
    reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + random.choice(UWUS)
    await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
async def react_meme(react):
    """ Make your userbot react to everything. """
    if environ.get("isSuspended") == "True":
        return
    await react.edit(random.choice(FACEREACTS))


@register(outgoing=True, pattern="^.hz$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    if environ.get("isSuspended") == "True":
        return
    await shg.edit(random.choice(SHGS))


@register(outgoing=True, pattern="^.chase$")
async def police(chase):
    """ U better run better run, faster than my bullet !! """
    if environ.get("isSuspended") == "True":
        return
    await chase.edit(random.choice(CHASE_STR))


@register(outgoing=True, pattern="^.run$")
async def runner_lol(run):
    """ Run, run, RUNNN! """
    if environ.get("isSuspended") == "True":
        return
    await run.edit(random.choice(RUNS_STR))


@register(outgoing=True, pattern="^.metoo$")
async def metoo(hahayes):
    """ Haha yes """
    if environ.get("isSuspended") == "True":
        return
    await hahayes.edit(random.choice(METOOSTR))


@register(outgoing=True, pattern="^.oof$")
async def Oof(e):
    if environ.get("isSuspended") == "True":
        return
    t = "Oof"
    for j in range(15):
        t = t[:-1] + "of"
        await e.edit(t)

@register(outgoing=True, pattern="^.gr$")
async def Gr(e):
    if environ.get("isSuspended") == "True":
        return
    t = "*Грр"
    for j in range(10):
        t = t[:-1] + "р*"
        await e.edit(t)

@register(outgoing=True, pattern="^.grr$")
async def Gr(e):
    if environ.get("isSuspended") == "True":
        return
    t = "*Грр"
    for j in range(20):
        t = t[:-1] + "р*"
        await e.edit(t)

@register(outgoing=True, pattern="^.10iq$")
async def iqless(e):
    if environ.get("isSuspended") == "True":
        return
    await e.edit("♿")


@register(outgoing=True, pattern="^.moon$")
async def moon(event):
    if environ.get("isSuspended") == "True":
        return
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            await asyncio.sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.clock$")
async def clock(event):
    if environ.get("isSuspended") == "True":
        return
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            await asyncio.sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    if environ.get("isSuspended") == "True":
        return
    reply_text = list()
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
        return

    for charac in message:
        if charac.isalpha() and random.randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
async def claptext(memereview):
    """ Praise people! """
    if environ.get("isSuspended") == "True":
        return
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await memereview.edit("`Hah, I don't clap pointlessly!`")
        return
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@register(outgoing=True, pattern="^.bt$")
async def bluetext(bt_e):
    if environ.get("isSuspended") == "True":
        return
    """ Believe me, you will find this useful. """
    if await bt_e.get_reply_message() and bt_e.is_group:
        await bt_e.edit(
            "/BLUETEXT /MUST /CLICK.\n"
            "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS ?"
        )


@register(outgoing=True, pattern=r"^.f (.*)")
async def payf(event):
    if environ.get("isSuspended") == "True":
        return
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2)
    await event.edit(pay)


@register(outgoing=True, pattern="^.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):
    if environ.get("isSuspended") == "True":
        return
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {'format': 'json', 'url': lfy_url}
    r = requests.get('http://is.gd/create.php', params=payload)
    await lmgtfy_q.edit(f"Here you are, help yourself.\
    \n[{query}]({r.json()['shorturl']})")


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    """ Just a small command to fake chat actions for fun !! """
    if environ.get("isSuspended") == "True":
        return
    options = [
        'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
        'photo', 'document', 'cancel'
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) is 0:  # Let bot decide action and time
        scam_action = random.choice(options)
        scam_time = random.randint(30, 60)
    elif len(args) is 1:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(args[0]).lower()
            scam_time = random.randint(30, 60)
        except ValueError:
            scam_action = random.choice(options)
            scam_time = int(args[0])
    elif len(args) is 2:  # User decides both action and time
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("`Invalid Syntax !!`")
        return
    try:
        if (scam_time > 0):
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await asyncio.sleep(scam_time)
    except BaseException:
        return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    if environ.get("isSuspended") == "True":
        return
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("`Give a text to type!`")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)
                      
#🦔🍎 kang from https://github.com/awitwicki/kodzu_thon
@register(pattern=r"🦔", outgoing=True)
async def handler(event):
    if environ.get("isSuspended") == "True":
        return
    try:
        origin_text = ''

        for i in range(19, -1, -1):
            edit_text = origin_text
            for r in range(i):
                edit_text += '🍎'
            edit_text += '🦔'
            await event.edit(edit_text)
            time.sleep(0.5)

    except Exception as e:
        print(e)
#🦔🍺 kang from https://github.com/awitwicki/kodzu_thon
@register(pattern=r"🍺", outgoing=True)
async def handler(event):
    if environ.get("isSuspended") == "True":
        return
    try:
        origin_text = ''

        for i in range(19, -1, -1):
            edit_text = origin_text
            for r in range(i):
                edit_text += '🍺'
            edit_text += '🦔'
            await event.edit(edit_text)
            time.sleep(0.5)

    except Exception as e:
        print(e)


@register(pattern=r".bruh", outgoing=True)
async def bruh(event):
  if environ.get("isSuspended") == "True":
        return
  await event.delete()
  wafe_form = speech.get_waveform(0, 31, 100)
  duration_ = int(os.popen("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 'media/bruh.ogg'").read().split('.')[0])
  await event.client.send_file(event.chat_id, 'media/bruh.ogg', reply_to = event.message.reply_to_msg_id, attributes=[types.DocumentAttributeAudio(duration=duration_, voice=True, waveform=utils.encode_waveform(bytes(wafe_form)))]) # 2**5 because 5-bit
                      
@register(outgoing=True, pattern="^.hzz$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    if environ.get("isSuspended") == "True":
        return
    await shg.edit("¯\_(ツ)_/¯")
CMD_HELP.update({"memes": ["Memes",
    " - `.cowsay`: cow which says things.\n"
    " - `:/`: Check yourself :)\n"
    " - `-_-`: Ok...\n"
    " - `;_;`: Like `-_-` but crying.\n"
    " - `.cp`: Vaporize everything!\n"
    " - `.vapor`: cow which says things.\n"
    " - `.str`: Stretch it.\n"
    " - `.10iq`: You retard !!\n"
    " - `.zal`: Invoke the feeling of chaos.\n"
    " - `Oof`: Oooooof\n"
    " - `.fp`: Facepalm :P\n"
    " - `.owo`: UwU\n"
    " - `.react`: Make your userbot react to everything..\n"
    " - `.moon`: kensar moon animation.\n"
    " - `.clock`: kensar clock animation.\n"
    " - `.hi`: Greet everyone!\n"
    " - `.slap`: reply to slap them with random objects !!\n"
    " - `.cry`: y u du dis, i cri.\n"
    " - `.shg`: Shrug at it !!\n"
    " - `.run`: Let Me Run, run, RUNNN!\n"
    " - `.chase`: You better start running\n"
    " - `.metoo`: Haha yes\n"
    " - `.mock`: Do it and find the real fun.\n"
    " - `.clap`: Praise people!\n"
    " - `.f <emoji/character>`: Pay Respects.\n"
    " - `.bt`: Believe me, you will find this useful.\n"
    " - `.type`: Just a small command to make your keyboard become a typewriter!\n"
    " - `.lfy <query>`: Let me Google that for you real quick !!\n"
    " - `.decide [Optional: (yes, no, maybe)]`: Make a quick decision.\n"
    " - `.scam <action> <time>`: Create fake chat actions, for fun. (Default action: typing)\nAvailable Actions: (typing, contact, game, location, voice, round, video, photo, document, cancel)"

                        ]})
