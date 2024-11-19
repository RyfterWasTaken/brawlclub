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
        
        self.add_item(discord.ui.InputText(label="Enter pin", min_length=6, max_length=6))
    
    async def callback(self, interaction: discord.Interaction):
        pin = self.children[0].value
        response = await validate_login(self.email, pin) 
        # TODO: Remove hardcoded values
        # response =  {
        #     "ok": True,
        #     "tag": "#GCVV09UC2",
        #     "token": "eyJ0eXAiOiJKV1QiLCJraWQiOiJjNzVhN2Y4M2U5MzMiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI1MS05YTZhZGViNy1jYWQwLTQwZWUtYjk2MS05MzQ3YWFlZjBhMGUiLCJnYW1lIjoibGFzZXIiLCJpc3MiOiJpZC5zdXBlcmNlbGwuY29tIiwicGlkIjoiMTktNTEwNTc2MDciLCJodHRwczovL2lkLnN1cGVyY2VsbC5jb20vYXBwIjoibGFzZXIiLCJlbnYiOiJwcm9kIiwiaHR0cHM6Ly9pZC5zdXBlcmNlbGwuY29tL3R5cGUiOiJhY2NvdW50IiwiaHR0cHM6Ly9pZC5zdXBlcmNlbGwuY29tL2FwcEVudiI6InByb2QiLCJodHRwczovL2lkLnN1cGVyY2VsbC5jb20vYXBwQWNjb3VudElkIjoiMTktNTEwNTc2MDciLCJodHRwczovL2lkLnN1cGVyY2VsbC5jb20vaW5pdGlhbFJlZnJlc2hUb2tlbklzc3VlZEF0IjoxNzMxNTE5Mzg4LCJpYXQiOjE3MzE1MTkzODgsInNjaWQiOiI1MS05YTZhZGViNy1jYWQwLTQwZWUtYjk2MS05MzQ3YWFlZjBhMGUifQ.vzpTa_zgw9BSLZdrptuMuCBn27j4TAdG-5aZ2tLF4ST8oZbUBlmP-9Nxpp1KnJvczabwSMFFBRhpnp9PuiLxww"
        # }
        try:
            if response["ok"] == True:
                tag: str = response["tag"]
                tag = tag.replace("#", "%23")
                token = response["token"]
                response = await sc_request(f"players/{tag}")

                club_bot = ClubBot(token, interaction.channel_id)

                await club_bot.login(interaction.client, True)
                self.clubs.append(club_bot)
                
                await self.prev_interaction.edit_original_response(embed=discord.Embed(f"Successfully logged in to {response["name"]}. Activating club bot for {response["club"]["name"]}")) 
            else:
                await self.prev_interaction.edit_original_response(embed=discord.Embed(description=f"Wrong pin, try again")) 
        except Exception as e:
            print(e) 
            await self.prev_interaction.edit_original_response("An error occured, try again later")
        try:
            await interaction.response.send_message(content=".", delete_after=0.0)
        except:
            pass