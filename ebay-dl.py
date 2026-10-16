import requests
from bs4 import BeautifulSoup
import argparse
from decimal import Decimal, InvalidOperation
import json
import re

def extract_listings(html):

    soup = BeautifulSoup(html, 'html.parser')

    items = soup.select('.s-item')
    results = []

    for item in items:
        name_tag = item.select_one('.s-item__title')
        if name_tag:
            name = name_tag.get_text(strip=True)
        else:
            name = None

        price_tag = item.select_one('.s-item__price')
        price = None
        if price_tag:
            price_text = price_tag.get_text(strip=True)
            first_price = price_text.split(' to ')[0]
            first_price = first_price.replace('$', '').replace(',', '')
            try:
                price = int(Decimal(first_price) * 100)
            except InvalidOperation:
                price = None
        
        status_tag = item.select_one('.SECONDARY_INFO')
        if status_tag:
            status = status_tag.get_text(strip=True)
        else:
            status = None
        
        shipping_tag = item.select_one('.s-item__shipping')

        if shipping_tag:
            shipping_text = shipping_tag.get_text(strip=True)
            if 'free' in shipping_text.lower():
                shipping = 0
            else:
                match = re.search(r'\$\s*([\d,]+(?:\.\d{1,2})?)', shipping_text)
                if match:
                    shipping_price = match.group(1).replace(',', '')
                    shipping = int(Decimal(shipping_price) * 100)
                else:
                    shipping = None
        else:
            shipping = None
        
        returns_tag = item.select_one('.s-item__free-returns')
        if returns_tag:
            returns_text = returns_tag.get_text(strip=True)
            if 'free returns' in returns_text.lower():
                free_returns = True
            else:
                free_returns = False
        else:
            free_returns = None
        
        sold_tag = item.select_one('.s-item__hotness')
        if sold_tag:
            sold_text = sold_tag.get_text(strip=True)
            items_sold = int(sold_text.split(' ')[0])
        else:
            items_sold = None

        listing = {
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': free_returns,
            'items_sold': items_sold
        }

        results.append(listing)

    return results

parser = argparse.ArgumentParser()
parser.add_argument('--search', required=True)
parser.add_argument('--pages-dir')
args = parser.parse_args()

search_term = args.search
print('Search term:', search_term)

all_results = []
for page in range(1, 11):
    if args.pages_dir:
        filename = args.pages_dir + '/page-' + str(page) + '.html'

        with open(filename, encoding='utf-8') as f:
            html = f.read()

    else:
        url = 'https://www.ebay.com/sch/i.html'

        params = {
            '_nkw': search_term,
            '_pgn': page
        }

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        print('Status code:', response.status_code)

        if response.status_code != 200:
            raise SystemExit('Could not download eBay listings.')

        html = response.text

        # Stop if the response does not contain actual listing cards.
        if not BeautifulSoup(html, 'html.parser').select('.s-item'):
            raise SystemExit('No listing cards found. Stop live requests.')

    page_results = extract_listings(html)

    all_results.extend(page_results)

    print('Page', page, ':', len(page_results), 'items')

filename = search_term + '.json'

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=4)

print('Saved', len(all_results), 'items to', filename)