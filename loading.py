import discord

def loading():
    embed = discord.Embed(
        title="",
        description=f"<a:loading:1308525270105591860> Loading...",
        color=0x0099FF
    )
    embed.set_footer(text="This should update within 10s")
    return embed