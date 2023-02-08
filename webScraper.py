import requests
from bs4 import BeautifulSoup
import pandas as pd
from resultClass import Result

## Manual Enter
manual = 0
if manual:
    first_names = "Colin"
    last_names = "Richter"


def webScraper(
    first_names, last_names, results_only=0, show_work=1, debug_reject_headers=1
):
    """
    Scrapes https://results.o2cm.com/ given someone's name.

    first_names : comma (or comma space(s))-delimited string of first names to check
    last_names : comma (or comma space(s))-delimited string of last names to check
    ^^Note that the length of the above two lists must be the same
    
    results_only : set to 1 if you want to calculate the results and not display them
    show_work : 1 means print out points and names as they're being added
    debug_reject_headers : 1 means print out any results that couldn't be added for some reason
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

    top6_results_links = []
    # For loop here for people who have multiple O2CM accounts
    for first_name, last_name in zip(first_names, last_names):
        if show_work:
            print("\n", f"Calculating points for {first_name} {last_name}.", "\n")
        response = requests.get(
            f"https://results.o2cm.com/individual.asp?szLast={last_name}&szFirst={first_name}"
        )
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            link_text = link.text
            if (
                link_text.startswith(("1)", "2)", "3)", "4)", "5)", "6)"))
                and "-- Combine --" not in link_text
            ):
                top6_results_links.append(
                    Result(link, first_name + " " + last_name, debug_reject_headers)
                )

    # Check rounds
    for result in top6_results_links:
        # Open results page
        response = requests.get(result.link)
        soup = BeautifulSoup(response.text, "html.parser")

        # Count number of rounds in event
        select_element = soup.select_one("select")
        num_rounds = 0
        if select_element:
            options = select_element.find_all("option")
            num_rounds = len(options)

        # Check if we earned points. If we did, add those points to the data
        if (num_rounds == 2 and result.placement <= 3) or (
            num_rounds > 2 and result.placement <= 6
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
            if show_work:
                print(f"{result} {num_rounds} rounds. Adding {num_points} point(s).")

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
    if results_only:
        return {
            "smooth": smooth_data,
            "standard": standard_data,
            "rhythm": rhythm_data,
            "latin": latin_data,
        }
    
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
        """If you have 7 points in any dance, you have pointed out of that entire style for that level.
         For example, having 7 Bronze Latin Rumba points means you have pointed out of Bronze Latin.
         YCN points are calculated according to this system:
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
if manual:
    output = webScraper(first_names, last_names)

    for line in output:
        print()
        print(line)
