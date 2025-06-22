import whois
import socket
import requests
import webbrowser
import os
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import init, Fore, Style

init(autoreset=True)
GREEN = Style.BRIGHT + Fore.GREEN

BANNER = r"""

██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗     ███████╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║     ╚══███╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║█████╗ ███╔╝ 
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║╚════╝███╔╝  
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║     ███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝     ╚══════╝
          ▄︻┻═━一  HACK THE PLANET  一━═┻︻▄

🔍 RECON-Z | Created by 𝘡𝘦𝘴𝘩𝘢𝘯 𝘏𝘢𝘪𝘥𝘦𝘳 (TurboHacks110)
📺 YouTube: https://youtube.com/@turbohacks110
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_results(content, filename):
    choice = input(GREEN + "\n💾 Do you want to save the results? (y/n): ").lower()
    if choice == 'y':
        with open(filename, "a") as f:
            f.write("\n" + "="*60 + f"\n{datetime.now()}:\n")
            f.write(content + "\n" + "="*60 + "\n")
        print(GREEN + f"✅ Results saved to {filename}")

def wait_and_clear():
    input(GREEN + "\n➤ Press 0 to return to main menu...")
    clear_screen()
    print(GREEN + BANNER)

def whois_lookup():
    domain = input(GREEN + "\n🌐 Enter target website (e.g. example.com): ").strip()
    print(GREEN + "\n🔍 WHOIS Lookup Results")
    result = f"WHOIS Lookup for: {domain}\n"
    try:
        if not hasattr(whois, 'whois'):
            raise ImportError("python-whois package not installed correctly.")
        data = whois.whois(domain)
        result += f"📛 Domain       : {data.domain_name if not isinstance(data.domain_name, list) else data.domain_name[0]}\n"
        result += f"📅 Created      : {data.creation_date}\n"
        result += f"⌛ Expiry       : {data.expiration_date}\n"
        result += f"📨 Emails       : {data.emails}\n"
        result += f"🧬 Name Servers : {data.name_servers}\n"
        result += f"🔒 Status       : {data.status}\n"
        print(GREEN + result)
    except Exception as e:
        result = f"[!] Error during WHOIS lookup: {e}"
        print(GREEN + result)
    save_results(result, "whois_results.txt")
    wait_and_clear()

def social_media_finder():
    username = input(GREEN + "\n🕵️ Enter username (no @): ").strip()
    platforms = [
        "facebook.com", "instagram.com", "youtube.com/@", "x.com", "tiktok.com/@", "linkedin.com/in",
        "pinterest.com", "snapchat.com/add", "reddit.com/user", "tumblr.com", "github.com", "medium.com/@",
        "flickr.com/photos", "vimeo.com", "soundcloud.com", "twitch.tv", "discord.com/users", "quora.com/profile",
        "behance.net", "dribbble.com", "deviantart.com", "mix.com", "vk.com", "ok.ru", "weheartit.com",
        "badoo.com", "about.me", "imgur.com/user", "slideshare.net", "meetup.com", "patreon.com",
        "bitbucket.org", "bandcamp.com", "goodreads.com", "houzz.com", "ello.co", "reverbnation.com",
        "wattpad.com/user", "tripadvisor.com/Profile", "codepen.io", "producthunt.com/@", "kaggle.com",
        "500px.com", "angel.co/u", "unsplash.com/@", "stackexchange.com/users", "stackoverflow.com/users"
    ]
    result = f"OSINT for username: {username}\n"
    print(GREEN + "\n🔗 Social Media Profiles Found:")
    for site in platforms:
        url = f"https://{site}/{username}"
        print(GREEN + f"{site}: {url}")
        result += f"{site}: {url}\n"

    if input(GREEN + "\n🌍 Open all in browser? (y/n): ").lower() == 'y':
        for site in platforms:
            webbrowser.open(f"https://{site}/{username}")

    save_results(result, "osint_results.txt")
    wait_and_clear()

def ip_address_lookup():
    ip = input(GREEN + "\n📡 Enter target IP address: ").strip()
    print(GREEN + "\n🌍 IP Address Lookup")
    result = f"IP Lookup for: {ip}\n"

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        if res['status'] == 'success':
            lat = res.get('lat')
            lon = res.get('lon')
            gmap = f"https://www.google.com/maps?q={lat},{lon}"

            result += f"🔎 IP Address   : {ip}\n"
            try:
                host = socket.gethostbyaddr(ip)
                result += f"🌐 Hostname     : {host[0]}\n"
            except:
                result += "🌐 Hostname     : N/A\n"
            result += f"🗺️  Country     : {res['country']}\n"
            result += f"🏙️  City        : {res['city']}\n"
            result += f"🌐 Region       : {res['regionName']}\n"
            result += f"🕒 Time Zone    : {res['timezone']}\n"
            result += f"📡 ISP         : {res['isp']}\n"
            result += f"📍 Org         : {res['org']}\n"
            result += f"🗺️  Google Maps : {gmap}\n"
            print(GREEN + result)

            if input(GREEN + "\n🌍 Open Google Maps? (y/n): ").lower() == 'y':
                webbrowser.open(gmap)
        else:
            result += "❌ Could not retrieve info.\n"
            print(GREEN + result)
    except Exception as e:
        result = f"[!] IP lookup error: {e}"
        print(GREEN + result)

    save_results(result, "ip_results.txt")
    wait_and_clear()

def subdomain_finder():
    domain = input(GREEN + "\n🌐 Enter target domain (e.g. example.com): ").strip()
    print(GREEN + f"\n🔍 Scanning subdomains for: {domain}")
    wordlist = [
        "www", "mail", "ftp", "webmail", "smtp", "vpn", "test", "ns1", "ns2", "portal",
        "admin", "dev", "cdn", "api", "beta", "mobile", "app", "auth", "m", "store", "login",
        "intranet", "cms", "server", "office", "dashboard", "blog", "news", "media", "static"
    ]
    result = f"Subdomain scan results for: {domain}\n"
    found = []
    for sub in wordlist:
        url = f"http://{sub}.{domain}"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code < 400:
                print(GREEN + f"✅ Found: {sub}.{domain}")
                result += f"{sub}.{domain}\n"
                found.append(sub)
        except:
            print(GREEN + f"❌ {sub}.{domain} - Failed")
    if not found:
        result += "❌ No subdomains found or all are offline.\n"
    save_results(result, "subdomains_results.txt")
    wait_and_clear()

def phone_number_osint():
    phone = input(GREEN + "\n📱 Enter phone number with country code (e.g. +14155552671): ").strip()
    result = f"Phone Number OSINT: {phone}\n"
    try:
        parsed = phonenumbers.parse(phone)
        if not phonenumbers.is_possible_number(parsed):
            print(GREEN + "❌ Invalid number.")
            return
        result += f"✅ Valid        : {phonenumbers.is_valid_number(parsed)}\n"
        result += f"🌍 Region       : {geocoder.description_for_number(parsed, 'en')}\n"
        result += f"📞 Carrier      : {carrier.name_for_number(parsed, 'en')}\n"
        result += f"🕒 Time Zones   : {', '.join(timezone.time_zones_for_number(parsed))}\n"
        print(GREEN + result)
    except Exception as e:
        result = f"[!] Error: {e}"
        print(GREEN + result)

    save_results(result, "phone_results.txt")
    wait_and_clear()

def menu():
    clear_screen()
    print(GREEN + BANNER)
    while True:
        print(GREEN + "╔═════════════════════════════════════════════╗")
        print("║                MAIN MENU                   ║")
        print("╠═════════════════════════════════════════════╣")
        print("║ 1️⃣  WHOIS Record Lookup                    ║")
        print("║ 2️⃣  Social Media Username Finder           ║")
        print("║ 3️⃣  IP Address Lookup + Hostname + Map     ║")
        print("║ 4️⃣  Subdomain Finder                       ║")
        print("║ 5️⃣  Phone Number OSINT                     ║")
        print("║ 6️⃣  Exit                                    ║")
        print("╚═════════════════════════════════════════════╝")

        choice = input(GREEN + "➤ Select an option: ").strip()

        if choice == '1':
            whois_lookup()
        elif choice == '2':
            social_media_finder()
        elif choice == '3':
            ip_address_lookup()
        elif choice == '4':
            subdomain_finder()
        elif choice == '5':
            phone_number_osint()
        elif choice == '6':
            print(GREEN + "\n👋 Exiting RECON-Z. Fly high, Turbo Hacks 🦅")
            break
        else:
            print(GREEN + "❌ Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
