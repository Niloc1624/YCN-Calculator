# YCN-Calculator
This is a YCN point calculator that scrapes from https://results.o2cm.com/. It is very janky, probably isn't right, and is horribly inelegant. BUT, it's better than nothing. Points are calculated according to MIT's system: http://ballroom.mit.edu/index.php/ycn-proficiency-points/

If you want to use this to check a dancer's YCN points you have these options:
- It's alive! Navigate to ballroom-calc.azurewebsites.net, note that this website may take up to 2 minutes to load or to calulate points for a dancer. It's a slow website and currently doesn't give much feedback that it's loading, so give it a minute or two to calculate and display the points.
- Run app.py on your local machine and open the localhost link it outputs in your browser of choice.
- Set manual=1 in webScraper.py, put the first and last names there, and run webScrapyer.py. Outputs will be printed to terminal.

If you want to use this to check a given comp for dancers who have placed out of events they've registered for (this is still pretty experimental and hasn't been tested much):
- Set manual=1 in compChecker.py, put the entries website code (should be 3 letters) in comp_code, and run compChecker.py on your local machine. Outputs will be printed to terminal.  Make sure in webScaper.py, manual=0. Not sure why exactly but for some reason compChecker.py really screws up if manual=1 in webscraper.py.

If you want to check how many competitors there are for every competition available on https://events.o2cm.com/ (not including entrants starting with "TBA" (case-sensitive) and not including duplicates):
- Run countCompetitorsAllComps.py on your local machine. Outputs will be printed to terminal.

Modules used
- beautifulsoup4
- pandas
- flask
- requests
- gunicorn

Since https://ballroom.union.rpi.edu/calculator is back up and running again, my next steps will be:
- Test compChecker.py more
- Make compChecker.py available on ballroom-calc.azurewebsites.net
- Make a database?
- Add features to retroactively see how many points a dancer earned between two dates