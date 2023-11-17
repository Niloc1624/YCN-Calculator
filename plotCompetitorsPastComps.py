from countCompetitorsPastComps import count_competitors_past_comps
from utils import get_most_recent_comp_year
import matplotlib.pyplot as plt
import csv
import os

## Manual Enter
manual = True
plot = True
if manual:
    comp_code_list = ["mit", "big", "inf", "bds", "pbc", "idi", "ndc"]


def plot_past_comps(comp_code_list, show_work=True, plot=True):
    """
    Plots the number of competitors in each past competition with the given competition code.

    Parameters:
    comp_code_list (list): A list of competition codes to plot.
    show_work (bool): Whether to print progress information to the console. Default is True.

    Returns:
    None
    """

    comp_code_list = [x.lower() for x in comp_code_list]

    # Dictionary to hold data from CSV or fetched data
    data = {}
    csv_file_path = "numCompetitorsPastComps.csv"

    # Read existing data from CSV if it exists
    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode="r") as file:
            reader = csv.reader(file)
            headers = next(reader)  # First row is headers
            for row in reader:
                competition = row[0]
                if competition in comp_code_list:
                    values = {
                        int(year): (int(count) if count else None)
                        for year, count in zip(headers[1:], row[1:])
                    }
                    data[competition] = values

    start_year = float("inf")
    end_year = 0

    if show_work:
        print()

    for comp_code in comp_code_list:
        most_recent_year_website = get_most_recent_comp_year(comp_code)

        if comp_code in data:
            most_recent_year_csv = max(data[comp_code].keys())
            if most_recent_year_website > most_recent_year_csv:
                # Fetch data from the website for the missing years
                new_data = count_competitors_past_comps(
                    comp_code, show_work, earliest_year=most_recent_year_csv + 1
                )
                data[comp_code].update(new_data)
        else:
            # Fetch all available data for this competition
            data[comp_code] = count_competitors_past_comps(comp_code, show_work)

        # Update start and end years
        returned_years = list(data[comp_code].keys())
        if returned_years:
            start_year = min(min(returned_years), start_year)
            end_year = max(max(returned_years), end_year)

    if show_work:
        print()

    # Write updated data back to CSV
    years = list(range(start_year, end_year + 1))
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Competition"] + years)
        for competition, values in data.items():
            row = [competition] + [values.get(year, "") for year in years]
            writer.writerow(row)

    if plot:
        plt.figure(figsize=(10, 5))

        # Plot each competition's line
        for competition, values in data.items():
            # Separate the years and number of competitors, skipping missing data
            valid_years = [year for year, num in values.items() if num]
            valid_competitors = [num for num in values.values() if num]

            plt.plot(valid_years, valid_competitors, label=competition, marker=".")

        # Add title and labels
        plt.title("Number of Competitors Over Years")
        plt.xlabel("Year")
        plt.xticks(list(range(start_year, end_year + 1)))
        plt.ylabel("Value")
        plt.ylim(bottom=0)

        # Add a legend and gridlines
        plt.legend()
        plt.grid()

        # Show the plot
        plt.show()
    return


plot_past_comps(comp_code_list, plot=plot)
