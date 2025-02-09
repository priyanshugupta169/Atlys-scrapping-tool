from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from scrapping.config import settings
from scrapping.scraper import Scraper
from scrapping.storage import JSONStorage
from scrapping.notify import ConsoleNotifier
from scrapping.cache import CacheManager

app = FastAPI(title="Scraping Tool API")

security = HTTPBearer()

# The `ScrapeRequest` class defines a data model for a scraping request with optional parameters for
# page limit and proxy.
class ScrapeRequest(BaseModel):
    page_limit: int = None
    proxy: str = None

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    The function `verify_token` checks if the provided token matches a static token and returns it if
    valid.

    :return: The token value from the credentials is being returned.
    """
    if credentials.credentials != settings.STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials.credentials

@app.post("/scrape")
def scrape_endpoint(request_data: ScrapeRequest, token: str = Depends(verify_token)):
    """
    The function `scrape_endpoint` scrapes a specified endpoint using provided or default values and
    returns a message indicating the completion status along with the total number of products
    processed.
    """
    # Use provided values or fall back to defaults.
    page_limit = request_data.page_limit or settings.DEFAULT_PAGE_LIMIT
    proxy = request_data.proxy or settings.DEFAULT_PROXY

    # Instantiate dependencies.
    storage = JSONStorage()
    notifier = ConsoleNotifier()
    cache = CacheManager()

    scraper = Scraper(
        page_limit=page_limit,
        proxy=proxy,
        retry_delay=settings.RETRY_DELAY,
        storage=storage,
        notifier=notifier,
        cache=cache
    )
    total_products = scraper.scrape()
    return {"message": f"Scraping complete. {total_products} products processed."}
