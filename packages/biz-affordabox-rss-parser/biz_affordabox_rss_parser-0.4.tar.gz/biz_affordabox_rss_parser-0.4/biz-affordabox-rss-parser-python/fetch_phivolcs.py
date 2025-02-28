import cloudscraper
import requests
from bs4 import BeautifulSoup
import ssl
import json
import random
import time

from pprint import pprint 

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# List of user agents to rotate
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
]

class CustomCloudScraper(cloudscraper.CloudScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mount('https://', self.get_custom_adapter())
    
    def get_custom_adapter(self):
        adapter = requests.adapters.HTTPAdapter()
        adapter.init_poolmanager(
            connections=adapter._pool_connections,
            maxsize=adapter._pool_maxsize,
            ssl_context=self.get_custom_ssl_context()
        )
        return adapter

    def get_custom_ssl_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

def fetch_volcano_bulletins(url, max_retries=5):

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    scraper = CustomCloudScraper()

    retries = 0

    while retries < max_retries:
        try:
            # Disable SSL certificate verification and hostname checking
            # scraper.verify = False
            # ssl._create_default_https_context = ssl._create_unverified_context

            response = scraper.get(url, headers=headers, verify=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            bulletins = soup.find_all('div', class_='mnwall-item')

            bulletin_list = []
            for bulletin in bulletins:
                h3_element = bulletin.find('h3', class_='mnwall-title')
                title_element = h3_element.find('a') if h3_element else None
                pub_date_element = bulletin.find('div', class_='mnwall-date')
                description_element = bulletin.find('div', class_='mnwall-desc')

                title = title_element.get_text(strip=True) if title_element else 'No title found'
                pub_date = pub_date_element.get_text(strip=True) if pub_date_element else 'No date found'
                description = description_element.get_text(strip=True) if description_element else 'No description found'

                bulletin_data = {
                    "title": title,
                    "publication_date": pub_date,
                    "description": description
                }
                bulletin_list.append(bulletin_data)


                print("====================================Bulletins====================================")
                pprint(bulletin_list)
                print("===================================================================================")

            result = {
                "bulletins": bulletin_list
            }

            return result

        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                retries += 1
                wait_time = random.uniform(1, 5)  # Varying interval between 1 and 5 seconds
                print(f"403 Forbidden error. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                return {"error": str(e)}

    return {"error": "Max retries exceeded"}
