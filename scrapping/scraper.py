import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .config import settings
from .storage import StorageInterface
from .notify import NotifierInterface
from .cache import CacheManager

class Scraper:
    BASE_URL = "https://dentalstall.com/shop/"

    def __init__(
        self,
        page_limit: int = None,
        proxy: str = None,
        retry_delay: int = None,
        storage: StorageInterface = None,
        notifier: NotifierInterface = None,
        cache: CacheManager = None
    ):
        self.page_limit = page_limit or settings.DEFAULT_PAGE_LIMIT
        self.proxy = proxy or settings.DEFAULT_PROXY
        self.retry_delay = retry_delay or settings.RETRY_DELAY
        self.storage = storage
        self.notifier = notifier
        self.cache = cache
        self.scraped_products = []

        # Setup proxies if a proxy string is provided.
        if self.proxy:
            self.proxies = {
                "http": self.proxy,
                "https": self.proxy
            }
        else:
            self.proxies = None

        # Ensure the directory for images exists.
        if not os.path.exists(settings.IMAGE_DIR):
            os.makedirs(settings.IMAGE_DIR)

    def scrape(self) -> int:
        total_updated = 0
        for page in range(1, self.page_limit + 1):
            print(f"Scraping page {page}...")
            page_url = urljoin(self.BASE_URL, f"page/{page}/")
            html = self.fetch_page(page_url)
            if html:
                products = self.parse_products(html)
                for product in products:
                    # Check cache: if product exists and price is unchanged, skip updating.
                    cached_product = self.cache.get(product['product_title'])
                    if cached_product and cached_product['product_price'] == product['product_price']:
                        print(f"Skipping '{product['product_title']}' as price unchanged.")
                        continue
                    else:
                        self.cache.set(product['product_title'], product)
                        self.scraped_products.append(product)
                        total_updated += 1
            else:
                print(f"Failed to retrieve page {page}.")
        # Save the scraped data.
        self.storage.save_data(self.scraped_products)
        # Notify the results.
        self.notifier.notify(
            f"Scraping complete. {len(self.scraped_products)} products scraped, {total_updated} updated."
        )
        return len(self.scraped_products)

    def fetch_page(self, url: str, retries: int = 3) -> str:
        attempt = 0
        while attempt < retries:
            try:
                response = requests.get(url, proxies=self.proxies, timeout=10)
                if response.status_code == 200:
                    return response.text
                elif response.status_code >= 500:
                    print(f"Server error ({response.status_code}) on {url}. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    attempt += 1
                else:
                    print(f"Failed to fetch {url} with status code {response.status_code}.")
                    return None
            except requests.RequestException as e:
                print(f"Request exception: {e}. Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                attempt += 1
        return None

    def parse_products(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        products = []
        # Assuming products are contained within <li class="product"> elements.
        product_elements = soup.find_all("li", class_="product")
        for element in product_elements:
            try:
                title_element = element.find("h2", class_="woo-loop-product__title")
                product_title = title_element.text.strip() if title_element else "No Title"
                
                price_element = element.find("span", class_="price")
                if price_element:
                    price_text = price_element.get_text(strip=True)
                    product_price = self.extract_price(price_text)
                else:
                    product_price = 0.0

                img_element = element.find("img")
                if img_element:
                    img_url = img_element.get("data-lazy-src")
                    local_image_path = self.download_image(img_url, product_title)
                else:
                    local_image_path = ""
                
                products.append({
                    "product_title": product_title,
                    "product_price": product_price,
                    "path_to_image": local_image_path
                })
            except Exception as e:
                print(f"Error parsing product: {e}")
        return products

    def extract_price(self, price_text: str) -> float:
        # Remove any currency symbols and formatting.
        import re
        price_numbers = re.findall(r"[\d\.,]+", price_text)
        if price_numbers:
            price_str = price_numbers[0].replace(',', '')
            try:
                return float(price_str)
            except ValueError:
                return 0.0
        return 0.0

    def download_image(self, img_url: str, product_title: str) -> str:
        try:
            response = requests.get(img_url, stream=True, proxies=self.proxies, timeout=10)
            if response.status_code == 200:
                # Sanitize the product title to create a valid filename.
                import re
                sanitized_title = re.sub(r'\W+', '_', product_title)
                file_extension = img_url.split('.')[-1].split('?')[0]  # Handle query parameters.
                filename = f"{sanitized_title}.{file_extension}"
                filepath = os.path.join(settings.IMAGE_DIR, filename)
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return filepath
            else:
                print(f"Failed to download image {img_url} with status {response.status_code}")
                return ""
        except Exception as e:
            print(f"Exception downloading image {img_url}: {e}")
            return ""
