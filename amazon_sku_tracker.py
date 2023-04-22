import requests
from bs4 import BeautifulSoup
import json
import os

# Configuration
storefront_links = []

def get_product_skus(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_links = soup.find_all('a', class_='a-link-normal', href=True)
    
    skus = set()
    for link in product_links:
        product_url = link['href']
        sku = product_url.split('/')[-1]
        skus.add(sku)

    return skus

def load_old_skus():
    if os.path.exists('old_skus.json'):
        with open('old_skus.json', 'r') as file:
            old_skus = json.load(file)
    else:
        old_skus = {}
    return old_skus

def save_new_skus_as_old(url, new_skus):
    old_skus = load_old_skus()
    old_skus[url] = list(new_skus)
    with open('old_skus.json', 'w') as file:
        json.dump(old_skus, file)

def check_for_new_skus(url):
    new_skus = get_product_skus(url)
    old_skus_data = load_old_skus()
    old_skus = set(old_skus_data.get(url, []))

    new_added_skus = new_skus.difference(old_skus)

    # Save new_skus as old_skus for the next check
    save_new_skus_as_old(url, new_skus)

    return new_added_skus

async def send_discord_notification(channel, new_skus):
    message = 'The following SKUs have been added:\n' + '\n'.join(new_skus)
    await channel.send(message)

async def job(channel):
    for url in storefront_links:
        new_skus = check_for_new_skus(url)
        if new_skus:
            await send_discord_notification(channel, new_skus)
