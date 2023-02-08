import requests
from bs4 import BeautifulSoup
from utils import which_ele_is_in_str, lists_both_have_ele_in_str
from eventClass import Event


class Result(Event):
    """
    Class for results.

    self.dancer_name    : dancer's name for this result in form "first_name last_name"
    self.link           : link from the individual results.o2cm.com page for that event
    self.placement      : what place the person got in the event
    self.dances_string  : (overrides Event) ,-delimited list of dances

    from Event class:
    self.raw_text       : raw text from the individual results.o2cm.com page for that event
    self.level          : what level the event was
    self.style          : what style the event was
    self.dances         : list of dances in the result
    self.debug_reject_headers: 1 to print out things we don't know what to do with
    """

    def __init__(self, result, dancer_name, debug_reject_headers=0):
        """
        Initialize the Result class.

        Inputs:
            result : html element object from beautiful soup
            dancer_name : dancer's name in form "first_name last_name"
            debug_reject_headers : 1 to print dances (headers) that the program doesn't know what to do with
        """
        self.dancer_name = dancer_name
        self.debug_reject_headers = debug_reject_headers
        self.link = result.get("href")
        super().__init__(result, debug_reject_headers)
        self.placement = int(self.raw_text.split(")")[0])
        self.dances_string = ", ".join(self.dances)

    def __repr__(self):
        """
        When the Result object is printed, this is what is returned
        """
        return f"#{self.placement} in {self.level.title()} {self.style.title()} {self.dances_string.title()}."

    def _getDances(self):
        """
        Returns a list of what dances are in the event.
        Have to refactor from the Event class because this isn't the title on entries.o2cm.com,
        but rather the results from results.o2cm.com/individual
        """
        result_text = self.raw_text.lower()
        dance_list = [
            "v. waltz",
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
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, "html.parser")

        # Make sure dancer actually made the final (may not be the case if <6 couples in final)
        if self.dancer_name not in soup.get_text():
            return [""]

        # Pull all the table headers
        headers = soup.select(".h3")
        headers_text = [header.text.lower() for header in headers]

        # See which headers have names in the dance_list and which don't
        dances = []
        reject_dances = []
        for header_text in headers_text:
            dance = which_ele_is_in_str(dance_list, header_text)
            if dance:
                dances.append(dance)
            # Add jank becuase viennese waltz sometimes has a different name
            elif "viennese waltz" in headers_text:
                dances.append("v. waltz")
            elif self.debug_reject_headers and header_text != "summary":
                reject_dances.append(header_text)

        # Print out any headers we haven't somehow haven't accounted for
        if reject_dances:
            print(f"{result_text}: invalid dance(s) {reject_dances}")

        if dances:
            return dances

        return [""]
