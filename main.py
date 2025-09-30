from fastapi import FastAPI
from src.scripts.scraper import ScraperBook
from src.api.routes import router

app = FastAPI()
app.include_router(router)

scraper = ScraperBook()
books = scraper.scrape_books()
if books:
    scraper.save_to_csv(books)
    scraper.save_on_db(books)