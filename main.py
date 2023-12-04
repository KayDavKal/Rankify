import os
TOKEN = my_secret = os.environ['TOKEN']

from user import *
from app import stay_alive
from progressbar import create_progress_bar

import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

intents = discord.Intents.all()
client = discord.Client(intents=intents, status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="to /rank"))
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
    User = await get_user(interaction.guild.id, interaction.author.id)
    if User is not True:
      await add_user(interaction.guild.id, interaction.author.id)
    else:
      await add_xp(interaction.guild.id, interaction.author.id, 1)

#ping command
@tree.command(name = "ping", description = "See how fast I reply")
async def first_command(interaction):
    user = interaction.user
    latency = round(client.latency * 1000)
    if latency <= 100:
      color = discord.Color.green()
    elif latency <= 300:
      color = discord.Color.orange()
    elif latency <= 500:
      color = discord.Color.red()
    elif latency >= 500:
      color = discord.Color.dark_red()
    embed = discord.Embed(
      title = "Pong!",
      description = f"It took me {latency} ms to reply!",
      color = color
    )
    embed.set_author(name=user.name, icon_url=user.avatar)
    await interaction.response.send_message(embed=embed)

#rank command
@tree.command(name="rank", description="See your or others rank")
async def rank(interaction, user: discord.Member = None):
  if user is None:
    user = interaction.user
  num = random.randint(0,2)
  xp = await  get_xp(interaction.guild.id, user.id)
  level = await get_level(interaction.guild.id, user.id)
  embed = discord.Embed(
    color = discord.Color.yellow()
  )
  embed.add_field(name="Level", value=f"```{level}```")
  embed.add_field(name="XP", value=f"```{xp}```")
  embed.set_author(name=f"{user.name}'s rank", icon_url=user.avatar)
  if num == 0:
    embed.set_footer(text="")
  elif num == 1:
    embed.set_footer(text="You can gain XP by chatting in the server.")
  elif num == 2:
    embed.set_footer(text="Get better lol.")
  await create_progress_bar(interaction.guild.id, user.id, 100)
  embed.set_image(url="")
  await interaction.response.send_message(embed=embed)
  os.remove("progress_bar.png")

#daily command
@tree.command(name="daily", description="Get your daily reward")
async def daily(interaction):
  guild_id = interaction.guild.id
  user = interaction.user
  ranxp = random.randint(1, 100)
  if interaction.user.id in cooldowns and datetime.utcnow() < cooldowns[interaction.user.id]:
    embed = discord.Embed(
      title = "Slow down a bit!",
      description=f"You can get your daily reward again in ```{str(timedelta(seconds=(cooldowns[interaction.user.id] - datetime.utcnow()).seconds))}h```",
      color = discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
  else:
    await add_xp(guild_id, user.id, ranxp)
    embed = discord.Embed(
    title = "Daily Rewards colected!",
    color = discord.Color.yellow()
    )
    embed.add_field(name="XP", value=f"```{ranxp}```")
    await interaction.response.send_message(embed=embed)
    cooldowns[interaction.user.id] = datetime.utcnow() + timedelta(seconds=86400)
  
@client.event
async def on_ready():
  await tree.sync()
  await table()
  stay_alive()
  print("Ready!")

stay_alive()
client.run(TOKEN)