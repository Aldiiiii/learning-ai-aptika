# Kompas Article Scraper

## Overview
This project is a web scraper designed to extract article titles, content, and publication dates from the Kompas website. It collects article links from multiple pages and scrapes the full text of each article.

## Features
- Scrapes article links from multiple pages.
- Extracts title, content, and publication date.
- Saves the scraped data to a CSV file.
- Handles errors and continues scraping.

## Requirements
Ensure you have Python installed along with the following dependencies:

```sh
pip install requests beautifulsoup4 pandas tqdm
```

## Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/kompas-scraper.git
   cd kompas-scraper
   ```
2. Run the scraper:
   ```sh
   python scraper.py
   ```
3. Scraped data will be saved in the `output/` directory as `kompas_articles.csv`.

## Configuration
You can modify the scraper settings in `scraper.py`:
- `base_url`: The URL pattern for the Kompas tag page.
- `article_selector`: CSS selector to find article links.
- `title_selector`: CSS selector for the article title.
- `content_selector`: CSS selector for the article content.
- `max_pages`: The number of pages to scrape.

## Output
- `article_links.csv`: Contains collected article URLs.
- `kompas_articles.csv`: Contains article title, content, date, and URL.

## License
This project is licensed under the MIT License.

## Author
[Your Name] - [Your GitHub Profile](https://github.com/yourusername)

