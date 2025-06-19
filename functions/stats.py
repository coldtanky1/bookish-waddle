import discord
from discord.ext import commands

from db import Info, Mil, Nation
from functions.construct import Construct

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, user: discord.Member = None): # type: ignore

        if user is None:
            user_id = ctx.author.id
        else:
            user_id = user.id

        if Info.get_or_none(Info.user_id==user_id) is not None:
            nation = Nation.select().where(Nation.user_id==user_id).first()

            embed = discord.Embed(
                title=f"\U0001f4ca {nation.nation_name}'s Stats",
                description=f'Name: {nation.nation_name}',
                color=0x04a5e5
            )
            embed.add_field(name="", value="\n"
                f"\U0001fac5 Ruler: <@{user_id}>\n"
                f"\U0001f60a Happiness: {nation.happiness}", inline=False)

            embed.add_field(name="", value="\n"
                f"\U0001f4b0 Balance: {nation.balance}", inline=False)

            embed.add_field(name="", value="\n"
                f"\U0001f482 Population: {nation.pop}")

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)

    @commands.command()
    async def mstats(self, ctx, user: discord.Member = None): # type: ignore

        if user is None:
            user_id = ctx.author.id
        else:
            user_id = user.id

        if Info.get_or_none(Info.user_id==user_id) is not None:
            milstats = Mil.select().where(Mil.user_id==user_id).first()
            nation = Nation.select().where(Nation.user_id==user_id).first()

            embed = discord.Embed(
                title=f"\u2694 {nation.nation_name}'s Military Stats",
                description='',
                color=0xe64553
            )

            embed.add_field(name="\U0001fa96 Troops", value=f"{milstats.troops:,}\n", inline=False)
            embed.add_field(name="\u26df Tanks", value=f"{milstats.tanks:,}\n", inline=False)
            embed.add_field(name="\U0001f4a5 Artillery", value=f"{milstats.artillery:,}\n", inline=False)
            embed.add_field(name="\U0001f4a5 Anti-Air", value=f"{milstats.anti_air:,}\n", inline=False)
            embed.add_field(name="\U0001f6eb Planes", value=f"{milstats.planes:,}\n", inline=False)
            embed.add_field(name="\U0001f6e1\ufe0f War Status", value=f"{nation.war_status}\n", inline=False)

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot))
