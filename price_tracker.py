import requests
from bs4 import BeautifulSoup

# List of websites to scrape
urls = {
    "Best Buy": "https://www.bestbuy.com/site/apple-homepod-2nd-generation-smart-speaker-with-siri-midnight/6519336.p?skuId=6519336&ref=212&loc=1&utm_source=feed&extStoreId=806",
    "Target": "https://www.target.com/p/apple-homepod-2023-2nd-generation-white/-/A-85979028?sid=2607S&afid=google&TCID=OGS&CPNG=Electronics&adgroup=57-10&gStoreCode=2607S&gQT=2&preselect=85979029",
    "B&H": "https://www.bhphotovideo.com/c/product/1746862-REG/apple_mqj83ll_a_homepod_2nd_generation.html?ap=y&smp=Y&srsltid=AfmBOoo1Uv63CwppZ7smYdlc1ixeNvyZleLRkDYhJIGNHkyd8gv0jiKiC7Y&gQT=2",
    "Staples": "https://www.staples.com/apple-homepod-2nd-generation-smart-speaker-midnight-mqj73ll-a/product_24555217",
    "Verizon": "https://www.verizon.com/products/apple-homepod/?sku=sku5820138",
    "Walmart": "https://www.walmart.com/ip/Apple-HomePod-2nd-Generation-Midnight/1740070616?wmlspartner=wlpa&selectedSellerId=0",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

selectors = {
    "Best Buy": "#large-customer-price",
    "Target": '[data-test="product-price"]',
    "B&H": '[data-selenium="pricingPrice"]',
    "Staples": ".price-info__final_price_sku span",
    "Verizon": 'div.customBlur.pt-6 p[aria-hidden="false"]',
    "Walmart": '[data-testid="variant-tile-price-text-Midnight"]',
... }
... 
... 
... def get_price(url, selector):
...     try:
...         page = requests.get(url, headers=headers, timeout=15)
...         soup = BeautifulSoup(page.content, 'html.parser')
...         element = soup.select_one(selector)
...         return element.text.strip() if element else "Price not found"
...     except Exception as e:
...         return f"Error: {e}"
... 
... import os
... import requests
... 
... def send_email(report):
...     return requests.post(
...         f"https://api.mailgun.net/v3/{os.environ['MAILGUN_DOMAIN']}/messages",
...         auth=("api", os.environ['MAILGUN_API_KEY']),
...         data={
...             "from": f"Mailgun Bot <postmaster@{os.environ['MAILGUN_DOMAIN']}>",
...             "to": [os.environ['TO_EMAIL']],
...             "subject": "Daily HomePod Price Tracker",
...             "text": report
...         })
... 
... 
... def compile_report():
...     results = []
...     for store, link in urls.items():
...         selector = selectors.get(store)
...         price = get_price(link, selector)
...         results.append(f"{store}: {price}")
...     return "\n".join(results)
... 
... if __name__ == "__main__":
...     report = compile_report()
...     print(report)
...     send_email(report)
