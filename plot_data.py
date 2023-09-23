
import pandas as pd
import matplotlib.pyplot as plt

def read_and_filter_csv(filename, msa_filter):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Filter the DataFrame based on the MSA column
    df_filtered = df[df['MSA'] == msa_filter]

    return df_filtered

def plot_data(df, x_col, y_col):
    # Convert the 'date' column to a pandas datetime object for better plotting
    df[x_col] = pd.to_datetime(df[x_col])

    # Sort the DataFrame by the 'date' column
    df.sort_values(by=[x_col], inplace=True)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(df[x_col], df[y_col], marker='o')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} over Time in Orlando-Kissimmee-Sanford, FL")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    filename = "master.csv"
    msa_filter = "Orlando-Kissimmee-Sanford, FL"
    x_col = "date"
    y_col = "five_plus_units"

    # Read and filter the CSV file
    df_filtered = read_and_filter_csv(filename, msa_filter)

    # Plot the data
    plot_data(df_filtered, x_col, y_col)
