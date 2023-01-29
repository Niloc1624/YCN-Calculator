from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from resultChecker import resultValid
from resultClass import Result

##Manual Enter

first_name = "first_name"
last_name = "last_name"


def webScraper(first_name, last_name):

    # config
    show_browser = 0
    show_work = 1
    debug_reject_headers = 1

    ##Make blank tables
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

    ##Open Chrome and search for a dancer

    op = webdriver.ChromeOptions()
    if not show_browser:
        op.add_argument("headless")  # makes it so Chrome doesn't actually open
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=op
    )

    driver.get("https://results.o2cm.com/individual.asp")

    first_name_field = driver.find_element(By.ID, "szFirst")
    last_name_field = driver.find_element(By.ID, "szLast")
    search = driver.find_element(By.ID, "DoSearch")

    first_name_field.send_keys(first_name)
    last_name_field.send_keys(last_name)
    search.click()

    ## Do shit with results

    all_results = driver.find_elements(By.PARTIAL_LINK_TEXT, ") ")

    # Get results in top 6
    top6_results_links = []
    for i, result in enumerate(all_results):
        # if result.get_attribute("innerHTML")[0:2] == "3)":
        #    print("starts with 3)")

        # print(result.get_attribute("innerHTML"))
        if resultValid(driver, result):
            top6_results_links.append(Result(result, driver, debug_reject_headers))

    # Check rounds
    for result in top6_results_links:

        result.calculateDances()

        # Open results page
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        # print(result_link)
        driver.get(result.link)

        # Count number of rounds in event
        options = driver.find_elements(By.CSS_SELECTOR, "option")
        num_rounds = len(options)

        # If event is straight semi, did we get top 3?
        if (num_rounds == 2 and result.placement <= 3) or (
            num_rounds > 2 and result.placement <= 6
        ):
            if result.placement <= 3:
                for dance in result.dances:
                    # print(result.style + "_data")
                    num_points = max(4 - result.placement, 1)
                    for i in range(2):
                        eval(result.style + "_data")[result.level][dance][
                            i
                        ] += num_points

                # print(result.raw_text)
                if show_work:
                    print(
                        f"{result} There were {num_rounds} rounds. Adding {num_points} point(s)."
                    )
                # print()

        # Close results page
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])

    for data in [smooth_data, standard_data, rhythm_data, latin_data]:
        levels = list(data)[::-1]
        for i, level in enumerate(levels):
            for dance in data[level]:
                if i:
                    higher_level = levels[i - 1]
                    current_points = data[level][dance][0]
                    new_point_total = 2 * data[higher_level][dance][0] + current_points
                    data[level][dance][0] = new_point_total

    smooth_df = pd.DataFrame(smooth_data)
    standard_df = pd.DataFrame(standard_data)
    rhythm_df = pd.DataFrame(rhythm_data)
    latin_df = pd.DataFrame(latin_data)

    data_frames = [smooth_df, standard_df, rhythm_df, latin_df]

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

    smooth_df.index = ["Waltz", "Tango", "Foxtrot", "V. Waltz"]
    standard_df.index = ["Waltz", "Tango", "V. Waltz", "Foxtrot", "Quickstep"]
    rhythm_df.index = ["Cha cha", "Rumba", "Swing", "Bolero", "Mambo"]
    latin_df.index = ["Samba", "Cha cha", "Rumba", "Paso Doble", "Jive"]

    output = [f"Results for {first_name} {last_name}"]

    output.append(
        'The first number is the number of the points including the "double points each level down" rule. This is the number that matters'
    )
    output.append(
        "The second number is the number of the points earned by reaching finals in that level. This number is just fyi."
    )

    output.append("Smooth")
    output.append(smooth_df)

    output.append("Standard")
    output.append(standard_df)

    output.append("Rhythm")
    output.append(rhythm_df)

    output.append("Latin")
    output.append(latin_df)

    return output


'''output = webScraper(first_name, last_name)

for line in output:
    print()
    print(line)'''
