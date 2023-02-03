import os
import discord
import asyncio
import math

import pandas as pd

from discord.ext import commands, pages
from dotenv import load_dotenv

from analysis import utils
from analysis import describe

# token for dc bot
load_dotenv()

# global
TOKEN = os.getenv("TOKEN")
MSGLIMIT = 2000
COLS_PER_PAGE = 7
INFORMATION_THUMBNAIL_URL = "https://i.imgur.com/KY5QcLw.jpg"
SUMMARY_THUMBNAIL_URL = "https://i.imgur.com/P1ZNLBa.jpg"


bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    

# -------------------- Helpers -----------------------------
def get_page_buttons():
    page_buttons = [
        pages.PaginatorButton(
            "first", emoji="⏪", style=discord.ButtonStyle.green
        ),
        pages.PaginatorButton("prev", emoji="⬅", style=discord.ButtonStyle.green),
        pages.PaginatorButton(
            "page_indicator", style=discord.ButtonStyle.gray, disabled=True
        ),
        pages.PaginatorButton("next", emoji="➡", style=discord.ButtonStyle.green),
        pages.PaginatorButton("last", emoji="⏩", style=discord.ButtonStyle.green),
    ]
    
    return page_buttons
    

# ------------------ INFORMATION ----------------------
@bot.command(name="info")
async def information(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    resp.name = url.split("/")[-1]
         
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:    
        des = describe.Describe(resp)
        rows, feats, null, dtypes, memuse = des.perform_info()
        
        await ctx.send(f"{ctx.message.author.mention} analyzing your data...🔃")
        
        info_embed_pages = []
        num_bins = math.ceil(len(feats) / COLS_PER_PAGE)
        
        for i in range(num_bins):
            embed = discord.Embed(
                title="**dataset information** 📝",
                description=f"here is the information related to\nthe dataset _{resp.name}_\n\nit contains **{rows}** rows and **{len(feats)}** columns...",
                color=discord.Color.dark_teal()
            )
            for j, fe in enumerate(feats[7*i: 7*(i+1)]):
                embed.add_field(
                    name=f"✅ **{fe}**",
                    value=f"• {null[j]} null values\n• data type: {dtypes[j]}",
                    inline=False
                )
                
            embed.add_field(name=f"📚 Memory usage", value=f"{str(memuse)}", inline=True)       
        
            embed.set_thumbnail(url=INFORMATION_THUMBNAIL_URL)
            embed.set_author(name="🤖 MLinit")
            embed.set_footer(text="analyzed by MLinit")
            info_embed_pages.append(embed)
            
        info_paginator = pages.Paginator(
            pages=info_embed_pages,
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=get_page_buttons(),
            loop_pages=True,
        )
        
        t_msg = f"{ctx.message.author.mention} check your DM for the result 😁"
        await info_paginator.send(ctx, target=user, target_message=t_msg)
        
            
@information.error
async def info_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")


# --------------------- DESCRIPTION ----------------------
@bot.command(name="des")
async def description(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    resp.name = url.split("/")[-1]
         
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:
        des = describe.Describe(resp)
        _, feats, count, uniq, top, freq, mean, std, mini, q25, q50, q75, maxi = des.perform_summ()
        
        await ctx.send(f"{ctx.message.author.mention} analyzing your data...🔃")
        
        summ_embed_pages = []
        num_bins = math.ceil(len(feats) / COLS_PER_PAGE)
        
        for i in range(num_bins):
            embed = discord.Embed(
                title="**dataset summary** 📝",
                description=f"here is the summary related to\nthe dataset _{resp.name}_'s features\n\nit shows the statistical measures of **{len(feats)}** columns...",
                color=discord.Color.dark_teal()
            )
            for j, fe in enumerate(feats[7*i: 7*(i+1)]):
                val = f"• count: {count[j]}\n"
                val = val + f"• unique: {uniq[j]}\n" if not pd.isnull(uniq[j]) else val
                val = val + f"• top: {top[j]}\n" if not pd.isnull(top[j]) else val
                val = val + f"• frequency: {freq[j]}\n" if not pd.isnull(freq[j]) else val
                val = val + f"• mean: {mean[j]}\n" if not pd.isnull(mean[j]) else val
                val = val + f"• std: {std[j]}\n" if not pd.isnull(std[j]) else val
                val = val + f"• minimum: {mini[j]}\n" if not pd.isnull(mini[j]) else val
                val = val + f"• quantile 1 (25%): {q25[j]}\n" if not pd.isnull(q25[j]) else val
                val = val + f"• quantile 2 (50%): {q50[j]}\n" if not pd.isnull(q50[j]) else val
                val = val + f"• quantile 1 (75%): {q75[j]}\n" if not pd.isnull(q75[j]) else val
                val = val + f"• maximum: {maxi[j]}\n" if not pd.isnull(maxi[j]) else val
                
                embed.add_field(
                    name=f"✅ **{fe}**",
                    value=val,
                    inline=False
                )      
        
            embed.set_thumbnail(url=SUMMARY_THUMBNAIL_URL)
            embed.set_author(name="🤖 MLinit")
            embed.set_footer(text="analyzed by MLinit")
            summ_embed_pages.append(embed)
            
        info_paginator = pages.Paginator(
            pages=summ_embed_pages,
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=get_page_buttons(),
            loop_pages=True,
        )
        
        t_msg = f"{ctx.message.author.mention} check your DM for the result 😁"
        await info_paginator.send(ctx, target=user, target_message=t_msg)


@description.error
async def des_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")


# ------------------------- DUPLICATES -------------------------------
@bot.command(name="dup")
async def duplicates(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    resp.name = url.split("/")[-1]
    
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:
        des = describe.Describe(resp)
        duprows, dupcols = des.perform_dupl()
        
        await ctx.reply(f"analyzing your data...🔃")
        embed = discord.Embed(
            title="**duplicates in the dataset** ✌🏻",
            description=f"here is the information related to\nthe duplicate rows in the dataset _{resp.name}_\n",
            color=discord.Color.dark_teal()
        )
        
        embed.add_field(
            name=f"✅ original dataset has",
            value=f"• {resp.shape[0]} rows and {resp.shape[1]} columns",
            inline=False
        )
        embed.add_field(
            name=f"✅ duplicates analysis",
            value=f"• **{duprows}** duplicate rows and **{len(dupcols)}** columns",
            inline=False
        )
        embed.add_field(
            name="",
            value=f"\nafter removing the duplicate rows, dataset shape will be\n**{resp.shape[0] - duprows}** X **{len(dupcols)}**\n",
            inline=False
        )
        
        embed.set_thumbnail(url=SUMMARY_THUMBNAIL_URL)
        embed.set_author(name="🤖 MLinit")
        embed.set_footer(text="analyzed by MLinit")
        
        await ctx.send(f"{user.mention} check your DM for the result 😁")
        await user.send(embed=embed)

@duplicates.error
async def dup_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")


# driver code
bot.run(TOKEN)