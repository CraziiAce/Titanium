from discord.ext import commands
import discord
from pymongo import MongoClient


class config(commands.Cog):
    """Settings for Starry"""
    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.Starry
        self.prfx = db.prefixes

    @commands.group(aliases=['set'])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """Change Starry's settings"""
        pass

    @settings.command()
    async def prefix(self, ctx, *, prefix: str = None):
        """Set Starry's prefix. If no prefix is specified, the prefix will be reset to default."""
        doc = self.prfx.find_one({"_id":ctx.guild.id})
        if not doc:
            if prefix and not doc:
                self.prfx.insert_one({"_id": ctx.guild.id, "prfx": prefix})
                await ctx.send(f"Successfully set the server prefix to {prefix}")
                return
            elif not prefix:
                await ctx.send("You didn't specify a prefix!")
                return
        elif doc:
            if not prefix and not doc.get('prfx'):
                await ctx.send("You didn't specify a prefix!")
                return
            elif not prefix and doc.get('prfx'):
                self.prfx.update_one(filter = {"_id": ctx.guild.id}, update={"$unset": {"prfx": ""}})
                await ctx.send("Prefix cleared")
                return
            else:
                self.prfx.update_one(filter = {"_id": ctx.guild.id}, update={"$set": {"prfx": prefix}})
                await ctx.send(f"Successfully set the server prefix to {prefix}")
                return


def setup(bot):
    bot.add_cog(config(bot))
