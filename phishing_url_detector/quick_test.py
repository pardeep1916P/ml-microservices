#!/usr/bin/env python3
import requests
import json
import time
from urllib.parse import urlparse
import re

PHISHING_URLS = [
    "https://et.interac-amazon.com",
    "https://sellercentral.amazon.com-rs0.nl",
    "https://zhongyangjx.com/Amazon",
    "https://amazon.tecaock.shop",
    "https://amazon.com.lqi9vrvsacilykqnddyxwst1faf0.tecaock.shop",
    "https://sellercentral.amazon.com-plr.net",
    "https://amazon.com.zurzdtrfkx6bsdk3olklfxv1q6qwbe4g.petatonc.com",
    "https://fls-na.amazon.tecaock.shop",
    "https://runwayparking.com/?d=b-ankofamerica.com&pkAId=2143526812",
    "https://runwayparking.com/?d=vinance.care&pkAId=2143526812",
    "https://aws-binance.com",
    "https://runwayparking.com/?d=binance-korea.com&pkAId=2143526812",
    "https://runwayparking.com/?d=binance-store.com&pkAId=2143526812",
    "https://pay-interbank.webcindario.com",
    "https://cintesa.com",
    "https://runwayparking.com/?d=correios-rastreios.com&pkAId=2143526812",
    "http://holaserviciio11.cloudaccess.host/wp-content/uploads/2025/10/correoss/SS/corr/corr.php",
    "http://networkwebcr78.cloudaccess.host/wp-content/uploads/2025/10/correoss/SS/corr/corr.php",
    "https://runwayparking.com/?d=correios-rastreios.help&pkAId=2143526812",
    "https://paper.dropbox.devicesecurity.deviceverifcationsnapcht.app",
    "https://www.kkinstagram.com/reel/DQEwcpJDNJY/?igsh=MWZhZHhtN3Bnb2VteQ==",
    "https://kkinstagram.com/reel/DQWWpSwjDSZ/?igsh=YWY1aTJpeDNzbHEz",
    "http://instagram-reset-password-guigagondim.vercel.app",
    "http://instagram-clone-get-data.vercel.app",
    "http://instagrammalo.blogspot.mk",
    "https://instagram-friends.com/lander",
    "https://netflix-clone-tau-opal.vercel.app",
    "https://islington-cc.netflix-subscription-uae.com",
    "https://runwayparking.com/?d=betflix-amb1.com&pkAId=2143526812",
    "https://netflix-ui-clone-india.vercel.app",
    "http://netflix-free.vercel.app",
    "https://crm.netflix-france-abonnement.com",
    "https://linkedin-vip.com",
    "https://linkedin-scraper.com",
    "https://metamask-io.ghost.io/learn/",
    "https://b305869a-9bbf-4bb2-855c-3713eb150d45.metamask-io-online.com",
    "https://vpn.extension-wallet-metamask.com",
    "https://hostmaster.metamask-io-online.com",
    "https://6568c4df-aa32-4903-8e5e-3f3dfbec67fe.office365-cloud-portal.com",
    "https://runwayparking.com/?d=praypal.in&pkAId=2143526812",
    "https://paypals.pro",
    "https://int2o2.paypal-online.antimoney-laundering.org",
    "https://mobile.paypal.com-informationaccounts.com",
    "https://paypal-help.top",
    "http://opensee-app.carrd.co",
    "http://bulk-metadata-refresh-opensea.vercel.app",
    "https://uehoymftoy.myfunnelish.com/Spotify",
    "https://spotify-export.xyz",
    "http://spotify-02.vercel.app",
    "https://steamcaummunity.com/tradeoffer/new/?partner=123760205&token=hL5xYoI9r",
    "https://trustwallbt.com/index.html",
    "https://m.trustwallet.great-site.net",
    "https://trustwallzt.com/index.html",
    "https://runwayparking.com/?d=twitter-tools.com&pkAId=2143526812",
    "https://runwayparking.com/?d=to-witter.cafe&pkAId=2143526812",
    "https://static.staging.welolsfargo.com",
]

def extract_features(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path + parsed.query
        full_url = url.lower()
        
        features = []
        
        # 1. IP address detection
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        features.append(95 if re.search(ip_pattern, domain) else 5)
        
        # 2. @ symbol
        features.append(90 if '@' in full_url else 10)
        
        # 3. URL length (75 is threshold)
        url_length_score = min(100, max(0, (len(url) - 75) * 0.5))
        features.append(url_length_score)
        
        # 4. Dots in domain (excluding TLD)
        dot_count = domain.count('.') - 1
        features.append(min(100, dot_count * 15))
        
        # 5. Hyphens in domain
        hyphen_count = domain.count('-')
        features.append(min(100, hyphen_count * 20))
        
        # 6. HTTPS vs HTTP
        features.append(15 if parsed.scheme == 'https' else 85)
        
        # 7. Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.ru', '.xyz', '.top', '.shop', '.net', '.info', '.online', '.host']
        has_suspicious = any(domain.endswith(tld) for tld in suspicious_tlds)
        features.append(90 if has_suspicious else 20)
        
        # 8. Subdomain count
        subdomain_count = domain.count('.') - 1
        features.append(min(100, subdomain_count * 10))
        
        # 9. Special characters in path
        special_chars = len(re.findall(r'[^a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]', path))
        features.append(min(100, special_chars * 5))
        
        # 10. Numeric characters in domain
        numeric_in_domain = bool(re.search(r'\d', domain))
        features.append(70 if numeric_in_domain else 20)
        
        return features
    except Exception as e:
        return [50] * 10

def test_url(url):
    try:
        features = extract_features(url)
        response = requests.post("http://127.0.0.1:5000/predict", json={"features": features}, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction", -1)
            confidence = result.get("confidence", 0)
            is_phishing = prediction == 0
            
            return {
                "url": url,
                "phishing": is_phishing,
                "confidence": confidence,
                "features_avg": sum(features) / len(features)
            }
        else:
            return None
    except Exception as e:
        return None

phishing_count = 0
legitimate_count = 0
results = []

for i, url in enumerate(PHISHING_URLS, 1):
    result = test_url(url)
    if result:
        results.append(result)
        if result["phishing"]:
            phishing_count += 1
            status = "PHISHING"
        else:
            legitimate_count += 1
            status = "LEGIT"
        print(f"{i:3d}. {status:10s} ({result['confidence']:.2f}) | {url[:55]}")
        time.sleep(0.05)

print(f"\nTotal: {len(PHISHING_URLS)} | Phishing: {phishing_count} | Legitimate: {legitimate_count}")
print(f"Accuracy: {phishing_count/len(PHISHING_URLS)*100:.1f}%")

with open("phishing_test_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nResults saved to phishing_test_results.json")
