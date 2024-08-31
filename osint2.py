import requests
from bs4 import BeautifulSoup
import urllib.parse
from getpass import getpass
import os

def get_redirected_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        return response.url
    except requests.exceptions.RequestException:
        return "loading"

def clean_url(url):
    url = urllib.parse.unquote(url)
    url = url.split('&sa=U&')[0]
    url = url.split('&usg=')[0]
    url = url.split('?_rdc=1&_rdr')[0]
    return url

def get_google_search_results(query):
    try:
        response = requests.get(query, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('a')
    except requests.exceptions.RequestException:
        return []

def extract_urls(links):
    urls = []
    for link in links:
        href = link.get('href')
        if href and href.startswith('/url?q='):
            url = href[7:]
            url = clean_url(url)
            if 'google.com' not in url:
                urls.append(url)
    return urls

def print_social_media_links(platform, links, nama_input):
    print(f"Akun {platform} untuk nama '{nama_input}':")
    for link in links:
        print(link)
    print()

def search_social_media_accounts(nama_input, key):
    if key != '0737':
        print("Kunci tidak valid. Access denied.")
        return

    platforms = {
        'Facebook': 'site:facebook.com',
        'Twitter': 'site:twitter.com',
        'Instagram': 'site:instagram.com'
    }

    for platform, search_query in platforms.items():
        query = f'intext:"{nama_input}" {search_query}'
        url = f'https://www.google.com/search?q={urllib.parse.quote(query)}'
        search_results = get_google_search_results(url)
        social_media_links = extract_urls(search_results)

        if social_media_links:
            print_social_media_links(platform, social_media_links, nama_input)
        else:
            print(f"Tidak ditemukan akun {platform} untuk '{nama_input}'.")

def main():
    os.system("clear")
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    print("    Tools Osint SOCIAL Media")
    print("        -CREATE BY MRY07XPLOIT -")
    print("    MEDAN CYBER TEAM  ")
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")

    nama_input = input("Masukkan nama akun yang ingin dicari: ").strip()
    kunci = getpass("Masukkan key: ").strip()
    search_social_media_accounts(nama_input, kunci)

if __name__ == "__main__":
    main()
