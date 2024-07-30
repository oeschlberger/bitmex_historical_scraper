# BITMEX Historical Data Scraper

Bitmex no longer offers historical trade data on their REST API. They do have the data in a public AWS bucket, which this scrapes and converts to CSV files (by year).


### Installation
1. Clone/download repository
2. Install requirements: pip install -r requirements.txt


### Usage
The script provides various options to scrape data over specified date ranges and for specific symbols.

* Scrape all available data (default symbol is `XBTUSD`):
  ```bash
  python scrape.py
  ```

* Scrape data from a specific start date through yesterday:
  ```bash
  python scrape.py --start YYYYMMDD
  ```

* Scrape data from a start date to an end date (inclusive):
  ```bash
  python scrape.py --start YYYYMMDD --end YYYYMMDD
  ```

* Scrape data up to a specific end date from the earliest available data:
  ```bash
  python scrape.py --end YYYYMMDD
  ```

* Scrape data for a specific trading pair (e.g., `ETHUSD`):
  ```bash
  python scrape.py --symbol ETHUSD
  ```

* Combining options, such as scraping `ETHUSD` data from a specific start date to an end date:
  ```bash
  python scrape.py --start YYYYMMDD --end YYYYMMDD --symbol ETHUSD
  ```

### Notes
- The default symbol for scraping is `XBTUSD`. You can change this using the `--symbol` parameter.
- Date formats should follow `YYYYMMDD`.
- Ensure you have sufficient storage for the downloaded and processed data.

### Contributing
Feel free to submit issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.

