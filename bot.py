import asyncio
import threading
import os

import discord
from discord.ext.commands import Bot

WAIT_TIME = 10 # seconds

intents = discord.Intents.all()
client = Bot(command_prefix=[], intents=intents)

typing_channels = {}

async def set_start_permissions(channel_id, user_id):
    channel = client.get_channel(channel_id)
    everyone_perm = channel.set_permissions(channel.guild.default_role, send_messages=False, read_messages=False)
    typer_perm = channel.set_permissions(channel.guild.get_member(user_id), send_messages=True, read_messages=True)
    await asyncio.gather(everyone_perm, typer_perm)

async def set_end_permissions(channel_id, user_id):
    await asyncio.sleep(WAIT_TIME)
    channel = client.get_channel(channel_id)
    typer_perm = channel.set_permissions(channel.guild.get_member(user_id), send_messages=None, read_messages=None)
    typing_channels[channel_id] -= 1
    if typing_channels[channel_id] > 0:
        return
    del typing_channels[channel_id]
    everyone_perm = channel.set_permissions(channel.guild.default_role, send_messages=True, read_messages=True)
    await asyncio.gather(everyone_perm, typer_perm)

@client.event
async def on_raw_typing(ctx):
    print(f"{ctx.user.name}#{ctx.user.discriminator} is typing in {ctx.channel_id}")
    await set_start_permissions(ctx.channel_id, ctx.user_id)
    typing_channels[ctx.channel_id] = typing_channels.get(ctx.channel_id, 0) + 1
    threading.Thread(
        target=lambda channel, user: asyncio.get_event_loop().create_task(set_end_permissions(channel, user)),
        args=(ctx.channel_id, ctx.user_id)
    ).run()

try:
    client.run(os.environ["SAFE_BOT_TOKEN"])
except KeyError:
    print("You must put bot's token into SAFE_BOT_TOKEN varaible and export it")
    exit(1)