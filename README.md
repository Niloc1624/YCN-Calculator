# YCN-Calculator
This is a YCN point calculator that scrapes from https://results.o2cm.com/. It is very janky, probably isn't right, and is horribly inelegant. BUT, it's better than nothing.

If you want to use this you have two options:
- Run website.py on your local machine and open the localhost link it outputs in your browser of choice
- Set manual=1 in webScraper.py, put the first and last names there, and run webScrapyer.py. Outputs will be printed to screen

Modules used
- beautifulsoup4
- pandas
- flask

Since https://ballroom.union.rpi.edu/calculator is back up and running again, my next steps will be:
- Add ability to check a given competition for people who are registered for levels they've pointed out of
- Make this available on a website somehow (like fly.io)
