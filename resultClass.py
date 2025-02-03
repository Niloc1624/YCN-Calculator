from eventClass import Event
from utils import (
    which_ele_is_in_str,
    get_result_from_link,
    streamlit_or_print,
    get_comp_code_from_url,
)


class Result(Event):
    """
    Class for results.

    self.first_name     : dancer's first name for this result
    self.last_name      : dancer's last name for this result
    self.dancer_name    : dancer's name for this result in form "first_name last_name"
    self.date           : date of the event stored with date object
    self.competition_name: name of the competition with the date from results.o2cm.com/individual
    self.o2cm_results_cache_dict: dictionary of results from the cache
    self.link           : link from the individual results.o2cm.com page for that event
    self.placement      : what place the person got in the event
    self.dances_string  : (overrides Event) ,-delimited list of dances
    self.comp_code       : 3-letter competition code for the event
    ## self.comp_code_with_year: 3-letter competition code for the event with the 2-digit year ## Needs to be fixed
    self.num_rounds     : number of rounds in the event
    self.is_new_result  : True if the result is new, False if it was cached

    from Event class:
    self.raw_text       : raw text from the individual results.o2cm.com page for that event
    self.level          : what level the event was
    self.style          : what style the event was
    self.dances         : list of dances in the result (note that _getDances() is overridden in this class)
    self.debug_reject_headers: 1 to print out things we don't know what to do with
    self.streamlit_mode : 1 to print to streamlit, 0 to print to console
    self.expander       : Expander object for Streamlit. Default is None
    self.valid          : 1 if the event is valid, 0 if it is not
    self.invalid_text   : reasoning for invalidity
    """

    def __init__(
        self,
        result,
        first_name,
        last_name,
        date,
        competition_name,
        o2cm_results_cache_dict,
        debug_reject_headers=0,
        streamlit_mode=False,
        expander=None,
    ):
        """
        Initialize the Result class.

        Inputs:
            result : html element object from beautiful soup
            first_name : dancer's first name
            last_name : dancer's last name
            date : date of the event stored with date object
            debug_reject_headers : 1 to print dances (headers) that the program doesn't know what to do with
        """
        self.first_name = first_name
        self.last_name = last_name
        self.dancer_name = first_name + " " + last_name
        self.date = date
        self.competition_name = competition_name
        self.o2cm_results_cache_dict = o2cm_results_cache_dict
        self.debug_reject_headers = debug_reject_headers
        self.link = result.get("href")
        if self.link.startswith("http:"):
            self.link = "https:" + self.link[5:]
        super().__init__(result, debug_reject_headers, streamlit_mode, expander)
        self.placement = int(self.raw_text.split(")")[0])
        self.dances_string = ", ".join(self.dances)
        self.comp_code = get_comp_code_from_url(self.link)
        # self.comp_code_with_year = get_comp_code_from_url(self.link, include_year=True) # Needs to be fixed

    def __repr__(self):
        """
        When the Result object is printed, this is what is returned
        """
        if self.valid:
            return f"#{self.placement} in {self.level.title()} {self.style.title()} {self.dances_string.title().strip()}."
        else:
            return f"{self.invalid_text}"

    def _getDances(self):
        """
        Returns a list of what dances are in the event.
        Have to refactor from the Event class because this isn't the title on entries.o2cm.com,
        but rather the results from results.o2cm.com/individual
        """
        result_text = self.raw_text.lower()
        dance_list = [
            "v. waltz",
            "viennese waltz",  # this second vwaltz is jank but is addressed later
            "waltz",
            "tango",
            "foxtrot",
            "quickstep",
            "cha cha",
            "rumba",
            "samba",
            "jive",
            "paso doble",
            "swing",
            "mambo",
            "bolero",
        ]

        # Click in to the event
        o2cm_result_info_dict, self.o2cm_results_cache_dict, is_new_result = (
            get_result_from_link(self.link, self.o2cm_results_cache_dict)
        )
        # Add whether the result was new or not and the number of rounds
        self.is_new_result = is_new_result
        self.num_rounds = o2cm_result_info_dict["num_rounds"]

        # If the result page doesn't exist, quit early
        if o2cm_result_info_dict["dancer_names"] == []:
            streamlit_or_print(
                f"{result_text}: 0 dancers found (likey due to 500 error)",
                self.streamlit_mode,
                self.expander,
            )
            return [""]

        # Make sure dancer actually made the final (may not be the case if <6 couples in final)
        if self.dancer_name.casefold() not in [
            name.casefold() for name in o2cm_result_info_dict["dancer_names"]
        ]:
            return [""]

        # See which headers have names in the dance_list and which don't
        dances = []
        reject_dances = []
        for header_text in o2cm_result_info_dict["headers_text"]:
            dance = which_ele_is_in_str(dance_list, header_text)
            # Add jank becuase viennese waltz sometimes has a different name
            if dance == "viennese waltz":
                dances.append("v. waltz")

            elif dance:
                dances.append(dance)
            elif self.debug_reject_headers and header_text != "summary":
                reject_dances.append(header_text)

        # Print out any headers we haven't somehow haven't accounted for
        if reject_dances:
            streamlit_or_print(
                f"{result_text}: invalid dance(s) {reject_dances}",
                self.streamlit_mode,
                self.expander,
            )

        if dances:
            return dances

        return [""]
