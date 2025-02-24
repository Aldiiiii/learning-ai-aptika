import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

class KompasScraper:
    def __init__(self, base_url, article_selector, title_selector, content_selector, max_pages=100):
        self.base_url = base_url
        self.article_selector = article_selector
        self.title_selector = title_selector
        self.content_selector = content_selector
        self.max_pages = max_pages
        self.headers = {"User-Agent": "Mozilla/5.0"}
        
    def extract_date_from_url(self, url):
        match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        return "No Date"
    
    def scrape_links(self):
        """Scrape article links from multiple pages"""
        all_links = set()
        print("Starting to scrape links...")
        
        for page_number in tqdm(range(1, self.max_pages + 1), desc="Scraping pages"):
            url = self.base_url.format(page_number=page_number)
            
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                containers = soup.select(self.article_selector)
                
                for container in containers:
                    links = container.find_all("a", href=True)
                    for link in links:
                        all_links.add(link["href"])
                        
            except Exception as e:
                print(f"Error on page {page_number}: {e}")
                continue
                
        return list(all_links)
    
    def scrape_article(self, url):
        """Scrape individual article content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract title
            title = soup.select_one(self.title_selector)
            title = title.text.strip() if title else "No Title"
            
            # Extract content
            content_div = soup.select_one(self.content_selector)
            content = " ".join(p.text.strip() for p in content_div.find_all("p")) if content_div else "No content found"
            
            # Get date from URL
            date = self.extract_date_from_url(url)
            
            return {
                "Title": title,
                "Content": content,
                "Date": date,
                "URL": url
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {
                "Title": "Error",
                "Content": str(e),
                "Date": self.extract_date_from_url(url),
                "URL": url
            }
    
    def scrape_all_articles(self, links):
        """Scrape content from all collected links"""
        articles = []
        for link in tqdm(links, desc="Scraping articles"):
            article_data = self.scrape_article(link)
            articles.append(article_data)
        return articles
    
    def save_results(self, data, filename, output_folder="output"):
        """Save results to CSV file"""
        os.makedirs(output_folder, exist_ok=True)
        filepath = os.path.join(output_folder, filename)
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"Results saved to {filepath}")
        return filepath

def main():
    # Initialize scraper with dynamic selectors
    base_url = "https://www.kompas.com/tag/bogor?page={page_number}"
    article_selector = "div.article__list__title > h3"
    title_selector = "h1.read__title"
    content_selector = "div.read__content"
    
    scraper = KompasScraper(base_url, article_selector, title_selector, content_selector, max_pages=1)
    
    # Scrape links
    print("Phase 1: Collecting article links...")
    links = scraper.scrape_links()
    
    # Optional: Save links to CSV
    scraper.save_results({"link": links}, "article_links.csv")
    
    # Scrape articles
    print("\nPhase 2: Scraping article contents...")
    articles = scraper.scrape_all_articles(links)
    
    # Save final results
    scraper.save_results(articles, "kompas_articles.csv")
    print("\nScraping completed successfully!")

if __name__ == "__main__":
    main()
