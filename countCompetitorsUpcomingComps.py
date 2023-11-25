import requests
from bs4 import BeautifulSoup
from utils import count_competitors_in_comp, NoDropdown

if __name__ == "__main__":
    verify_entries = True


def count_competitors_upcoming_comps(verify_entries=False):
    """
    Checks https://events.o2cm.com/, outputs the number of competitors entered in each competition.
    Excludes duplicate names and names starting with "TBA"

    Args:
        verify_entries (bool): True:  only show competitors with at least one event at the competition
                               False: show all competitors registered for the competition
    """
    # Go to the events website
    response = requests.get("https://events.o2cm.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    print()
    for link in soup.find_all("a"):
        link_url = link.get("href")
        # Make sure the URL is a registration URL
        if link_url.startswith("https://register.o2cm.com"):
            # Generate the entries URL and go there
            entries_url = "https://entries.o2cm.com/?event=" + link_url.split("=")[-1]

            # Find everyone who is registered at the competition
            # If there's an error it's probably because registration isn't open but the link exists
            try:
                competitors_dict = count_competitors_in_comp(
                    entries_url, verify_entries=verify_entries
                )
                num_competitors = competitors_dict["num_competitors"]
                num_verified_competitors = competitors_dict["num_verified_competitors"]
                if verify_entries:
                    percent_with_events = round(
                        num_verified_competitors / num_competitors * 100
                    )
                    print(
                        f"{num_verified_competitors}/{num_competitors} ({percent_with_events}%) dancers have events : {entries_url}"
                    )
                else:
                    print(f"{num_competitors} dancers : {entries_url}")
            except NoDropdown:
                print(f"Registration not open for {entries_url}")
    print()


if __name__ == "__main__":
    count_competitors_upcoming_comps(verify_entries=verify_entries)
