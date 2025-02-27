import requests
from bs4 import BeautifulSoup
import re
class Events():
    def get_events(self):
        url = "https://www.time.ir/" 

        response = requests.get(url)

        events = {}
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            event_items = soup.find_all('li')

            for item in event_items:
                date = item.find('span')
                if date:
                    date_text = date.get_text(strip=True)
                    event_name = item.get_text(strip=True).replace(date_text, '').strip()

                    event_name = re.sub(r"\[.*?\]", "", event_name)
                    event_name = re.sub(r"[^\u0600-\u06FF\s]", "", event_name)
                    event_name = re.sub(r"\s+", " ", event_name).strip()
                    event_name = re.sub(r"[،]", "", event_name)

                    if date_text and event_name:
                        events[date_text] = event_name
        try: 
            return events
        except Exception as e:
            print(f"Error occurred: {e}")
            return None