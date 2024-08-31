import requests
from bs4 import BeautifulSoup
import urllib.parse
from getpass import getpass
import os
import time

def get_redirected_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.exceptions.RequestException:
        return None

def clean_url(url):
    parsed_url = urllib.parse.urlparse(url)
    clean_query = urllib.parse.parse_qs(parsed_url.query)
    for param in ['sa', 'usg']:
        clean_query.pop(param, None)
    clean_url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(clean_query, doseq=True)))
    return clean_url.split('?_rdc=1&_rdr')[0]

def get_google_search_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
    }
    try:
        response = requests.get(query, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('a')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results for query: {query}")
        print(f"Error details: {str(e)}")
        return []

def print_social_media_links(platform, links, nama_input):
    if links:
        print(f"Akun {platform} untuk nama '{nama_input}':")
        for link in links:
            print(link)
        print()
    else:
        print(f"Tidak ditemukan akun {platform} untuk nama '{nama_input}'.")
        print()

def search_social_media_accounts(nama_input, key):
    if key != '0737':
        print("Kunci tidak valid. Access denied.")
        print("Untuk mendapatkan kunci, silahkan memeriksanya kembali.")
        return

    platforms = {
        'Facebook': 'site:facebook.com',
        'Twitter': 'site:twitter.com',
        'Instagram': 'site:instagram.com',
        'LinkedIn': 'site:linkedin.com',
        'GitHub': 'site:github.com'
    }

    for platform, search_query in platforms.items():
        query = f'intext:"{nama_input}" {search_query}'
        url = f'https://www.google.com/search?q={urllib.parse.quote(query)}'
        search_results = get_google_search_results(url)
        social_media_links = set()

        for link in search_results:
            href = link.get('href')
            if href and href.startswith('/url?q='):
                url = clean_url(href[7:])
                if platform.lower() in url:
                    redirected_url = get_redirected_url(url)
                    if redirected_url:
                        social_media_links.add(redirected_url)

        print_social_media_links(platform, social_media_links, nama_input)
        time.sleep(2)  # Add a delay between searches to avoid rate limiting

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*40)
    print("    Tools OSINT Social Media")
    print("    -CREATE BY MRY07XPLOIT-")
    print("    MEDAN CYBER TEAM")
    print("="*40)

    while True:
        nama_input = input("Masukkan nama akun yang ingin dicari (atau 'q' untuk keluar): ").strip()
        if nama_input.lower() == 'q':
            break

        kunci = getpass("Masukkan key: ").strip()
        search_social_media_accounts(nama_input, kunci)

        lanjut = input("Apakah Anda ingin mencari lagi? (y/n): ").strip().lower()
        if lanjut != 'y':
            break

    print("Terima kasih telah menggunakan tool ini!")

if __name__ == "__main__":
    main()
