import logging
from discord.ext import commands

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbosity
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Log to file
        logging.StreamHandler()         # Also print to terminal
    ]
)

logger = logging.getLogger("pwboat")  # Customize your logger name

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logger.error(f"Error in command {ctx.command}: '{error}'", exc_info=True)
        await ctx.send("An error occurred.")

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
