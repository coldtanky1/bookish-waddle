import json
import discord
from discord.ext import commands

from db import Info, Nation, Resources

with open("functions/prices.json", 'r') as file:
    prices = json.load(file)


class IM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def im(self, ctx):
        user_id = ctx.author.id

        if Info.get_or_none(Info.user_id==user_id) is not None:
            embed = discord.Embed(color=discord.Color.green(), title="International Market", type='rich',
                                  description="Displays the products on the international market.")
            for k, v in prices.items():
                value = f"{k}: {v['buy']} | {v['sell']}"
                embed.add_field(name="", value=value, inline=False)

            embed.set_footer(text="Format is: ITEM: BUY_PRICE | SELL_PRICE")

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, mat: str = "", amount: int = 0):
        user_id = ctx.author.id

        if mat == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a material.\n')
            await ctx.send(embed=embed)

        if amount == 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a valid amount.\n')
            await ctx.send(embed=embed)

        if Info.get_or_none(Info.user_id==user_id) is not None:
            res = Resources.select().where(Resources.user_id==user_id).first()
            nation = Nation.select().where(Nation.user_id==user_id).first()

            bill = amount * prices[mat]["buy"]

            if nation.balance < bill:
                embed = discord.Embed(colour=0xEF2F73, title="Market Order", type='rich',
                                    description=f'You do not have enough money.\n')
                await ctx.send(embed=embed)

            else:
                field = getattr(Resources, mat)
                res.update({field: field + amount}).execute()

                nation.update(balance=nation.balance-bill).execute()

                order_done = discord.Embed(title="Market Order", type='rich', description="Order fulfilled!",
                                                   color=0x5BF9A0)
                await ctx.send(embed=order_done)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)


    @commands.command()
    async def sell(self, ctx, mat: str = "", amount: int = 0):
        user_id = ctx.author.id

        if mat == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a material.\n')
            await ctx.send(embed=embed)

        if amount == 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a valid amount.\n')
            await ctx.send(embed=embed)

        if Info.get_or_none(Info.user_id==user_id) is not None:
            res = Resources.select().where(Resources.user_id==user_id).first()
            nation = Nation.select().where(Nation.user_id==user_id).first()

            bill_of_sale = prices[mat]["sell"] * amount

            field = getattr(Resources, mat)

            if getattr(res, mat) < amount:
                embed = discord.Embed(colour=0xEF2F73, title="Market Sell", type='rich',
                                    description=f'You don\'t have enough materials for this sale.\n')
                await ctx.send(embed=embed)

            else:
                nation.update(balance=nation.balance+bill_of_sale).execute()
                res.update({field: field - amount}).execute()

                order_done = discord.Embed(title="Market Sell", type='rich', description="Sale fulfilled!",
                                                   color=0x5BF9A0)
                await ctx.send(embed=order_done)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(IM(bot))
