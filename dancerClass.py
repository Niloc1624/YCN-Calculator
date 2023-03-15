from webScraper import webScraper


class Dancer:
    """
    Class for dancers
    self.first_name : first name of dancer
    self.last_name : last name of dancer
    self.full_name : dancer's name in format "first_name last_name"
    """

    def __init__(self, dancer_name, format):
        """
        Initialize the Dancer class

        format : determines how dancer is expected
                 0 : "last_name, first_name"
                 1 : "first_name last_name"
        dancer_name : name of dancer as beautiful soup element
        """
        raw_text = dancer_name.text

        if format:
            # assume no spaces in first name
            self.first_name = raw_text.split(" ", 1)[0]
            self.last_name = raw_text.split(" ", 1)[1]
            self.full_name = raw_text
        else:
            # rsplit because of people with commas in last name
            self.first_name = raw_text.rsplit(", ", 1)[1]
            self.last_name = raw_text.rsplit(", ", 1)[0]
            self.full_name = self.first_name + " " + self.last_name

    def __repr__(self):
        """
        Output when Dancer class is printed
        """
        return f"{self.first_name} {self.last_name}"

    def calculate_points(self, show_work=1, debug_reject_headers=1):
        """
        calls webScraper() on the dancer, takes a while
        """
        self.styles_data_dict = webScraper(
            self.first_name, self.last_name, 1, show_work, debug_reject_headers
        )

    def get_points(self, style, level, dance):
        """
        Returns the number of points a dancer has for a given style, level, and dance (strings)
        """
        # You have to place out of gold to place out of syllabus
        if level.lower() == "syllabus":
            level = "gold"
        # You have to place out of champ to place out of syllabus
        if level.lower() == "open":
            level = "champ"
        return self.styles_data_dict[style.lower()][level][dance.lower()][0]
