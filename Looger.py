import discord
from discord.ext import commands
from colorama import Fore, init
import os

init(autoreset=True)

print(Fore.GREEN + "--- EdGhost Message Logger (Gelişmiş) ---")
token = input("Token gir: ")

bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    print(Fore.BLUE + f"[✓] Giriş yapıldı: {bot.user}")
    print(Fore.YELLOW + "[!] İzleme aktif! Mesajları silinmesini bekle...")

@bot.event
async def on_message_delete(message):
    print(Fore.RED + f"\n[!] SİLİNEN MESAJ YAKALANDI!")
    print(Fore.WHITE + f"Kullanıcı: {message.author}")
    print(Fore.WHITE + f"Mesaj: {message.content}")

try:
    bot.run(token, bot=False)
except Exception as e:
    print(Fore.RED + f"Hata: {e}")
