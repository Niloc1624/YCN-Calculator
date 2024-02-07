import streamlit as st
from webScraper import webScraper
import pandas as pd
import json


def process_names(first_names, last_names):
    """
    Process a list of first names and last names and return a list of full names.

    Args:
        first_names (list): A list of first names.
        last_names (list): A list of last names.

    Returns:
        list: A list of full names, where each full name is a concatenation of the corresponding first name and last name.
    """
    full_names = [f"{first} {last}" for first, last in zip(first_names, last_names)]
    return full_names


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


@st.cache_data()
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
        result_dict, new_o2cm_results_cache_dict = webScraper(
            first_names,
            last_names,
            streamlit=True,
            o2cm_results_cache_dict=o2cm_results_cache_dict,
        )

        output_tables = {}
        for style in result_dict:
            values_dict = result_dict[style]
            values_df = process_result(values_dict, simple=simple)
            output_tables[style] = values_df
    return output_tables, new_o2cm_results_cache_dict


def ask_for_json():
    o2cm_results_cache_dict = None
    o2cm_results_cache_json = st.file_uploader(
        "I'm working on a way to automate this. For now, you have to do it manually.",
        type=["json"],
    )
    if o2cm_results_cache_json is not None:
        o2cm_results_cache_dict = json.load(o2cm_results_cache_json)
    return o2cm_results_cache_dict


def display_results(output_tables, new_o2cm_results_cache_dict):
    st.write("#### When running this in the future, please upload this new JSON file.")
    st.download_button(
        "Download new JSON",
        json.dumps(new_o2cm_results_cache_dict),
        "o2cm_results_cache.json",
    )
    st.write(
        """Results are pulled from https://results.o2cm.com/. YCN points are calculated
             according to this system: http://ballroom.mit.edu/index.php/ycn-proficiency-points/."""
    )

    for style in output_tables:
        st.write(f"### {style.title()}")
        st.table(output_tables[style])

    return


def main():
    """
    Main function to run the application.
    """

    st.title("YCN Point Calculator")

    requirements = """#### REQUIRED: Upload the .json file from the last time you used this.
                   If this is your first time or if you lost the file, Download the .json file from
                   [this link]() and upload it into the field below."""
    st.markdown(requirements.replace("\n", ""))

    with st.expander("Why?"):
        st.write(
            """The .json contains a cache of the results from several thousand O2CM results pages.
                 This is necessary to avoid hitting the O2CM servers too hard. Also, getting a result from the .json
                 is about 7x faster than getting it from the O2CM servers."""
        )
        st.write(
            """When you run this, you will get a new .json file to use next time. This new .json
                 will contain the results from the new results pages you hit if they are not already in the cache.
                 Additionally, the the more resent searches will be moved to the top of the .json file, so they will not
                 be deleted as quickly if the cache is full (currently set to 10k results, or about 5 MB)."""
        )

    o2cm_results_cache_dict = ask_for_json()

    if o2cm_results_cache_dict is None:
        st.write("Enter a first and last name (or lists of each)")
        st.write(
            """Bonus feature! If the person you are searching for has multiple O2CM accounts,
            you can enter comma-delimited lists of first names and last names.
            The calculator will add the results from these accounts together.
            Make sure there are an equal number of first names and last names in each list.""",
        )

        # Display two input boxes side by side
        col1, col2 = st.columns(2)
        with col1:
            first_names = st.text_input("First Name(s)")
        with col2:
            last_names = st.text_input("Last Name(s)")

        simple = not st.checkbox("Detailed Tables")
        if not simple:
            st.write(
                """Detailed tables include two numbers in each box. The first number is what displays
                    in the simple table. That is the points a dancer has in that level. The second number is
                    the number of points earned by reaching finals in that level. It does not include points
                    from the "double points one level down and +7 points for 2+ levels down" rule."""
            )

        if st.button("Process Name(s)"):
            output_tables, new_o2cm_results_cache_dict = process_names(
                first_names, last_names, simple, o2cm_results_cache_dict
            )
            display_results(output_tables, new_o2cm_results_cache_dict)

    return


if __name__ == "__main__":
    main()
