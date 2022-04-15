import discord
from discord.ext import commands
import json
from downloader import Downloader
import os
import embeds

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
    download = Downloader(url, '/home/aaatipamula/downloads', '/home/aaatipamula/downloads')

    option = getattr(download, f"download_{opt}", ".")
    
    if option is None:
        await ctx.send(embed=embeds.cmd_error("Please enter a valid option."))
    else:
        option()
        
        if opt == 'audio':
            await ctx.send(embed=embeds.embed_a("Audio is here!"), file=discord.File(f'/home/aaatipamula/downloads/{download.video_title}.mp3'))
            os.remove(f'/home/aaatipamula/downloads/{download.video_title}.mp3')

        # elif opt == 'video':
        #     ctx.send(embeds.embed_b("Video is here!", file=discord.File(f'/home/aaatipamula/downloads/{download.video_title}.mp4')))
        #     os.remove(f'/home/aaatipamula/downloads/{download.video_title}.mp4')

        # elif opt == 'both':
        #     ctx.send(embeds.embed_b("Audio is here!", file=discord.File(f'/home/aaatipamula/downloads/{download.video_title}.mp3')))
        #     ctx.send(embeds.embed_b("Video is here!", file=discord.File(f'/home/aaatipamula/downloads/{download.video_title}.mp4')))
        #     os.remove(f'/home/aaatipamula/downloads/{download.video_title}.mp3')
        #     os.remove(f'/home/aaatipamula/downloads/{download.video_title}.mp4')

@bot.command()
async def help(ctx, opt='general'):
    await ctx.send(embed=embeds.help_command(opt))

bot.run(settings.get("bot_secret"))
