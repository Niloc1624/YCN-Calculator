import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import (
    count_competitors_in_comp,
    get_comp_code_from_url,
    get_comp_year_from_url,
)

if __name__ == "__main__":
    kwargs = {
        "comp_code": "mit",
        "show_work": True,
        "earliest_year": 2016,
        "index": None,
        "verify_entries": True,
    }


def count_competitors_past_comps(
    comp_code=None, show_work=False, earliest_year=0, index=None, verify_entries=False
):
    """
    Returns a pandas DataFrame with the number of competitors in each past competition with the given competition code.

    Parameters:
    comp_code (str): The competition code to search for.
    show_work (bool): Whether to print progress information to the console. Default is True.
    index (str): The name of the index column for the DataFrame. Default is None.
    earliest_year (int): The earliest year to get data for. Default is 0.
    verify_entries (bool): Whether to only count competitors with at least one event at the competition. Default is False.

    Returns:
    pandas.DataFrame: A DataFrame with the year as the index and the number of competitors as the column "num_competitors".
    """
    num_competitors_df = pd.DataFrame(columns=[comp_code])
    num_competitors_df.index.name = index

    # Go to the events website
    response = requests.get("https://results.o2cm.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        link_url = "https://results.o2cm.com/" + link.get("href")

        if get_comp_code_from_url(link_url) == comp_code:
            year = get_comp_year_from_url(link_url)
            if year < earliest_year:
                break
            yearly_num_competitors_dict = count_competitors_in_comp(
                link_url, verify_entries, show_work
            )
            if verify_entries:
                num_competitors_key = "num_verified_competitors"
            else:
                num_competitors_key = "num_competitors"
            if yearly_num_competitors_dict is not None:
                num_competitors_df.loc[year] = yearly_num_competitors_dict[
                    num_competitors_key
                ]

    if show_work:
        print(
            f'\nCompetitions with comp_code "{comp_code}" after the earliest_year {earliest_year} were found with data:'
        )
        print(num_competitors_df)

    return num_competitors_df


if __name__ == "__main__":
    count_competitors_past_comps(**kwargs)
