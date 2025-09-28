from scripts.scraper import ScraperBook

scraper = ScraperBook()
books = scraper.scrape_books()
if books:
    scraper.save_to_csv(books)
    scraper.save_on_db(books)