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
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html5lib')
    return soup

def get_link(soup): #return all html code in navigation bar as a list
    links = []
    re_nav = re.compile('^nav')
    if (soup.find_all(re_nav) != []):
        # Find all navagtion links in the webpage
        for nav in soup.find_all(re_nav):
            a = nav.find_all('a') #Find all 'a' tag
            for link in a:
                if (link not in links):
                    # print(link.get('href')) #Print all link
                    links.append(link)
    else:
        for nav in soup.find_all(class_=re_nav):
            a = nav.find_all('a') #Find all 'a' tag
            for link in a:
                if (link not in links):
                    # print(link.get('href')) #Print all link
                    links.append(link)
    
    return links

def get_pages(links):
    pages=[]
    for i in links:
        if (i.find(text=re.compile('[Pp]revious')) == None and\
             i.find(text=re.compile('\d{4}')) == None):
            link = i.get('href')
            pages.append(link)
    if (links == []):# For ACM CCS 2017
        pages = ['posters.html', 'agenda.html', 'progcommittee.html', 
        'orgcommittee.html', 'accepted-posters-demo.html', 'awards.html']
    pages = list(set(pages))
    return pages

def get_previous_years(links, url):
    pages = []
    for i in links:
        # print(i)
        if (i.find(text=re.compile('[Pp]revious')) != None or\
             i.find(text=re.compile('\d{4}')) != None or \
                 i.find(text=re.compile('[Pp]ast\s[Cc]onference[s*]')) != None):
            link = i.get('href')
            if (link[:link.find('.')] != 'index'):
                pages.append(link)
    if (len(pages) == 1):
        soup = make_soup(url + pages[0])
        past_site = soup.find_all('a', text='Website')
        pages = []
        for site in past_site:
            link = site.get('href')
            if (link not in pages):
                pages.append(link)
            if ('2014' in link):
                break
    if ('sigsac' in url):
        for year in range(2016, 2020):
            pages.append('https://www.sigsac.org/ccs/CCS' + str(year) + '/index.html')
        pages.reverse()
    return pages

def get_names(url):
    soup = make_soup(url)
    year_re = re.compile('\d{4}')
    if ('steering' in url and 'sigsac' not in url):
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
    
    if ('shadowpc' in url):
        brs = soup.find_all('p', class_='', style='')
        for br in brs:
            info = ' '.join(str(br).split())
            if ('<br/>' in info):
                info = ' '.join(info.split())
                tag = re.sub('<br/> ', '\n\n', info).lstrip()
                tag = re.sub(r'<[^>]*>', '', tag).lstrip()
                print(tag)
        return None
    
    if ('awards' in url and 'sigsac' not in url):
        brs = soup.find_all('p', class_='', style='')
        for br in brs:
            info = ' '.join(str(br).split())
            if (re.findall('</strong>.*</p>', info) != []):
                tag = re.findall('</strong>.*</p>', info)[0]
                tag = re.sub(r'<[^>]*>', '', tag).lstrip()
                tag = re.sub(r'(,\s)*(\(*)\d{4}(\)*)', '', tag).lstrip()
                tag = re.sub(r'\),\s', ')), ', tag).lstrip()
                tag = ' '.join(tag.split())
                info = tag.replace(', and ', ', ')
                info = info.replace(' and ', ', ')
                if (') , ' in info):
                    info = info.replace(') , ', '), ')
                info = info.split('), ')
                for i in info:
                    if (i[-1] != ')' and '(' in i):
                        i += ')'
                    if ('(' in i):
                        i = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n')\
                            + i[i.find('('):]
                    else:
                        i = i.replace(', ', '\n\n')
                    print(i + '\n')
                    # print("===================================")
        return None
    
    # if ('program-committee' in url or 'organizing-committee' in url or \
    #     'call-for-posters' in url or 'program-2' in url or \
    #         'accepted-papers' in url):
    if ('sigsac' in url):
        r_pa_ar = '\[[Paper, Artifact]*\]'
        ps = soup.find_all('p', class_='', style='')
        if (len(ps) < 2 or '2017/posters' in url):
            ps = soup.find_all('li', class_='', style='')
        if (len(ps) < 2 or 'agenda' in url):
            ps = soup.find_all('div', id='authorshort')
        if (len(ps) < 2):
            ps = soup.find_all('td')
            for p in ps:
                if ('strong' in str(p)):
                    ps.remove(p)
        if ('CCS2018/program/' in url):
            ps = soup.find_all('i', class_='', style='')
            for p in ps:
                if ('<b>' in str(p)):
                    ps[ps.index(p)] = ''
        if (len(ps) < 2):
            ps = soup.find_all('div', class_='pcmember')
        if (len(ps) < 2):
            ps = soup.find_all('div', class_='', style='', id='')
        if ('CCS2017/awards' in url):
            ps = soup.find_all('b', class_='', style='')
        if ('2016/program-committee' in url):
            ps += soup.find_all('li', class_='', style='')
        if ('2016/awards' in url or '2016/accepted-papers' in url):
            ps = soup.find_all('em', class_='', style='')
        if ('2016/agenda' in url):
            ps = soup.find_all('span', class_='authors')
        # print(ps)
        count = 0
        for p in ps:
            if (p != ''):
                info = p.text
            else:
                info = ''
            name_list = []
            if ('2017/accepted-posters-demo' in url):
                # r = '<b>[\w, \s, \?, \:, \-, \(, \)]*<\/b>'
                r = '<br\/>[\w, \s, \(, \), \-]*<br\/>'
                p = ' '.join(str(p).split())
                db = re.findall(r, p)
                for i in db:
                    i = re.sub(r'<[^>]*>', '', i).lstrip()
                    # print(i)
                    name_list.append(i)
                    info = 'None'
                for i in name_list:
                    new_i = i.replace(', and ', ', ')
                    new_i = new_i.replace(' and ', ', ')
                    name_list[name_list.index(i)] = new_i
                    # name_list[name_list.index(i)] = new_i.replace('), ', ')\n\n')
                for i in name_list:
                    if ('), ' in i):
                        new_i = i.replace('), ', ')), ')
                        sub_list = new_i.split('), ')
                        for sub in sub_list:
                            sub_list[sub_list.index(sub)] = '\n\n' + sub[:sub.find('(')].replace(', ', sub[sub.find('(')-1:] + '\n\n') + sub[sub.find('('):]
                        name_list[name_list.index(i)] =''.join(sub_list)
                    else:
                        name_list[name_list.index(i)] = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n') + i[i.find('('):]

                # print(name_list)
                
            if ('CCS2018/cfposters/' in url):
                info = str(p)
                info = info.replace('<br/>', ')\n')
                info = re.sub(r'<[^>]*>', '', info).lstrip()
                info = info.replace(', ', ' (')
                if (info[-1] != ')'):
                    info += ')'
                # info = info.replace('\n', ')\n')
                # print("===================================")
            if ('accepted/papers/' in url or '2016/awards' in url):
                if(count % 2 ==  0):
                    info = ''
                count += 1
            if ('2016/awards' in url or '2016/accepted-papers' in url or '2016/agenda' in url):
                if ('(Royal Holloway, University of London' in info):
                    info += ')'
                info = info.replace(' and ', ', ')
                info = info.replace(') and ', '), ')
                info = info.replace(') ', '), ')
                info = info.replace('; ', ' (), ')
                r = '\([^\)]*\)'
                if (re.findall(r, info) == [] and info != '' and info != ' '):
                    info += ' ()'
            if (';' in info):
                name_list = info.split(';')
            if ('),' in info):
                info = info.replace('),', ')),')
                name_list = info.split('),')
            if (':' in info):
                info = info[info.find(':')+2:]
            if ('2016/steering-committee' in url):
                info = info.replace('\n', ', ')
                info = re.sub(r'\([^\)]*\)', '', info).lstrip()
            r = '\([^\)]*\)'
            if (',' in info and re.findall(r, info) == []):
                if ('CCS2017/awards' in url):
                    info = info.replace(', ', '\n\n')
                else:
                    if ('2016/organizing-committee' in url or '2016/program-committee' in url):
                        # info = info.replace('\n', '\n\n')
                        tem_list = info.split('\n')
                        # print(tem_list)
                        for i in tem_list:
                            if ('' != i and ',' in i):
                                name = i[:i.find(',')].strip()
                                org = i[i.find(',')+2:i.rfind(',')].strip()
                                loc = i[i.rfind(','):].strip()
                                tem_info = name + ' (' + org + ') ' + loc + '\n'
                                info = info.replace(info[info.find(i):info.find(i)+len(i)], tem_info)
                    else:
                        info = info.split(',')
                        name = info[0].strip()
                        org = info[1].strip()
                        loc = ' '.join(info[2:]).strip()
                        info = name + ' (' + org + ') ' + loc
                        # print("===================================")
            if (',' in info and re.findall(r, info) != []):
                if (';' in info):
                    name_list = info.split(';')
                    for i in name_list:
                        if (', and ' in i):
                            new_i = i.replace(', and ', ', ')
                            new_i = i.strip()
                            name_list[name_list.index(i)] = new_i
                            i = new_i
                        if (',' in i):
                            name_list[name_list.index(i)] = \
                                i[:i.find('(')].replace(', ', i[i.find('(')-1:] \
                                    + '\n\n') + i[i.find('('):]
                if (', and ' in info):
                    info = info.replace(', and ', ', ')
                info = info[:info.find('(')].replace(', ', \
                    info[info.find('(')-1:] + '\n\n') + info[info.find('('):]
            
            if (re.findall(year_re, info) != [] or 'poster' in info or 'Agenda' in info\
                or 'Keynotes' in info or 'Accepted' in info or 'workshops' in url or \
                    'Cornell Tech' in info or 'CCS2018/papers/' in url or \
                        'Workshops' in info or 'Posters' in info or 'Awards' in url \
                            or 'Award' in info or 'Contact' in info or '@acm_ccs' in info \
                                or 'cookies' in info or 'Close' in info or 'Sandboxed' in info):
                info = ''
            if (info == ''):
                None
            elif (name_list == []):
                # if ('CCS2018/cfposters/' not in url):
                #     info = info.replace('\n', '')
                info = info.strip()
                if (re.findall(r_pa_ar, info) != []):
                    for i in re.findall(r_pa_ar, info):
                        info = info.replace(i, '')
                if (info == ''):
                    None
                elif ('\n' in info):
                    if (info[-1:] != '\n'):
                        print(info + '\n')
                    else:
                        print(info)
                else:
                    print(info + '\n')
                # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            else:
                for name in name_list:
                    # name = name.replace('\n', '')
                    name = name.strip()
                    if (name != '' and name != '\n'):
                        if (re.findall(r_pa_ar, name) != []):
                            for i in re.findall(r_pa_ar, name):
                                name = name.replace(i, '')
                        if ('(' in name and ',' in name[:name.find('(')]):
                            name = name[:name.find('(')].replace(', ', \
                                name[name.find('(')-1:] + '\n\n') + name[name.find('('):]
                        print(name + '\n')
                        # print("===================================")
            # print(count)
            # print("===================================")
        return None

    if ('accepted' in url or 'program-papers' in url or 'program' == \
        url[url.rfind('/')+1:url.rfind('.')] or 'program-posters' in url or 'program-shorttalks' in url):
        na = soup.find_all('p', class_='', style='')
        # print("===================================")
        if ('program' not in url):
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
                        i = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n')\
                            + i[i.find('('):]
                        print(i + '\n')
            
        if (url[-3:] == 'php' or 'program-papers' in url or 'program.html' in url\
             or 'program-posters' in url or 'program-shorttalks' in url):
            # print("===================================")
            if ('program-posters' in url or 'program-shorttalks' in url):
                brs = soup.find_all('p', class_='', style='')
                if (brs == []):
                    brs = soup.find_all('div', class_='list-group-item')
                for br in brs:
                    info = ' '.join(str(br).split())
                    try:
                        tag = re.findall('<br/>.*</p>', info)[0]
                    except:
                        tag = re.findall('<br/>.*</div>', info)[0]
                    tag = re.sub(r'<[^>]*>', '', tag).lstrip()
                    tag = ' '.join(tag.split())
                    info = tag.replace(', and ', ', ')
                    info = info.replace(' and ', ', ')
                    if ('); ' in info):
                        info = info.split('); ')
                    elif ('), ' in info):
                        info = info.split('), ')
                    else:
                        info = info.split('; ')
                    if ('SP2016/program-posters' in url):
                        i = 0
                        while i < len(info):
                            info[i] += ')'
                            info[i] = info[i][:info[i].find(',')] + info[i].replace(info[i][:info[i].find(', ')+2], ' (')
                            i+=1
                    for i in info:
                        if(i[-1] == '.'):
                            i = i[:-1]
                        if (i[-1] != ')' and '(' in i):
                            i += ')'
                        i = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n')\
                            + i[i.find('('):]
                        print(i + '\n')
                        # print("===================================")
            else:
                brs = soup.find_all('div', class_='list-group-item')
                for br in brs:
                    info = ' '.join(str(br).split())
                    if (re.findall('<br/>.*</div>', info) != []):
                        tag = re.findall('<br/>.*</div>', info)[0]
                        if (re.findall(r'(\s*)\w*\:', tag)):
                            # print(tag + '\n')
                            tag = re.sub(r'<[^>]*>(\s*)\w*\:', ' ', tag).lstrip()
                            tag = tag.replace(', ', ' (')
                            tag = tag.replace('<br/>', '), ')
                        tag = re.sub(r'<[^>]*>', '', tag).lstrip()
                        tag = ' '.join(tag.split())
                        r = '\([\w,\s,&amp;]+(\([^\)]+\),)[\w,\s]+\)'
                        if (re.findall(r, tag) != []):
                            tem = re.findall(r, tag)
                            for t in tem:
                                index = tag.find(t)
                                tag = tag.replace(t, t[:-1])
                            # print("===================================")
                        r = '\([\w,\s,&amp;]+(\([^\)]+\)\sand\s)[\w,\s,\(,\)]+\)'
                        if (re.findall(r, tag) != []):
                            tem = re.findall(r, tag)
                            for t in tem:
                                tag = tag.replace(t, t.replace('and', '&'))
                        if ('2019' not in url):
                            if ('),' not in tag and '(' not in tag):
                                info = ''
                            else:
                                if ('), and ' in tag):
                                    tag = tag.replace('), and ', '), ')
                                if (') and ' in tag):
                                    tag = tag.replace(') and ', '),')
                                if ('), ' in tag):
                                    info = tag.split('), ')
                                if (') , ' in tag):
                                    info = tag.split(') , ')
                                if ('); ' in tag):
                                    info = tag.split('); ')
                                else:
                                    info = tag.split('),')
                        else:
                            if ('); ' in tag):
                                info = tag.split('); ')
                            else:
                                info = tag.split('), ')
                        for i in info:
                            i = i.strip()
                            if (i != ''):
                                if (i[-1] == ','):
                                    i = i[:-1]
                                if (i[-1] != ')' and '(' in i):
                                    i += ')'
                                if (', and' in i):
                                    i = i.replace(', and', ',')
                                i = i.replace(' and ', ', ')
                                r = '\([\w,\s,&amp;]+(\([^\)]+\)\s&\s)[\w,\s,\(,\)]+\)'
                                if (i.count('(') > 1 and re.findall(r, tag) == []):
                                    i = i.replace(i[i.find('('):i.find(')')+2], '')
                                i = i[:i.find('(')].replace(', ', i[i.find('(')-1:] + '\n\n') + i[i.find('('):]
                                if ('limited' in i or 'reproducibility' in i):
                                    None
                                else:
                                    print(i + '\n')
                                # print("===================================")
        return None
    
    if ('2016/committee-organizing' in url):
        # print("===================================")
        body = soup.select('tr')
        if (body == []):
            body = soup.find_all('div', class_='list-group-item')
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
    uni_re = re.compile('[Uu]niversity')
    # print("===================================")
    for i in body:
        info = ' '.join(i.text.split())
        if ('Chairs' in info or 'Members' in info or 'Chair' in info or 'Organizers' in info\
            or 'Treasurer' in info or 'TBD' in info or 'Admin' in info):
            # print('Position: ' + info)
            count=0
        elif (info == ''):
            count=0
        elif (':' in info or ((re.findall(year_re, info) != []) and \
            (re.findall(uni_re, info) == []))or 'deadline' in info \
            or 'notification' in info or 'Poster' in info or 'registration' in info \
                or 'period' in info or 'abstracts' in info or 'Rebuttal' in info \
                    or 'papers' in info or 'Papers' in info or 'Conference' in info \
                        or 'Notification' in info or len(i) != 1 or 'poster' in info \
                            or 'Submissions' in info or 'Student' in info or \
                                'Registration' in info or 'ready' in info or \
                                    'Short' in info or 'Events' in info or \
                                        'resources' in info):
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
        # print("===================================")

def crawl_site(url, links):
    name = ['accepted', 'cfw', 'committee-steering', \
        'committee-program', 'committee-organizing', 'workshops', \
            'program', 'program-papers', 'program-posters', \
                'program-shorttalks', 'awards', 'cfpapers', 'shadowpc', \
                    'cfposters', 'organizers', 'cfp', 'program-committee', \
                        'organizing-committee', 'call-for-posters', 'program-2', \
                            'accepted-papers', 'papers', 'posters', 'agenda', \
                                'progcommittee', 'orgcommittee', 'accepted-posters-demo', \
                                    'steering-committee', 'program-committee', \
                                        'organizing-committee']
    
    if (url[url.rfind('/')+1:] == 'index.html'):
        url = url[:url.rfind('/')+1]
    for link in links:
        page_name = link[:link.find('.')]
        # print(link)
        if ('sigsac' in url and 'index' == link[link.rfind('/')+1:link.rfind('.')]):
            if ('/' not in link):
                page_name = link
            else:
                page_name = link.split('/')[-2]
                if (link[:3] == './'):
                    link = link[2:]
        if ('sigsac' in url and 'CCS2020' not in url and link != '' and '#' not in link):
            # print(link)
            if ('https' not in link and '.' in link and '/' not in link):
                page_name = link[:link.find('.')]
            else:
                page_name = link.split('/')[-2]
            # print(link.split('/'))
        if (link[:2] == './'):
            link = link[2:]
        # print(link)
        if (page_name in name or 'workshops' in link):
            print(link + '----------' + page_name)
            print(url + link)
            print('************************************')
            print('Names (Organization) Location' + '\n')
            if (link == './workshops.html'):
                get_names(url + 'workshops.html')
                print()
            elif ('https' == link[:link.find(':')]):
                get_names(link)
            else:
                get_names(url + link)
                print()

def crawl_conferences(url):
    soup = make_soup(url)
    links_html = get_link(soup)
    links = get_pages(links_html)
    
    # for link in links:
    #     print(link)
    # print('\n\n')

    print(re.findall('[A-Za-z]{2,6}\d{4}', url)[0])
    print('************************************')
    crawl_site(url, links)

    # crawl previous years
    previous_years = get_previous_years(links_html, url)
    for url in previous_years:
        soup = make_soup(url)
        links_html = get_link(soup)
        links = get_pages(links_html)
        print(re.findall('[A-Za-z]{2,6}\d{4}', url)[0])
        print('************************************')
        crawl_site(url, links)

    print('************************************')
    for link in previous_years:
        print(link)
    print('************************************')

if __name__ == '__main__':
    conferences_urls = ["http://www.ieee-security.org/TC/EuroSP2020/", 
    "http://www.ieee-security.org/TC/SP2020/", 
    "https://www.sigsac.org/ccs/CCS2020/index.html"]
    for url in conferences_urls:
        crawl_conferences(url)

    # For test separate page
    # url = "http://www.ieee-security.org/TC/SP2020/"
    # crawl_conferences(url)