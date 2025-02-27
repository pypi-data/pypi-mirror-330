import pytz
import jdatetime
import requests
from bs4 import BeautifulSoup
from tzlocal import get_localzone
import re

local_tz = get_localzone()  
import re

class Date_time():
    def get_time(self):
        time_zone = pytz.timezone(str(local_tz)) 
        time_now = jdatetime.datetime.now(time_zone)  

        zekr_rozane = {
            "Sat": "یا رَبَّ الْعالَمین",
            "Sun": "یا ذَالجَلالِ وَالإِکرام",
            "Mon": "یا قاضیَ الحاجات",
            "Tue": "یا اَرحَمَ الراحمین",
            "Wed": "یا حَیُّ یا قَیّوم",
            "Thu": "لا إِلَهَ إِلَّا اللهُ الْمَلِکُ الْحَقُّ الْمُبین",
            "Fri": "اللَّهُمَّ صَلِّ عَلَی مُحَمَّدٍ وَ آلِ مُحَمَّدٍ وَ عَجِّلْ فَرَجَهُمْ"
        }

        day_of_week = time_now.strftime("%a") 
        zekr_today = zekr_rozane.get(day_of_week, "not find!")

        time_now_str = time_now.strftime("%H:%M:%S")
        date_now_str = time_now.strftime("%Y/%m/%d")
        time_h = time_now.strftime("%H")
        time_m = time_now.strftime("%M")
        time_s = time_now.strftime("%S")
        time_year = time_now.strftime("%Y")
        time_month = time_now.strftime("%m")
        time_day = time_now.strftime("%d")
        try: 
            return {
                "time_now": time_now_str,
                "time_h": time_h,
                "time_m": time_m,
                "time_s": time_s,
                "date_now": date_now_str,
                "time_year": time_year,
                "time_month": time_month,
                "time_day": time_day,
                "day_of_week": day_of_week,
                "zekr_today": zekr_today
            }

        except Exception as e:
            print(f"Error occurred: {e}")
            return None
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

                    # حذف توضیحات اضافی مانند تاریخ میلادی یا سایر متون
                    event_name = re.sub(r"\[.*?\]", "", event_name)  # حذف توضیحات داخل []
                    event_name = re.sub(r"[^\u0600-\u06FF\s]", "", event_name)  # حذف کاراکترهای غیر فارسی
                    event_name = re.sub(r"\s+", " ", event_name).strip()  # حذف فضاهای اضافی
                    event_name = re.sub(r"[،]", "", event_name)  # حذف کاماهای اضافی

                    if date_text and event_name:
                        events[date_text] = event_name
        try: 
            return events
        except Exception as e:
            print(f"Error occurred: {e}")
            return None



