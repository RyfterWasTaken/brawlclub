import discord
from club_bot import ClubBot
from sc_login import validate_login
from my_requests import sc_request

class LoginButton(discord.ui.View):
    def __init__(self, email, clubs, channel_id):
        super().__init__()
        self.email = email
        self.clubs = clubs
        self.channel_id = channel_id

    @discord.ui.button(label="Enter pin", style=discord.ButtonStyle.grey)
    async def button_callback(self, _, interaction: discord.Interaction):
        await interaction.response.send_modal(LoginModal(self.email, self.clubs, self.channel_id))

class LoginModal(discord.ui.Modal):
    def __init__(self, email: str, clubs: list, channel_id: int):
        super().__init__(title="Enter pin")
        self.email = email
        self.clubs = clubs
        self.channel_id = channel_id
        
        self.add_item(discord.ui.InputText(label="Enter pin", min_length=6, max_length=6))
    
    async def callback(self, interaction: discord.Interaction):
        pin = self.children[0].value
        response = await validate_login(self.email, pin)  
        if response["ok"] == True:
            tag: str = response["tag"]
            tag.replace("#", "%23")
            token = response["token"]

            club_bot = ClubBot(token, interaction.channel_id)
            club_bot.login()
            self.clubs.append(club_bot)

            response = await sc_request(f"players/{tag}")
            interaction.response.send_message(f"Successfully logged in to {response["name"]}. Activating club bot for {response["club"]["name"]}", ephemeral=True) 
        else:
            interaction.response.send_message("An error occured, try again later", ephemeral=True)