import aiowiki
import discord
from discord.ext import commands

# pylint throws an error if I do not include this try statement it's dumb...

try:
	from .utils import scrape
except (SystemError, ImportError):
	import scrape

class GBF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def gbf(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No subcommand passed!")

    @gbf.command()
    async def chara(self, ctx, *, query):
        wiki = aiowiki.Wiki("https://gbf.wiki/api.php")
        pages = await wiki.opensearch(query)
        url = await pages[0].html()

        char = scrape.CharaScraper(url)

        embed = discord.Embed(title=f'{char.title()} {char.name()}',
        description=char.summary())
        embed.set_image(url=char.image())
        embed.set_thumbnail(url=char.element())

        embed.add_field(name='Max HP', value=char.hp())
        embed.add_field(name='Max ATK', value=char.atk())
        embed.add_field(name='Skills',
        value=f"\n".join(char.skills()))

        await ctx.send(embed=embed)
        await wiki.close()

def setup(bot):
    bot.add_cog(GBF(bot))