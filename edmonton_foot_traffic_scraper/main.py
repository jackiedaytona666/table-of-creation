"""
Main entry point for Edmonton Foot Traffic Scraper
"""
from scrapers.events_scraper import scrape_events
from scrapers.venues_scraper import scrape_venues
from scrapers.utils import setup_logging
import logging

def main():
    setup_logging()
    logging.info("Starting Edmonton Foot Traffic Scraper...")
    events = scrape_events()
    venues = scrape_venues()
    # TODO: Save data to /data or process as needed
    logging.info(f"Scraped {len(events)} events and {len(venues)} venues.")

if __name__ == "__main__":
    main()


# I fully agree we do need to begin somehow recording fluctuations and times and changes for sure for sure for sure because that would be nice to have like a historical to go back on