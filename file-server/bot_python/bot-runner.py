import discord
from discord.ext import commands
from downloader import Downloader
from yt_dlp import DownloadError
import os
import json
import embeds
import base64
import random
import sqlite3

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)
connection = sqlite3.connect('/home/aaatipamula/vscode_projects/yt-dlp-bot/file-server/database/db.sqlite')
cursor = connection.cursor()

os.chdir(__file__.split('bot-runner.py')[0])
settings = json.load(open('settings.json'))

@bot.event
async def on_ready():
    print('I am ready')
    bot_channel = bot.get_channel(914650069687492729)
    await bot_channel.send("I Am Ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="In development!"))

def dump_id(req_id :str, *content_ids :str):
    connection = sqlite3.connect('/home/aaatipamula/vscode_projects/yt-dlp-bot/file-server/database/db.sqlite')
    cursor = connection.cursor()
    
    a = cursor.execute("SELECT * FROM videoids WHERE videoids = %s" %req_id) 
    b = [x[0] for x in a] 
    
    if req_id in b:
        
        req_id = base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8')
    
    cursor.execute("INSERT INTO videoids (reqid, idone) VALUES (%s, %s)" %(req_id, content_ids(1)))
    
    connection.commit()
    connection.close()

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
    
    dump_id(req_id, download.video_title_base64) 
    
    await ctx.send(embed=embeds.embed_b(f"{opt.capitalize()} is Here!", f'http://localhost:3000/audio/{req_id}\n\nSave the code below to access your video download for the next 24 hours!:\n\n*{req_id}*'))

@download.error
async def download_error(ctx, error):

    if isinstance(error, DownloadError):
        await ctx.send(embeds.cmd_error("Please enter a valid YouTube URL."))

@bot.command()
async def help(ctx, opt='general'):
    await ctx.send(embed=embeds.help_command(opt))

bot.run(settings.get("bot_secret"))
