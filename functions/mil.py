import discord
from discord.ext import commands

from db import Info, Mil, Nation, Resources


class Military(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def recruit(self, ctx, amount: int = 0):
        user_id = ctx.author.id

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                            description="Invalid amount, please try a positive number.")
            await ctx.send(embed=embed)
            return

        if Info.get_or_none(Info.user_id==user_id) is not None:
            res = Resources.select().where(Resources.user_id==user_id).first()
            nation = Nation.select().where(Nation.user_id==user_id).first()
            mil = Mil.select().where(Mil.user_id==user_id).first()

            if mil.in_recruitment > 0:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                        description="You already have soldiers in recruitment. You cannot recruit at this time.")
                await ctx.send(embed=embed)
                return

            inf_grain = round(amount * 0.03)
            inf_water = round(amount * 0.02)
            inf_turns = int(round(amount * 0.00003 + 1))

            if (res.water < inf_water) or (res.grain < inf_grain):
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                        description="You do not have enough resources to recruit.")
                await ctx.send(embed=embed)
                return

            else:
                emb = discord.Embed(title='Recruitment', type='rich', colour=0xDD7878,
                                    description=f'{amount:,} soldier(s) will be recruited into {nation.nation_name}\'s military.\n'
                                                f'They will be ready within {inf_turns} turn(s).')
                await ctx.send(embed=emb)

                mil.update(recruiting_time_left=inf_turns, in_recruitment=amount).execute()
                res.update(grain=res.grain-inf_grain, water=res.water-inf_water).execute()

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)
