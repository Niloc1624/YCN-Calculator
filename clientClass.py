import os
import datetime
import gspread
from google.oauth2.service_account import Credentials
from eventClass import Event
from resultClass import Result

class Client:
    def __init__(self):
        """
        Initializes the client for compChecker to use for storing/checking 
        results and opens the spreadsheet used as the database for that
        """
        #authenticate with Google's API using credentials file
        creds_path = os.path.join(os.getcwd(), 'Credentials', 'credentials.json')
        creds = Credentials.from_service_account_file(creds_path)
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key('1d-dE2idytfW8E_rfIs2lsrO_OQSZcgKjXr8zLSr0reg')
        #variables to access the Raw_Data and Metadata worksheets respectively
        self.raw_data = self.spreadsheet.worksheet('0')
        self.metadata = self.spreadsheet.worksheet('1806068062')

    def storeResult(self, result):
        """
        Store the result appended to the end of the spreadsheet 
        Doesn't call updateMetadata itself, even though it changes the 
        spreadsheet--that's left to the caller to avoid unnecessary wait time
        by updating it at the end instead of with every change.
        (I imagine Google is going to be much more responsive than O2CM, but
        why take the chance. They did just lay off 12k.)
        """

        #split dancer name for storage in separate columns
        first_name, last_name = [result.dancer_name.split(' ')[i] for i in (0, 1)]
        level = result.level
        style = result.style
        dances = result.getDances()
        date = result
        num_points = result
        comp_code = result
        self.client.flush()

    def checkResult(self, result):
        """
        Check to see if the passed result is newer than the dancer's most recent
        entry
        """
        #TODO
        raise NotImplementedError


    def updateMetadata(self):
        """
        Updates the Metadata worksheet with the current date/time
        """
        self.metadata.update('A2', datetime.now())
        self.client.flush()
