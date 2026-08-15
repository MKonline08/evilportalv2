# Evil Portal Framework v2 — Universal Edition

Adaptive captive portal that detects and mimics real network providers. Built for authorized red team operations and WiFi security testing.

## Why "Universal"?

Instead of a generic "Guest WiFi" page that screams fake, this framework:
- **Auto-detects the target SSID** and switches branding (Starbucks, Xfinity, hotel, airport, etc.)
- **Uses real colors, logos, and language** from actual providers
- **Adapts form fields** (room number for hotels, email for ISPs)
- **Passes device captive portal checks** for iOS, Android, Windows, macOS

## Built-in Profiles

| Profile | Trigger SSID Keywords | Form Style |
|---------|----------------------|------------|
| `starbucks` | starbucks, sbux | Email + password |
| `xfinity` | xfinity, xfi | Xfinity login |
| `att` | attwifi, at&t | AT&T credentials |
| `spectrum` | spectrum, twc | Spectrum login |
| `hotel` | hotel, hilton, marriott | Room number + last name |
| `airport` | airport, fly, terminal | Email + password |
| `default` | (fallback) | Generic network login |

## Real-World Deployment Scenarios

### 1. Evil Twin (Most Effective)
```bash
# Use aircrack-ng or hostapd to clone a real network
# Example: clone "Starbucks WiFi"
./captive_portal.sh wlan0 192.168.1.1 starbucks
```


### 2. Open Hotspot with Stronger Signal
```bash
# Create "XfinityWiFi" in an area where Xfinity exists
./captive_portal.sh wlan0 192.168.1.1 xfinity
```


### 3. Hotel/Airport Social Engineering
```bash
# Deploy in hotel lobby or airport terminal
./captive_portal.sh wlan0 192.168.1.1 hotel
```

```bash
# Broadcast "xfinitywifi" or "ATT-WiFi" in apartment complex
./captive_portal.sh wlan0 192.168.1.1 xfinity
```






## Quick Start

```bash
# Install
pip install flask

# Run with specific profile
sudo python3 portal.py --profile starbucks

# Or full deployment with routing
sudo ./captive_portal.sh wlan0 192.168.1.1 starbucks
```

## Files

- `portal.py` — Flask engine with profile switching
- `templates/index.html` — Adaptive login page
- `templates/success.html` — Fake confirmation
- `static/style.css` — Responsive + dark mode
- `static/portal.js` — Fingerprinting + UX
- `captive_portal.sh` — Auto-setup for Pineapple/Linux

## Output

- `creds.json` — Harvested credentials with metadata
- `access.log` — Full access logs

## Legal

For authorized security testing only. Obtain written permission before deployment.
