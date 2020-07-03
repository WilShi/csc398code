import os
import sys
import pandas as pd

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

        for i in range(len(lines)):
            break_line = '************************************'
            if (lines[i] == break_line == lines[i+2]):
                file_name = lines[i+1]
                name = []
                org = []
                loc = []

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
            try:
                if (lines[i+1] == break_line and lines[i+2] != file_name and \
                    lines[i+3] == break_line):
                    file_name += '.csv'
                    csv_file = pd.DataFrame(\
                        {'Name':name,'Organization':org,'Location':loc})
                    csv_file.to_csv(file_name, index=False, sep=',')
            except:
                file_name += '.csv'
                csv_file = pd.DataFrame({'Name':name,'Organization':org,'Location':loc})
                csv_file.to_csv(file_name, index=False, sep=',')

if __name__ == '__main__':
    if (len(sys.argv) == 2):
        creat_file(sys.argv[1])
                
    else:
        print('hello World')
        print('The rest is for data analysis')

        file = os.popen('python3 scraping_webpages.py')
        lines = file.read()
        lines = lines.split('\n')
        name = ''
        name_list = []

        for line in lines:
            if (line != ''):
                if ('(' in line):
                    name = line[:line.find('(')].strip()
                else:
                    name = line.strip()
                if (name not in name_list):
                    name_list.append(name)
                else:
                    print('same')

        print(name_list)
        
