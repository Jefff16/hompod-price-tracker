import os
import requests
from bs4 import BeautifulSoup

# List of websites to scrape
urls = {
    "Best Buy": "https://www.bestbuy.com/site/apple-homepod-2nd-generation-smart-speaker-with-siri-midnight/6519336.p?skuId=6519336&ref=212&loc=1&utm_source=feed&extStoreId=806",
    "Target": "https://www.target.com/p/apple-homepod-2023-2nd-generation-white/-/A-85979028?sid=2607S&afid=google&TCID=OGS&CPNG=Electronics&adgroup=57-10&gStoreCode=2607S&gQT=2&preselect=85979029",
    "B&H": "https://www.bhphotovideo.com/c/product/1746862-REG/apple_mqj83ll_a_homepod_2nd_generation.html",
    "Staples": "https://www.staples.com/apple-homepod-2nd-generation-smart-speaker-midnight-mqj73ll-a/product_24555217",
    "Verizon": "https://www.verizon.com/products/apple-homepod/?sku=sku5820138",
    "Walmart": "https://www.walmart.com/ip/Apple-HomePod-2nd-Generation-Midnight/1740070616"
}

selectors = {
    "Best Buy": "#large-customer-price",
    "Target": '[data-test="product-price"]',
    "B&H": '[data-selenium="pricingPrice"]',
    "Staples": ".price-info__final_price_sku span",
    "Verizon": 'div.customBlur.pt-6 p[aria-hidden="false"]',
    "Walmart": 'span[itemprop="price"]'
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
]

def get_price(url, selector):
    try:
        # Use a session to maintain a connection
        session = requests.Session()
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        page = session.get(url, headers=headers, timeout=60)
        soup = BeautifulSoup(page.content, 'html.parser')
        element = soup.select_one(selector)
        if not element:
            # Log the full page content to investigate issues
            with open(f"{url.split('//')[1].split('/')[0]}_debug.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            return "Price not found"
        return element.text.strip()
    except Exception as e:
        return f"Error: {e}"


def compile_report():
    results = []
    for store, link in urls.items():
        selector = selectors.get(store)
        price = get_price(link, selector)
        results.append(f"{store}: {price}")
    return "\n".join(results)

def send_email(report):
    return requests.post(
        f"https://api.mailgun.net/v3/{os.environ['MAILGUN_DOMAIN']}/messages",
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={
            "from": f"Mailgun Bot <postmaster@{os.environ['MAILGUN_DOMAIN']}>",
            "to": [os.environ['TO_EMAIL']],
            "subject": "Daily HomePod Price Tracker",
            "text": report
        })

if __name__ == "__main__":
    report = compile_report()
    print(report)
    send_email(report)

