import requests
from bs4 import BeautifulSoup
import json
import os
import time

from common import send_discord_notification

async def job(channel):
    for url in storefront_links:
        new_skus = check_for_new_skus(url)
        if new_skus:
            print(f"Found new SKUs for URL {url}: {', '.join(new_skus)}")
            await send_discord_notification(channel, new_skus)
        else:
            print(f"No new SKUs found for URL {url}")
            await channel.send(f"No new SKUs found for URL {url}")



# List of storefront URLs to track for newly added SKUs
storefront_links = []

# Number of search result pages to scrape through
search_pages = 3


# Retrieve the product SKUs from a storefront with multiple pages
def get_product_skus(url):
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
  }
  skus = set()
  page_number = 1
  while True:
    page_url = f"{url}&page={page_number}"
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = soup.find_all('a', class_='a-link-normal', href=True)
    page_skus = set()
    for link in product_links:
      product_url = link['href']
      if "/dp/" in product_url:
        sku = product_url.split('/')[-2]
        page_skus.add(sku)
    if not page_skus:
      break
    skus.update(page_skus)
    page_number += 1
    time.sleep(0.5)  # Sleep for 0.5 seconds to avoid rate limiting
  return skus


# Retrieve the product SKUs from a storefront
def get_storefront_skus(url):
  storefront_skus = set()
  for page_num in range(1, search_pages + 1):
    search_url = url + f"&page={page_num}"
    product_skus = get_product_skus(search_url)
    storefront_skus |= product_skus
  return storefront_skus


# Load the list of previously seen SKUs stored in a JSON file
def load_old_skus():
  if os.path.exists('old_skus.json'):
    with open('old_skus.json', 'r') as file:
      old_skus = json.load(file)
  else:
    old_skus = {}
  return old_skus
  

# Save a list of new SKUs as the list of previously seen SKUs for a particular storefront URL
def save_new_skus_as_old(url, new_skus):
  old_skus = load_old_skus()
  old_skus[url] = list(new_skus)
  with open('old_skus.json', 'w') as file:
    json.dump(old_skus, file)


# Check a storefront URL for newly added SKUs; return a list containing any found SKUs
def check_for_new_skus(url):
  new_skus = get_storefront_skus(url)
  old_skus_data = load_old_skus()
  old_skus = set(old_skus_data.get(url, []))

  new_added_skus = new_skus.difference(old_skus)

  # Save new_skus as old_skus for the next check
  save_new_skus_as_old(url, new_skus)

  return new_added_skus
