from selenium.webdriver.common.by import By


class Result:
    """
    Result class.

    self.raw_text       : raw text from the individual results.o2cm.com page for that event
    self.link           : link from the individual results.o2cm.com page for that event
    self.placement      : what place the person got in the event
    self.driver         : web object from selenium
    self.level          : what level the event was
    self.style          : what style the event was
    self.dances_string  : ,-delimited list of dances. Not calculated until calculateDances() is called
    self.dances         : list of dances in the result
    """

    def __init__(self, result, driver, debug_reject_headers=0):
        """
        Initialize the Result class.

        Inputs:
            result - html element object from selenium
            driver - web object from selenium
            debug_reject_headers - 1 to print dances (headers) that the program doesn't know what to do with
        """
        self.debug_reject_headers = debug_reject_headers
        self.raw_text = result.get_attribute("innerHTML")
        self.link = result.get_attribute("href")
        self.placement = int(self.raw_text.split(")")[0])
        self.driver = driver
        self.level = self._getLevel()
        self.style = self._getStyle()

        self.dances_string = "Not yet calculated"

    def __repr__(self):
        """
        When the Result object is printed, this is what is returned
        """
        return f"#{self.placement} in {self.level} {self.style} {self.dances_string}."

    def _which_ele_is_in_str(self, list, string):
        """
        Returns the first element from list that is in string.
        """
        return next((x for x in list if x in string), None)

    def _lists_both_have_ele_in_str(self, list1, list2, string):
        """
        Returns if string is in both list1 and list2.
        """
        return self._which_ele_is_in_str(list1, string) and self._which_ele_is_in_str(
            list2, string
        )

    def _getStyle(self):
        """
        Gets the style from the result.
        """
        result_text = self.raw_text.lower()
        styles_list = ["smooth", "standard", "rhythm", "latin"]

        style = self._which_ele_is_in_str(styles_list, result_text)
        if style:
            return style

        latin_rhythm_dance_list = [
            "cha",
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
        if self._lists_both_have_ele_in_str(
            ballroom_dance_list, american_list, result_text
        ):
            return "smooth"
        elif self._lists_both_have_ele_in_str(
            latin_rhythm_dance_list, american_list, result_text
        ):
            return "rhythm"
        elif self._lists_both_have_ele_in_str(
            latin_rhythm_dance_list, international_list, result_text
        ):
            return "latin"
        elif self._lists_both_have_ele_in_str(
            ballroom_dance_list, international_list, result_text
        ):
            return "standard"
        elif self.debug_reject_headers:
            print(f"{result_text}: has no valid style.")

        return None

    def _getLevel(self):
        result_text = self.raw_text.lower()
        champ_list = ["champ", "championship"]
        prechamp_list = ["pre-champ", "cre-championship", "prechamp", "prechampionship"]
        novice_list = ["novice", "open"]
        gold_list = ["gold", "advanced"]
        silver_list = ["silver", "intermediate"]
        bronze_list = ["bronze", "beginner", "syllabus", "other"]
        newcomer_list = ["newcomer"]

        # novice at the end because "open" could be in the names of other events
        # prechamp before champ because prechamp has champ in the name
        levels_list = [
            prechamp_list,
            champ_list,
            gold_list,
            silver_list,
            bronze_list,
            newcomer_list,
            novice_list,
        ]

        # Returns the first element from the level list that is matched
        for lst in levels_list:
            if self._which_ele_is_in_str(lst, result_text):
                return lst[0]
        if self.debug_reject_headers:
            print(f"{result_text}: has no valid level.")

        return None

    def _getDances(self):
        """
        Returns a list of what dances are in the event.
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

        # If the event name has a dance in it, return the dance
        dance = self._which_ele_is_in_str(dance_list, result_text)
        if dance:
            return [dance]

        # If not, then it's probably because it's a multi-dance event
        # Click in to the event
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(self.link)

        # Pull all the table headers
        headers = self.driver.find_elements(By.CLASS_NAME, "h3")
        headers_text = [header.get_attribute("innerHTML").lower() for header in headers]
        # See which headers have names in the dance_list
        dances = list(filter(lambda x: x in headers_text, dance_list))

        # Add jank becuase viennese waltz sometimes has a different name
        if "viennese waltz" in headers_text:
            dances.append("v. waltz")

        # Print out any headers we haven't somehow haven't accounted for
        if self.debug_reject_headers:
            reject_dances = []
            for header in headers_text:
                if (
                    header not in dance_list
                    and header != "summary"
                    and header != "viennese waltz"
                ):
                    reject_dances.append(header)
            if reject_dances:
                print(f"{result_text}: invalid dance(s) {reject_dances}")

        # Close results page
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        if dances:
            return dances

        return [""]

    def calculateDances(self):
        """
        Call this to calculate the dances in the event.
        """
        self.dances = self._getDances()
        self.dances_string = ", ".join(self.dances)
