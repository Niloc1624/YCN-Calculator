import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import os
from utils import get_most_recent_comp_year
from countCompetitorsPastComps import count_competitors_past_comps


if __name__ == "__main__":
    # EDIT THESE VARIABLES
    plot = True
    show_work = True
    verify_entries = False
    comp_code_list = [
        "idi",
        "bds",
        "idg",
        "ndc",
        "mit",
        "inf",
        "big",
        "pbc",
        "tub",
        "upc",
        "vub",
        "occ",
        "usa"
    ]

    if verify_entries:
        csv_file_path = "numCompetitorsPastCompsVerified.csv"
    else:
        csv_file_path = "numCompetitorsPastComps.csv"


# If a CSV doesn't exist, create it
def create_or_verify_csv(csv_file_path, index):
    """
    Create or verify the existence of a CSV file at the given file path.

    Args:
        csv_file_path (str): The path to the CSV file.
        index (str): The value to be used as the first cell in the CSV file and the index to be used if imported as a Pandas DataFrame.
    """
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([index])


# Load the CSV file into a DataFrame
def load_csv(csv_file_path):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    csv_file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: The loaded DataFrame.
    """
    index = "Year"
    create_or_verify_csv(csv_file_path, index)
    df = pd.read_csv(csv_file_path, index_col=index)
    df.index.name = index
    return df


# Check the competitions in the CSV file against the competitions in the list
def update_df_with_comp_list(df, comp_code_list, verify_entries=False, show_work=True):
    """
    Updates the given DataFrame with competitor information for each competition code in the comp_code_list.
    Checks CSV file first and only updates if the competition is not already in the CSV file or if the last year
    in the CSV file is not the most recent year on the website.

    Args:
        df (pandas.DataFrame): The DataFrame to be updated.
        comp_code_list (list): A list of competition codes to check.
        verify_entries (bool, optional): WARNING: TAKES A LONG TIME. Whether to only count the number of
                                         competitors with at least one event. Defaults to False.
        show_work (bool, optional): Whether to show the work. Defaults to True.

    Returns:
        pandas.DataFrame: The updated DataFrame.
    """
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
                if show_work:
                    print(
                        f"{comp_code} {most_recent_year_csv} is most recent in CSV and on website, continuing to next comp_code"
                    )
                continue

            if show_work:
                print(
                    f"{comp_code} is missing {most_recent_year_csv+1} - {most_recent_year_website}, fetching and adding to CSV"
                )
        elif show_work:
            print(f"{comp_code} is not in CSV, fetching and adding to CSV")

        df_to_add = count_competitors_past_comps(
            comp_code,
            show_work,
            earliest_year=most_recent_year_csv + 1,
            index=df.index.name,
            verify_entries=verify_entries,
        )
        df = df.combine_first(df_to_add)

    return df


# Write updated data back to CSV
def write_df_to_csv(df, csv_file_path, show_work=True):
    """
    Writes a pandas DataFrame to a CSV file.

    Args:
        df (pandas.DataFrame): The DataFrame to be written to CSV.
        csv_file_path (str): The file path of the CSV file.
        show_work (bool, optional): Whether to print the DataFrame after writing to CSV. Defaults to True.
    """
    df = df.astype("Int64")  # Convert all values to Int64
    df.to_csv(csv_file_path)
    if show_work:
        print("\nData written to CSV:\n")
        print(df)


# Plot the data
def plot_data(df, comp_code_list, verified_entries=False):
    """
    Plots the number of competitors over years for each competition code in the given list.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data.
    comp_code_list (list): The list of competition codes.
    verify_entries (bool, optional): WARNING: TAKES A LONG TIME. Whether to only count the number of
                                    competitors with at least one event. Defaults to False.

    Returns:
    None
    """
    plt.figure(figsize=(10, 5))

    for comp_code in comp_code_list:
        # Drop NaN values from the column before plotting so there aren't breaks in the line
        non_na_df = df[comp_code].dropna()
        plt.plot(non_na_df.index, non_na_df, label=comp_code, marker="o")

    if verified_entries:
        plt.title("Number of Competitors With At Least One Event Over Years")
    else:
        plt.title("Number of Competitors Registered Over Years")

    plt.xlabel("Year")
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.ylabel("Number of Competitors")
    plt.ylim(bottom=0)

    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    df = load_csv(csv_file_path)
    df = update_df_with_comp_list(df, comp_code_list, verify_entries, show_work)
    write_df_to_csv(df, csv_file_path)
    if plot:
        plot_data(df, comp_code_list, verify_entries)
