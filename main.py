import os
import discord
import math

from discord.ext import commands
from dotenv import load_dotenv
from analysis import describe
from analysis.utils import read_dataset_from_url, split_into_parts

# token for dc bot
load_dotenv()

# global
TOKEN = os.getenv("TOKEN")
MSGLIMIT = 2000


bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="des")
async def description(ctx, url: str):
    resp = read_dataset_from_url(url)
         
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:    
        des = describe.Describe(resp)
        reply = ctx.message.author.mention + "\nthe dataset contains the following features/columns.\n\n"
        info = des.perform_info()
        reply += info
        
        if len(reply) > MSGLIMIT:
            replies = split_into_parts(reply, MSGLIMIT) 
            for rep in replies:
                await ctx.send(rep)
        else:
            await ctx.send(reply)
            
@description.error
async def des_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, you forgot to enter the dataset URL? 🤨")


# driver code
bot.run(TOKEN)