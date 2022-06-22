import discord
from discord.ext import commands
import json
from downloader import Downloader
import os
import embeds
from yt_dlp import DownloadError
import base64
import random

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)

os.chdir(__file__.split('bot-runner.py')[0])
settings = json.load(open('settings.json'))

@bot.event
async def on_ready():
    print('I am ready')
    bot_channel = bot.get_channel(914650069687492729)
    await bot_channel.send("I Am Ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="In development!"))

@bot.command()
async def download(ctx, opt :str, url :str):

    opt = opt.lower()
    
    req_id = base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8')

    if opt == 'audio':
        await ctx.send(embed=embeds.cmd_error("Please enter a valid option.\n\nI am working on adding support for video and simultaneous audio/video downloads!"))
        return

    elif "&list=" in url:
        url = url.split("&list=")[0]
        await ctx.send(embed=embeds.cmd_error(f"Warning, Playlists are not supported yet! I am working on playlist support!\n\nThis video will be downloaded instead:\n{url}"))

    elif "playlist?list=" in url:
        await ctx.send(embed=embeds.cmd_error("Warning, Playlists are not supported yet! Please select the url of a single video you would like to download."))
        return
    
    download = Downloader(url, settings.get("audio_dir"), settings.get("video_dir"))
    option = getattr(download, f"download_{opt}", ".")
    option()
    
    #dump id and shit into database **MAKE A FUNCTION FOR THIS** 
    
    await ctx.send(embed=embeds.embed_b(f"{opt.capitalize()} is Here!", f'http://localhost:3000/audio/{req_id}\n\nSave the code below to access your video download for the next 24 hours!:\n\n*{req_id}*'))

@download.error
async def download_error(ctx, error):

    if isinstance(error, DownloadError):
        await ctx.send(embeds.cmd_error("Please enter a valid YouTube URL."))

@bot.command()
async def help(ctx, opt='general'):
    await ctx.send(embed=embeds.help_command(opt))

bot.run(settings.get("bot_secret"))
