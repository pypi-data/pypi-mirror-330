import cloudscraper
import requests
from bs4 import BeautifulSoup
import ssl
import json
import random
import time
from pprint import pprint
from collections import defaultdict

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

MONTH_DATABASE = ('January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December')
def valiDATE(date_text : str):
    for month in MONTH_DATABASE:
        if month.upper() in date_text.upper():
            return True
    return False
    

def fetch_weather_outlook(url, max_retries=5):

    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    scraper = cloudscraper.create_scraper()
    retries = 0

    while retries < max_retries:
        try:
            response = scraper.get(url, headers=headers)

            # print(response)

            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            outlook_section = soup.find('div', class_='weather-outlook-weekly')

            if not outlook_section:
                return {"error": "Weather outlook section not found"}

            issued_date = None
            validity_date = None
            date_div = outlook_section.find('div', class_='col-md-8 col-sm-7 col-xs-8 text-right')
            if date_div:
                date_texts = date_div.find_all('h5')
                for text in date_texts:
                    text_content = text.get_text(strip=True)
                    if text_content.startswith("Issued at"):
                        issued_date = text_content.replace("Issued at", "").strip()
                    elif text_content.startswith("Valid Until"):
                        validity_date = text_content.replace("Valid Until", "").strip()

            advisory_dict = defaultdict(lambda: { "title": "", "descriptions": [] })
            table = outlook_section.find('table')
            if table:
                rows = table.find_all('tr')
                data = table.find_all('p')
                # all_data = table.find_all('td')
                # stringed_data = [data.get_text(strip=True) for data in all_data]
                # print("========================All Data=======================")
                # pprint(stringed_data)
                # print("=======================================================")

                
                # for stringed in stringed_data:
                #     advisory_data = {}
                #     if valiDATE(stringed):
                #         advisory_data['date'] = stringed
                #     else:
                #         advisory_data['description'] = stringed
                #     advisories.append(advisory_data)
                
                # previous_date = None
                # for d in data:
                #     columns = data.find_all('td')
                #     if len(columns) >= 2:
                #         date_element = columns[0].get_text(strip=True)
                #         # print("Date Valid? ", valiDATE(date_element))
                        
                #         if not date_element:
                #             continue
                #         description_element = columns[1].find('p').get_text(strip=True)

                #         title = ""
                #         if not valiDATE(date_element):
                #             title = date_element
                #             # description_element = date_element + " " + description_element
                #             date_element = previous_date

                #         # advisory = {
                #         #     "title" : title,
                #         #     "date": date_element,
                #         #     "description": description_element
                #         # }

                #         if valiDATE(date_element):
                #             previous_date = date_element

                #         if title:
                #             advisory_dict[date_element]["title"] = title
                #         advisory_dict[date_element]["descriptions"].append(description_element)

                print(valiDATE('TODAY UNTIL MONDAY (14-17 FEBRUARY)'))
                title = ""
                for d in data:
                    if valiDATE(d.get_text(strip=True)):
                        title = d.get_text(strip=True)
                    else:
                        advisory_dict[title]["descriptions"].append(d.get_text(strip=True))
                    
                    print(title)
                        # advisory_dict[title]["title"] = d.get_text(strip=True)

            print("=====================================Advisory Dict=====================================")
            pprint(advisory_dict)
            print("=====================================================================================")

            advisories = [{"title": title, "description": " ".join(data["descriptions"])} for title, data in advisory_dict.items()]
            result = {
                "issued_date": issued_date,
                "validity_date": validity_date,
                "advisories": advisories
            }

            print("=====================================Advisories=====================================")
            pprint(result['advisories'])
            print("=====================================================================================")

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


if __name__ == '__main__':
    import os
    url = os.environ.get('SOURCE_URL_PAGASA')
    result = fetch_weather_outlook(url)
    pprint(result)
