from utils import which_ele_is_in_str, lists_both_have_ele_in_str, streamlit_or_print


class Event:
    """
    Class for an event

    self.raw_text       : raw text from entries.o2cm.com for that event
    self.debug_reject_headers: 1 to print out things we don't know what to do with
    self.streamlit_mode : 1 to print to streamlit, 0 to print to console
    self.level          : what level the event was
    self.style          : what style the event was
    self.dances         : list of dances in the result
    self.dances_string  : capital letters for each dance (example: WTFQ)
    """

    def __init__(
        self, event, debug_reject_headers=False, streamlit_mode=False, expander=None
    ):
        """
        Initializes the Event class

        event: html element from beautiful soup
        debug_reject_headers: 1 to print out things we don't know what to do with
        streamlit_mode: 1 to print to streamlit, 0 to print to console
        expander: Expander object for Streamlit. Default is None.
        """
        self.raw_text = event.text
        self.debug_reject_headers = debug_reject_headers
        self.streamlit_mode = streamlit_mode
        self.expander = expander
        self.level = self._getLevel()
        self.style = self._getStyle()
        self.dances = self._getDances()
        self.dances_string = ""
        for dance in self.dances:
            if dance != "":
                self.dances_string += dance[0].upper()

    def __repr__(self):
        """
        When the Event object is printed, this is what is returned
        """
        return f"{self.level.title()} {self.style.title()} {self.dances_string}"

    def _getLevel(self):
        """
        Gets the level for the event.
        """
        result_text = self.raw_text.lower()
        champ_list = ["champ", "championship"]
        prechamp_list = ["pre-champ", "pre-championship", "prechamp", "prechampionship"]
        novice_list = ["novice"]
        gold_list = ["gold", "advanced"]
        silver_list = ["silver", "intermediate"]
        bronze_list = ["bronze", "beginner", "other"]
        newcomer_list = ["newcomer"]

        syllabus_list = ["syllabus"]
        open_list = ["open"]

        # open at the end because "open" could be in the names of other events
        # prechamp before champ because prechamp has champ in the name
        levels_list = [
            prechamp_list,
            champ_list,
            gold_list,
            silver_list,
            bronze_list,
            newcomer_list,
            novice_list,
            syllabus_list,
            open_list,
        ]

        # Returns the first element from the level list that is matched
        for lst in levels_list:
            if which_ele_is_in_str(lst, result_text):
                return lst[0]
        if self.debug_reject_headers:
            streamlit_or_print(
                f"{result_text}: has no valid level.",
                self.streamlit_mode,
                self.expander,
            )

        return None

    def _getStyle(self):
        """
        Gets the style from the event.
        """
        result_text = self.raw_text.lower()
        styles_list = ["smooth", "standard", "rhythm", "latin"]

        style = which_ele_is_in_str(styles_list, result_text)
        if style:
            return style

        latin_rhythm_dance_list = [
            "cha cha",
            "rumba",
            "samba",
            "jive",
            "paso doble",
            "swing",
            "mambo",
            "bolero",
        ]
        ballroom_dance_list = ["waltz", "tango", "foxtrot", "quickstep", "ballroom"]
        american_list = ["am.", "amer.", "american"]
        international_list = ["intl", "international", "ballroom"]

        # Standard at the end because sometimes standard is called ballroom
        if lists_both_have_ele_in_str(ballroom_dance_list, american_list, result_text):
            return "smooth"
        elif lists_both_have_ele_in_str(
            latin_rhythm_dance_list, american_list, result_text
        ):
            return "rhythm"
        elif lists_both_have_ele_in_str(
            latin_rhythm_dance_list, international_list, result_text
        ):
            return "latin"
        elif lists_both_have_ele_in_str(
            ballroom_dance_list, international_list, result_text
        ):
            return "standard"
        elif self.debug_reject_headers:
            streamlit_or_print(
                f"{result_text}: has no valid style.",
                self.streamlit_mode,
                self.expander,
            )

        return None

    def _getDances(self):
        """
        Returns a list of what dances are in the event.
        """
        dances_list = [
            "waltz",
            "tango",
            "v. waltz",
            "foxtrot",
            "quickstep",
            "cha cha",
            "rumba",
            "paso doble",
            "samba",
            "jive",
            "mambo",
            "bolero",
            "swing",
        ]
        dances_dictionary = {}

        for dance in dances_list:
            if dance[0] != "s":
                dances_dictionary[dance[0]] = dance

        result_text = self.raw_text.lower()
        event_dance_letters = result_text[
            result_text.rfind("(") + 1 : result_text.rfind(")")
        ]

        dances = []
        for dance_letter in event_dance_letters:
            if dance_letter == "s":
                if self.style == "latin":
                    dances.append("samba")
                elif self.style == "rhythm":
                    dances.append("swing")
            elif dance_letter in dances_dictionary:
                dances.append(dances_dictionary[dance_letter])
            elif self.debug_reject_headers:
                streamlit_or_print(
                    f"{dance_letter}: not a valid dance letter in {event_dance_letters}.",
                    self.streamlit_mode,
                    self.expander,
                )

        if dances:
            return dances

        return [""]
