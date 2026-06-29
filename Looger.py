import requests
import json
import os
import sys
import threading
import time
from colorama import Fore, init

# Termux'ta websocket kütüphanesini import etmeye çalışıyoruz, yoksa hata basmasın diye
try:
    import websocket
except ImportError:
    print(Fore.RED + "[X] HATA: websocket-client kütüphanesi eksik! Lütfen kurulmasını bekleyin...")
    os.system("pip install websocket-client")
    import websocket

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

clear_screen()
print(Fore.CYAN + "======================================================")
print(Fore.MAGENTA + "    --- EdGhost Safe API Message Logger (V4) ---")
print(Fore.CYAN + "======================================================")

# Senin attığın Typer kodunun birebir aynı mermer token giriş yapısı
token = input(Fore.YELLOW + "Yan Hesabının Tokenını Gir: ")

headers = {'Authorization': token, 'Content-Type': 'application/json'}
print(Fore.CYAN + "[*] Token doğrulanıyor, lütfen bekleyin...")
validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

if validate.status_code == 200:
    username = validate.json().get("username", "Bilinmeyen")
    user_id = validate.json().get("id", "0")
    print(Fore.GREEN + f"[✓] Token geçerli! Aktif Hesap: {username}")
else:
    print(Fore.RED + "[X] Token geçersiz veya patlamış!")
    sys.exit()

print(Fore.CYAN + "======================================================")
print(Fore.YELLOW + "[*] Discord Canlı Hattına Bağlanılıyor...")
print(Fore.YELLOW + "[*] Durdurmak için Termux'ta CTRL + C yapabilirsin kanka.")
print(Fore.CYAN + "======================================================")

# Silinen mesajların eski içeriklerini hafızada tutmak için küçük bir sözlük (cache)
msg_cache = {}

def on_message(ws, message):
    global msg_cache
    data = json.loads(message)
    
    # Discord Gateway'den gelen olay türüne bakıyoruz
    t = data.get("t")
    d = data.get("d")
    
    # 1. Yeni Mesaj Geldiğinde Hafızaya Al (Silinirse içeriğini okuyabilmek için)
    if t == "MESSAGE_CREATE":
        if d.get("author", {}).get("id") != user_id and not d.get("author", {}).get("bot"):
            msg_id = d.get("id")
            content = d.get("content")
            author_name = d.get("author", {}).get("username")
            author_id = d.get("author", {}).get("id")
            channel_id = d.get("channel_id")
            
            if content:
                msg_cache[msg_id] = {
                    "content": content,
                    "author_name": author_name,
                    "author_id": author_id,
                    "channel_id": channel_id
                }
                
    # 2. Biri Mesaj Sildiğinde Saniyede Yakala ve Ekrana Bas!
    elif t == "MESSAGE_DELETE":
        msg_id = d.get("id")
        # Eğer silinen mesaj bizim hafızamızda varsa ekrana döker
        if msg_id in msg_cache:
            cached = msg_cache[msg_id]
            print(Fore.RED + f"\n[SİLİNDİ] Kanal ID: {cached['channel_id']}")
            print(Fore.WHITE + f"Yazan Kişi : {cached['author_name']} ({cached['author_id']})")
            print(Fore.YELLOW + f"Silinen Mesaj: {cached['content']}")
            print(Fore.CYAN + "------------------------------------------------------")
            del msg_cache[msg_id] # Hafızayı şişirmemek için temizle

def on_open(ws):
    # Discord hattına giriş (auth) sinyali gönderiyoruz
    auth_data = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "linux",
                "$browser": "chrome",
                "$device": "pc"
            }
        }
    }
    ws.send(json.dumps(auth_data))

def heartbeat(ws, interval):
    # Bağlantının kopmaması için arkada tıkır tıkır çalışan kalp atışı sinyali
    while True:
        time.sleep(interval / 1000)
        try:
            ws.send(json.dumps({"op": 1, "d": None}))
        except:
            break

def on_error(ws, error):
    pass

def on_close(ws, close_status_code, close_msg):
    pass

# Websocket akışını başlatma ayarı
ws = websocket.WebSocketApp(
    "wss://gateway.discord.gg/?v=9&encoding=json",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# Arka planda kalp atışını tetikle
def start_ws():
    ws.run_forever()

ws_thread = threading.Thread(target=start_ws)
ws_thread.daemon = True
ws_thread.start()

# Programın Termux'ta açık kalmasını sağlayan ana döngü
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(Fore.RED + "\n[-] Logger EdGhost tarafından kapatıldı.")
