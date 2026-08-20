import asyncio
import aiohttp
from colorama import Fore, Style, Back

BEKLEME_SURESI = 0.1

color = {
    "green": Fore.GREEN,
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "white": Fore.WHITE,
    "cyan": Fore.CYAN,
}

def giris():
    VANITY = input('discord-tools > discord.gg/')
    async def main():
        print(f'{color['cyan']}URL Düştü mesajını gördükten sonra hemen url\'yi sunucuna ekle!')
    
        url = f"https://discord.com/api/v10/invites/{VANITY}"
    
        async with aiohttp.ClientSession() as session:
            gonderilenAtak = 0
            while True:
                try:
                    gonderilenAtak += 1
                    async with session.get(url) as response:
                        if response.status == 200:
                            print(f"{color['red']}Saldırı discord.gg/{VANITY} başlatıldı. ({response.status}) : {gonderilenAtak} Adet Gönderildi.")
                        elif response.status == 400:
                            print(f"{color['green']}URL Başarıyla düştü : {VANITY}")
                        elif response.status == 404:
                            print(f"{color['cyan']}URL Zaten aktif değil.")
                        else:
                            print(f"{color['red']}Bu URL discord tarafından yasaklanmış.")
    
                except aiohttp.ClientError as hata:
                    print(f"Ağ hatası: {hata}")
    
                await asyncio.sleep(BEKLEME_SURESI)
    
    
    if __name__ == "__main__":
        asyncio.run(main())

# Coded By Crew