

import cfscrape

import sys

scraper = cfscrape.create_scraper()

content = scraper.get("https://www.zacks.com/stock/research/NVDA/stock-style-scores").content

sys.stdout.buffer.write(content)