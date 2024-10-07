from newscatcher import Newscatcher
import json
import time
import os
from loguru import logger
from urllib.parse import urlparse

def save_articles_to_json(domain, articles, output_dir='output'):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the file name based on the domain
    file_name = f"{domain}.json"
    file_path = os.path.join(output_dir, file_name)

    # Write articles to a JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved articles to {file_path}")

def get_domain_from_url(url):
    # Parse the domain from URL excluding www and top-level domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '').split('.')[0]
    return domain

def main():
    # Load config
    sites_list_file_path = os.environ.get("SITES_LIST_FILE")
    
    if not sites_list_file_path or not os.path.exists(sites_list_file_path):
        logger.error("Site list file not found or not specified.")
        return

    with open(sites_list_file_path, encoding='utf-8') as sites_list_file:
        sites_list = json.load(sites_list_file)

    # Process each website
    for site in sites_list:
        site_url = site.get('URL')
        logger.info(f"Processing site: {site_url}")

        catcher_url = Newscatcher(website=site_url)
        results = catcher_url.get_news()
        
        if results and 'articles' in results:
            articles = results['articles']
            
            domain = get_domain_from_url(site_url)
            save_articles_to_json(domain, articles)

            count = 0
            for article in articles:
                count += 1
                ''' 
                print(
                    f"{count}. {article.get('title', 'No title')}\n"
                    f"\t\t{article.get('published', 'No publish date')}\n"
                    f"\t\t{article.get('link', 'No link')}\n\n"
                )
                '''
                time.sleep(0.33)
        else:
            logger.warning(f"No articles found for {site_url}")

if __name__ == "__main__":
    main()