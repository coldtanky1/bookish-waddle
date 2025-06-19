import discord
from discord.ext import commands

from db import Info, Infra, Nation, Resources

# format goes: ("BUILDING_NAME", WOOD_COST, STEEL_COST, MONEY_COST)
structures = [
    ("Iron Mine", 100, 50, 500),
    ("Coal Mine", 100, 50, 500),
    ("Oil Well", 150, 75, 750),
    ("Lumber Camp", 75, 25, 300),
    ("Grain Farm", 75, 25, 300),
    ("Water Plant", 100, 40, 400),

    ("Steel Mill", 150, 100, 1000),
    ("Sawmill", 100, 50, 500),
    ("Flour Mill", 100, 50, 500),
    ("Food Processing", 120, 60, 600),
    ("Oil Refinery", 200, 150, 1200),
    ("Cement Plant", 100, 75, 700),
    ("Electronics Factory", 150, 100, 1000),
]

build_list_code = ["iron_mine", "coal_mine", "oil_well", "lumber_camp", "grain_farm", "water_plant", "steel_mill", "sawmill", "flour_mill", "food_processing", "oil_refinery", "cement_plant", "electronics_factory"]

class Construct(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def construct(self, ctx, building: str = "", amount: int = 0):
        user_id = ctx.author.id

        if building == '':
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a building.')
            await ctx.send(embed=embed)
            return

        building = building.lower()

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f"Amount must be positive.")
            await ctx.send(embed=embed)
            return

        if Info.get_or_none(Info.user_id==user_id) is not None:
            res = Resources.select().where(Resources.user_id==user_id).first()
            bal = Nation.select().where(Nation.user_id==user_id).first()
            infra = Infra.select().where(Infra.user_id==user_id).first()

            match building:
                case "ironmine":
                    build_id = 0
                case "coalmine":
                    build_id = 1
                case "oilwell":
                    build_id = 2
                case "lumbercamp":
                    build_id = 3
                case "grainfarm":
                    build_id = 4
                case "waterplant":
                    build_id = 5
                case "steelmill":
                    build_id = 6
                case "sawmill":
                    build_id = 7
                case "flourmill":
                    build_id = 8
                case "foodprocessor" | "foodprocessing":
                    build_id = 9
                case "oilrefinery":
                    build_id = 10
                case "cementplant":
                    build_id = 11
                case "electronicsfactory" | "electronics":
                    build_id = 12
                case _:
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f'Building not found.')
                    await ctx.send(embed=embed)
                    return

            wood_cost = amount * structures[build_id][1]
            steel_cost = amount * structures[build_id][2]
            money_cost = amount * structures[build_id][3]

            if (res.wood >= wood_cost) and (res.steel >= steel_cost) and (bal.balance >= money_cost):
                res.update(wood=res.wood-wood_cost, steel=res.steel-steel_cost).execute()
                bal.update(balance=bal.balance-money_cost).execute()

                field_name = build_list_code[build_id]
                field = getattr(Infra, field_name)
                infra.update({field: field + amount}).execute()

                cons_done = discord.Embed(colour=0xdd7878, title='Contruct', type='rich',
                                            description='Construction complete!')
                await ctx.send(embed=cons_done)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                            description=f'You do not have enough materials')
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)

    @commands.command()
    async def demolish(self, ctx, building: str = '', amount: int = 0):
        user_id = ctx.author.id

        if building == '':
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'Please specify a building.')
            await ctx.send(embed=embed)
            return

        building = building.lower()

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f"Amount must be positive.")
            await ctx.send(embed=embed)
            return

        if Info.get_or_none(Info.user_id==user_id) is not None:
            infra = Infra.select().where(Infra.user_id==user_id).first()

            match building:
                case "ironmine":
                    build_id = 0
                case "coalmine":
                    build_id = 1
                case "oilwell":
                    build_id = 2
                case "lumbercamp":
                    build_id = 3
                case "grainfarm":
                    build_id = 4
                case "waterplant":
                    build_id = 5
                case "steelmill":
                    build_id = 6
                case "sawmill":
                    build_id = 7
                case "flourmill":
                    build_id = 8
                case "foodprocessor" | "foodprocessing":
                    build_id = 9
                case "oilrefinery":
                    build_id = 10
                case "cementplant":
                    build_id = 11
                case "electronicsfactory" | "electronics":
                    build_id = 12
                case _:
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                              description=f'Building not found.')
                    await ctx.send(embed=embed)
                    return

            field_name = build_list_code[build_id]
            field = getattr(Infra, field_name)

            if amount < field:
                infra.update({field: field - amount}).execute()

                if amount == 1:
                    demo_done = discord.Embed(colour=0xdd7878, title='Demolish', type='rich',
                                            description=f'{amount:,} {structures[build_id][0]} was demolished.')
                    await ctx.send(embed=demo_done)
                else:
                    demo_done = discord.Embed(colour=0xdd7878, title='Demolish', type='rich',
                                            description=f'{amount:,} {structures[build_id][0]}s were demolished.')
                    await ctx.send(embed=demo_done)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                            description=f'You cannot demolish more buildings than you have.')
                await ctx.send(embed=embed)
                return
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Construct(bot))
