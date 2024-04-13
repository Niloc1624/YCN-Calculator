from bs4 import BeautifulSoup
from eventClass import Event
from dancerClass import Dancer
from time import time
from utils import (
    remove_TBAs_and_dups,
    httpx_client,
    get_percent,
    streamlit_or_print,
)
import streamlit as st

if __name__ == "__main__":
    comp_code = "mit"
    first_name = ""
    last_name = ""
    format_for_spreadsheet = True


def comp_checker(
    comp_code,
    show_work=1,
    debug_reject_headers=1,
    first_name="",
    last_name="",
    format_for_spreadsheet=False,
    streamlit=False,
):
    """
    Checks a competition for any dancers who are registered for an event they've placed out of.
    Can also check a specific dancer at a competition to see what events they've placed out of.

    Parameters:
    comp_code (str): The three-letter code for the competition.
    show_work (int, optional): 1 for printing things to screen as it calculates. Defaults to 1.
    debug_reject_headers (int, optional): 1 for printing out things that could not be evaluated. Defaults to 1.
    first_name (str, optional): The first name of the specific dancer to check. Defaults to "".
    last_name (str, optional): The last name of the specific dancer to check. Defaults to "".
    format_for_spreadsheet (bool, optional): True for formatting the output for a spreadsheet with | delimiters. Defaults to False.
    streamlit (bool, optional): True if running in a Streamlit app. Defaults to False.

    Returns:
    If streamlit==1: A dictionary containing information about ineligible dancers, if running in Streamlit mode.
    Otherwise, None.
    """

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
    text = f"{num_dancers:,d} dancer(s) to check for {comp_entries_website}"
    expander = None
    if streamlit:
        expander = st.status(text, expanded=True)
    elif show_work:
        print("\n", text)

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
                if dancer_element.text[:3] != "TBA":
                    dancer = Dancer(dancer_element, 1)
                    dancers_and_events_dict[dancer.full_name]["events"].append(event)

    # Start timer
    start_time = time()
    total_num_new_results = 0
    total_num_total_results = 0

    # Call webScraper() on each person to get their points (this will take a while)
    for i, information in enumerate(dancers_and_events_dict.keys()):
        dancer = dancers_and_events_dict[information]["dancer_obj"]
        dancer.calculate_points(
            show_work,
            debug_reject_headers,
            streamlit=streamlit,
            expander=expander,
            from_comp_checker=True,
        )
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

            streamlit_or_print(
                f"Completed {dancers_completed:,d}/{num_dancers:,d} dancers in {time_in_minutes} minutes. "
                + f"Estimated {est_min_remaining} minutes remaining. "
                + f"Averaging {seconds_per_dancer} seconds/dancer.",
                streamlit,
                expander,
            )
            if not streamlit and i + 1 == num_dancers:
                print("\n\n")

            total_num_new_results += dancer.results_nums_dict["num_new_results"]
            total_num_total_results += dancer.results_nums_dict["num_total_results"]

    # Minimize the expander and update its state
    if streamlit:
        expander.update(expanded=False, state="complete")

    # Compare their points to their registration, keep track of people who have pointed out
    num_found = 0
    num_dancers_with_events = 0
    if streamlit:
        ineligible_dancers_dict = {
            "Dancer": [],
            "Level": [],
            "Style": [],
            "Event": [],
            "Ineligible Dance": [],
            "Points in Ineligible Dance": [],
        }
    elif format_for_spreadsheet and show_work:
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
                    if streamlit:
                        ineligible_dancers_dict["Dancer"].append(dancer)
                        ineligible_dancers_dict["Level"].append(event.level)
                        ineligible_dancers_dict["Style"].append(event.style)
                        ineligible_dancers_dict["Event"].append(event.dances_string)
                        ineligible_dancers_dict["Ineligible Dance"].append(dance)
                        ineligible_dancers_dict["Points in Ineligible Dance"].append(
                            points
                        )
                    elif show_work:
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
        streamlit_or_print(
            f"\n{num_dancers_with_events:,d}/{num_dancers:,d} dancers have events."
            + f"\n{num_found:,d}/{num_dancers_with_events:,d} are registered for an event they have placed out of.\n",
            streamlit,
        )

    # End timer
    time_in_seconds = time() - start_time
    time_in_minutes = round(time_in_seconds / 60, 1)
    seconds_per_dancer = round(time_in_seconds / num_dancers, 1)
    streamlit_or_print(
        f"This took {time_in_minutes:,d} minutes to run for {num_dancers:,d} dancers. "
        + f"That is an average {seconds_per_dancer} seconds/dancer.\n",
        streamlit,
    )

    percent_new_results = get_percent(total_num_new_results, total_num_total_results)
    streamlit_or_print(
        f"{total_num_new_results:,d}/{total_num_total_results:,d} results ({percent_new_results}%) were new and therefore added to the JSON.\n",
        streamlit,
    )
    if streamlit:
        return ineligible_dancers_dict


if __name__ == "__main__":
    comp_checker(
        comp_code,
        first_name=first_name,
        last_name=last_name,
        format_for_spreadsheet=format_for_spreadsheet,
    )
