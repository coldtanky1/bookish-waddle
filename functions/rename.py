import discord
from discord.ext import commands

from db import Info, Nation

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rename(self, ctx, *args: str):
        user_id = ctx.author.id

        new_name = ' '.join(args)

        if new_name == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You forgot to write the new name.\n\n'
                                              f'Command Format: `$rename [new_name]`')
            await ctx.send(embed=embed)

        if len(new_name) > 25:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Your nation name cannot be longer than 25 characters.')
            await ctx.send(embed=embed)
            return

        name_taken = Nation.select().where(Nation.nation_name == new_name).exists()
        if name_taken:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'That name is already used.')
            await ctx.send(embed=embed)
            return

        if Info.get_or_none(Info.user_id==user_id) is not None:
            Nation.update(nation_name=new_name).execute()

            embed = discord.Embed(
                title='Nation Rename',
                description=f'You have successfully changed your nation\'s name to **{new_name}**!',
                color=0x5BF9A0
            )
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Rename(bot))
