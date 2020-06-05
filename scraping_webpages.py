import sys
import requests
import re
from bs4 import BeautifulSoup

def make_soup(url):
    html = requests.get(url) #Creat html file by url
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def get_link(soup): #return all html code in navigation bar as a list
    links = []
    if (soup.find_all(re.compile('^nav')) != []):
        # Find all navagtion links in the webpage
        for nav in soup.find_all(re.compile('^nav')):
            a = nav.find_all('a') #Find all 'a' tag
            for link in a:
                if (link not in links):
                    # print(link.get('href')) #Print all link
                    links.append(link)
    else:
        for nav in soup.find_all(class_=re.compile('^nav')):
            a = nav.find_all('a') #Find all 'a' tag
            for link in a:
                if (link not in links):
                    # print(link.get('href')) #Print all link
                    links.append(link)
    return links

def get_speaker_page(links): #return speaker page link
    for i in links:
        if (i.find(text=re.compile('[Ss]peak')) != None):
            link = i.get('href')
            return link

def get_info(url):
    soup = make_soup(url)
    all_h = soup.find_all('div')
    return all_h

if __name__ == '__main__':
    url=sys.argv[1]

    # html = requests.get(url) #Creat html file by url
    soup = make_soup(url)

    links = get_link(soup)

    speaker_page_url = get_speaker_page(links)
    print(speaker_page_url)

    hs = get_info(speaker_page_url)
    for i in hs:
        print(i.text)

    