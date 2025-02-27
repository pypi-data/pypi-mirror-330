from tzlocal import get_localzone
import pytz
import jdatetime
local_tz = get_localzone()
class Time():
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

        time_now = time_now.strftime("%H:%M:%S")
        date_now = time_now.strftime("%Y/%m/%d")
        time_h = time_now.strftime("%H")
        time_m = time_now.strftime("%M")
        time_s = time_now.strftime("%S")
        time_year = time_now.strftime("%Y")
        time_month = time_now.strftime("%m")
        time_day = time_now.strftime("%d")
        try: 
            return {
                "time_now": time_now,
                "time_h": time_h,
                "time_m": time_m,
                "time_s": time_s,
                "date_now": date_now,
                "time_year": time_year,
                "time_month": time_month,
                "time_day": time_day,
                "day_of_week": day_of_week,
                "zekr_today": zekr_today
            }

        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    def get_formatted_date(self, format_type="full"):
        time_now = jdatetime.datetime.now()
        formats = {
            "full": "%Y/%m/%d %H:%M:%S",
            "date_only": "%Y/%m/%d",
            "time_only": "%H:%M:%S",
            "short_date": "%y/%m/%d",
            "month_day": "%m/%d"
        }
        return time_now.strftime(formats.get(format_type, formats["full"]))
    def change_country(self,time, origin, dest):
        ...

