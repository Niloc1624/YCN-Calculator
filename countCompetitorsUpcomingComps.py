from utils import (
    count_competitors_in_comp,
    NoDropdown,
    get_comps_from_events_o2cm,
)

if __name__ == "__main__":
    verify_entries = False


def count_competitors_upcoming_comps(verify_entries=False):
    """
    Checks https://events.o2cm.com/, outputs the number of competitors entered in each competition.
    Excludes duplicate names and names starting with "TBA"

    Args:
        verify_entries (bool): True:  only show competitors with at least one event at the competition
                               False: show all competitors registered for the competition
    """

    available_comps_dict = get_comps_from_events_o2cm()

    for comp_code in available_comps_dict:
        entries_url = available_comps_dict[comp_code]["entries_url"]
        comp_name = available_comps_dict[comp_code]["comp_name"]
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
                    f"{num_verified_competitors}/{num_competitors} ({percent_with_events}%) dancers have events : {comp_name}"
                )
            else:
                print(f"{num_competitors} dancers : {comp_name}")
        except NoDropdown:
            print(f"Registration not open for {comp_name}")

    print()
    return


if __name__ == "__main__":
    count_competitors_upcoming_comps(verify_entries=verify_entries)
