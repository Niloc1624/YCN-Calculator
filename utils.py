import requests
from bs4 import BeautifulSoup


def which_ele_is_in_str(list, string):
    """
    Returns the first element from list that is in string.
    """
    return next((x for x in list if x in string), None)


def lists_both_have_ele_in_str(list1, list2, string):
    """
    Returns if string is in both list1 and list2.
    """
    return which_ele_is_in_str(list1, string) and which_ele_is_in_str(list2, string)


def remove_TBAs_and_dups(competitor_name_elements_with_TBAs_and_dups):
    """
    Removes entries that start with TBA (case-sensitive) and duplicate names.

    competitor_name_elements_with_TBAs_and_dups : list of beautiful soup elements
    """
    competitor_names = []
    competitor_name_elements = []
    for ele in competitor_name_elements_with_TBAs_and_dups:
        if ele.text[:3] != "TBA" and ele.text not in competitor_names:
            competitor_name_elements.append(ele)
            competitor_names.append(ele.text)
    return competitor_name_elements


def count_competitors_in_comp(url):
    """
    Returns a dictionary containing the number of competitors in a given URL element, the year of the competition,
    and the URL itself.

    url (str): The URL of the competition to count competitors for.

    Returns:
    A dictionary containing num_competitors and comp_code. It also returns year if the URL is a results URL.
    Returns None if there is no dropdown on the page (probably because there is an error).
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dropdown = soup.find("select", attrs={"id": "selEnt"})

    # If there is no dropdown, there are no competitors, probably because there is an error on the page
    try:
        competitor_name_elements_with_TBAs_and_dups = dropdown.find_all("option")[1:]
    except:
        return None

    # Remove dancers who start with "TBA" (case-sensitive) or are duplicates
    competitor_name_elements = remove_TBAs_and_dups(
        competitor_name_elements_with_TBAs_and_dups
    )

    output = {
        "num_competitors": len(competitor_name_elements),
        "comp_code": get_comp_code_from_url(url),
    }
    return output


def get_comp_code_from_url(url, with_year=False):
    """
    Returns the competition code from a given URL element.

    Args:
    url (str): The URL of the competition to get the code for.
    with_year (int, optional): Whether or not to include the year in the competition code (results URLs only).

    Returns:
    str: The competition code.
    """

    if with_year:
        if "results" not in url:
            raise "Must be a https://results.o2cm.com/ URL to have a year"
        num_chars = 5
    else:
        num_chars = 3

    return url.split("event=")[1][:num_chars].lower()


def get_comp_year_from_url(url):
    """
    Returns the competition year from a given URL element.

    Args:
    url (str): The URL of the competition to get the year for.

    Returns:
    int: The competition year.
    """

    if "results" not in url:
        raise "Must be a https://results.o2cm.com/ URL to have a year"

    year = "20" + url.split("event=")[1][3:5]

    return int(year)


# Global variable to store the cached soup object
cached_soup = None


def get_most_recent_comp_year(comp_code):
    """
    Returns the most recent year of a competition with the given competition code.

    Args:
    comp_code (str): The competition code to search for.

    Returns:
    int: The most recent year of the competition.
    """
    global cached_soup

    # Fetch the soup object if it is not already cached
    if cached_soup is None:
        response = requests.get("https://results.o2cm.com/")
        cached_soup = BeautifulSoup(response.text, "html.parser")

    for link in cached_soup.find_all("a"):
        link_url = "https://results.o2cm.com/" + link.get("href")
        if get_comp_code_from_url(link_url) == comp_code:
            most_recent_year = get_comp_year_from_url(link_url)
            break
    return most_recent_year
