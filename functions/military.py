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

            inf_food = round(amount * 0.03)
            inf_water = round(amount * 0.02)
            inf_turns = int(round(amount * 0.00003 + 1))

            if (res.water < inf_water) or (res.processed_food < inf_food):
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
                res.update(processed_food=res.processed_food-inf_food, water=res.water-inf_water).execute()

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def produce(self, ctx, mil_type: str = "", amount: int = 0):
        user_id = ctx.author.id
        mil_type = mil_type.lower()

        mil_production = [
            # Format goes: MIL_TYPE, COST_STEEL, COST_ELECTRONICS, COST_PETROL, FIELD_NAME_IN_DB
            ("Tank", 50, 10, 20, "tanks"),
            ("Plane", 40, 20, 40, "planes"),
            ("Artillery", 30, 10, 10, "artillery"),
            ("Anti-air", 20, 15, 5, "anti_air"),
        ]

        if mil_type == "":
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                            description="Please choose a valid type.")
            await ctx.send(embed=embed)
            return

        if amount <= 0:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                            description="Invalid amount, please try a positive number.")
            await ctx.send(embed=embed)
            return

        if Info.get_or_none(Info.user_id==user_id) is not None:
            res = Resources.select().where(Resources.user_id==user_id).first()
            mil = Mil.select().where(Mil.user_id==user_id).first()

            mil_id = None
            match mil_type:
                case "tank":
                    mil_id = 0
                case "plane":
                    mil_id = 1
                case "artillery" | "arty":
                    mil_id = 2
                case "aa" | "anti-air" | "anti_air":
                    mil_id = 3
                case _:
                    embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                    description="Please choose a valid type.")
                    await ctx.send(embed=embed)
                    return

            cost_steel = mil_production[mil_id][1] * amount
            cost_elec = mil_production[mil_id][2] * amount
            cost_petrol = mil_production[mil_id][3] * amount

            mil_type_to_update = getattr(Mil, mil_production[mil_id][4])

            if (res.steel < cost_steel) or (res.electronics < cost_elec) or (res.petrol < cost_petrol):
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                description="You do not have enough materials for this exchange.")
                await ctx.send(embed=embed)
                return

            else:
                res.update(steel=res.steel-cost_steel, electronics=res.electronics-cost_elec, petrol=res.petrol-cost_petrol).execute()
                mil.update({mil_type_to_update: mil_type_to_update + amount}).execute()

                mil_done = discord.Embed(colour=0xdd7878, title='Military', type='rich',
                                            description='Production complete!')
                await ctx.send(embed=mil_done)

        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.\n'
                                              f'To create one, type `$create [NATION_NAME]`.')
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def doctrine(self, ctx, doctrine: int = 0):
        user_id = ctx.author.id

        doctrines = [
            "Mobile Warfare",
            "Superior Firepower",
            "Grand Battleplan",
            "Mass Assault",
            "Strategic Destruction",
            "Battlefield Support",
        ]

        if doctrine == 0:
            embed = discord.Embed(color=0x780DDB, title="Military Doctrines", type='rich',
                                  description="Displays all the military doctrines.")

            embed.add_field(name="Land Doctrines", value="\n", inline=False)
            for index, ld in enumerate(doctrines[:4], start=1):
                value = f"{index}. " + "".join(ld)
                embed.add_field(name="", value=value, inline=False)

            embed.add_field(name="Air Doctrines", value="\n", inline=False)
            for index, ad in enumerate(doctrines[4:], start=5):
                value = f"{index}. " + "".join(ad)
                embed.add_field(name="", value=value, inline=False)

            await ctx.send(embed=embed)

        else:

            if doctrine > 6:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                                description="Please input a valid number.")
                await ctx.send(embed=embed)

            if Info.get_or_none(Info.user_id==user_id) is not None:
                embed = discord.Embed(color=discord.Color.dark_teal(), title="Setting military doctrine", type='rich',
                                    description=f"setting your military doctrine to {doctrines[doctrine-1]}")
                embed.set_footer(text="Use `$doctrine` to see a list of doctrines.")
                setting_embed = await ctx.send(embed=embed)

                if doctrine == 5 or doctrine == 6:
                    Mil.update(mil_air_doctrine=doctrines[doctrine-1]).execute()
                else:
                    Mil.update(mil_ground_doctrine=doctrines[doctrine-1]).execute()

                done_embed = discord.Embed(color=discord.Color.green(), title="Setting military doctrine", type='rich',
                                        description="Your military doctrine has been set successfully.")
                done_embed.set_footer(text="Use `$doctrine` to see a list of doctrines.")
                await setting_embed.edit(embed=done_embed)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                    description=f'You do not have a nation.\n'
                                                f'To create one, type `$create [NATION_NAME]`.')
                await ctx.send(embed=embed)
                return

async def setup(bot):
    await bot.add_cog(Military(bot))
