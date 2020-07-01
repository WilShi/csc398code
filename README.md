# CSC398 Scraping Webpages Project
The Software is for pulling names and contextual information from pages in `Information Security conferences`.

This software calls `Beautiful Soup 4`, `requests` and `pandas` library to parse the HTML code of the website, and automatically recognizes the navigation bar of the website to analyze pages that may contain names. After finding a website that may contain a name, it automatically crawls the names and related information on the page. After the software confirms to crawl the webpage information of the year, it will automatically find the previous conference websites of the conference, and crawl the information year by year (5-7 years). 

The current crawling targets of the software are three conferences:

`IEEE European Symposium on Security and Privacy` (http://www.ieee-security.org/TC/EuroSP2020/index.html)

`IEEE Symposium on Security and Privacy` (http:/ /www.ieee-security.org/TC/SP2020/)

`ACM CCS` (https://www.sigsac.org/ccs/CCS2020/#)

The software consists of two python programs: `scraping_webpages.py` and `analysis.py`. 

`scraping_webpages.py` will automatically crawl the aforementioned webpage information, and when the result is obtained, it will print the person’s name and information to the terminal command line. 

`analysis.py` is mainly used to analyze the data obtained by `scraping_webpages.py`, but there are also files that can be output in CSV and txt format using `analysis.py`. It would make the results of `scraping_webpages.py` be saved easier.

# How to install
Clone `scraping_webpages.py` and `analysis.py` from git hub

`Requisites`: Need Python 3.0 or later to run software

`Install Beautiful Soup 4`: `pip install beautifulsoup4` (Some `pip` may be named `pip3` respectively if you’re using Python 3)
recent version of Debian or Ubuntu Linux : `apt-get install python3-bs4`

`Install requests`: `pip install requests` (Some `pip` may be named `pip3` respectively if you’re using Python 3)

`Install pandas`: `sudo apt-get install python3-pandas` (pip might cause errors)

# How to use
(In terminal)
`scraping_webpages.py`: `python3 scraping_webpages.py`  -> print all names and information

(In terminal)
`analysis.py`: `python3 analysis.py` `txt/csv` (Optional arguments) -> creat txt or csv file, if no argument start analyze the data

