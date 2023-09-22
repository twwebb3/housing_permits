


import requests as re
import bs4 as bs
import os
import time

os.chdir('raw')

# gather text from url
def get_text(url):
    r = re.get(url)
    soup = bs.BeautifulSoup(r.text, 'lxml')
    text = soup.get_text('p')
    return text


def text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)
    return str(filename) + ' written'


years = range(2004, 2022)
months = range(1, 13)

for year in years:
    for month in months:
        if month < 10:
            month = '0' + str(month)
        url = 'https://www.census.gov/construction/bps/txt/tb3u' + str(year) + str(month) + '.txt'

        text = get_text(url)
        status = text_to_file(text, 'permits' + str(year) + str(month) + '.txt')
        print(status)
        time.sleep(3)



https://www.census.gov/construction/bps/xls/msamonthly_201911.xls
