import discord
from src.progression_roles import get_next_role, can_progress, VALID_ROLES

class ProgressionView(discord.ui.View):
    def __init__(self, member, current_role, next_role):
        super().__init__(timeout=86400)
        self.member = member
        self.current_role = current_role
        self.next_role = next_role

    @discord.ui.button(label="Yes, uppgradera mig", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button):
        await self.member.add_roles(discord.utils.get(interaction.guild.roles, name=self.next_role))
        await self.member.remove_roles(discord.utils.get(interaction.guild.roles, name=self.current_role))
        await interaction.response.send_message(
            f"Uppgraderad {self.member.mention} från {self.current_role} till {self.next_role}.",
            ephemeral=True
        )
        self.stop()

    @discord.ui.button(label="Not yet", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button):
        await interaction.response.send_message("Ok, du blir tillfrågad igen nästa år.", ephemeral=True)
        self.stop()

async def ask_for_progression(member):
    current_role = None
    for role in member.roles:
        if role.name in VALID_ROLES:
            current_role = role.name
            break

    if current_role is None:
        return

    next_role = get_next_role(current_role)
    if next_role is None:
        return

    await member.send(
        f"Hallo! Du är för närvarande {current_role}. "
        f"Har du slutfört det här året och vill du gå till {next_role}?"
    )

    view = ProgressionView(member, current_role, next_role)
    await member.send("Choose an option below:", view=view)