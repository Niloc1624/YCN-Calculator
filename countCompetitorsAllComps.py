import requests
from bs4 import BeautifulSoup
from utils import remove_TBAs_and_dups


def count_competitors_all_comps():
    """
    Checks https://events.o2cm.com/, outputs the number of competitors entered in each competition
    """
    # Go to the events website
    response = requests.get("https://events.o2cm.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        link_url = link.get("href")
        # Make sure the URL is a registration URL
        if link_url.startswith("https://register.o2cm.com"):
            # Generate the entries URL and go there
            entries_url = "https://entries.o2cm.com/?event=" + link_url.split("=")[-1]
            response2 = requests.get(entries_url)
            soup2 = BeautifulSoup(response2.text, "html.parser")
            # Find everyone who is regsitered at the competition
            # If there's an error it's probably because registration isn't open but the link exists
            try:
                dropdown = soup2.find("select", attrs={"id": "selEnt"})
                competitor_name_elements_with_TBAs_and_dups = dropdown.find_all(
                    "option"
                )[1:]
                # Remove dancers who start with "TBA" (case-sensitive) or are duplicates
                competitor_name_elements = remove_TBAs_and_dups(
                    competitor_name_elements_with_TBAs_and_dups
                )

                print(f"{len(competitor_name_elements)} dancers : {entries_url}")
            except:
                print(f"Registration not open for {entries_url}")
    return


count_competitors_all_comps()
