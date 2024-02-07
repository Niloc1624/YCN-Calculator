import httpx
from bs4 import BeautifulSoup
import streamlit as st


def which_ele_is_in_str(list, string):
    """
    Returns the first element from a list of elements that is in a string.
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
        text = ele.text
        if text[:3] != "TBA" and text not in competitor_names:
            competitor_name_elements.append(ele)
            competitor_names.append(text)
    return competitor_name_elements


class NoDropdown(Exception):
    """
    Exception for when a dropdown menu with competitor names is not available.
    """

    pass


def count_competitors_in_comp(url, verify_entries=False, show_work=False):
    """
    Returns a dictionary containing the number of competitors in a given URL element, the year of the competition,
    and the URL itself.

    url (str): The URL of the competition to count competitors for.
    verify_entries (bool): Whether or not to verify entrants actually are registered for at least one event. Default is False.

    Returns:
    A dictionary containing num_competitors and comp_code. It also returns year if the URL is a results URL.
    Returns None if there is no dropdown on the page (probably because there is an error).
    """

    comp_code = get_comp_code_from_url(url)

    response = httpx_client().get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dropdown = soup.find("select", attrs={"id": "selEnt"})

    # If there is no dropdown, there are no competitors, probably because there is an error on the page
    try:
        competitor_name_elements_with_TBAs_and_dups = dropdown.find_all("option")[1:]
    except:
        raise NoDropdown()

    # Remove dancers who start with "TBA" (case-sensitive) or are duplicates
    competitor_name_elements = remove_TBAs_and_dups(
        competitor_name_elements_with_TBAs_and_dups
    )
    num_competitors = len(competitor_name_elements)

    num_verified_competitors = f"verify_entries set to {verify_entries}"
    if verify_entries:
        payload = {
            "selDiv": "",
            "selAge": "",
            "selSkl": "",
            "selSty": "",
            "submit": "OK",
            "selEnt": "",
        }

        # Go to the website
        response2 = httpx_client().post(url, data=payload)
        soup2 = BeautifulSoup(response2.text, "html.parser")

        verified_competitor_name_elements = []
        td_elements = soup2.find_all("td")
        # Only keep the td class elements with "&" in them, since those are the couples, also extract text
        td_elements_text = [
            element.text for element in td_elements if "&" in element.text
        ]

        for element in competitor_name_elements:
            # Converst "last_name, first_name" to "first_name last_name"
            last_first = element.text
            first_name = last_first.rsplit(", ", 1)[1]
            last_name = last_first.rsplit(", ", 1)[0]
            full_name = first_name + " " + last_name

            if any(full_name in text for text in td_elements_text):
                verified_competitor_name_elements.append(element)
        num_verified_competitors = len(verified_competitor_name_elements)

        if show_work:
            try:
                comp_year = get_comp_year_from_url(url)
            except:
                comp_year = "coming up"
            percent_with_events = round(
                100 * num_verified_competitors / num_competitors
            )
            print(
                f"At {comp_code} {comp_year}, {num_verified_competitors}/{num_competitors} ({percent_with_events}%) competitors had at least one event."
            )

    output = {
        "num_competitors": num_competitors,
        "num_verified_competitors": num_verified_competitors,
        "comp_code": comp_code,
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
        response = httpx_client().get("https://results.o2cm.com/")
        cached_soup = BeautifulSoup(response.text, "html.parser")

    for link in cached_soup.find_all("a"):
        link_url = "https://results.o2cm.com/" + link.get("href")
        if get_comp_code_from_url(link_url) == comp_code:
            most_recent_year = get_comp_year_from_url(link_url)
            break
    return most_recent_year


def get_result_from_link(
    link, o2cm_results_cache_dict, max_links=10000, show_work=True
):
    """
    Retrieve the result response_text from a given link. If the link has been visited before,
    the response_text is retrieved from the cache. Otherwise, the response_text is retrieved
    from the link and added to the cache.

    Args:
        link (str): The link to retrieve the data from.
        o2cm_results_cache_dict (dict): A dictionary to cache the results.
        max_links (int, optional): The maximum number of links to cache. Defaults to 1000.

    Returns:
        tuple: A tuple containing the retrieved data and the updated cache dictionary and whether the result was new.
    """
    is_new_result = False
    if link not in o2cm_results_cache_dict:
        response_text = httpx_client().get(link).text
        o2cm_result_info_dict = get_info_from_o2cm_results(response_text)
        o2cm_results_cache_dict[link] = o2cm_result_info_dict
        is_new_result = True
    else:
        o2cm_result_info_dict = o2cm_results_cache_dict[link]
        # Doing this to make the added link more-recently used
        o2cm_results_cache_dict.pop(link)
        o2cm_results_cache_dict[link] = o2cm_result_info_dict

    if len(o2cm_results_cache_dict) > max_links:
        oldest_link = o2cm_results_cache_dict.pop(0)  # Remove the oldest link
        if show_work:
            print(f"Removing oldest link: {oldest_link}")

    return o2cm_result_info_dict, o2cm_results_cache_dict, is_new_result


def get_info_from_o2cm_results(html):
    """
    Extracts information from the O2CM results HTML.

    Args:
        html (str): The HTML content of the O2CM results page.

    Returns:
        dict: A dictionary containing the extracted information.
            - num_rounds (int): The number of rounds in the competition.
            - dancer_names (list): A list of dancer names.
            - headers_text (list): A list of header texts.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Get num_rounds
    select_element = soup.select_one("select")
    num_rounds = 0
    if select_element:
        options = select_element.find_all("option")
        num_rounds = len(options)

    # Get dancer_names
    dancer_names = [link.get_text() for link in soup.find_all("a")]

    # Get headers_text
    headers = soup.select(".h3")
    headers_text = [header.text.lower() for header in headers]

    return {
        "num_rounds": num_rounds,
        "dancer_names": dancer_names,
        "headers_text": headers_text,
    }


def httpx_client(timeout=120):
    """
    Create an HTTP client with the specified timeout.

    Args:
        timeout (int): The timeout value in seconds. Default is 20.

    Returns:
        httpx.Client: An instance of the HTTP client.

    """
    client = httpx.Client(timeout=timeout)
    return client


def streamlit_or_print(text, streamlit_mode):
    """
    Print the text if in print mode, otherwise use streamlit.write.

    Args:
        text (str): The text to print or write.
        streamlit_mode (bool): Whether to use streamlit.write or print.

    Returns:
        None
    """
    if streamlit_mode:
        st.write(text)
    else:
        print(text)
    return
