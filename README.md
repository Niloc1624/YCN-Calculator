# YCN-Calculator
This is a YCN point calculator that scrapes from https://results.o2cm.com/. It is very janky, probably isn't right, and is horribly inelegant. BUT, it's better than nothing.

If you want to use this to check a dancer's YCN points you have two options:
- Run website.py on your local machine and open the localhost link it outputs in your browser of choice
- Set manual=1 in webScraper.py, put the first and last names there, and run webScrapyer.py. Outputs will be printed to screen

If you want to use this to check a given comp for dancers who have placed out of events they've registered for (this is still pretty experimental and hasn't been tested much):
- Set manual=1 in compChecker.py, put the entries website in there, and run compChecker.py. Outputs will be printed to screen

Modules used
- beautifulsoup4
- pandas
- flask

Since https://ballroom.union.rpi.edu/calculator is back up and running again, my next steps will be:
- Test compChecker.py more
- Make this available on a website somehow (like fly.io)
