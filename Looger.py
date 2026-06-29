import discord
from discord.ext import commands
import os
from colorama import Fore, init

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

clear_screen()
print(Fore.CYAN + "======================================================")
print(Fore.MAGENTA + "       --- EdGhost Gelişmiş Mesaj Logger ---")
print(Fore.CYAN + "======================================================")

# Tokenı terminalden alıyoruz
token = input(Fore.YELLOW + "Yan Hesabının Tokenını Gir: ")

# Self-bot modunu aktif ediyoruz
bot = commands.Bot(command_prefix=".", self_bot=True)

@bot.event
async def on_ready():
    clear_screen()
    print(Fore.GREEN + f"[✓] İzleme Başladı! Hesap: {bot.user.name}")
    print(Fore.CYAN + "======================================================")
    print(Fore.YELLOW + "[*] Bulunduğun tüm sunucu ve gruplardaki silinen mesajlar taranıyor...")
    print(Fore.CYAN + "======================================================")

@bot.event
async def on_message_delete(message):
    # Kendi sildiğin mesajları veya bot mesajlarını loglamasın diye filtre
    if message.author.id == bot.user.id or message.author.bot:
        return
        
    # Eğer mesajın içi boşsa (sadece fotoğraf veya embed ise) geç
    if not message.content:
        return

    print(Fore.RED + f"\n[SİLİNDİ] Yer: #{message.channel}")
    print(Fore.WHITE + f"Yazan Kişi : {message.author.name} ({message.author.id})")
    print(Fore.YELLOW + f"Silinen Mesaj: {message.content}")
    print(Fore.CYAN + "------------------------------------------------------")

try:
    bot.run(token, bot=False) # Kullanıcı hesabı olduğunu belirtiyoruz
except discord.LoginFailure:
    print(Fore.RED + "[X] HATA: Girdiğin token yanlış veya patlamış!")
except Exception as e:
    print(Fore.RED + f"[X] Bir hata oluştu: {e}")
