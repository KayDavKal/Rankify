import os
TOKEN = my_secret = os.environ['TOKEN']

from user import *

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#sync command
@client.event
async def on_guild_join():
  await tree.sync()

@client.event
async def on_message(interaction):
  if interaction.author.bot:
    return
  else:
    User = get_user(interaction.guild.id, interaction.author.id)
    if User is not True:
      await add_user(interaction.guild.id, interaction.author.id)
    else:
      await add_xp(interaction.guild.id, interaction.author.id, 1)

#ping command
@tree.command(name = "ping", description = "See how fast I reply")
async def first_command(interaction):
    user = interaction.user
    latency = round(client.latency * 1000)
    embed = discord.Embed(
      title = "Pong!",
      description = f"It took me {latency} ms to reply!",
      color = discord.Color.green()
    )
    embed.set_author(name=user.name, icon_url=user.avatar)
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
  await tree.sync()
  await table()
  print("Ready!")

client.run(TOKEN)
