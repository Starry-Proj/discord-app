import discord as Discord
import dotenv as Env
import os as OS

from modules.functions import *
from discord.ext import commands as Commands

Env.load_dotenv()

class Admin(Commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.isDebug = OS.getenv("DEBUG") # 0 == False, 1 == True

    @Commands.cooldown(1, 5, Commands.BucketType.user) 
    @Commands.has_permissions(administrator=True)
    @Commands.command()
    async def sync(self, CTX: Commands.Context):
        await CTX.reply(embed=successEmbed(None,
                                           "Syncing Tree ‎ <:connect:1281034647480045719>",
                                           "To view the updated command tree, restarting Discord.",
                                           "This command is available to Administrator roles only.",
                                           fields=[
                                                ["Preview", "* On Windows, use **Ctrl + R** &\n* On MacOS use **Cmd + R** to reload Discord", False]
                                           ]), delete_after=3)
        
        await self.bot.tree.sync()

    @Commands.cooldown(1, 2, Commands.BucketType.user) 
    @Commands.has_permissions(manage_messages=True)
    @Commands.hybrid_command(name="purge",
                             description="[🔒] Deletes a specified number of messages")
    async def purge(self, CTX: Commands.Context, amount: int):
        plural = "s" if amount != 1 else ""
        
        try:
            await CTX.channel.purge(limit=amount + 1)

        except Exception:
            pass

        await CTX.send(embed=successEmbed(None,
                                          f"Message{plural} Purge ‎ <a:bonk:1289335115045928981>",
                                          f"Successfully deleted {formatNumber(amount)} messages.",
                                          "This command is available with Manage Messages perms only."), delete_after=3)

    @Commands.cooldown(1, 5, Commands.BucketType.user) 
    @Commands.has_permissions(administrator=True)
    @Commands.hybrid_command(name="default-roles",
                             description="[🔒] Assigns default roles to all members")
    async def default_roles(self, CTX: Commands.Context):
        # Idea:
        # - Have a list-variable that contains the IDs of all default roles
        # - Iterate through the list and assign each role to the member
        # - Send a success message to the channel

        currentIndex = 0
        totalIndex = CTX.guild.member_count
        embed = successEmbed(Discord.Color.gold(),
                             "Role Assignment ‎ <a:arnold:1259228840056717413>",
                             "Giving every user their default roles...",
                             "This command is available to Administrator roles only.",
                             fields=[
                                 ["Progress", f"{formatNumber(currentIndex)} of {formatNumber(totalIndex)} members", False],
                                 ["Percentage", f"{round((currentIndex / totalIndex) * 100)}%", False]
                             ])
        
        message = await CTX.send(embed=embed)
        ids = [1314031703324495902] if self.isDebug == "0" else [1314112853942472735]

        try:
            for id in ids:
                role = CTX.guild.get_role(id)

                for member in CTX.guild.members:
                    currentIndex += 1

                    if role not in member.roles:
                        try:
                            await member.add_roles(role)

                            embed.set_field_at(0,
                                               name="Progress",
                                               value=f"{formatNumber(currentIndex)} of {formatNumber(totalIndex)} members",
                                               inline=False)

                            embed.set_field_at(1,
                                               name="Percentage",
                                               value=f"{round((currentIndex / totalIndex) * 100)}%",
                                               inline=False)

                            await message.edit(embed=embed)
                        except:
                            pass

            await message.edit(embed=successEmbed(Discord.Color.green(),
                                                  "Role Assignment ‎ <a:arnold:1259228840056717413>",
                                                  "Successfully assigned default roles to all members.",
                                                  "This command is available to Administrator roles only.",
                                                  fields=[
                                                      ["Progress", f"{formatNumber(currentIndex)} of {formatNumber(totalIndex)} members", False],
                                                      ["Percentage", f"{round((currentIndex / totalIndex) * 100)}%", False]
                                                  ]))
            
        except Exception as errorCode:
            await message.edit(embed=errorEmbed(Discord.Color.red(),
                                                "Role Assignment",
                                                f"Error:\n```{errorCode}\n```",
                                                "This command is available to Administrator roles only."))

async def setup(bot):
    await bot.add_cog(Admin(bot))