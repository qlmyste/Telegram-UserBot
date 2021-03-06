import time

from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, User, Chat

from userbot.utils import inline_mention
from userbot import CMD_HELP
from userbot.events import register
from os import environ

@register(outgoing=True, pattern=f'^.stats')
async def stats(event: NewMessage.Event) -> None:  # pylint: disable = R0912, R0914, R0915
    """Command to get stats about the account"""
    if environ.get("isSuspended") == "True":
        return
    waiting_message = await event.edit('Collecting stats. This might take a while.')
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    largest_group_member_count = 0
    largest_group_with_admin = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity

        if isinstance(entity, Channel):
            # participants_count = (await event.get_participants(dialog, limit=0)).total
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1

            elif entity.megagroup:
                groups += 1
                # if participants_count > largest_group_member_count:
                #     largest_group_member_count = participants_count
                if entity.creator or entity.admin_rights:
                    # if participants_count > largest_group_with_admin:
                    #     largest_group_with_admin = participants_count
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1

        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1

        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1

        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time

    full_name = inline_mention(await event.client.get_me())
    response = f'**Stats for {full_name}** \n'
    response += f'    **Private Chats:** {private_chats} \n'
    response += f'        **Users:** {private_chats - bots} \n'
    response += f'        **Bots:** {bots} \n'
    response += f'    **Groups:** {groups} \n'
    response += f'    **Channels:** {broadcast_channels} \n'
    response += f'    **Admin in Groups:** {admin_in_groups} \n'
    response += f'        **Creator:** {creator_in_groups} \n'
    response += f'        **Admin Rights:** {admin_in_groups - creator_in_groups} \n'
    response += f'    **Admin in Channels:** {admin_in_broadcast_channels} \n'
    response += f'        **Creator:** {creator_in_channels} \n'
    response += f'        **Admin Rights:** {admin_in_broadcast_channels - creator_in_channels} \n'
    response += f'    **Unread:** {unread} \n'
    response += f'    **Unread Mentions:** {unread_mentions} \n\n'
    response += f'__Took:__ {stop_time:.02f}s \n'

    await event.edit(response)

CMD_HELP.update({"stats": ["Stats",
    " - `.stats`: Get info about yourself.\n"
                        ]})
