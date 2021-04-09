
++++Scraper funda.nl and domain.com.ua++++


Install script:
1. Install Python 3.7+
2. Open terminal(Linux,Mac) or cmd (Windows)
3. Go to the folder "PropertyParsing" using "cd" command in terminal
4. Install libs in requirments.txt (pip3 install -r requirments.txt)
5. Install Chrome latest version if you have not
6. Create new profile in Chrome(right corner upsite) and authorize in Gmail.
7. Go to chrome://version/ in Chrome and copy Profile Path
8. Insert Profile Path in config.txt
6. Install ChromeDriver (6.1 - 6.2)
6.1 brew cask install chromedriver
6.2 brew tap homebrew/cask


Script commands:
--help / -h
--url / -u If you want to scripe 1 certain zone, type the url: python3 main.py --url "YOURURL"
--file / -f File where you want to save your data: python3 main.py --url "YOURURL" --file out.csv (output.csv is default file)
--clear / -cc Clear .cvs file: python3 main.py -cc "FILENAME"

Scrape funda.nl:
Open Chrome and open funda.nl then decide a repactcha and close the browser
python3 main.py -u "funda.nl/.../..."
Then Chrome will be opened.
