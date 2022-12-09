


# deal with msa column values that are wider than 38 characters
# functionalize process
# run thru every file in raw folder


import pandas as pd

cols = ['msa', 'total', 'one_unit', 'two_unit', 'three_four_unit', 'five_plus', 'five_plus_structures']

# read data from txt file, skip first 4 lines, specify column widths.
# skip last 2 lines
df = pd.read_fwf('raw/permits200401.txt',
                 header=None, widths=[38,5,8,8,8,8,8],
                 skiprows=12,
                 names=cols)


# drop last 2 rows
df = df[:-2]

# fill 'msa' column nan values with '' (empty string)
df['msa'] = df['msa'].fillna('')

# if row i-1 of column 'total' is nan combine row i of 'msa' with row i-1 of 'msa'
# and drop row i of 'msa'
for i in range(1, len(df)):
    if pd.isna(df['total'][i-1]):
        df['msa'][i] = str(df['msa'][i-1]) + ' ' + str(df['msa'][i])
        #df = df.drop([i-1])

# drop rows where 'total' is nan
df = df.dropna(subset=['total'])

# remove commas from every row of 'msa' column
df['msa'] = df['msa'].str.replace(',', '')
df.to_csv('processed/permits200401.csv', index=False)
#362

# Print the first few rows of the DataFrame
print(df.head())