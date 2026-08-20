from colorama import Fore, Style, Back
import time

import urlSniper
import urlDos
import voiceDos

color = {
    "green": Fore.GREEN,
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "white": Fore.WHITE,
    "cyan": Fore.CYAN,
}

print(rf"""
{color['red']}
╭────────────────────────────────────╮
│  [ CREW ]  NETWORK LOAD ENGINE     │
│                                    │
│  ┌─ TARGET ─────────────────────┐  │
│  │  ● CONNECTED                 │  │
│  └──────────────────────────────┘  │
│                                    │
│  >>> INITIALIZING ASYNC ENGINE     │
│  >>> ESTABLISHING CONNECTION...    │
│  >>> READY                         │
╰────────────────────────────────────╯

{color['cyan']}                                         
[1] URL Sniper (discord.gg/)          
[2] URL Dos/DDoS Atak
[3] Voice Dos/DDoS Atak
                             
[0] Çıkış                                                

""")

secim = int(input(f'{color["green"]} discord-tools > '))
if secim == 1:
    urlSniper.giris()
elif secim == 2:
    urlDos.giris()
elif secim == 3:
    voiceDos.giris()
elif secim == 0:
    print(f'{color['white']} Görüşmeküzere..')
else:
    print(f"{color['red']} Geçerli bir seçenek belirt.")
