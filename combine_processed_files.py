
import os
import pandas as pd

def read_column_mapping(excel_file):
    df = pd.read_excel(excel_file)
    column_mapping = {}
    for _, row in df.iterrows():
        for col in ["name_1", "name_2", "name_3", "name_4"]:
            column_mapping[row[col]] = row["fin_name"]
    return column_mapping

def process_and_combine_csvs(directory, column_mapping):
    combined_df = pd.DataFrame()

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            # Extract year and month from filename and add them as new columns
            year = filename[7:11]
            month = filename[11:13]
            df['year'] = year
            df['month'] = month
            df['date'] = f"{year}-{month}-01"

            # Rename columns based on mapping
            df.rename(columns=column_mapping, inplace=True)

            # Check for duplicate columns
            if df.columns.duplicated().any():
                duplicate_columns = df.columns[df.columns.duplicated()].tolist()
                original_columns = [k for k, v in column_mapping.items() if v in duplicate_columns]
                print \
                    (f"Warning: Duplicate columns found in {filename}. Original: {original_columns}, Duplicate: {duplicate_columns}. Skipping this file.")
                continue

            # Strip white space from the "MSA" column if it exists
            if "MSA" in df.columns:
                df["MSA"] = df["MSA"].str.strip()

            # Combine into the final DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

if __name__ == "__main__":
    excel_file = "column_compare.xlsx"
    directory = "processed"
    output_filename = "master.csv"

    column_mapping = read_column_mapping(excel_file)
    combined_df = process_and_combine_csvs(directory, column_mapping)

    if not combined_df.empty:
        combined_df.to_csv(output_filename, index=False)
    else:
        print("No data to write.")
