import discord
from discord.ext import commands
from downloader import Downloader
from yt_dlp import DownloadError
import json
import embeds
import base64
import random
import sqlite3

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)

settings = json.load(open('./settings.json'))

@bot.event
async def on_ready():
    print('I am ready')
    bot_channel = bot.get_channel(914650069687492729)
    await bot_channel.send("I Am Ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="In development!"))

def dump_id(content_id :str):

    req_id = base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8')
    
    connection = sqlite3.connect(settings.get("db_source"))
    cursor = connection.cursor()
    
    a = cursor.execute("SELECT * FROM ids WHERE reqids = \'%s\'" %req_id) 
    b = [x[0] for x in a] 
    
    if req_id in b:
        
        req_id = base64.urlsafe_b64encode(str(random.choice(range(1, 999999))).encode('utf-8')).decode('utf-8')
    
    cursor.execute("INSERT INTO ids (reqids, idone) VALUES (?, ?)", (req_id, content_id))
    
    connection.commit()
    connection.close()
    
    return req_id

@bot.command()
async def download(ctx, opt :str, url :str):

    opt = opt.lower()
    
    if opt not in ['mp3', 'webm']:
        await ctx.send(embed=embeds.cmd_error("Please enter a valid option!"))
        return

    elif "&list=" in url:
        url = url.split("&list=")[0]
        await ctx.send(embed=embeds.cmd_error("Warning, Playlists are not supported!\n\nThis video will be downloaded instead:\n{url}"))

    elif "playlist?list=" in url:
        await ctx.send(embed=embeds.cmd_error("Warning, Playlists are not supported! Please select the url of a single video you would like to download."))
        return
    
    download = Downloader(url, settings.get("webm_dir"), settings.get("mp3_dir"))
    option = getattr(download, f"download_{opt}", ".")
    option()
    
    req_id = dump_id(download.video_title_base64) 
    
    await ctx.send(embed=embeds.embed_b(f"Your Content is Here!", f'http://localhost:8000/{opt}/{req_id} \n\nSave the code below to access your video download for the next 24 hours!:\n\n*{req_id}*'))

@download.error
async def download_error(ctx, error):

    if isinstance(error, DownloadError):
        await ctx.send(embeds.cmd_error("Please enter a valid YouTube URL."))

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embeds.cmd_error('Please enter what format you would like to download the video in!'))

@bot.command()
async def help(ctx, opt='general'):
    await ctx.send(embed=embeds.help_command(opt))

bot.run(settings.get("bot_secret"))