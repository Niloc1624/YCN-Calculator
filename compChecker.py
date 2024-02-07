from bs4 import BeautifulSoup
from eventClass import Event
from dancerClass import Dancer
from time import time
from utils import remove_TBAs_and_dups, httpx_client

if __name__ == "__main__":
    comp_code = "ndc"
    first_name = ""
    last_name = ""
    format_for_spreadsheet = True


def compChecker(
    comp_code,
    show_work=1,
    debug_reject_headers=1,
    first_name="",
    last_name="",
    format_for_spreadsheet=False,
):
    """
    Checks a competition for any dancers who are registered for an event they've placed out of.
    Can also check a specific dancer at a competition to see what events they've placed out of.

    comp_code: the three-letter code for the competition
    show_work: 1 for printing things to screen as it calculates
    debug_reject_headers: 1 for printing out things that could not be evaluated
    first_name / last_name: Strings. If they both have values, the program
                            will check that one dancer for the given competition
    format_for_spreadsheet: True for formatting the output for a spreadsheet with | delimiters
    """
    # Start timer
    start_time = time()
    total_num_new_results = 0
    total_num_total_results = 0

    comp_entries_website = "https://entries.o2cm.com/?event=" + comp_code

    payload = {
        "selDiv": "",
        "selAge": 00,
        "selSkl": 00,
        "selSty": "",
        "submit": "OK",
        "selEnt": "",
        "event": comp_code,
    }

    # Go to the website
    response = httpx_client().post("https://entries.o2cm.com/default.asp", data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find everyone who is regsitered at the competition
    dropdown = soup.find("select", attrs={"id": "selEnt"})

    if first_name and last_name:
        competitor_name_elements_with_TBAs_and_dups = dropdown.find_all(
            "option", string=last_name + ", " + first_name
        )
    else:
        competitor_name_elements_with_TBAs_and_dups = dropdown.find_all("option")[1:]

    competitor_name_elements = remove_TBAs_and_dups(
        competitor_name_elements_with_TBAs_and_dups
    )

    num_dancers = len(competitor_name_elements)
    if show_work:
        print("\n", f"{num_dancers} dancer(s) to check for {comp_entries_website}")

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
            if first_name and last_name:
                dancer_elements = element.find_all(
                    "a", string=first_name + " " + last_name
                )
            else:
                dancer_elements = element.find_all("a")
            for dancer_element in dancer_elements:
                dancer = Dancer(dancer_element, 1)
                dancers_and_events_dict[dancer.full_name]["events"].append(event)

    # Call webScraper() on each person to get their points (this will take a while)
    for i, information in enumerate(dancers_and_events_dict.keys()):
        dancer = dancers_and_events_dict[information]["dancer_obj"]
        dancer.calculate_points(show_work, debug_reject_headers)
        if show_work:
            dancers_completed = i + 1
            time_in_seconds = time() - start_time
            time_in_minutes = round(time_in_seconds / 60, 1)
            est_min_remaining = round(
                time_in_minutes
                * (num_dancers - dancers_completed)
                / (dancers_completed),
                1,
            )
            seconds_per_dancer = round(time_in_seconds / dancers_completed, 1)
            print(
                f"Completed {dancers_completed}/{num_dancers} dancers in {time_in_minutes} minutes. "
                + f"Estimated {est_min_remaining} minutes remaining. "
                + f"Averaging {seconds_per_dancer} seconds/dancer."
            )
            if i + 1 == num_dancers:
                print("\n\n")

            total_num_new_results += dancer.results_nums_dict["num_new_results"]
            total_num_total_results += dancer.results_nums_dict["num_total_results"]

    # Compare their points to their registration, keep track of people who have pointed out
    num_found = 0
    num_dancers_with_events = 0
    if format_for_spreadsheet:
        print(
            "Dancer|Level|Style|Event|Ineligible Dance|Points in Ineligible Dance|Exceptions"
        )
    for information in dancers_and_events_dict.keys():
        events = dancers_and_events_dict[information]["events"]
        dancer = dancers_and_events_dict[information]["dancer_obj"]
        dancer_placed_out = 0
        dancer_has_events = 0
        for event in events:
            dancer_has_events = 1
            for dance in event.dances:
                points = dancer.get_points(event.style, event.level, dance)
                if (points >= 7) and (event.level != "champ"):
                    ##ADD KEEPING TRACK HERE##

                    # prob replace this with len(list)
                    dancer_placed_out = 1
                    if show_work:
                        if format_for_spreadsheet:
                            print(
                                f"{dancer}|{event.level}|{event.style}|{event.dances_string}|{dance}|{points}"
                            )
                        else:
                            print(
                                f"{dancer} is registered for {event}, but has {points} points in {dance}."
                            )
        num_found += dancer_placed_out
        num_dancers_with_events += dancer_has_events

    if show_work:
        print(
            "\n",
            f"{num_dancers_with_events}/{num_dancers} dancers have events.",
            "\n",
            f"{num_found}/{num_dancers_with_events} are registered for an event they have placed out of.",
            "\n",
        )

    # End timer
    time_in_seconds = time() - start_time
    time_in_minutes = round(time_in_seconds / 60, 1)
    seconds_per_dancer = round(time_in_seconds / num_dancers, 1)
    print(
        f"This took {time_in_minutes} minutes to run for {num_dancers} dancers. "
        + f"That is an average {seconds_per_dancer} seconds/dancer.\n"
    )

    percent_new_results = round(100 * total_num_new_results / total_num_total_results)
    print(
        f"{total_num_new_results}/{total_num_total_results} results ({percent_new_results}%) were new and therefore added to the JSON."
    )
    return


if __name__ == "__main__":
    compChecker(
        comp_code,
        first_name=first_name,
        last_name=last_name,
        format_for_spreadsheet=format_for_spreadsheet,
    )
