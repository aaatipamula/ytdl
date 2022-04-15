import discord
import json
import os
import random

os.chdir(__file__.strip('embeds.py'))
commands = json.load(open('commands.json'))

#embed on command error
def cmd_error(value):
    a = discord.Embed(color=0xD40D08)
    a.add_field(name= "Error!", value= value)
    return a

#title only embed
def embed_a(title):
    a = discord.Embed(title= title, color=0xD40D08)
    return a

#name and value only embed
def embed_b(name, value):
    a = discord.Embed(color=0xD40D08)
    a.add_field(name= name, value= value)
    return a

#title, name, and value embed
def embed_c(title, name, value):
    a = discord.Embed(title= title, color=0xD40D08)
    a.add_field(name= name, value= value)
    return a

#help command, scalable through the commands.json file
def help_command(opt):

    opts = ["Help Has Arrived!", "At Your Service!", "HI!"]

    if opt == 'general':
        cmdEmbed = discord.Embed(title=random.choice(opts), color=0xD40D08)
        cmdEmbed.add_field(name="About Me!", value="I am a bot that converts YT videos into mp3 and mp4 and gives it to you!\n\nBelow are some commands you can use with me. For any extra information on a command type the *help* command again along with the name of the command.")
        for x in commands:
            cmdEmbed.add_field(name=f"*{x}*", value="\u200b", inline=False)
        cmdEmbed.set_footer(text= "Bot Command Prefix = '.'")
        return cmdEmbed

    elif opt not in commands:
        return cmd_error("Not a valid option.")

    elif opt in commands:
        cmd = commands.get(opt)
        return embed_c(f"{opt} {cmd[0]}", cmd[1], cmd[2])
