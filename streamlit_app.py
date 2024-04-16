import streamlit as st
from webScraper import webScraper
import pandas as pd
import os
import json
from utils import httpx_client, get_percent, streamlit_page_header
from firebase_funcs import pull_dicts_from_firebase, upload_dict_to_firebase


def process_result(values_dict, simple=False):
    """
    Process the result dictionary and convert it into a DataFrame.

    Parameters:
    values_dict (dict): A dictionary containing dance, level, and points.
    simple (bool): A boolean indicating whether to return a detailed or simple DataFrame. Simple only contains total points.

    Returns:
    pandas.DataFrame: A DataFrame containing the processed values.
    """
    # Convert dictionary values to strings without brackets
    values_dict_capitalized = {
        dance.capitalize(): {
            level.capitalize(): scores for level, scores in levels.items()
        }
        for dance, levels in values_dict.items()
    }

    values_dict_str = {}
    for dance, levels in values_dict_capitalized.items():
        values_dict_str[dance] = {}
        for level, scores in levels.items():
            if simple:
                values_dict_str[dance][level] = scores[0]
            else:
                values_dict_str[dance][level] = ", ".join(map(str, scores))

    # Create a DataFrame from the modified smooth_data dictionary
    values_df = pd.DataFrame(values_dict_str)
    return values_df


# @st.cache_data(ttl="10m", show_spinner=False)
def process_names(first_names, last_names, simple=False, o2cm_results_cache_dict=None):
    """
    Process the given first names and last names.

    Args:
        first_names (list): A list of first names.
        last_names (list): A list of last names.
        simple (bool): A boolean indicating whether to return a detailed or simple DataFrame. Simple only contains total points.


    Returns:
        None
    """
    if not first_names or not last_names:
        st.warning("Please enter both first and last names.")
    else:
        expander = st.status(
            f"Calculating points for {first_names} {last_names}.", expanded=True
        )
        result_dict, new_o2cm_results_cache_dict, results_nums_dict = webScraper(
            first_names,
            last_names,
            streamlit=True,
            expander=expander,
            o2cm_results_cache_dict=o2cm_results_cache_dict,
        )

        output_tables = {}
        for style in result_dict:
            values_dict = result_dict[style]
            values_df = process_result(values_dict, simple=simple)
            output_tables[style] = values_df

        expander.update(expanded=False, state="complete")
    return output_tables, new_o2cm_results_cache_dict, results_nums_dict


def ask_for_json():
    """
    Asks the user to upload a JSON file and returns its contents as a dictionary.

    Returns:
        dict: The contents of the uploaded JSON file as a dictionary.
    """
    o2cm_results_cache_dict = None
    o2cm_results_cache_json = st.file_uploader(
        "I'm working on a way to automate this. For now, you have to do it manually.",
        type=["json"],
    )
    if o2cm_results_cache_json is not None:
        o2cm_results_cache_dict = json.load(o2cm_results_cache_json)
    return o2cm_results_cache_dict


def display_results(
    output_tables, new_o2cm_results_cache_dict, results_nums_dict, results_location
):
    """
    Display the results in a Streamlit app and provide a download button for a new JSON file if using github.

    Args:
        output_tables (dict): A dictionary containing the output tables for different styles.
        new_o2cm_results_cache_dict (dict): A dictionary containing the new O2CM results cache.
        results_nums_dict (dict): A dictionary containing the number of new and total results.
        json_location (str): A string indicating the location of the JSON file (github or firebase).

    Returns:
        None
    """

    if results_location == "github":
        file = "JSON"
    else:
        file = "cache"

    num_new_results = results_nums_dict["num_new_results"]
    num_total_results = results_nums_dict["num_total_results"]
    percent_new_results = get_percent(num_new_results, num_total_results)
    st.write(
        f"{num_new_results:,d}/{num_total_results:,d} results ({percent_new_results}%) were new and therefore added to the {file}.",
        f"The {file} now has {len(new_o2cm_results_cache_dict):,d} results.",
    )

    if results_location == "github":
        st.write(
            "#### If there are any new results, please upload this new JSON file when running this in the future."
        )
        st.download_button(
            "Download new JSON",
            json.dumps(new_o2cm_results_cache_dict, indent=2),
            "o2cm_results_cache.json",
        )
    elif results_location == "firebase" and num_new_results:
        with st.spinner("Uploading results to Firebase..."):
            upload_dict_to_firebase(new_o2cm_results_cache_dict)

    for style in output_tables:
        st.write(f"### {style.title()}", output_tables[style])

    return


def warn_about_leading_or_trailing_spaces(str):
    """
    Check for leading or trailing spaces in a string.

    Args:
        str (str): The string to check.

    Returns:
        None
    """
    if str.startswith(" "):
        st.warning("This starts with a space, is that on purpose?")
    if str.endswith(" "):
        st.warning("This ends with a space, is that on purpose?")
    return


def main():
    """
    Main function to run the application.
    """

    # Can be github or firebase. If github, the JSON file will asked from the user and downloaded from GitHub.
    # If firebase, the JSON file will be downloaded from and reuploaded to Firebase.
    results_location = "github"

    streamlit_page_header("YCN Point Calculator")

    
    ####TODO: Figure out how to get it to run with results_location="github" if I get an error from Firebase
    
    
    if results_location == "github":

        st.write(
            "#### RECOMMENDED: Upload the JSON file from the last time you used this. "
            + "If this is your first time or if you lost the file, you can skip this step."
        )

        json_url = "https://raw.githubusercontent.com/Niloc1624/YCN-Calculator/master/o2cm_results_cache.json"

        o2cm_github_dict = httpx_client().get(json_url).json()

        o2cm_results_cache_dict = ask_for_json()
        # Combine the uploaded JSON with the GitHub JSON
        if o2cm_results_cache_dict is not None:
            o2cm_results_cache_dict.update(o2cm_github_dict)
        elif not os.path.exists("o2cm_results_cache.json"):
            o2cm_results_cache_dict = o2cm_github_dict

        with st.expander("Why?"):
            st.write(
                """The JSON contains a cache of the results from several thousand O2CM results pages.
                    This is necessary to avoid hitting the O2CM servers too hard. Also, getting a result from the JSON
                    is about 7x faster than getting it from the O2CM servers."""
            )
            st.write(
                """When you run this, you will get a new JSON file to use next time. This new JSON
                    will contain the results from the new results pages you hit if they are not already in the cache.
                    Additionally, the more recent searches will be moved to the top of the JSON file, so they will not
                    be deleted as quickly if the cache is full (currently set to 10k results, or about 5 MB)."""
            )
            st.markdown(
                """By default, the JSON file from
                        [here](https://github.com/Niloc1624/YCN-Calculator/blob/master/o2cm_results_cache.json)
                        is used. If you upload a JSON file, the program will combine it with the default one
                        above and use the combined JSON file."""
            )

    st.write("## Enter a first and last name (or lists of each)")
    st.write(
        """If the person you are searching for has multiple O2CM accounts, you can enter comma-delimited
        lists of first names and last names. The calculator will add the results from these accounts together.
        Make sure there are an equal number of first names and last names in each list.""",
    )
    st.write(
        """Results are pulled from https://results.o2cm.com/. YCN points are calculated
        according to [MIT's rules](http://ballroom.mit.edu/index.php/ycn-proficiency-points/)."""
    )

    # Display two input boxes side by side
    col1, col2 = st.columns(2)
    with col1:
        first_names = st.text_input("First Name(s)")
        warn_about_leading_or_trailing_spaces(first_names)
    with col2:
        last_names = st.text_input("Last Name(s)")
        warn_about_leading_or_trailing_spaces(last_names)

    simple = not st.checkbox("Detailed Tables")
    if not simple:
        st.write(
            """Detailed tables include two numbers in each box. The first number is what displays
                in the simple table. That is the points a dancer has in that level. The second number is
                the number of points earned by reaching finals in that level. It does not include points
                from the "double points one level down and +7 points for 2+ levels down" rule."""
        )

    if st.button("Process Name(s)"):
        # Pull the results from firebase only after someone is searched for
        if results_location == "firebase":
            with st.spinner("Fetching results from Firebase..."):
                o2cm_results_cache_dict = pull_dicts_from_firebase()

        output_tables, new_o2cm_results_cache_dict, results_nums_dict = process_names(
            first_names, last_names, simple, o2cm_results_cache_dict
        )
        display_results(
            output_tables,
            new_o2cm_results_cache_dict,
            results_nums_dict,
            results_location,
        )

    return


if __name__ == "__main__":
    main()
