import discord
from discord.ext import commands

from db import Info, Infra, Nation

class Infrastructure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def infra(self, ctx):
        user_id = ctx.author.id

        if Info.get_or_none(Info.user_id==user_id) is not None:
            infra_res = Infra.select().where(Infra.user_id==user_id).first()
            nation = Nation.select().where(Nation.user_id==user_id).first()

            embed = discord.Embed(title="Infrastructure", type='rich',
                                  description=f'Displays {nation.nation_name}\'s infrastructure.\n',
                                  color=0x1E66F5)

            embed.add_field(name="", value=f"\n\n"
                            f"Iron Mine: {infra_res.iron_mine}\n"
                            f"Coal Mine: {infra_res.coal_mine}\n"
                            f"Oil Well: {infra_res.oil_well}\n"
                            f"Lumber Camp: {infra_res.lumber_camp}\n"
                            f"Grain Farm: {infra_res.grain_farm}\n"
                            f"Water Plant: {infra_res.water_plant}\n"
                            f"Steel Mill: {infra_res.steel_mill}\n"
                            f"Sawmill: {infra_res.sawmill}\n"
                            f"Flour Mill: {infra_res.flour_mill}\n"
                            f"Food Processor: {infra_res.food_processing}\n"
                            f"Oil Refinery: {infra_res.oil_refinery}\n"
                            f"Cement Plant: {infra_res.cement_plant}\n"
                            f"Electronics Factory: {infra_res.electronics_factory}\n", inline=False)

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Infrastructure(bot))
