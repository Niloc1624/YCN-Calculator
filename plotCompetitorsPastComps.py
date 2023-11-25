import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
from utils import get_most_recent_comp_year
from countCompetitorsPastComps import count_competitors_past_comps

# Get list of competitions from user
if __name__ == "__main__":
    plot = True
    show_work = True
    comp_code_list = ["mit", "big", "inf", "bds", "pbc", "idi", "idg", "upc", "occ", "usa"]
    csv_file_path = "numCompetitorsPastComps.csv"


# If a CSV doesn't exist, create it
def create_or_verify_csv(csv_file_path, index):
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([index])


# Load the CSV file into a DataFrame
def load_csv(csv_file_path):
    index = "Year"
    create_or_verify_csv(csv_file_path, index)
    df = pd.read_csv(csv_file_path, index_col=index)
    df.index.name = index
    return df


# Check the competitions in the CSV file against the competitions in the list
def update_df_with_comp_list(df, comp_code_list, show_work=True):
    comp_code_list = [x.lower() for x in comp_code_list]
    for comp_code in comp_code_list:
        # Set to 0 if the competition is not in the CSV file
        most_recent_year_csv = 0

        # If the competition is in the CSV file, check the last in the CSV file against the last year on the website
        if comp_code in df.columns.to_list():
            most_recent_year_csv = max(df[comp_code].dropna().keys())
            most_recent_year_website = get_most_recent_comp_year(comp_code)

            # If the years are the same, skip this competition
            if most_recent_year_csv == most_recent_year_website:
                continue

        df_to_add = count_competitors_past_comps(
            comp_code,
            show_work,
            earliest_year=most_recent_year_csv + 1,
            index=df.index.name,
        )
        df = df.combine_first(df_to_add)

    return df


# Write updated data back to CSV
def write_df_to_csv(df, csv_file_path, show_work=True):
    df = df.astype("Int64")  # Convert all values to Int64
    if show_work:
        print("\nData to be written to CSV:\n")
        print(df)
    df.to_csv(csv_file_path)


# Plot the data
def plot_data(df, comp_code_list):
    plt.figure(figsize=(10, 5))

    for comp_code in comp_code_list:
        # Drop NaN values from the column before plotting so there aren't breaks in the line
        non_na_df = df[comp_code].dropna()
        plt.plot(non_na_df.index, non_na_df, label=comp_code, marker="o")

    plt.title("Number of Competitors Over Years")
    plt.xlabel("Year")
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.ylabel("Number of Competitors")
    plt.ylim(bottom=0)

    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    df = load_csv(csv_file_path)
    df = update_df_with_comp_list(df, comp_code_list, show_work)
    write_df_to_csv(df, csv_file_path)
    if plot:
        plot_data(df, comp_code_list)
