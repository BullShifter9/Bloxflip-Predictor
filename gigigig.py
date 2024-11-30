import discord
from discord import app_commands
import random


class MinesBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

intents = discord.Intents.default()
intents.message_content = True
client = MinesBot(intents=intents)


# gimme credits😏😏
print("""
#####################################################
🚨 CREDITS 🚨
Special Thanks to BullShifter9 for Creating this Bot!

IF YOU WANT A DISCORD BOT THAT HAS LINK COMMANDS AND REAL METHODS/ALGORITHM DISCORD USER DM: bullshifter10
#########################################################
""")

used_round_ids = []

async def mines_checker(round_id):
    try:
        round_id = str(round_id)
        dash_parts = round_id.split("-")
        
        if sum(c.isalpha() for c in round_id) < 5:
            return False
        
        if dash_parts[0].isalpha() or dash_parts[-1].isalpha():
            return False
        
        validation_checks = [
            len(dash_parts) == 5,
            len(dash_parts[0]) == 8,
            len(dash_parts[1]) == 4,
            len(dash_parts[2]) == 4,
            len(dash_parts[3]) == 4,
            len(dash_parts[4]) == 12,
            dash_parts[2].startswith("4"),
            all(c in "0123456789abcdef" for part in dash_parts for c in part)
        ]
        
        return all(validation_checks)
    
    except Exception:
        return False

@client.tree.command(name='mines', description="mines command")
@discord.app_commands.checks.has_role("Member")
async def mines(
    interaction: discord.Interaction, 
    round_id: str, 
    num_spot: int
):
    if round_id in used_round_ids:
        embed = discord.Embed(
            title='Prediction Error', 
            description="This Round ID has already been used", 
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
        return

    if not await mines_checker(round_id):
        embed = discord.Embed(
            title='Invalid Round ID', 
            description="The provided Round ID is not valid", 
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
        return

    board = [0] * 25
    safe_spots = random.sample(range(25), num_spot)

    for spot in safe_spots:
        board[spot] = 1

    accuracy = random.randint(35, 60)
    board_symbols = ["🟢" if x == 1 else "💥" for x in board]
    board_str = "\n".join("".join(map(str, board_symbols[i:i + 5])) for i in range(0, len(board), 5))

    used_round_ids.append(round_id)

    em = discord.Embed(
        title=" Prediction", 
        description=f"Round ID: `{round_id}`",
        color=discord.Color.blue()
    )
    
    em.add_field(
        name="Grid Prediction", 
        value=f"```\n{board_str}\n```", 
        inline=False
    )
    
    em.add_field(
        name="Accuracy", 
        value=f"**{accuracy}%**", 
        inline=True
    )
    
    em.add_field(
        name="Number of Safe Tiles", 
        value=f"**{num_spot}**", 
        inline=True
    )

    await interaction.response.send_message(embed=em, ephemeral=False)

client.run('YOUR_DISCORD_BOT_TOKEN')
