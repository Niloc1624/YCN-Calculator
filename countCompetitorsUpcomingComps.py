import requests
from bs4 import BeautifulSoup
from utils import count_competitors_in_comp


def count_competitors_upcoming_comps():
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

            # Find everyone who is regsitered at the competition
            # If there's an error it's probably because registration isn't open but the link exists
            try:
                num_competitors = count_competitors_in_comp(entries_url)[
                    "num_competitors"
                ]
                print(f"{num_competitors} dancers : {entries_url}")
            except:
                print(f"Registration not open for {entries_url}")
    return


count_competitors_upcoming_comps()
