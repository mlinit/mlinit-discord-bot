import os
import discord
import math

import pandas as pd

from discord.ext import commands, pages
from dotenv import load_dotenv

from analysis import utils
from analysis import describe
from analysis import outliers
from analysis import contents

# token for dc bot
load_dotenv()

# global
TOKEN = os.getenv("TOKEN")
MSGLIMIT = 2000
COLS_PER_PAGE = 7
INFORMATION_THUMBNAIL_URL = "https://i.imgur.com/KY5QcLw.jpg"
SUMMARY_THUMBNAIL_URL = "https://i.imgur.com/P1ZNLBa.jpg"
OUTLIERS_THUMBNAIL_URL = "https://i.imgur.com/FmNH0qi.jpg"
DUPLICATES_THUMBNAIL_URL = "https://i.imgur.com/NMDm8A2.jpg"
ICON_URL = "https://i.imgur.com/E7Ppwmj.png"


bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="need some help?", color=discord.Color.dark_teal())
        for _, commands in mapping.items():
            command_signatures = [self.get_command_signature(c) for c in commands]
            if command_signatures:
                # cog_name = getattr(cog, "qualified_name", "list of commands")
                val = contents.get_general_help()
                embed.add_field(name="", value=val, inline=False)
                embed.set_author(name="🤖 mLinit")
                embed.set_footer(text="sent by MLinit", icon_url=ICON_URL)
        
        channel = self.get_destination()
        await channel.send(embed=embed)
        
    async def send_command_help(self, command):
        command_name = self.get_command_signature(command)
        command_name = command_name.split(' ')[0][1:]
        embed = discord.Embed(
            title=f"help for **{command_name}**",
            color=discord.Color.dark_teal()
        )
        
        if command.help:
            embed.description = command.help
            embed.set_author(name="🤖 mLinit")
            embed.set_footer(text="sent by mLinit", icon_url=ICON_URL)
        
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()


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
@bot.command(name="info", help=contents.get_info_help())
async def information(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    resp.name = url.split("/")[-1]
         
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:    
        des = describe.Describe(resp)
        rows, feats, null, dtypes, memuse = des.perform_info()
        
        await ctx.reply(f"analyzing your data 🔃")
        
        info_embed_pages = []
        num_bins = math.ceil(len(feats) / COLS_PER_PAGE)
        
        for i in range(num_bins):
            embed = discord.Embed(
                title="**dataset information** ℹ️",
                description=f"here is the information related to the dataset _{resp.name}_\nit contains **{rows}** rows and **{len(feats)}** columns\n\n{'⎯'*10}\n‎‎ ",
                color=discord.Color.dark_teal()
            )
            for j, fe in enumerate(feats[COLS_PER_PAGE*i: COLS_PER_PAGE*(i+1)]):
                ind = COLS_PER_PAGE*i + j
                embed.add_field(
                    name=f"✅ **{fe}**",
                    value=f"• {null[ind]} null values\n• data type: {dtypes[ind]}",
                    inline=False
                )
                
            embed.add_field(name=f"📚 Memory usage", value=f"{str(memuse)}", inline=True)       
        
            embed.set_thumbnail(url=INFORMATION_THUMBNAIL_URL)
            embed.set_author(name="🤖 mLinit")
            embed.set_footer(text="analyzed by mLinit", icon_url=ICON_URL)
            info_embed_pages.append(embed)
            
        info_paginator = pages.Paginator(
            pages=info_embed_pages,
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=get_page_buttons(),
            loop_pages=True,
        )
        
        t_msg = f"{user.mention} check your DM for the result ✔️"
        await info_paginator.send(ctx, target=user, target_message=t_msg)
        
            
@information.error
async def info_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")


# --------------------- DESCRIPTION ----------------------
@bot.command(name="des", help=contents.get_des_help())
async def description(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    resp.name = url.split("/")[-1]
         
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:
        des = describe.Describe(resp)
        _, feats, count, uniq, top, freq, mean, std, mini, q25, q50, q75, maxi = des.perform_summ()
        
        await ctx.reply(f"analyzing your data 🔃")
        
        summ_embed_pages = []
        num_bins = math.ceil(len(feats) / COLS_PER_PAGE)
        
        for i in range(num_bins):
            embed = discord.Embed(
                title="**dataset summary** 📝",
                description=f"here is the summary related to the dataset _{resp.name}_'s features\nit shows the statistical measures of **{len(feats)}** columns\n\n{'⎯'*10}\n‎‎ ",
                color=discord.Color.dark_teal()
            )
            for j, fe in enumerate(feats[COLS_PER_PAGE*i: COLS_PER_PAGE*(i+1)]):
                ind = COLS_PER_PAGE*i + j
                val = f"• count: {count[ind]}\n"
                val = val + f"• unique: {uniq[ind]}\n" if not pd.isnull(uniq[ind]) else val
                val = val + f"• top: {top[ind]}\n" if not pd.isnull(top[ind]) else val
                val = val + f"• frequency: {freq[ind]}\n" if not pd.isnull(freq[ind]) else val
                val = val + f"• mean: {mean[ind]}\n" if not pd.isnull(mean[ind]) else val
                val = val + f"• std: {std[ind]}\n" if not pd.isnull(std[ind]) else val
                val = val + f"• minimum: {mini[ind]}\n" if not pd.isnull(mini[ind]) else val
                val = val + f"• quantile 1 (25%): {q25[ind]}\n" if not pd.isnull(q25[ind]) else val
                val = val + f"• quantile 2 (50%): {q50[ind]}\n" if not pd.isnull(q50[ind]) else val
                val = val + f"• quantile 1 (75%): {q75[ind]}\n" if not pd.isnull(q75[ind]) else val
                val = val + f"• maximum: {maxi[ind]}\n" if not pd.isnull(maxi[ind]) else val
                
                embed.add_field(
                    name=f"✅ **{fe}**",
                    value=val,
                    inline=False
                )      
        
            embed.set_thumbnail(url=SUMMARY_THUMBNAIL_URL)
            embed.set_author(name="🤖 mLinit")
            embed.set_footer(text="analyzed by mLinit")
            summ_embed_pages.append(embed)
            
        info_paginator = pages.Paginator(
            pages=summ_embed_pages,
            show_disabled=True,
            show_indicator=True,
            use_default_buttons=False,
            custom_buttons=get_page_buttons(),
            loop_pages=True,
        )
        
        t_msg = f"{user.mention} check your DM for the result ✔️"
        await info_paginator.send(ctx, target=user, target_message=t_msg)


@description.error
async def des_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")


# ------------------------- DUPLICATES -------------------------------
@bot.command(name="dup", help=contents.get_dup_help())
async def duplicates(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:
        resp.name = url.split("/")[-1]  
        des = describe.Describe(resp)
        duprows, dupcols = des.perform_dupl()
        
        await ctx.reply(f"analyzing your data 🔃")
        embed = discord.Embed(
            title="**duplicates in the dataset** ✌🏻",
            description=f"here is the information related to the duplicate rows in the dataset _{resp.name}_\n\n{'⎯'*10}\n‎‎ ",
            color=discord.Color.dark_teal()
        )
        
        embed.add_field(
            name=f"✅ original dataset has",
            value=f"• **{resp.shape[0]}** rows and **{resp.shape[1]}** columns",
            inline=False
        )
        embed.add_field(
            name=f"✅ duplicates analysis",
            value=f"• **{duprows}** duplicate rows and **{len(dupcols)}** columns",
            inline=False
        )
        embed.add_field(
            name="",
            value=f"\nafter removing the duplicate rows, dataset shape will be\n```{resp.shape[0] - duprows} rows x {len(dupcols)} columns```‎‎ ",
            inline=False
        )
        
        embed.set_thumbnail(url=DUPLICATES_THUMBNAIL_URL)
        embed.set_author(name="🤖 mLinit")
        embed.set_footer(text="analyzed by mLinit", icon_url=ICON_URL)
        
        await ctx.send(f"{user.mention} check your DM for the result ✔️")
        await user.send(embed=embed)

@duplicates.error
async def dup_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")


# ----------------------- OUTLIERS --------------------------------------
class OutlierView(discord.ui.View):
    def __init__(self, ctx, user, df):
        super().__init__()
        self.df = df
        self.ctx = ctx
        self.user = user
    
    @discord.ui.select(
        placeholder="Choose an option...",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="z-score",
                description="choose this for analyzing outliers using z-score",
                emoji="♎"
            ),
            discord.SelectOption(
                label="quantile",
                description="choose this for analyzing outliers using quantiles",
                emoji="📦"
            )
        ]
    )
    async def out_callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "z-score":
            await interaction.response.defer()
            
            out = outliers.Outliers(self.df)
            feats, zouts = out.perform_zscore_out()
            
            out_embed_pages = []
            num_bins = math.ceil(len(feats) / COLS_PER_PAGE)
        
            await self.ctx.reply(f"analyzing your data 🔃")
        
            for i in range(num_bins):
                embed = discord.Embed(
                    title="**dataset outliers using Z-SCORE** 🚫",
                    description=f"here are the outliers related to the dataset _{self.df.name}_'s features\nit shows the outlier numbers of **{len(feats)}** columns using the **Z-score** test\n\n{'⎯'*10}\n‎‎ ",
                    color=discord.Color.dark_teal()
                )
                for j, fe in enumerate(feats[COLS_PER_PAGE*i: COLS_PER_PAGE*(i+1)]):
                    ind = COLS_PER_PAGE*i + j
                    embed.add_field(
                        name=f"✅ **{fe}**",
                        value=f"• {zouts[ind]} outlier(s)\n",
                        inline=False
                    )
                    
                embed.set_thumbnail(url=OUTLIERS_THUMBNAIL_URL)
                embed.set_author(name="🤖 mLinit")
                embed.set_footer(text="analyzed by mLinit", icon_url=ICON_URL)
                out_embed_pages.append(embed)
                
            out_paginator = pages.Paginator(
                pages=out_embed_pages,
                show_disabled=True,
                show_indicator=True,
                use_default_buttons=False,
                custom_buttons=get_page_buttons(),
                loop_pages=True,
            )
            
            t_msg = f"{self.user.mention} check your DM for the result ✔️"
            await out_paginator.send(self.ctx, target=self.user, target_message=t_msg)            

        if select.values[0] == "quantile":
            await interaction.response.defer()
            out = outliers.Outliers(self.df)
            feats, lower_outs, upper_outs = out.perform_quantile_out()
            
            out_embed_pages = []
            num_bins = math.ceil(len(feats) / COLS_PER_PAGE)
        
            await self.ctx.reply(f"analyzing your data 🔃")
        
            for i in range(num_bins):
                embed = discord.Embed(
                    title="**dataset outliers using Quantiles** 🚫",
                    description=f"here are the outliers related to the dataset _{self.df.name}_'s features\nit shows the outlier numbers of **{len(feats)}** columns using the **Quantiles** test\n\n{'⎯'*10}\n‎‎ ",
                    color=discord.Color.dark_teal()
                )
                for j, fe in enumerate(feats[COLS_PER_PAGE*i: COLS_PER_PAGE*(i+1)]):
                    ind = COLS_PER_PAGE*i + j
                    embed.add_field(
                        name=f"✅ **{fe}**",
                        value=f"• {lower_outs[ind]} lower outlier(s)\n• {upper_outs[ind]} upper outlier(s)",
                        inline=False
                    )
                    
                embed.set_thumbnail(url=OUTLIERS_THUMBNAIL_URL)
                embed.set_author(name="🤖 mLinit")
                embed.set_footer(text="analyzed by mLinit", icon_url=ICON_URL)
                out_embed_pages.append(embed)
                
            out_paginator = pages.Paginator(
                pages=out_embed_pages,
                show_disabled=True,
                show_indicator=True,
                use_default_buttons=False,
                custom_buttons=get_page_buttons(),
                loop_pages=True,
            )
            
            t_msg = f"{self.user.mention} check your DM for the result ✔️"
            await out_paginator.send(self.ctx, target=self.user, target_message=t_msg)


@bot.command(name="out", help=contents.get_out_help())
async def outliers_analysis(ctx, url: str, user: discord.User):
    resp = utils.read_dataset_from_url(url)
    resp.name = url.split("/")[-1]
    
    if isinstance(resp, str):
        await ctx.reply(resp)
    else:
        await ctx.reply("cool, tell me the method", view=OutlierView(ctx, user, resp))


@outliers_analysis.error
async def out_error(ctx, err):
    if isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.reply("bruh, missing arguments for this command 🤨")

# driver code
bot.run(TOKEN)