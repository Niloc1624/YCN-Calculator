import sqlite3
import resultClass

class Database:
    """
    Database object associated with a connection to a particular database file
    I'm not sure if this would be better as a module or something
    but as best as I can figure, arranging it as an object works?

    self.cx: the connection object for the file
    self.cu: the cursor object on self.cx
    self.dancer_id: holds the current highest id for the dancer table 
    self.event_id: holds the current highest id for the event table
    """
    def __init__(self, filename):
        """
        Initializes Database object for compChecker to use for storing/checking 
        results 

        filename: filename of the database file to open (presumably "YCN.db"
        but hey who doesn't like extensibility)
        """
        #open connection object
        self.cx = sqlite3.connect(filename)
        #open cursor object on connection
        self.cu = self.cx.cursor()
        self.dancer_id = self.cu.execute("SELECT MAX(ID) FROM dancers")
        self.event_id = self.cu.execute("SELECT MAX(ID) FROM events")

    def addResult(self, result):
        """
        Adds provided result to YCN.db.
        """



    def isOutdated(self, result):
        """
        Compares result against the most recent stored one for its dancer.
        Returns true if result is newer, false otherwise.
        """


    def findDancer(self, dancer):
        """
        finds dancer by first+last name and returns id 
        returns 0 if not found
        """

    def findEvent(self, event):
        """
        finds event by level/style/dances and returns id
        returns 0 if not found
        """

    def addEvent(self, event):
        """
        adds event and returns its id
        """
        level = event.level 
        style = event.style
        dances = event.dances_string
        self.cu.execute("INSERT INTO events(level, style, dances)")

    def close(self):
        """
        closes connection and flushes changes to disk
        """
        self.cx.close()
    