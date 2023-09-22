


import pandas as pd
import requests
from io import BytesIO


years = range(2020, 2022)
months = range(7, 9)

years = [2023]

for year in years:
    for month in months:
        if month < 10:
            month = '0' + str(month)

        url = "https://www.census.gov/construction/bps/xls/msamonthly_" + str(year) + str(month) + ".xls"

        # Fetching the content using requests
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request failed

        # Using BytesIO to convert the binary content to a file-like object so pandas can read it
        excel_file = BytesIO(response.content)

        # Reading the content into a pandas DataFrame
        df = pd.read_excel(excel_file, skiprows=7)

        # Displaying the first few rows
        print(df.head())

        output_file = 'processed/' + 'permits' + str(year) + str(month) + '.csv'

        df.to_csv(output_file, index=False)