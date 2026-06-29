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
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if res.status_code == 200:
            username = res.json().get("username", "Bilinmeyen")
            return True, username
    except:
        pass
    return False, None

clear_screen()
print(Fore.CYAN + "======================================================")
print(Fore.MAGENTA + "   --- EdGhost Gelişmiş Mesaj Logger (V2.5-Fix) ---")
print(Fore.CYAN + "======================================================")

while True:
    token = input(Fore.YELLOW + "Yan Hesabının Tokenını Gir: ")
    
    print(Fore.CYAN + "[*] Token doğrulanıyor, please wait...")
    is_valid, discord_username = check_token(token)
    
    if is_valid:
        print(Fore.GREEN + f"[✓] Giriş Başarılı! Aktif Hesap: {discord_username}")
        break
    else:
        print(Fore.RED + "[X] HATA: Girdiğin token yanlış veya patlamış! Tekrar dene.\n")

# Güncel discord.py sürümleri için gerekli izin ayarları (Intents)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # İçerikleri okuyabilmek için aktif olmalı

# Yeni sürümlerde self_bot=True yerine doğrudan commands.Bot kullanıyoruz
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    clear_screen()
    print(Fore.CYAN + "======================================================")
    print(Fore.GREEN + f"[✓] İzleme Başladı! Hesap: {bot.user.name}")
    print(Fore.CYAN + "======================================================")
    print(Fore.YELLOW + "[*] Silinen mesajlar anlık olarak taranıyor...")
    print(Fore.CYAN + "======================================================")

@bot.event
async def on_message_delete(message):
    # Mesaj nesnesi veya yazar boşsa ya da bot ise geç
    if not message or not message.author or message.author.bot:
        return
        
    if message.author.id == bot.user.id:
        return
        
    if not message.content:
        return

    print(Fore.RED + f"\n[SİLİNDİ] Yer: #{message.channel}")
    print(Fore.WHITE + f"Yazan Kişi : {message.author.name} ({message.author.id})")
    print(Fore.YELLOW + f"Silinen Mesaj: {message.content}")
    print(Fore.CYAN + "------------------------------------------------------")

try:
    # Güncel sürümde bot=False yerine doğrudan tokenı çalıştırıyoruz
    bot.run(token)
except Exception as e:
    print(Fore.RED + f"[X] Bağlantı sırasında bir hata oluştu: {e}")
        break
    else:
        print(Fore.RED + "[X] HATA: Girdiğin token yanlış, eksik veya patlamış! Lütfen tekrar dene.\n")

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
    if message.author.id == bot.user.id or message.author.bot:
        return
        
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
