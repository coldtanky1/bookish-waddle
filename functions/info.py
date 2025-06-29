import json
import discord
from discord.ext import commands

from db import Info

with open("functions/buildings.json", 'r') as file:
    values = json.load(file)

build_codes = [x for x, _ in values.items()]

class BuildingInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, building: str = ""):
        user_id = ctx.author.id
        building = building.lower()

        if Info.get_or_none(Info.user_id==user_id) is not None:
            if building not in build_codes:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                    description=f'Not a valid build code.\n'
                                                f'These are the valid build codes: **{', '.join(build_codes)}**')
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Building Info", type='rich',
                                      description="Displays the info of a building.")

                def format_data(d):
                    if not d:
                        return "None"
                    return ", ".join(f"{k}: {v}" for k, v in d.items())

                embed.add_field(name=f"`{building}`", value="\n"
                                f"**Construction Requirements**\n{format_data(values[building]['construction'])}\n"
                                f"**Inputs** \n{format_data(values[building]['inputs'])}\n"
                                f"**Upkeep** \n{format_data(values[building]['upkeep'])}\n"
                                f"**Output** \n{format_data(values[building]['output'])}", inline=False)

                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BuildingInfo(bot))
