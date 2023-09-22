


import os
import pandas as pd


def get_unique_columns_from_csvs(directory):
    unique_columns = set()

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(filepath)

            # Add the column names to the set
            unique_columns.update(df.columns)

    return list(unique_columns)


def write_to_excel(columns, output_filename):
    # Create a DataFrame from the unique column names
    df = pd.DataFrame(columns, columns=["Unique Columns"])

    # Write the DataFrame to an Excel file
    df.to_excel(output_filename, index=False, engine='openpyxl')


if __name__ == "__main__":
    directory = "processed"
    output_filename = "unique_columns.xlsx"

    # Get unique column names from all CSV files in the directory
    unique_columns = get_unique_columns_from_csvs(directory)

    # Write the unique column names to an Excel file
    write_to_excel(unique_columns, output_filename)
