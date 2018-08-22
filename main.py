import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_websites():
    for month in ["january", "febuary", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november",
                  "december"]:
        yield "http://holidayinsights.com/moreholidays/{0}.htm".format(month), month


def crawl_holidays():
    for site, month in get_websites():
        print("Processing: {0}".format(month.capitalize()))
        page = requests.get(site)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(page.content)

        posts: BeautifulSoup = soup.find_all("p", recursive=True)
        # print(posts)
        for post in posts:
            if str(list(post.contents)[0]).strip().isdigit():
                date_num = str(list(post.contents)[0]).strip()
                holiday_name = post.find('a').contents[0]
                yield {"date": date_num,
                       "month": month.capitalize(),
                       "holiday": holiday_name}


def holidays_to_pandas():
    df = pd.DataFrame(list(crawl_holidays()))
    df = df[['date', 'month', 'holiday']]
    df.to_csv("holidays.csv", index=False)


if __name__ == "__main__":
    holidays_to_pandas()
