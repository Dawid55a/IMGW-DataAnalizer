from bs4 import BeautifulSoup
import requests
import os
import re
from tqdm import tqdm
from pathlib import Path
SITE_URL = r'https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/'
# showing possible dates
print("You can choose from 01.2008 to 03.2020")

# connecting to site and mapping data
r = requests.get(SITE_URL)
html_doc = r.content
soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

# getting all years with data
years = []
for link in soup.find_all('a'):
    adress = link.get('href')
    # print(adress)
    if re.search("[0-9]/$", adress) is not None:
        # print(adress)
        years.append(adress)
print(f"All years: {years}")

# TODO: --------------------Try tu use RegEx Dawid------------------------

# raw_date = input("Give date range in format [mm-rrrr/mm-rrrr]: ")
# TODO: choosing from when we want to download data
date_range = {'2008': ['01', '02']}

for year in years:
    # print(f"{SITE_URL}/{year}")
    r2 = requests.get(f"{SITE_URL}/{year}")
    year_site = BeautifulSoup(r2.content, 'html.parser')

    for link in year_site.find_all('a'):
        adress2 = link.get('href')
        # print(adress2)
        if re.search("zip$", adress2) is not None:
            file = requests.get(f"{SITE_URL}/{year}/{adress2}", stream=True)
            # print(file.headers)

            path = f'{Path.home()}/Downloads'
            with open(f'{path}/{adress2}', 'wb') as f:
                total_size = int(r.headers['content-length'])
                for data in tqdm(iterable=file.iter_content(chunk_size=1024), total=total_size / 1024, unit='KB'):
                    f.write(data)
            print("Download complete!")

