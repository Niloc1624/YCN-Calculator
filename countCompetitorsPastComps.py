import requests
from bs4 import BeautifulSoup
from utils import (
    count_competitors_in_comp,
    get_comp_code_from_url,
    get_comp_year_from_url,
)

## Manual Enter
manual = 0
if manual:
    comp_code = "mit"


def count_competitors_past_comps(comp_code, show_work=True, earliest_year=0):
    """
    Returns a dictionary with the number of competitors in each past competition with the given competition code.

    Parameters:
    comp_code (str): The competition code to search for.
    show_work (bool): Whether to print progress information to the console. Default is True.
    earliest_year (int): The earliest year to get data for. Default is 0.

    Returns:
    dict: A dictionary with the year as the key and the number of competitors as the value. If get_counts is False, the value is None.
    """
    num_competitors_dict = {}

    # Go to the events website
    response = requests.get("https://results.o2cm.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        link_url = "https://results.o2cm.com/" + link.get("href")

        if get_comp_code_from_url(link_url) == comp_code:
            year = get_comp_year_from_url(link_url)
            if year < earliest_year:
                break
            yearly_num_competitors_dict = count_competitors_in_comp(link_url)
            if yearly_num_competitors_dict is not None:
                num_competitors_dict[year] = yearly_num_competitors_dict[
                    "num_competitors"
                ]

    if show_work:
        print(comp_code, num_competitors_dict)

    return num_competitors_dict


if manual:
    print(count_competitors_past_comps(comp_code))
