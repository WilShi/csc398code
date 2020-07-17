import os
import re
import sys
import json
import pickle
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import hypothesis_test

break_line = '************************************'

def creat_file(file_type):
    """
    Create a file in the corresponding format according to the input of parameter.
    """
    if (file_type == 'txt'):
            os.system('python3 scraping_webpages.py >list.txt')
    if (file_type == 'csv'):
        file = os.popen('python3 scraping_webpages.py')
        lines = file.read()
        lines = lines.split('\n')
        csv_file_list = []

        for i in range(len(lines)):
            if (lines[i] == break_line == lines[i+2]):
                file_name = lines[i+1]
                name = []
                org = []
                loc = []
                gender = []
                race = []

            if (lines[i] != '' and lines[i] != file_name and lines[i] != break_line):
                if ('(' in lines[i]):
                    if (')' not in lines[i]):
                        lines[i] += ')'
                    name.append(lines[i][:lines[i].find('(')].strip())
                    org.append(lines[i][lines[i].find('('):lines[i].rfind(')')+1].strip())
                    loc.append(lines[i][lines[i].rfind(')')+1:].strip())
                else:
                    name.append(lines[i])
                    org.append('')
                    loc.append('')
                gender.append('')
                race.append('')
            try:
                if (lines[i+1] == break_line and lines[i+2] != file_name and \
                    lines[i+3] == break_line):
                    file_name += '.csv'
                    csv_file_list.append(file_name)
                    csv_file = pd.DataFrame(\
                        {'Name':name,'Organization':org,'Location':loc,'Gender':gender,'Race':race})
                    csv_file.to_csv(file_name, index=False, sep=',')
            except:
                file_name += '.csv'
                csv_file_list.append(file_name)
                csv_file = pd.DataFrame({'Name':name,'Organization':org,'Location':loc,'Gender':gender,'Race':race})
                csv_file.to_csv(file_name, index=False, sep=',')
        f = open('csv_list.txt', 'w')
        for name in csv_file_list:
            f.write(name)
            f.write('\n')
        f.close()

def creat_dict(name_list, api_key):
    name_dict = {}
    name_dict = pickle.load(open('name_dict.pickle', "rb"))

    for name in name_list:
        if (name not in name_dict):
            info_dict = {}
            api_link_gender = 'http://v2.namsor.com/NamSorAPIv2/api2/json/genderFull/' + name
            parseName = 'https://v2.namsor.com/NamSorAPIv2/api2/json/parseName/' + name
            api_race = 'https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/'

            gender = requests.get(api_link_gender, headers={'X-API-KEY': api_key})
            fs_name = requests.get(parseName, headers={'X-API-KEY': api_key})
            api_dict = json.loads(gender.text)
            info_dict['Gender'] = api_dict['likelyGender']
            fs_name = json.loads(fs_name.text)
            api_race += fs_name['firstLastName']['firstName'] + '/' + fs_name['firstLastName']['lastName']
            race = requests.get(api_race, headers={'X-API-KEY': api_key})
            race = json.loads(race.text)
            info_dict['Race'] = race['raceEthnicity']
            name_dict[name] = info_dict

            print(name_dict)
            print('\n')
            pickle.dump(name_dict, open('name_dict.pickle', "wb"))


    gender = pickle.load(open('name_dict.pickle', "rb"))
    print(gender)
    print("===================================")
    print('Finshed')
    print("===================================")

def creat_name_list():
    file = os.popen('python3 scraping_webpages.py')
    lines = file.read()
    lines = lines.split('\n')

    name = ''
    name_list = []

    for line in lines:
        name2 = ''
        if line != '':
            if '(' in line:
                name = line[:line.find('(')].strip()
            else:
                name = line.strip()
            if ('/' in name):
                name = name[:name.find('/')]
            if ('*' in name):
                name = name[:name.find('*')]
            name = name.strip()
            if name not in name_list and break_line != name and \
                re.findall('[A-Za-z]{2,6}\d{4}', name) == [] and \
                    re.findall('[Uu]niversity', name) == [] and \
                        re.findall('[Cc]ollege', name) == [] and \
                            re.findall('[Ss]chedule', name) == [] and \
                                re.findall('[Aa]nonymous', name) == [] and \
                                    name.count(' ') > 0 and ')' not in name and \
                                        'Academy' not in name and \
                                            'School' not in name:
                if (' and ' in name):
                    name2 = name[name.find(' and ')+5:]
                    name = name[:name.find(' and ')]
                if (',' in name):
                    name2 = name[name.find(',')+1:]
                    name = name[:name.find(',')]
                name2 = name2.strip()
                if (name2.count(' ') > 0):
                    name_list.append(name2)
                if (name.count(' ') > 0):
                    name_list.append(name)
    return name_list

def set_grToCSV():
    name_dict = pickle.load(open('name_dict.pickle', "rb"))
    
    f = open('csv_list.txt')
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        data = pd.read_csv(line)
        for i in range(len(data['Name'])):
            if data['Name'][i] in name_dict:
                gender = name_dict[data['Name'][i]]['Gender']
                race = name_dict[data['Name'][i]]['Race']
                data['Gender'][i] = gender
                data['Race'][i] = race
        data.to_csv(line, index=False, sep=',')

        line = f.readline()
    
def population():
    male = 0
    female = 0
    population = 0

    white = 0
    hispano = 0
    asian = 0
    black = 0

    f = open('csv_list.txt')
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        data = pd.read_csv(line)
        for i in data['Gender']:
            if i == 'male':
                male += 1
            if i == 'female':
                female += 1
        population = male + female
        for i in data['Race']:
            if i == 'W_NL':
                white += 1
            if i == 'HL':
                hispano += 1
            if i == 'A':
                asian += 1
            if i == 'B_NL':
                black += 1
        print(line)
        print("Population: {} Female: {}({}) Male: {}({})".\
            format(population, female, round(female/population, 2), \
                male, round(male/population, 2)))
        print("Race:")
        print("White, non latino: {}({})".format(white, round(white/population, 2)))
        print("Hispano latino: {}({})".format(hispano, round(hispano/population, 2)))
        print("Asian, non latino: {}({})".format(asian, round(asian/population, 2)))
        print("Black, non latino: {}({})\n".format(black, round(black/population, 2)))
        male = 0
        female = 0
        population = 0
        white = 0
        hispano = 0
        asian = 0
        black = 0
        line = f.readline()

def draw_bar(conf, pop, year):
    plt.bar(range(len(pop)), pop, 0.4, color='b', alpha = 0.8)
    plt.ylabel('Population')
    plt.title('Population for ' + conf)
    plt.xticks(range(len(year)), year)
    plt.ylim([0,1800])

    for x,y in enumerate(pop):
        plt.text(x, y+100,'%s' %y,ha='center')

    plt.show()

def gender_bar(conf, year, female, male):
    x_sy = year
    x = np.arange(len(year)) #总共有几组，就设置成几，我们这里有三组，所以设置为3
    total_width, n = 0.8, 2  # 有多少个类型，只需更改n即可，比如这里我们对比了四个，那么就把n设成4
    width = total_width / n
    x = x - (total_width - width) / 2
    plt.bar(x, female, color = "r",width=width,label='Female')
    plt.bar(x + width, male, color = "b",width=width,label='Male')
    plt.title('Male Female for ' + conf)
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.legend(loc = "best")
    plt.xticks(range(0,len(year)), x_sy)
    my_y_ticks = np.arange(0, 1800, 100)
    plt.ylim((0, 1800))
    plt.yticks(my_y_ticks)
    for x,y in enumerate(female):
        plt.text(x, y+100,'%s' %y,ha='right')
    for x,y in enumerate(male):
        plt.text(x, y+100,'%s' %y,ha='left')

    plt.show()

def vs_bar(name, confs, female, male):
    x_sy = confs
    x = np.arange(len(confs)) 
    total_width, n = 0.8, 2 
    width = total_width / n
    x = x - (total_width - width) / 2
    plt.bar(x, female, color = "r",width=width,label='Female')
    plt.bar(x + width, male, color = "b",width=width,label='Male')
    plt.title('Compare ' + name)
    plt.xlabel("Conferences")
    plt.ylabel("Population")
    plt.legend(loc = "best")
    plt.xticks(range(0,len(confs)), x_sy)
    my_y_ticks = np.arange(0, 1800, 100)
    plt.ylim((0, 1800))
    plt.yticks(my_y_ticks)
    for x,y in enumerate(female):
        plt.text(x, y+100,'%s' %y,ha='right')
    for x,y in enumerate(male):
        plt.text(x, y+100,'%s' %y,ha='left')

    plt.show()

def draw_race_bar(conf, year, white, his, asian, black):
    x_sy = year
    x = np.arange(len(year)) 
    total_width, n = 0.8, 4 
    width = total_width / n
    x = x - (total_width - width) / 2
    plt.bar(x, white, color = "r",width=width,label='White')
    plt.bar(x + width, his, color = "b",width=width,label='Hispano')
    plt.bar(x + 2 * width, asian , color = "c",width=width,label='Asian')
    plt.bar(x + 3 * width, black , color = "g",width=width,label='Black')
    plt.title('Race for ' + conf)
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.legend(loc = "best")
    plt.xticks(range(0,len(year)), x_sy)
    my_y_ticks = np.arange(0, 1100, 100)
    plt.ylim((0, 1100))
    plt.yticks(my_y_ticks)
    for x,y in enumerate(white):
        plt.text(x-0.2, y+10,'%s' %y,ha='right')
    for x,y in enumerate(his):
        plt.text(x, y+10,'%s' %y,ha='right')
    for x,y in enumerate(asian):
        plt.text(x, y+10,'%s' %y,ha='left')
    for x,y in enumerate(black):
        plt.text(x+0.2, y+10,'%s' %y,ha='left')

    plt.show()

def vs_race_bar(conf, year, white, his, asian, black):
    x_sy = year
    x = np.arange(len(year)) 
    total_width, n = 0.8, 4 
    width = total_width / n
    x = x - (total_width - width) / 2
    plt.bar(x, white, color = "r",width=width,label='White')
    plt.bar(x + width, his, color = "b",width=width,label='Hispano')
    plt.bar(x + 2 * width, asian , color = "c",width=width,label='Asian')
    plt.bar(x + 3 * width, black , color = "g",width=width,label='Black')
    plt.title('Race for ' + conf)
    plt.xlabel("Conferences")
    plt.ylabel("Population")
    plt.legend(loc = "best")
    plt.xticks(range(0,len(year)), x_sy)
    my_y_ticks = np.arange(0, 600, 100)
    plt.ylim((0, 600))
    plt.yticks(my_y_ticks)
    for x,y in enumerate(white):
        plt.text(x-0.2, y+10,'%s' %y,ha='right')
    for x,y in enumerate(his):
        plt.text(x, y+10,'%s' %y,ha='right')
    for x,y in enumerate(asian):
        plt.text(x, y+10,'%s' %y,ha='left')
    for x,y in enumerate(black):
        plt.text(x+0.2, y+10,'%s' %y,ha='left')

    plt.show()


def hyp_test(pop1, target1, pop2, target2):
    size1 = pop1
    year1 = target1
    size2 = pop2
    year2 = target2
    # Null Hypothesis year1 == year2
    # Alternative Hypothesis year1 > year2
    alpha = 0.05
    p_h = (year2 + year1)/(size2 + size1)
    stdd = ((p_h * (1 - p_h))/size2) + ((p_h * (1 - p_h))/size1)
    z_value = (year2/size2 - year1/size1) / math.sqrt(stdd)
    print("z value: ", z_value)
    p_value = scipy.stats.norm.sf(abs(z_value))*2
    print("p value: ", p_value)
    if p_value > alpha:
        print("H0 is correct: Null Hypothesis year1 == year2")
    elif target2/pop2 < target1/pop1:
        print("Reject H0: Alternative Hypothesis year1 < year2")
    else:
        print("Reject H0: Alternative Hypothesis year1 > year2")
    sns.distplot(pd.Series([pop1, pop2]))
    plt.title('data distribution')
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'txt' or sys.argv[1] == 'csv':
            creat_file(sys.argv[1])
                    
        if sys.argv[1] == 'list':
            name_list = creat_name_list()
            pickle.dump(name_list, open('name_list.pickle', 'wb'))

        if sys.argv[1] == 'dict':
            name_list = pickle.load(open('name_list.pickle', "rb"))
            creat_dict(name_list, '61f8c3dc68d36e701dd558f668eb4fb9')

        if sys.argv[1] == 'setgr':
            set_grToCSV()

        if sys.argv[1] == 'population':
            population()

        if sys.argv[1] == 'pop_bar':
            conf = sys.argv[2]
            pop = sys.argv[3].split(',')
            pop = list(map(int, pop))
            year = sys.argv[4].split(',')
            fr = int(year[0])
            to = int(year[1])
            year = []
            while fr <= to:
                year.append(fr)
                fr += 1
                
            print(pop)
            print(year)
            draw_bar(conf, pop, year)

        if sys.argv[1] == 'race_bar':
            conf = sys.argv[2]
            white = list(map(int, sys.argv[3].split(',')))
            his = list(map(int, sys.argv[4].split(',')))
            asian = list(map(int, sys.argv[5].split(',')))
            black = list(map(int, sys.argv[6].split(',')))
            year = sys.argv[7].split(',')
            fr = int(year[0])
            to = int(year[1])
            year = []
            while fr <= to:
                year.append(fr)
                fr += 1
            draw_race_bar(conf, year, white, his, asian, black)

        if sys.argv[1] == 'gender_bar':
            conf = sys.argv[2]
            female = list(map(int, sys.argv[3].split(',')))
            male = list(map(int, sys.argv[4].split(',')))
            year = sys.argv[5].split(',')
            fr = int(year[0])
            to = int(year[1])
            year = []
            while fr <= to:
                year.append(fr)
                fr += 1
            gender_bar(conf, year, female, male)

        if sys.argv[1] == 'vs_bar':
            name = sys.argv[2]
            female = list(map(int, sys.argv[3].split(',')))
            male = list(map(int, sys.argv[4].split(',')))
            confs = sys.argv[5].split(',')
            vs_bar(name, confs, female, male)

        if sys.argv[1] == 'vs_race_bar':
            conf = sys.argv[2]
            white = list(map(int, sys.argv[3].split(',')))
            his = list(map(int, sys.argv[4].split(',')))
            asian = list(map(int, sys.argv[5].split(',')))
            black = list(map(int, sys.argv[6].split(',')))
            year = sys.argv[7].split(',')
            draw_race_bar(conf, year, white, his, asian, black)

        if sys.argv[1] == 'run_test':
            hypothesis_test.run_test()

    else:
        name_list = pickle.load(open('name_list.pickle', "rb"))
        # print(name_list)
        print(len(name_list))

        name_dict = pickle.load(open('name_dict.pickle', "rb"))
        # print(gender)
        print(len(name_dict))
        

    