import requests
from bs4 import BeautifulSoup
from eventClass import Event
from dancerClass import Dancer

## Manual Enter
manual = 1
if manual:
    comp_website = "https://entries.o2cm.com/?event=idg"


def compChecker(comp_website, show_work=1, debug_reject_headers=1):
    """
    Checks a competition for any dancers who are registered for an event they've placed out of

    comp_website: the entries website for the competition
    show_work: 1 for printing things to screen as it calculates
    debug_reject_headers: 1 for printing out things that could not be evaluated
    """
    # Go to the website
    response = requests.get(comp_website)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find everyone who is regsitered at the competition
    dropdown = soup.find("select", attrs={"id": "selEnt"})
    competitor_name_elements_with_TBAs = dropdown.find_all("option")[1:]
    # Remove entries that start with "TBA" (case-sensitive)
    competitor_name_elements = [
        ele for ele in competitor_name_elements_with_TBAs if ele.text[:3] != "TBA"
    ]

    num_dancers = len(competitor_name_elements)
    if show_work:
        print("\n", f"There are {num_dancers} dancers to check.")

    # Make dictionary skeleton of dancers for level/dance combo
    dancers_and_events_dict = {}
    for competitor_name_element in competitor_name_elements:
        dancer = Dancer(competitor_name_element, 0)
        dancers_and_events_dict[(dancer.full_name)] = {
            "events": [],
            "dancer_obj": dancer,
        }

    # Find what events people are registered for
    for element in soup.find_all(class_=["h5b", "h5n"]):
        # If it's the name of an event, make an Event object for it
        if element.get("class") == ["h5b"]:
            event = Event(element, debug_reject_headers)
        # If it's the name of a couple, add the Event object to each couple's dictionary entry
        elif element.get("class") == ["h5n"]:
            dancer_elements = element.find_all("a")
            for dancer_element in dancer_elements:
                dancer = Dancer(dancer_element, 1)
                dancers_and_events_dict[dancer.full_name]["events"].append(event)

    # Call webScraper() on each person to get their points (this will take a while)
    for i, information in enumerate(dancers_and_events_dict.keys()):
        dancer = dancers_and_events_dict[information]["dancer_obj"]
        dancer.calculate_points(show_work, debug_reject_headers)
        if show_work:
            print(f"Completed {i+1}/{num_dancers} dancers.")

    # Compare their points to their registration, keep track of people who have pointed out
    num_found = 0
    for information in dancers_and_events_dict.keys():
        events = dancers_and_events_dict[information]["events"]
        dancer = dancers_and_events_dict[information]["dancer_obj"]
        dancer_placed_out = 0
        for event in events:
            for dance in event.dances:
                points = dancer.get_points(event.style, event.level, dance)
                if (points >= 7) and (event.level != "champ"):

                    ##ADD KEEPING TRACK HERE##

                    # prob replace this with len(list)
                    dancer_placed_out = 1
                    if show_work:
                        print(
                            f"{dancer} is registered for {event}, but has {points} points in {dance}."
                        )
        num_found += dancer_placed_out

    if show_work:
        print(
            "\n",
            f"{num_found}/{num_dancers} dancers are registered for an event they have placed out of.",
            "\n",
        )

    return


compChecker(comp_website)
