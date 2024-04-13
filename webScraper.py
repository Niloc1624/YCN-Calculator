import re
from bs4 import BeautifulSoup
import pandas as pd
from resultClass import Result
from datetime import date
import json
from utils import httpx_client, get_percent, streamlit_or_print
import streamlit as st

if __name__ == "__main__":
    first_names = "first_names"
    last_names = "last_names"
    streamlit = False


def webScraper(
    first_names,
    last_names,
    results_only=False,
    show_work=True,
    debug_reject_headers=True,
    streamlit=False,
    expander=None,
    from_comp_checker=False,
    o2cm_results_cache_dict=None,
    comp_codes_to_exclude=[
        "bbj",
        "hbi",
    ],  # Exclude comps judged by amateurs (bbj is Bam Jam, hbi is Harvard Beginners)
):
    """
    Scrapes https://results.o2cm.com/ given someone's name.

    Args:
        first_names (str): Comma (or comma space(s))-delimited string of first names to check.
        last_names (str): Comma (or comma space(s))-delimited string of last names to check.
        results_only (bool, optional): Set to True if you want to calculate the results and not display them. Defaults to False.
        show_work (bool, optional): True means print out points and names as they're being added. Defaults to True.
        debug_reject_headers (bool, optional): True means print out any results that couldn't be added for some reason. Defaults to True.
        streamlit (bool, optional): Set to True if using Streamlit framework. Defaults to False.
        expander (streamlit.expander, optional): Streamlit expander to write to. Defaults to None.
        o2cm_results_cache_dict (dict, optional): dictionary of cache file of visited links. Defaults to None.

    Returns:
        if results_only or streamlit is True: returns a dictionary of results
        Otherwise, returns a string and dict output for website.py
    """

    ##Make blank tables - there's probably a way to automate this but...
    smooth_data = {
        "newcomer": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
        "bronze": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
        "silver": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
        "gold": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
        "novice": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
        "pre-champ": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
        "champ": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "foxtrot": [0, 0],
            "v. waltz": [0, 0],
        },
    }
    standard_data = {
        "newcomer": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
        "bronze": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
        "silver": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
        "gold": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
        "novice": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
        "pre-champ": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
        "champ": {
            "waltz": [0, 0],
            "tango": [0, 0],
            "v. waltz": [0, 0],
            "foxtrot": [0, 0],
            "quickstep": [0, 0],
        },
    }
    rhythm_data = {
        "newcomer": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
        "bronze": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
        "silver": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
        "gold": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
        "novice": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
        "pre-champ": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
        "champ": {
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "swing": [0, 0],
            "bolero": [0, 0],
            "mambo": [0, 0],
        },
    }
    latin_data = {
        "newcomer": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
        "bronze": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
        "silver": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
        "gold": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
        "novice": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
        "pre-champ": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
        "champ": {
            "samba": [0, 0],
            "cha cha": [0, 0],
            "rumba": [0, 0],
            "paso doble": [0, 0],
            "jive": [0, 0],
        },
    }

    # Convert strings to lists
    first_names = first_names.replace(", ", ",")
    first_names = first_names.split(",")
    last_names = last_names.replace(", ", ",")
    last_names = last_names.split(",")

    # Load json cache of visited links
    num_new_results = 0
    if o2cm_results_cache_dict:
        local_json = False
    else:
        local_json = True
        o2cm_results_cache_json = "o2cm_results_cache.json"
        try:
            with open(o2cm_results_cache_json, "r") as f:
                o2cm_results_cache_dict = json.load(f)
        except FileNotFoundError:
            o2cm_results_cache_dict = {}
            with open(o2cm_results_cache_json, "w") as f:
                json.dump(o2cm_results_cache_dict, f, indent=2)

    top6_results_links = []
    # For loop here for people who have multiple O2CM accounts
    for first_name, last_name in zip(first_names, last_names):
        text = f"Calculating points for {first_name} {last_name}."
        if streamlit and from_comp_checker:
            expander.write(text)
        elif not streamlit and show_work:
            print("\n", text, "\n")

        response = httpx_client().get(
            f"https://results.o2cm.com/individual.asp?szLast={last_name}&szFirst={first_name}"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        # find each date and create Result for each top 6 link that's
        # associated with it
        date_pattern = re.compile(r"\d{2}-\d{2}-\d{2}")
        # the date *should* be assigned before any link is, but I don't trust O2CM
        # or my own code, for that matter
        # so it's getting initialized here too to be safe
        date_str = soup.find(string=date_pattern)
        if date_str:
            date_str = date_str.text[:8]

        for element in soup.find_all("td"):
            elem_text = element.text
            for item in element.contents:
                if (
                    item.name == "a"
                    and item.text.startswith(("1)", "2)", "3)", "4)", "5)", "6)"))
                    and "-- Combine --" not in item.text
                ):
                    # Listen I'm hard-coding this because if O2CM is still in use
                    # and hasn't updated their date storage by The Year Of Our Lord *2100*
                    # you have bigger problems
                    # If I'm somehow still alive at 106 you can complain to me then
                    date_object = date(
                        int(("20" + date_str[6:])),
                        int(date_str[:2]),
                        int(date_str[3:5]),
                    )

                    top6_result = Result(
                        item,
                        first_name,
                        last_name,
                        date_object,
                        competition_name,
                        o2cm_results_cache_dict,
                        debug_reject_headers,
                        streamlit_mode=streamlit,
                        expander=expander,
                    )
                    top6_results_links.append(top6_result)
                    o2cm_results_cache_dict = top6_result.o2cm_results_cache_dict

            else:
                match = re.search(date_pattern, elem_text)
                if match:
                    date_str = match.group()
                    competition_name = elem_text

    # Check rounds
    current_competition_name = None
    num_total_results = len(top6_results_links)
    for result in top6_results_links:

        if result.comp_code in comp_codes_to_exclude:
            continue

        if result.is_new_result:
            num_new_results += 1

        # Check if we earned points. If we did, add those points to the data
        points_added = False
        if (result.num_rounds == 2 and result.placement <= 3) or (
            result.num_rounds > 2 and result.placement <= 6
        ):
            for dance in result.dances:
                num_points = max(4 - result.placement, 1)
                for i in range(2):
                    if result.style and result.level and dance:
                        # Events with level "syllabus" count for bronze points
                        if result.level == "syllabus":
                            level = "bronze"
                        # Events with level "open" count for pre-champ points
                        elif result.level == "open":
                            level = "pre-champ"
                        else:
                            level = result.level
                        eval(result.style + "_data")[level][dance][i] += num_points
                        points_added = True
            if points_added and not from_comp_checker:
                if current_competition_name != result.competition_name:
                    current_competition_name = result.competition_name
                    streamlit_or_print(
                        f"#### {current_competition_name}",
                        streamlit,
                        expander,
                    )

                if num_points == 1:
                    point_text = "point"
                else:
                    point_text = "points"
                streamlit_or_print(
                    f"{num_points} {point_text} - [{result}]({result.link}) {result.num_rounds} rounds.",
                    streamlit,
                    expander,
                )

    # Save the visited links back to the json
    if local_json:
        with open(o2cm_results_cache_json, "w") as f:
            json.dump(o2cm_results_cache_dict, f, indent=2)

    # Calculate the double points for level below and +7 for 2+ levels below rules
    for d in [smooth_data, standard_data, rhythm_data, latin_data]:
        levels_list = list(d.keys())
        num_levels = len(levels_list)
        for i, (level, dances) in enumerate(d.items()):
            if i < num_levels - 1:
                for dance in dances:
                    next_level = levels_list[i + 1]
                    d[level][dance][0] += 2 * d[next_level][dance][1]
                    if i + 2 < num_levels:
                        for j in range(i + 2, num_levels):
                            higher_level = levels_list[j]
                            if d[higher_level][dance][1]:
                                d[level][dance][0] += 7

    # For compChecker.py via dancerClass
    results_nums_dict = {
        "num_new_results": num_new_results,
        "num_total_results": num_total_results,
    }

    if results_only or streamlit:
        return (
            {
                "smooth": smooth_data,
                "standard": standard_data,
                "rhythm": rhythm_data,
                "latin": latin_data,
            },
            o2cm_results_cache_dict,
            results_nums_dict,
        )

    # The rest is all for website.py:

    # Probably there's a way to automate this
    # Make dictionaries to dataframes
    smooth_df = pd.DataFrame(smooth_data)
    standard_df = pd.DataFrame(standard_data)
    rhythm_df = pd.DataFrame(rhythm_data)
    latin_df = pd.DataFrame(latin_data)

    data_frames = [smooth_df, standard_df, rhythm_df, latin_df]

    # Column labels
    for df in data_frames:
        df.columns = [
            "Newcomer",
            "Bronze",
            "Silver",
            "Gold",
            "Novice",
            "Pre-champ",
            "Champ",
        ]

    # Row labels
    smooth_df.index = ["Waltz", "Tango", "Foxtrot", "V. Waltz"]
    standard_df.index = ["Waltz", "Tango", "V. Waltz", "Foxtrot", "Quickstep"]
    rhythm_df.index = ["Cha cha", "Rumba", "Swing", "Bolero", "Mambo"]
    latin_df.index = ["Samba", "Cha cha", "Rumba", "Paso Doble", "Jive"]

    # Lots of words to go at the top of the webpage
    if len(first_names) > 1 or len(last_names) > 1:
        output = ["Combined results for "]
        for first_name, last_name in zip(first_names, last_names):
            output[0] += f"{first_name} {last_name} + "
        output[0] = output[0][:-2]
    else:
        output = [f"Results for {first_names[0]} {last_names[0]} "]

    output[0] += f"from https://results.o2cm.com/."
    output.append(
        """YCN points are calculated according to this system:
         http://ballroom.mit.edu/index.php/ycn-proficiency-points/."""
    )

    output.append(
        """The first number is the number of the points including the "double points one level down and
         +7 points for 2+ levels down" rule. This is the number that matters. For example, 1 gold point
         is worth 2 silver points and 7 bronze points. The first number includes this in its calculation.
         The second number does not."""
    )
    output.append(
        """The second number is the number of the points earned by reaching finals in that level.
         This number is just fyi."""
    )

    percent_new_results = get_percent(num_new_results, num_total_results)
    output.append(
        f"{num_new_results:,d}/{num_total_results:,d} results ({percent_new_results}%) were new and therefore added to the JSON."
    )

    # The goods (data)
    output.append("Smooth")
    output.append(smooth_df)

    output.append("Standard")
    output.append(standard_df)

    output.append("Rhythm")
    output.append(rhythm_df)

    output.append("Latin")
    output.append(latin_df)

    return output


# For testing
if __name__ == "__main__":
    output = webScraper(first_names, last_names, streamlit=streamlit)

    for line in output:
        print()
        print(line)
