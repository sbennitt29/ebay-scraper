# ebay-scraper

## Description

This project uses python to scrape Ebay to collect information about search listings, then saves the results in JSON files.

The program I used is ebay-dl.py, which accepts a search term using argparse, uses requests to retrieve HTML pages, and uses Beautiful Soup to extract listing information.

For each listing, the program collects the item's name, price (in cents), status, shipping cost (in cents), whether free returns are offered, and the number of items sold.

Missing information is represented by 'None' in Python and 'null' in JSON.

The program processes 10 pages of search results and saves the listings to a JSON file named after the search term.

## Practice Pages

Live eBay requests returned HTTP 403, so I used the artificial HTML practice pages provided.

All three JSON files that I generated (flower seeds.json, headphones.json, and laptop.json) were generated using the same practice data. Each contains 30 listings from the 10 practice pages. The search terms determine the output filenames.

## How to Run:

1. Install the required Python libraries:

```bash
python3 -m pip install requests beautifulsoup4
```

2. Download the provided practice-pages.zip file and extract it into the repository.

3. To generate the three JSON files, run these commands from the repository directory:

```bash
python3 ebay-dl.py --search "flower seeds" --pages-dir practice-pages
```

```bash
python3 ebay-dl.py --search "headphones" --pages-dir practice-pages
```

```bash
python3 ebay-dl.py --search "laptop" --pages-dir practice-pages
```

These commands generate flower seeds.json, headphones.json, and laptop.json.

## Assignment

[Project 2: Scraping eBay](https://csci40.rtealwitter.com/projects/02_webscraping/project.html)