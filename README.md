# YCN-Calculator
This is a YCN point calculator that scrapes from https://results.o2cm.com/. Points are calculated according to MIT's system: http://ballroom.mit.edu/index.php/ycn-proficiency-points/

If you want to use this to check a dancer's YCN points you have these options:
- It's alive! Navigate to https://ballroom-calc.streamlit.app/
- Set manual=1 in webScraper.py, put the first and last names there, and run webScraper.py. Outputs will be printed to terminal.

If you want to use this to check a given comp for dancers who have placed out of events they've registered for:
- Put the entries website code (should be 3 letters) in comp_code, and run compChecker.py on your local machine. Outputs will be printed to terminal. If you want to check only one dancer at one comp, then you can also fill out first_name and last_name.

If you want to plot how many competitors there have been for a given competition over the years available on https://results.o2cm.com/ (not including entrants starting with "TBA" (case-sensitive) and not including duplicates):
- Run plotCompetitorsPastComps.py on your local machine. Outputs will be displayed using matplotlib. Has a parameter for only counting competitors with at least one event, but that makes it take much longer.

If you want to check how many competitors there are for every competition available on https://events.o2cm.com/ (not including entrants starting with "TBA" (case-sensitive) and not including duplicates):
- Run countCompetitorsUpcomingComps.py on your local machine. Outputs will be printed to terminal.

If you want to check how many competitors there have been for a given competition over the years available on https://results.o2cm.com/ (not including entrants starting with "TBA" (case-sensitive) and not including duplicates):
- Run countCompetitorsPastComps.py on your local machine. Outputs will be printed to terminal.

Modules used (probably an inaccurate list)
- beautifulsoup4
- pandas
- flask
- requests
- gunicorn
- gspread
- matplotlib


Since https://ballroom.union.rpi.edu/calculator is back up and running again, my next steps will be:
- Give https://ballroom-calc.azurewebsites.net/ feedback to the user that it's actually doing something
- Make compChecker.py available on https://ballroom-calc.azurewebsites.net/
- Make a database
- Add features to retroactively see how many points a dancer earned between two dates
- Add feature to see ineligible entries for previous competitions
