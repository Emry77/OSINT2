from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from getpass import getpass

def search_google(query):
    # Setup ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (without opening the browser)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open Google
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query + Keys.RETURN)

    # Wait for results to load
    time.sleep(2)

    # Collect all search result links
    links = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/a")

    results = []
    for link in links:
        href = link.get_attribute('href')
        results.append(href)

    driver.quit()
    return results

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
        social_media_links = search_google(query)

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
