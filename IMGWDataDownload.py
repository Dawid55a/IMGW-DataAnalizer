from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
from pathlib import Path
from zipfile import ZipFile

SITE_URL = r'https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/'
# showing possible dates
# print("You can choose from 01.2008 to 03.2020")

# connecting to site and mapping data
r = requests.get(SITE_URL)
html_doc = r.content
soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

# getting all years with data
years = []
for link in soup.find_all('a'):
    address = link.get('href')
    # print(address)
    if re.search("[0-9]/$", address) is not None:
        # print(address)
        years.append(address)
print(f"All years: {years}")

# years = ["2006/"]

# TODO: --------------------Try tu use RegEx Dawid------------------------

# raw_date = input("Give date range in format [mm-rrrr/mm-rrrr]: ")
# TODO: choosing from when we want to download data
# date_range = {'2008': ['01', '02']}

# home folder location
download_folder = f"{Path.home()}/Downloads/IMGWDataDownload"

try:
    Path.mkdir(Path(f'{download_folder}/Extracted'))
except FileExistsError:
    # TODO: Checking existing files in case they were downloaded already
    pass

# list holding  names of all downloaded files
downloaded_files = []

for year in years:
    # print(f"{SITE_URL}/{year}")
    r2 = requests.get(f"{SITE_URL}/{year}")
    year_site = BeautifulSoup(r2.content, 'html.parser')

    for link in year_site.find_all('a'):
        zip_file = link.get('href')
        if re.search("zip$", zip_file) is not None:
            file = requests.get(f"{SITE_URL}/{year}/{zip_file}", stream=True)

            with open(f'{download_folder}/{zip_file}', 'wb') as f:
                total_size = int(r.headers['content-length'])
                for data in tqdm(iterable=file.iter_content(chunk_size=1024), total=total_size / 1024, unit='KB'):
                    f.write(data)
            print(f"{zip_file}: Download complete!")
            downloaded_files.append(zip_file)

# extracting all downloaded files
for file in downloaded_files:
    with ZipFile(f'{download_folder}/{file}', 'r') as zip_ref:
        zip_ref.extractall(f'{download_folder}/Extracted')
print("Files extracted")
