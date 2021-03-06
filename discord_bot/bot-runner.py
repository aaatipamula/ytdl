import discord
from discord.ext import commands
from downloader import Downloader
from yt_dlp import DownloadError
import traceback as tb
import json
import embeds
import functions as fn
from datetime import datetime as dt

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)

settings = json.load(open('./discord_bot/settings.json'))

@bot.event
async def on_ready():
    print('I am ready')
    bot_channel = bot.get_channel(settings.get('bot_channel'))
    await bot_channel.send("I Am Ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="In development!"))


@bot.command()
async def download(ctx, opt :str, url :str):

    opt = opt.lower()
    
    if opt not in ['mp3', 'webm']:
        await ctx.send(embed=embeds.cmd_error("Please enter a valid option!"))
        return

    elif "&list=" in url:
        url = url.split("&list=")[0]
        await ctx.send(embed=embeds.cmd_error("Warning, Playlists are not supported!\n\nThis video will be downloaded instead:\n{url}"))
        return

    elif "playlist?list=" in url:
        await ctx.send(embed=embeds.cmd_error("Warning, Playlists are not supported! Please select the url of a single video you would like to download."))
        return
    
    download = Downloader(url, settings.get("mp3_dir"), settings.get("webm_dir"))

    prev_id = fn.check_contentids(download.base64_string + f'${opt}')
    
    if prev_id is not None:
        await ctx.send(embed=embeds.embed_b(f"Your Content is Here!", f"{settings.get('website_name')}{prev_id} \n\nThis link will be active for the next 24 hours!"))

    else:

        option = getattr(download, f"download_{opt}", ".")
        option()
        
        req_id = fn.dump_id(download.base64_string + f"${opt}") 
        
        await ctx.send(embed=embeds.embed_b(f"Your Content is Here!", f"{settings.get('website_name')}{req_id} \n\nThis link will be active for the next 24 hours!"))

@download.error
async def download_error(ctx, error):

    if isinstance(error, DownloadError):
        await ctx.send(embeds.cmd_error("Please enter a valid YouTube URL."))

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=embeds.cmd_error('Please enter all required arguments, *format* and *url*'))
    
    else:
        print(f"{error}\n{''.join(tb.format_exception(None, error, error.__traceback__))}")

@bot.command()
async def help(ctx, opt='general'):
    await ctx.send(embed=embeds.help_command(opt))

bot.run(settings.get("bot_secret"))