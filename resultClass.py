from selenium.webdriver.common.by import By


class Result:
    def __init__(self, result, driver, debug_reject_headers=0):
        self.raw_text = result.get_attribute("innerHTML")
        self.link = result.get_attribute("href")
        self.placement = int(self.raw_text.split(")")[0])
        self.driver = driver
        self.level = self._getLevel()
        self.style = self._getStyle()

        self.dances_string = "Not yet calculated"
        self.debug_reject_headers = debug_reject_headers

    def __repr__(self):
        return f"Placed #{self.placement} in {self.level} {self.style} {self.dances_string}."

    def _which_ele_is_in_str(self, list, string):
        return next((x for x in list if x in string), None)

    def _lists_both_have_ele_in_str(self, list1, list2, string):
        return self._which_ele_is_in_str(list1, string) and self._which_ele_is_in_str(
            list2, string
        )

    def _getStyle(self):
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
            "swing",
            "mambo",
            "bolero",
        ]
        ballroom_dance_list = ["waltz", "tango", "foxtrot", "quickstep"]
        american_list = ["am.", "amer.", "american"]
        international_list = ["intl", "international"]

        if self._lists_both_have_ele_in_str(
            ballroom_dance_list, american_list, result_text
        ):
            return "smooth"
        elif self._lists_both_have_ele_in_str(
            ballroom_dance_list, international_list, result_text
        ):
            return "standard"
        elif self._lists_both_have_ele_in_str(
            latin_rhythm_dance_list, american_list, result_text
        ):
            return "rhythm"
        elif self._lists_both_have_ele_in_str(
            latin_rhythm_dance_list, international_list, result_text
        ):
            return "latin"

        return None

    def _getLevel(self):
        result_text = self.raw_text.lower()
        champ_list = ["champ", "championship"]
        prechamp_list = ["pre-champ", "cre-championship", "prechamp", "prechampionship"]
        novice_list = ["novice", "open"]
        gold_list = ["gold", "advanced"]
        silver_list = ["silver", "intermediate"]
        bronze_list = ["bronze", "beginner", "syllabus"]
        newcomer_list = ["newcomer"]

        # novice at the end because "open" could be in the names of other events
        levels_list = [
            champ_list,
            prechamp_list,
            gold_list,
            silver_list,
            bronze_list,
            newcomer_list,
            novice_list,
        ]

        for lst in levels_list:
            match = self._which_ele_is_in_str(lst, result_text)
            if match:
                return lst[0]

    def _getDances(self):
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
            "swing",
            "mambo",
            "bolero",
        ]

        dance = self._which_ele_is_in_str(dance_list, result_text)
        if dance:
            return [dance]

        ##check what dances it is for multidance events

        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(self.link)

        headers = self.driver.find_elements(By.CLASS_NAME, "h3")
        headers_text = [header.get_attribute("innerHTML").lower() for header in headers]
        dances = list(filter(lambda x: x in headers_text, dance_list))

        if "viennese waltz" in headers_text:
            dances.append("v. waltz")

        if "intl. paso doble" in headers_text:
            dances.append("paso doble")

        if self.debug_reject_headers:
            reject_dances = []
            for header in headers_text:
                if (
                    header not in dance_list
                    and header != "summary"
                    and header != "viennese waltz"
                    and header != "intl. paso doble"
                ):
                    reject_dances.append(header)
            if reject_dances:
                print(reject_dances)

        # Close results page
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        if dances:
            return dances

        return ["unknown dance(s)"]

    def calculateDances(self):
        self.dances = self._getDances()
        self.dances_string = ", ".join(self.dances)
