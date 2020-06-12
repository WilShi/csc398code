import sys
import requests
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
from itertools import groupby
from nltk.tree import Tree

def make_soup(url):
    html = requests.get(url) #Creat html file by url
    soup = BeautifulSoup(html.text, 'lxml')
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

def get_committee(links):
    link = []
    for i in links:
        if (i.find(text=re.compile('[Cc]ommittee')) != None):
            link.append(i.get('href'))
    return link

def get_pages(links):
    pages=[]
    for i in links:
        if (i.find(text=re.compile('[Pp]revious')) == None and\
             i.find(text=re.compile('\d{4}')) == None):
            link = i.get('href')
            pages.append(link)
    return pages

def get_previous_years(links):
    pages=[]
    for i in links:
        if (i.find(text=re.compile('[Pp]revious')) != None or\
             i.find(text=re.compile('\d{4}')) != None):
            link = i.get('href')
            if (link[:link.find('.')] != 'index'):
                pages.append(link)
    return pages

def get_names(url):
    soup = make_soup(url)
    if ('steering' in url):
        # title = soup.find('h1')
        # print('Title: ' + title.text + '\n')
        body = soup.find_all('tr')
        for i in body:
            info = ' '.join(i.text.split())
            print(info + '\n')
        return None

    if ('accepted' in url):
        na = soup.find_all('p', class_='', style='')
        for i in na:
            # get_namesAndOrg(i.text)
            info = i.text
            # info = info.replace('and', ',')
            info = info.replace('; ', '\n\n').lstrip()
            info = info[:info.find('(')].replace(', ', info[info.find('(')-1:]\
                + '\n\n') + info[info.find('('):]
            print(info + '\n')
            # print("===================================")
        if (url[-3:] == 'php'):
            # print("===================================")
            brs = soup.find_all('div', class_='list-group-item')
            for br in brs:
                info = ' '.join(str(br).split())
                tag = re.findall('<br/>.*</div>', info)[0]
                tag = re.sub(r'<[^>]*>', '', tag).lstrip()
                # tag = tag.replace(', ', '\n\n').lstrip()
                if ('2019' not in url):
                    tag = tag.replace('), ', ')\n\n').lstrip()
                else:
                    tag = tag.replace('; ', '\n\n').lstrip()
                tag = tag[:tag.find('(')].replace(', ', tag[tag.find('(')-1:]\
                     + '\n\n') + tag[tag.find('('):]
                # tag = tag[:tag.find('(')].replace(', ', '\n\n') + tag[tag.find('('):]
                print(tag + '\n')
                # print("===================================")
        return None
    
    if ('program.php' in url or '2016/committee-organizing' in url):
        body = soup.select('tr')
        ct=0
        count=0
        for b in body:
            if ('Members' in b.text):
                ct=1
                # break
            elif (ct == 0):
                info = b.text.replace('\n', ' ').lstrip()
                print(info + '\n')
            else:
                info = ' '.join(b.text.split())
                if (info == ''):
                    count=0
                elif (count%2 == 0):
                    print(info, end=', ')
                    count+=1
                else:
                    print(info + '\n')
                    count=0
        return None

    # title = soup.find('h1')
    # print('Title: ' + title.text + '\n')
    body = soup.select('td')
    count=0
    for i in body:
        info = ' '.join(i.text.split())
        if ('Chairs' in info or 'Members' in info or 'Chair' in info or 'Organizers' in info\
            or 'Treasurer' in info):
            print('Position: ' + info)
            count=0
        elif (info == ''):
            count=0
        elif (':' in info):
            None
        elif ('Workshop' in info or 'events' in info):
            break
        elif (count%2 == 0):
            print(info, end=', ')
            count+=1
        else:
            print(info + '\n')
            count=0

def get_namesAndOrg(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)

    name_list = []

    for i in sentt:
        # print(type(i))
        if (type(i) == tuple):
            sentt.remove(i)
    # print(sentt)

    ne_in_sent = []
    for subtree in sentt:
        if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne_in_sent.append((ne_string, ne_label))
    # print(ne_in_sent)
    for chunk, tag in ne_in_sent:
        if(tag == 'PERSON'):
            name_list.append(chunk)

    for chunk, tag in ne_in_sent:
        if(tag == 'PERSON'):
            print('\n')
        print(chunk, end=', ')

def crawl_site(links):
    name = ['accepted', 'cfw', 'committee-steering', \
        'committee-program', 'committee-organizing', 'workshops']

    for link in links:
        if (link[:link.find('.')] in name):
            print(link)
            print('************************************')
            print('Names, Organization, Location' + '\n')
            if (link == './workshops.html'):
                get_names(url + 'workshops.html')
                print()
            else:
                get_names(url + link)
                print()

if __name__ == '__main__':
    url = "http://www.ieee-security.org/TC/EuroSP2020/"
    soup = make_soup(url)
    links_html = get_link(soup)

    links = get_pages(links_html)

    print(re.findall('EuroSP\d{4}', url)[0])
    print('************************************')
    crawl_site(links)

    # crawl previous years
    previous_years = get_previous_years(links_html)
    for url in previous_years:
        soup = make_soup(url)
        links_html = get_link(soup)
        links = get_pages(links_html)
        print(re.findall('EuroSP\d{4}', url)[0])
        print('************************************')
        crawl_site(links)

    print('************************************')
    for link in previous_years:
        print(link)
    print('************************************')
    