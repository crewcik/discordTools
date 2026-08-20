import discord

def giris():
    TOKEN = input('Bot Token: ')
    GUILD_ID = int(input('Guild ID: '))
    VOICE_CHANNEL_ID = int(input('Voice ID: '))
    
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"Giriş yapıldı: {client.user}")
    
        guild = client.get_guild(GUILD_ID)
    
        if guild is None:
            print("Sunucu bulunamadı.")
            await client.close()
            return
    
        channel = guild.get_channel(VOICE_CHANNEL_ID)
    
        if not isinstance(channel, discord.VoiceChannel):
            print("Ses kanalı bulunamadı.")
            await client.close()
            return
    
        while True:
            voice = await channel.connect()
            print(f"Voice bağlantısı kuruldu: {channel.name}")
            await voice.disconnect()
    
    
    client.run(TOKEN)


# Coded By Crew