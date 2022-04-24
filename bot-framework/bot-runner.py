import discord
from discord.ext import commands
import json
from downloader import Downloader
import os
import embeds
import base64

bot = commands.Bot(command_prefix='!', case_insensitive=True, help_command=None)

os.chdir(__file__.strip('bot-runner.py'))
settings = json.load(open('settings.json'))

@bot.event
async def on_ready():
    print('I am ready')
    bot_channel = bot.get_channel(914650069687492729)
    await bot_channel.send("I Am Ready")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="In development!"))

@bot.command()
async def download(ctx, opt, url):
    download = Downloader(url, '/home/aaatipamula/vscode_projects/ytdlp-website/src/downloads', '/home/aaatipamula/vscode_projects/ytdlp-website/src/downloads')

    if url.startswith('https://www.youtube.com') is False or url.startswith('www.youtube.com') is False:
        await ctx.send(embed=embeds.cmd_error("Please enter a valid YouTube URL!"))

    option = getattr(download, f"download_{opt}", ".")
    
    if option is None:
        await ctx.send(embed=embeds.cmd_error("Please enter a valid option."))
    else:
        option()
        
        if opt == 'audio':
            await ctx.send(embed=embeds.embed_b("Audio is Here!", f'websiteurlhere.com/downloads/{download.base64_string}\n\nSave the code below to access your video download for the next 24 hours!: \n {download.base64_string}'))

        elif opt == 'video':
            await ctx.send(embed=embeds.embed_b("Video is Here!", f'websiteurlhere.com/downloads/{download.base64_string}\n\nSave the code below to access your video download for the next 24 hours!: \n {download.base64_string}'))

@bot.command()
async def help(ctx, opt='general'):
    await ctx.send(embed=embeds.help_command(opt))

bot.run(settings.get("bot_secret"))
