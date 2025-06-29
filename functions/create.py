import discord
from discord.ext import commands

from db import Info, Infra, Mil, Nation, Resources

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx, *args: str):
        id = ctx.author.id

        nation_name = ' '.join(args)

        if nation_name == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please provide a nation name.')
            await ctx.send(embed=embed)
            return

        if len(nation_name) > 25:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Your nation name cannot be longer than 25 characters.')
            await ctx.send(embed=embed)
            return

        if Info.get_or_none(Info.user_id == id) is not None:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You already created a nation.')
            embed.set_footer(text="Dementia")
            await ctx.send(embed=embed)
            return

        name_taken = Nation.select().where(Nation.nation_name == nation_name).exists()
        if name_taken:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'That name is already used.')
            await ctx.send(embed=embed)
            return

        Info.create(user_id=id)

        Nation.create(user_id=id, nation_name=nation_name)

        Mil.create(user_id=id)

        Infra.create(user_id=id)

        Resources.create(user_id=id)

        embed = discord.Embed(
            title='Nation Successfully Created',
            description=f'This is the glorious start of the **{nation_name}**!'
                        f'\nWe wish you a successful journey in leading your people to greatness.',
            color=0x5BF9A0
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Create(bot))
