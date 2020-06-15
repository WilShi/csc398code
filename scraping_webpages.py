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
        body = soup.find_all('tr')
        for i in body:
            info = ' '.join(i.text.split())
            name = ' '.join(info.split()[:2])
            org = ' '.join(info.split()[2:-1])
            org = re.sub(r'\(.*\)', '', org).lstrip()
            if (org[-1] == ','):
                org = org[:-1]
            location = info.split()[-1]
            print(name + ' (' + org + ') ' + location + '\n')
            # print("===================================")
        return None

    if ('accepted' in url):
        na = soup.find_all('p', class_='', style='')
        for i in na:
            if (url[-3:] == 'php'):
                info = i.text.lstrip()
                info = info[:info.find(', ')]
                print(info + '\n')
            else:
                info = i.text
                info = info.replace(', and ', ', ')
                info = info.replace(' and ', ', ')
                info = info.split('); ')
                for i in info:
                    if (i[-1] != ')'):
                        i += ')'
                    i = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n') + i[i.find('('):]
                    print(i + '\n')
            # print("===================================")
            
        if (url[-3:] == 'php'):
            # print("===================================")
            brs = soup.find_all('div', class_='list-group-item')
            for br in brs:
                info = ' '.join(str(br).split())
                tag = re.findall('<br/>.*</div>', info)[0]
                tag = re.sub(r'<[^>]*>', '', tag).lstrip()
                tag = ' '.join(tag.split())
                if ('2019' not in url):
                    info = tag.split('), ')
                else:
                    info = tag.split('); ')
                for i in info:
                    if (i[-1] != ')'):
                        i += ')'
                    i = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n') + i[i.find('('):]
                    print(i + '\n')
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
                if (b.text != '\n'):
                    if ('2016/committee-organizing' in url):
                        info = b.text.strip()
                        info = info.split('\n')
                        info = info[1:]
                        if (len(info) != 2):
                            info = ' '.join(info)
                            info = info.replace('C', '; C')
                            info = info.split('; ')
                        name = info[0].strip()
                        org = info[1].strip()
                        if (org.count(',') > 1):
                            org = org.split(',')
                            loca = org.pop().strip()
                            org = ','.join(org).strip()
                            print(name + ' (' + org + ') ' + loca + '\n')
                        else:
                            print(name + ' (' + org + ')' + '\n')
                    else:
                        info = re.sub(r'.*Chairs\s', '', b.text)
                        info = info.strip()
                        info = info.split('\n')
                        name = info[0]
                        org = info[1].strip()
                        print(name + ' (' + org + ')' + '\n')
            else:
                info = ' '.join(b.text.split())
                if (info == ''):
                    count=0
                elif (count%2 == 0):
                    print(info, end=' (')
                    count+=1
                else:
                    if ('(' in info):
                        loca = info[info.find('(')+1:info.find(')')]
                        print(info[:info.find('(')-1] + ') ' + loca + '\n')
                    else:
                        print(info + ')\n')
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
            # print('Position: ' + info)
            count=0
        elif (info == ''):
            count=0
        elif (':' in info):
            None
        elif ('Workshop' in info or 'events' in info):
            break
        elif (count%2 == 0):
            print(info, end=' (')
            count+=1
        else:
            if (',' in info):
                info = info.replace(',', ')')
                if (info.count(')') > 1):
                    print(info.replace(')', ',', info.count(')') - 1) + '\n')
                else:
                    print(info + '\n')
            else:
                print(info + ')\n')
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
            print('Names (Organization) Location' + '\n')
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
    