import requests
import discord
from discord.ext import commands
import os
from colorama import Fore, init

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# --- TOKEN KONTROL FONKSİYONU ---
def check_token(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        # Discord API'sine istek atarak tokenı kontrol ediyoruz
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if res.status_code == 200:
            username = res.json().get("username", "Bilinmeyen")
            return True, username
    except:
        pass
    return False, None

clear_screen()
print(Fore.CYAN + "======================================================")
print(Fore.MAGENTA + "   --- EdGhost Gelişmiş Mesaj Logger (V2-Checker) ---")
print(Fore.CYAN + "======================================================")

# Sonsuz döngüye alıyoruz ki doğru token girilene kadar sorsun
while True:
    token = input(Fore.YELLOW + "Yan Hesabının Tokenını Gir: ")
    
    print(Fore.CYAN + "[*] Token doğrulanıyor, lütfen bekleyin...")
    is_valid, discord_username = check_token(token)
    
    if is_valid:
        print(Fore.GREEN + f"[✓] Giriş Başarılı! Aktif Hesap: {discord_username}")
        break
    else:
        print(Fore.RED + "[X] HATA: Girdiğin token yanlış, eksik veya patlamış! Lütfen tekrar dene.\n")

# Self-bot modunu aktif ediyoruz
bot = commands.Bot(command_prefix=".", self_bot=True)

@bot.event
async def on_ready():
    clear_screen()
    print(Fore.CYAN + "======================================================")
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
    bot.run(token, bot=False)
except Exception as e:
    print(Fore.RED + f"[X] Bağlantı sırasında bir hata oluştu: {e}")
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
