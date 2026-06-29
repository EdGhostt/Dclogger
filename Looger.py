import requests
import json
import os
import sys
import threading
import time
from colorama import Fore, init

try:
    import websocket
except ImportError:
    print(Fore.RED + "[X] HATA: websocket-client kütüphanesi eksik! Kuruluyor...")
    os.system("pip install websocket-client")
    import websocket

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

clear_screen()
print(Fore.CYAN + "======================================================")
print(Fore.MAGENTA + " --- EdGhost DM & Grup API Message Logger (V6) ---")
print(Fore.CYAN + "======================================================")

token = input(Fore.YELLOW + "Hesap Tokenını Gir: ")

headers = {'Authorization': token, 'Content-Type': 'application/json'}
print(Fore.CYAN + "[*] Token doğrulanıyor...")
validate = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

if validate.status_code == 200:
    username = validate.json().get("username", "Bilinmeyen")
    user_id = validate.json().get("id", "0")
    print(Fore.GREEN + f"[✓] Erişim Başarılı! Aktif Hesap: {username}")
else:
    print(Fore.RED + "[X] Token geçersiz veya bağlantı reddedildi!")
    sys.exit()

print(Fore.CYAN + "======================================================")
print(Fore.YELLOW + "[*] Sadece DM ve Gruplar Dinleniyor (Sunucular Kapatıldı)...")
print(Fore.CYAN + "======================================================")

msg_cache = {}
heartbeat_interval = 40000

def send_heartbeat(ws):
    while True:
        time.sleep(heartbeat_interval / 1000.0)
        try:
            ws.send(json.dumps({"op": 1, "d": None}))
        except:
            break

def on_message(ws, message):
    global msg_cache, heartbeat_interval
    data = json.loads(message)
    
    op = data.get("op")
    t = data.get("t")
    d = data.get("d")
    
    if op == 10:  # HELLO Sinyali
        heartbeat_interval = d.get("heartbeat_interval", 40000)
        threading.Thread(target=send_heartbeat, args=(ws,), daemon=True).start()
        
        auth_data = {
            "op": 2,
            "d": {
                "token": token,
                "intents": 32767,
                "properties": {
                    "$os": "linux",
                    "$browser": "chrome",
                    "$device": "pc"
                }
            }
        }
        ws.send(json.dumps(auth_data))
        return

    # 1. Yeni Mesaj Geldiğinde Kontrol Et
    if t == "MESSAGE_CREATE":
        guild_id = d.get("guild_id")  # Eğer guild_id varsa bu bir sunucu mesajıdır!
        
        # Sadece sunucu ID'si olmayan mesajları (yani DM veya Grup) önbelleğe alıyoruz
        if guild_id is None:
            msg_id = d.get("id")
            content = d.get("content")
            author = d.get("author", {})
            author_name = author.get("username", "Bilinmeyen")
            author_id = author.get("id", "0")
            channel_id = d.get("channel_id")
            
            # Mesajın bir gruptan mı yoksa tekil DM'den mi geldiğini ayırt etmek için basit kontrol
            # Genelde d.get("type") değeri de fikir verir ama guild_id olmaması kesin çözümdür.
            if content:
                msg_cache[msg_id] = {
                    "content": content,
                    "author_name": author_name,
                    "author_id": author_id,
                    "channel_id": channel_id
                }
            
    # 2. Mesaj Silindiğinde Yakala
    elif t == "MESSAGE_DELETE":
        msg_id = d.get("id")
        guild_id = d.get("guild_id") # Silinme olayında da sunucu kontrolü yapıyoruz
        
        # Eğer silinen mesaj sunucuda değilse ve hafızamızda yer alıyorsa ekrana bas
        if guild_id is None and msg_id in msg_cache:
            cached = msg_cache[msg_id]
            print(Fore.RED + f"\n[SİLİNDİ] DM/Grup Kanal ID: {cached['channel_id']}")
            print(Fore.WHITE + f"Yazan Kişi : {cached['author_name']} ({cached['author_id']})")
            print(Fore.YELLOW + f"Silinen İçerik: {cached['content']}")
            print(Fore.CYAN + "------------------------------------------------------")
            del msg_cache[msg_id]

def on_error(ws, error):
    pass

def on_close(ws, close_status_code, close_msg):
    time.sleep(3)
    connect_gateway()

def connect_gateway():
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    ws_thread = threading.Thread(target=connect_gateway)
    ws_thread.daemon = True
    ws_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Logger kapatıldı.")
