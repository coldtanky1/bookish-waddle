import discord
from discord.ext import commands

from db import Info, Infra, Nation, Resources

from helper_funcs.prod_helper import get_net_resource_output

class Production(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def res(self, ctx):
        user_id = ctx.author.id

        if Info.get_or_none(Info.user_id==user_id) is not None:
            infra = Infra.select().where(Infra.user_id==user_id).first()
            nation = Nation.select().where(Nation.user_id==user_id).first()

            embed = discord.Embed(colour=discord.Color.blurple(), title="Production", type='rich', 
                                  description=f"Displays {nation.nation_name}'s production.")

            prod_bonus = nation.admin_production_bonus

            embed.add_field(
                name="Raw Materials",
                value=(
                    f"Iron Ore: {get_net_resource_output(infra, 'iron_ore') * prod_bonus:.0f}\n"
                    f"Coal: {get_net_resource_output(infra, 'coal') * prod_bonus:.0f}\n"
                    f"Oil: {get_net_resource_output(infra, 'oil') * prod_bonus:.0f}\n"
                    f"Wood: {get_net_resource_output(infra, 'wood') * prod_bonus:.0f}\n"
                    f"Grain: {get_net_resource_output(infra, 'grain') * prod_bonus:.0f}\n"
                    f"Water: {get_net_resource_output(infra, 'water') * prod_bonus:.0f}"
                ),
                inline=False
            )

            embed.add_field(
                name="Manufactured Materials",
                value=(
                    f"Steel: {get_net_resource_output(infra, 'steel') * prod_bonus:.0f}\n"
                    f"Planks: {get_net_resource_output(infra, 'planks') * prod_bonus:.0f}\n"
                    f"Flour: {get_net_resource_output(infra, 'flour') * prod_bonus:.0f}\n"
                    f"Processed Food: {get_net_resource_output(infra, 'processed_food') * prod_bonus:.0f}\n"
                    f"Petrol: {get_net_resource_output(infra, 'petrol') * prod_bonus:.0f}\n"
                    f"Concrete: {get_net_resource_output(infra, 'concrete') * prod_bonus:.0f}\n"
                    f"Electronics: {get_net_resource_output(infra, 'electronics') * prod_bonus:.0f}"
                ),
                inline=False
            )

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def reserve(self, ctx):
        user_id = ctx.author.id


        if Info.get_or_none(Info.user_id==user_id) is not None:
            res = Resources.select().where(Resources.user_id==user_id).first()

            embed = discord.Embed(
                title=f"{ctx.author.display_name}'s Resources",
                color=discord.Color.green()
            )

            embed.add_field(
                name="Raw Materials",
                value=(
                    f"Iron Ore: {res.iron_ore}\n"
                    f"Coal: {res.coal}\n"
                    f"Oil: {res.oil}\n"
                    f"Wood: {res.wood}\n"
                    f"Grain: {res.grain}\n"
                    f"Water: {res.water}"
                ),
                inline=False
            )

            embed.add_field(
                name="Manufactured Materials",
                value=(
                    f"Steel: {res.steel}\n"
                    f"Planks: {res.planks}\n"
                    f"Flour: {res.flour}\n"
                    f"Processed Food: {res.processed_food}\n"
                    f"Petrol: {res.petrol}\n"
                    f"Concrete: {res.concrete}\n"
                    f"Electronics: {res.electronics}"
                ),
                inline=False
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(Production(bot))
