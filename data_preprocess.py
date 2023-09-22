


# deal with msa column values that are wider than 38 characters
# functionalize process
# run thru every file in raw folder

filename='raw/permits200401.txt'


def process_file(filename, widths=[38,5,8,8,8,8,8]):
    import pandas as pd

    cols = ['msa', 'total', 'one_unit', 'two_unit', 'three_four_unit', 'five_plus', 'five_plus_structures']

    read_filename = 'raw/' + filename
    write_filename = 'processed/' + str.replace(filename, '.txt', '.csv')
    # read data from txt file, skip first 4 lines, specify column widths.
    # skip last 2 lines
    df = pd.read_fwf(read_filename,
                     header=None, widths=widths,
                     skiprows=12,
                     names=cols)


    # drop last 2 rows
    df = df[:-2]

    # fill 'msa' column nan values with '' (empty string)
    df['msa'] = df['msa'].fillna('')


    # if row i-1 of column 'total' is nan combine row i of 'msa' with row i-1 of 'msa'
    # and drop row i of 'msa'
    for i in range(1, len(df)):
        if pd.isna(df['five_plus_structures'][i-1]):
            df['msa'][i] = str(df['msa'][i-1]) + ' ' + str(df['msa'][i])
            #df = df.drop([i-1])

    # drop rows where 'total' is nan
    df = df.dropna(subset=['five_plus_structures'])

    # remove commas from every row of 'msa' column
    df['msa'] = df['msa'].str.replace(',', '')
    df.to_csv(write_filename, index=False)

    return "Sucessfully processed file: " + filename


def process_file_2(filename, header_skip = 10):
    import pandas as pd

    data = []

    read_filename = 'raw/' + filename
    write_filename = 'processed/' + str.replace(filename, '.txt', '.csv')

    # Reading and processing each line of the file
    with open(read_filename, "r") as file:
        # Skipping the header lines
        for _ in range(header_skip):
            file.readline()

        # Processing the data lines
        for line in file:
            if not line.strip():  # skip empty lines
                continue

            # Splitting the line into components based on fixed-width positions
            csa = line[:3].strip()
            cbsa = line[4:9].strip()
            name = line[10:49].strip()
            total = line[49:56].strip()
            unit_1 = line[56:64].strip()
            unit_2 = line[64:72].strip()
            unit_3_4 = line[72:80].strip()
            unit_5_or_more = line[80:89].strip()
            unit_5_or_more_2 = line[89:98].strip()
            percent = line[98:].strip()

            data.append([csa, cbsa, name, total, unit_1, unit_2, unit_3_4, unit_5_or_more, unit_5_or_more_2, percent])

    # Creating a DataFrame from the processed data
    df = pd.DataFrame(data,
                      columns=['CSA', 'CBSA', 'Name', 'Total', '1 Unit', '2 Units', '3 & 4 Units', '5 Units or more',
                               '5 Units or more (2)', 'Coverage Percent'])

    df.to_csv(write_filename, index=False)

    return "Sucessfully processed file: " + filename


def parse_permits_data(filename):

    import re
    import pandas as pd

    read_filename = 'raw/' + filename
    write_filename = 'processed/' + str.replace(filename, '.txt', '.csv')

    # Read the file content
    with open(read_filename, "r") as file:
        content = file.read()

    # Splitting the content by newline to get individual lines
    lines = content.split("\n")

    data = []
    # Regular expression pattern to capture the beginning of each line (CSA, CBSA, and Name)
    pattern_start = r"(\d{3}|\d{2}|\d{1}) (\d{5}) ([a-zA-Z\s\-\,]+)"

    for line in lines:
        match = re.match(pattern_start, line)
        if match:
            csa, cbsa, name = match.groups()

            # Extracting the rest of the columns
            remaining_data = line[match.end():].split()

            # Handling cases where there's a missing 'Coverage Percent' column
            while len(remaining_data) < 7:
                remaining_data.append(None)

            total, unit_1, unit_2, unit_3_4, unit_5_or_more, unit_5_or_more_2, percent = remaining_data[:7]

            data.append(
                [csa, cbsa, name.strip(), total, unit_1, unit_2, unit_3_4, unit_5_or_more, unit_5_or_more_2, percent])

    # Creating a DataFrame from the extracted data
    df = pd.DataFrame(data,
                      columns=['CSA', 'CBSA', 'Name', 'Total', '1 Unit', '2 Units', '3 & 4 Units', '5 Units or more',
                               '5 Units or more (2)', 'Coverage Percent'])

    df.to_csv(write_filename, index=False)

    return "Sucessfully processed file: " + filename


# loop thru every file in raw folder
import os
for filename in sorted(os.listdir('raw')):
    yyyymm = filename[7:13]
    yyyymm = int(yyyymm)

    if yyyymm < 200908:
        print(process_file(filename))
    else:
        print(parse_permits_data(filename))

