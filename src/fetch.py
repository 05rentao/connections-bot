import json
import os
import requests
import time, random
import calendar

def get_prev_date(year, month, day):
    STOP_YEAR, STOP_MONTH, STOP_DAY = 2023, 6, 11

    current_year = year
    current_month = month
    current_day = day - 1

    while True:
        if current_day == 0:
            current_month -= 1
            if current_month == 0:
                current_year -= 1
                current_month = 12
            current_day = calendar.monthrange(current_year, current_month)[1]

        if current_year == STOP_YEAR and current_month == STOP_MONTH and current_day == STOP_DAY:
            break

        yield f'{current_year}-{current_month:02}-{current_day:02}'

        current_day -= 1

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/search?q=google+connections+answers&oq=google+connections+answers&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRhA0gEIMjkzOWowajeoAgiwAgE&sourceid=chrome&ie=UTF-8",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache"
    }
# "https://www.nytimes.com/svc/connections/v2/2023-06-12.json"
root_url = "https://www.nytimes.com/svc/connections/v2/"

for date in get_prev_date(2023, 11, 1):  # change starting date here
    time.sleep(random.uniform(2, 10))

    URL = f'{root_url}{date}.json'

    response = requests.get(URL, headers=header, timeout=10)
    response.raise_for_status()
    data = response.json()

    os.makedirs("data/raw", exist_ok=True)
    with open(f"data/raw/{date}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {date}")
