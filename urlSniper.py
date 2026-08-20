import asyncio
import aiohttp
import time
import os

from colorama import Fore, Style, init

init(autoreset=True)

def giris():
    TOKEN = input('URL\'nin olacağı sunucudaki botun Token\'i: ')
    
    BEKLEME_SURESI = 5
    ISTEK_ZAMAN_ASIMI = 10
    MAKS_ESZAMANLI_ISTEK = 5
    
    istatistik = {
        "toplam": 0,
        "kullanimda": 0,
        "bulunamadi": 0,
        "rate_limit": 0,
        "hata": 0
    }
    
    sonuclar = {}
    
    
    def ekrani_temizle():
        os.system("cls" if os.name == "nt" else "clear")
    
    
    def banner():
        print(Fore.CYAN + 
    r"""
     ██████╗██████╗ ███████╗██╗    ██╗
    ██╔════╝██╔══██╗██╔════╝██║    ██║
    ██║     ██████╔╝█████╗  ██║ █╗ ██║
    ██║     ██╔══██╗██╔══╝  ██║███╗██║
    ╚██████╗██║  ██║███████╗╚███╔███╔╝
     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝
    
    GitHub: crewcik
    
    C R E W - T O O L S
    """ + Style.RESET_ALL)
    
    
    def durum_ekrani(vanity_listesi):
        ekrani_temizle()
        banner()
    
        print(
            Fore.CYAN +
            "CREW-TOOLS (DISCORD) URL DURUMU"
        )
    
        print()
    
        for vanity in vanity_listesi:
            veri = sonuclar.get(
                vanity,
                {
                    "durum": "Kontrol ediliyor",
                    "ms": 0
                }
            )
    
            durum = veri["durum"]
            ms = veri["ms"]
    
            if durum == "Kullanımda":
                renk = Fore.GREEN
    
            elif durum == "Kullanımda Değil":
                renk = Fore.YELLOW
    
            elif durum == "Rate Limit":
                renk = Fore.YELLOW
    
            elif durum in ("Hata", "Zaman aşımı", "Ağ hatası"):
                renk = Fore.RED
    
            else:
                renk = Fore.CYAN
    
            print(
                Fore.WHITE +
                f"discord.gg/{vanity} "
                + renk +
                f"{durum} "
                + Fore.WHITE +
                f"{ms:.0f} ms"
            )
    
        print(f"{Fore.WHITE}__"*50)
        print(
            Fore.WHITE +
            f"Toplam İstek : {istatistik['toplam']}"
        )
    
        print(
            Fore.GREEN +
            f"Kullanımda   : {istatistik['kullanimda']}"
        )
    
        print(
            Fore.YELLOW +
            f"Bulunamadı   : {istatistik['bulunamadi']}"
        )
    
        print(
            Fore.YELLOW +
            f"Rate Limit   : {istatistik['rate_limit']}"
        )
    
        print(
            Fore.RED +
            f"Hatalar      : {istatistik['hata']}"
        )
    
        print(f"{Fore.WHITE}__"*50)
    
        print(
            Fore.CYAN +
            f"Sonraki kontrol: {BEKLEME_SURESI} saniye sonra"
        )
    
    
    async def vanity_kontrol(
        session,
        semaphore,
        vanity
    ):
        url = (
            f"https://discord.com/api/v10/"
            f"invites/{vanity}"
        )
    
        basliklar = {
            "Authorization": f"Bot {TOKEN}",
            "User-Agent": "Crew-Tools/1.0"
        }
    
        async with semaphore:
        
            try:
                baslangic = time.perf_counter()
    
                async with session.get(
                    url,
                    headers=basliklar
                ) as cevap:
    
                    gecikme = (
                        time.perf_counter() -
                        baslangic
                    ) * 1000
    
                    istatistik["toplam"] += 1
    
                    if cevap.status == 200:
                    
                        istatistik["kullanimda"] += 1
    
                        sonuclar[vanity] = {
                            "durum": "Kullanımda",
                            "ms": gecikme
                        }
    
                    elif cevap.status == 404:
                    
                        istatistik["bulunamadi"] += 1
    
                        sonuclar[vanity] = {
                            "durum": "Bulunamadı",
                            "ms": gecikme
                        }
    
                    elif cevap.status == 429:
                    
                        istatistik["rate_limit"] += 1
    
                        sonuclar[vanity] = {
                            "durum": "Rate Limit",
                            "ms": gecikme
                        }
    
                        try:
                            veri = await cevap.json()
                        except Exception:
                            veri = {}
    
                        bekle = veri.get(
                            "retry_after",
                            BEKLEME_SURESI
                        )
    
                        await asyncio.sleep(
                            float(bekle)
                        )
    
                    else:
                    
                        istatistik["hata"] += 1
    
                        sonuclar[vanity] = {
                            "durum": f"HTTP {cevap.status}",
                            "ms": gecikme
                        }
    
            except asyncio.TimeoutError:
            
                istatistik["hata"] += 1
    
                sonuclar[vanity] = {
                    "durum": "Zaman aşımı",
                    "ms": 0
                }
    
            except aiohttp.ClientError:
            
                istatistik["hata"] += 1
    
                sonuclar[vanity] = {
                    "durum": "Ağ hatası",
                    "ms": 0
                }
    
    
    async def ana():
    
        ekrani_temizle()
        banner()
    
        giris = input(
            Fore.CYAN +
            "crew-tools > discord.gg/"
        ).strip()
    
        if not giris:
        
            print(
                Fore.RED +
                "\nVanity boş bırakılamaz."
            )
    
            return
    
        vanity_listesi = [
            vanity.strip()
            for vanity in giris.split(",")
            if vanity.strip()
        ]
    
        for vanity in vanity_listesi:
        
            sonuclar[vanity] = {
                "durum": "Başlatılıyor",
                "ms": 0
            }
    
        timeout = aiohttp.ClientTimeout(
            total=ISTEK_ZAMAN_ASIMI
        )
    
        semaphore = asyncio.Semaphore(
            MAKS_ESZAMANLI_ISTEK
        )
    
        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:
    
            while True:
            
                gorevler = [
                    vanity_kontrol(
                        session,
                        semaphore,
                        vanity
                    )
                    for vanity in vanity_listesi
                ]
    
                await asyncio.gather(
                    *gorevler
                )
    
                durum_ekrani(
                    vanity_listesi
                )
    
                await asyncio.sleep(
                    BEKLEME_SURESI
                )
    
    
    if __name__ == "__main__":
    
        try:
            asyncio.run(ana())
    
        except KeyboardInterrupt:
        
            print(
                Fore.CYAN +
                "\n\nCREW-TOOLS kapatılıyor..."
            )