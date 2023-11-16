import requests
from bs4 import BeautifulSoup
from utils import count_competitors_in_comp, get_comp_code_from_url

## Manual Enter
manual = 0
if manual:
    comp_code = "mit"


def count_competitors_past_comps(comp_code, show_work=True, get_counts=True):
    """
    Returns a dictionary with the number of competitors in each past competition with the given competition code.

    Parameters:
    comp_code (str): The competition code to search for.

    Returns:
    dict: A dictionary with the year as the key and the number of competitors as the value.
    """
    num_competitors_dict = {}

    # Go to the events website
    response = requests.get("https://results.o2cm.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        link_url = "https://results.o2cm.com/" + link.get("href")

        ## TODO: Make it so if we don't need to get counts (get_counts=False), we don't need to go to the page and can instead pull the year from the URL

        if get_comp_code_from_url(link_url) == comp_code:
            yearly_num_competitors_dict = count_competitors_in_comp(link_url)
            if yearly_num_competitors_dict is not None:
                year = yearly_num_competitors_dict["year"]
                num_competitors_dict[year] = yearly_num_competitors_dict["num_competitors"]

    if show_work:
        print(comp_code, num_competitors_dict)

    return num_competitors_dict


if manual:
    print(count_competitors_past_comps(comp_code))
