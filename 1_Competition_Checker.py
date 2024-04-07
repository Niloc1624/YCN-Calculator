import streamlit as st
from utils import (
    get_comps_from_events_o2cm,
    NoDropdown,
    get_competitor_names_in_comp,
    streamlit_page_header,
)
from compChecker import comp_checker
import pandas as pd


#@st.cache_data(ttl="10m", show_spinner=False)
def call_comp_checker(comp_code):
    """
    Calls the comp_checker function to check the eligibility of dancers for a competition.

    Parameters:
    comp_code (str): The competition code.

    Returns:
    None
    """
    ineligible_dancers_dict = comp_checker(comp_code, streamlit=True)

    df = pd.DataFrame(ineligible_dancers_dict)
    st.write(df)
    return


def main():
    """
    Main function to run the application.
    """

    streamlit_page_header("Competition Checker")

    form_submitted = False

    with st.spinner("Fetching Competitions from O2CM..."):
        available_comps_dict = get_comps_from_events_o2cm()

        entries_open_comps = []
        entries_closed_comps = []

        for comp_code in available_comps_dict:
            url = available_comps_dict[comp_code]["entries_url"]
            comp_name = available_comps_dict[comp_code]["comp_name"]
            available_comps_dict[comp_code][
                "total_comp_string"
            ] = f"{comp_name} ({comp_code})"
            try:
                get_competitor_names_in_comp(url)
                entries_open_comps.append(comp_code)
            except NoDropdown:
                entries_closed_comps.append(comp_code)

        with st.form("Competition Checker"):
            automatic_comp_code = st.radio(
                "Select a competition to check",
                entries_open_comps,
                format_func=lambda option: available_comps_dict[option][
                    "total_comp_string"
                ],
                key="unique_key",
            )

            with st.expander(
                "The following competitions are not yet published", expanded=False
            ):
                for closed_entry in entries_closed_comps:
                    st.write(available_comps_dict[closed_entry]["total_comp_string"])

            # Ask the user if they want to enter their own comp code
            manual_comp_code = st.text_input(
                "Or enter your own 3-letter comp code",
            )
            if manual_comp_code:
                chosen_comp_code = manual_comp_code
            else:
                chosen_comp_code = automatic_comp_code

            if st.form_submit_button("Check Entries"):
                form_submitted = True

    if len(chosen_comp_code) != 3:
        st.warning("Your comp code is not 3 letters long. Are you sure it is correct?")

    if form_submitted:
        call_comp_checker(chosen_comp_code)

    return


if __name__ == "__main__":
    main()
