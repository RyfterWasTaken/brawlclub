import re
import discord
from club_bot import ClubBot
from sc_login import validate_login
from my_requests import sc_request
from loading import loading

class LoginButton(discord.ui.View):
    def __init__(self, email: str, clubs: list[ClubBot], channel_id: int, prev_interaction: discord.Interaction):
        super().__init__()
        self.email = email
        self.clubs = clubs
        self.channel_id = channel_id
        self.prev_interaction = prev_interaction

    @discord.ui.button(label="Enter pin", style=discord.ButtonStyle.grey)
    async def button_callback(self, _, interaction: discord.Interaction):
        await self.prev_interaction.edit_original_response(embed=loading())
        await interaction.response.send_modal(LoginModal(self.email, self.clubs, self.channel_id, self.prev_interaction))


class LoginModal(discord.ui.Modal):
    def __init__(self, email: str, clubs: list[ClubBot], channel_id: int, prev_interaction: discord.Interaction):
        super().__init__(title="Enter pin")
        self.email = email
        self.clubs = clubs
        self.channel_id = channel_id
        self.prev_interaction = prev_interaction
        
        self.add_item(discord.ui.InputText(label="Enter pin", min_length=6, max_length=7))
    
    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(content=".", delete_after=0.0, ephemeral=True)
            pin = "".join(re.findall(r"\d", self.children[0].value))
            print(f"{pin}: {type(pin)}")
            print(f"{self.children[0].value}: {type(self.children[0].value)}")
            type
            response = await validate_login(self.email, pin) 
            if response["ok"] == True:
                tag: str = response["tag"]
                tag = tag.replace("#", "%23")
                token = response["token"]
                
                # TODO: Remove
                print(token)

                response = await sc_request(f"players/{tag}")
                club_bot = ClubBot(token, interaction.channel_id)

                await club_bot.login(interaction.client, True)
                self.clubs.append(club_bot)
                
                await self.prev_interaction.edit_original_response(content="", embed=discord.Embed(description=f"Successfully logged in to {response["name"]}. Activating club bot for {response["club"]["name"]}")) 
            else:
                print(response)
                await self.prev_interaction.edit_original_response(content="", embed=discord.Embed(description=f"Wrong pin, try again")) 


        except Exception as e:
            print(e) 
            await self.prev_interaction.edit_original_response(content="An error occured, try again later")