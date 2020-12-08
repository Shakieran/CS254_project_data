# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 21:20:47 2020

@author: Kieran
"""

import requests
import os
import time
#------
#import traceback

from html.parser import HTMLParser
#from lxml.html import fromstring
#from itertools import cycle


'''
Steps in parsing the page:
    1.): determine whether this is womens soccer
        a.) if it is, go to the 2019-20 season and step through each season, and include all
            relevant team data
        b.) if it isn't, and there is womens soccer for the school, go to that team and do
            step a
        c.) if it isn't and there isn't for this school, just update the teams data
    2.) Get the team name
    3.) For each season:
        a.) Get relevant game data
        b.) Get team stats
    #IF TIME
        c.) For each game get box scores
'''
'''
class FinalParser(HTMLParser):
    def __init__(self, div):
        self.teams = []
        #self.flag = False
        self.division = div
        
    #def handle_data(self, data):
        #if self.flag:
            #self.flag = false
            #self.teams.append(data)
            
    def handle_starttag(self, tag, attrs):
        if(tag == 'a'):
            for attr in attrs:
                if(attr[0] == 'href' and "team" in attr[1]):
                    vals = attr[1].split("/")
                    self.teams.append()
    #'''
class CollegeParser(HTMLParser):
    
    def __init__(self, initial):
        HTMLParser.__init__(self)
        self.initial = initial
        '''
        counter =
            0: nothing  processed
            1: We have entered the fieldset
            2: We have pushed name as the first entry into data
            3: we have gotten to team ID's
            4: we have finished each year's team ID's
            5: we have gotten to sports (womens soccer, mens football, etc.)
            6: we have gotten past sports
            7: We have gotten to the first "Schedule/Results" section
            8: We have gotten to the second "Schedule/Results" section
        '''
        self.counter = 0
        self.push_data = False
        self.data = []
        self.years = {}
        self.year = ""
        self.teams = {}
        self.team = ""
        self.name = ""
        self.selected = False
        
        self.fail_type = -1
        #1 == wrong year
        #2 == wrong sport
        #ONLY CHECKED IF WE'RE LOOKING FOR INITIAL ETC
        
        #are we in a tr tag (in a row of a table)
        self.row = False
        #which column are we in
        self.row_col = 1
        self.row_col_pst = 1
        self.row_txt = ""
        
        self.match = []
        #schedule is composed of each match
        self.schedule = []
        
        self.testing = False
        self.running = True
        
        #if not -1, failure
        #if not -1, it is the womens soccer team
        self.success = -1
    
    def handle_starttag(self, tag, attrs):
        if(not self.running):
            pass  
        elif((tag == "fieldset") and (self.counter == 0)):
            self.counter = 1
            
        elif(self.counter == 1 and tag == 'a'):
            self.push_data = True
            
        elif(self.counter == 2 and tag == 'select'):
            self.counter = 3
            
        elif(self.counter == 3 and tag == 'option'):
            self.year = attrs[0][1]
                
            if(len(attrs) == 2 and attrs[1][1] == 'selected'):
                #we get here successfully
                self.selected = True
            
            if(attrs[0][0] == 'value'):
                self.push_data = True
                
            else:
                self.push_data = False
                print(attrs)
                print(attrs[0])
                print(attrs[0][0])
                print("INVALID SYNTAX -- COUNTER = 3 -- YEARS")
            
        elif(self.counter == 4 and tag == 'select'):
            self.counter = 5
            self.selected = False
            
        elif(self.counter == 5 and tag == 'option'):
            self.team = attrs[0][1]
            if(len(attrs) == 2 and attrs[1][1] == 'selected'):
                self.selected = True
                
        elif(self.counter == 8 and tag == 'tr'):
            self.row = True
            self.push_data = True
            #first col is 1 since we always increment
            self.row_col = 0
            self.row_col_pst = 0
            self.match = []
            
        elif(self.counter == 8 and tag == 'td'):
            self.row_col = self.row_col + 1
        
        #print("Encountered a start tag:", tag)
        #print("Attributes: ", attrs)

    def handle_endtag(self, tag):
        if(not self.running):
            pass
        elif(self.counter == 1 and self.push_data and tag == 'a'):
            self.push_data = False
            if(self.initial):
                self.counter = 2
            else:
                self.counter = 6
                self.push_data = True
        
        elif(self.counter == 3 and tag == 'select'):
            self.counter = 4
            if(self.success == 56):
                #WE ARE NOT A 2019-2020 SOCCER TEAM RIGHT NOW
                for i in self.years:
                    if "2019-" in i:
                        self.success = self.years[i]
                        self.fail_type = 1
                        self.running = False
                        
        #end of sport teams
        elif(self.counter == 5 and tag == 'select'):
            self.counter = 6
            if(self.success == 56):
                #WE ARE NOT A WOMENS SOCCER TEAM RIGHT NOW
                for i in self.teams:
                    if "Women" in i and "Soccer" in i:
                        self.success = self.teams[i]
                        self.fail_type = 2
                        self.running = False
            elif(self.initial):
                #we've gotten the info we don't need to parse the entire document -- YET
                #the rest is for initial=False
                x = 1
                #self.running = False
                        
        elif(self.counter == 8 and tag == 'tr'):
            self.row = False
            if(len(self.match) > 0):
                self.schedule.append(self.match)
            
            if(self.testing):
                self.schedule.append(self.match)
                #print(self.schedule)

    def handle_data(self, data):
        if(not self.running):
            pass
        
        elif(self.push_data):
            #years
            if(self.counter == 1):
                self.name = data
            #there was a '\n' as data so here we are making usre it's legit
            
            elif(self.counter == 3 and '-' in data):
                self.years[data] = self.year
                
                if(self.selected):
                    if("2019-" in data):
                        self.selected = False
                    else:
                        self.success = 56
                        self.selected = False
                        
            elif(self.counter == 5 and 's' in data):
                self.teams[data] = self.team
                if(self.selected):
                    #this is the selected team
                    if("Women" in data and "Soccer" in data):
                        #success
                        self.selected = False
                    else:
                        #WRONG SPORT!!!!!!!!
                        self.success = 56
                        self.selected = False
                        #stop if this isn't a legit page
            
            #    self.counter == 6 and "Schedule" in data
            elif(self.counter == 6 and "Schedule" in data):
                #NOTE: This is the first schedule/results
                self.counter = 7
                    
            elif(self.counter == 7 and "Schedule" in data):
                self.counter = 8
            elif(self.counter == 8 and self.row):
                if("Date" in data):
                    #if this is the header row
                    self.row = False
                elif("Team Stats" in data):
                    self.counter = 9
                else:
                    if("2003" in data):
                        self.testing = True
                    #if(self.row_col == 1 and self.row_col_pst == 0):
                        #self.match = []
                    
                    #if(self.row_col < 4 and not('\n' in data)):
                    '''
                    if(self.row_col < 4):
                        self.row_txt = self.row_txt + data
                        if(not self.row_col_pst == self.row_col):
                            self.match.append(self.row_txt)
                            self.row_txt = ""
                            '''
                    #if(data[0].isalnum() or (len(data) > 2 and data[2].isalnum())):
                        #self.match.append(data.strip())
                        
                    if(data.strip() != ''):
                        self.match.append(data.strip())
                        
                    #self.row_col_pst = self.row_col
                    
                    #CHANGE 3 IF MORE DATA INCLUDED PER MATCH
                    #IF CHANGE 3 CHANGE 4 ABOVE TOO
                    #if(self.row_col == 4):
                        #print(self.match)
                        #self.schedule.append(self.match)
                        #self.row = False
                    #print(data)
                    
                    
        elif(self.initial and "page you were looking for" in data):
            self.running = False

def test_parser(n, headers, url_incomp, valid, teams):
    url = url_incomp + str(n)
    r = requests.get(url, allow_redirects=True, headers=headers)
    html_content = r.content.decode()

    #print("LINE 260")
    
    parser = CollegeParser(True)
    #print("LINE 263")
    parser.feed(html_content)
    #print("LINE 265")
    val = -1
    wrongs = []
    seasons = []
    
    if(parser.name in teams):
        return ("__ERROR", -1, [])
    
    #wrongs_comp = []
    
    #if data is empty then it wasn't a valid team
    #if success isn't -1 then it wasn't a women's soccer team
    #if neither of these conditions are true then we're gucci
    
    #if 1 go of non-(-1) success then wrong team or wrong year, if 2 goes both were wrong
    
    while(parser.success != -1):
        #list(d.values())
        val = parser.success
        
        #print(wrongs)
        for i in parser.teams:
            wrongs.append(parser.teams[i])
        
        #print(wrongs)
        #print(parser.years)
        for i in parser.years:
            wrongs.append(parser.years[i])
        #print(wrongs)
        
        if(not("2019-20" in parser.years.keys()) and not("2019-2020" in parser.years.keys())):
            parser.success = -2
            file = open("Not_Current.txt", "a")
            file.write(parser.name + "\n")
            file.close()
            
            break;
        
        
        #as long as year wasn't issue
        if(parser.fail_type != 1):
            for t in parser.teams.values():
                if(not(t in valid)):
                    url_temp = url_incomp + str(t)
                    r_temp = requests.get(url_temp, allow_redirects=True, headers=headers)
                    p_temp = CollegeParser(True)
                    p_temp.feed(r_temp.content.decode())
                    
                    for i in p_temp.years:
                        wrongs.append(p_temp.years[i])
        
        
        url = url_incomp + str(parser.success)
        r = requests.get(url, allow_redirects=True, headers=headers)
        
        html_content = r.content.decode()
        parser = CollegeParser(True)
        parser.feed(html_content)
    
    #print(parser.data)
    #print(parser.success)
    #print(parser.schedule)
    
    #--------------------------------------
    #AT THIS POINT parser IS THE 2019-2020 WOMENS SOCCER HTML FILE
    #--------------------------------------
    #print("LINE 296")
    
    try:
        os.makedirs("Data/" + parser.name)
    except OSError as e:
        #we  must have an except so here we are
        x = 1
        
    #for each year
    for y in parser.years:
        if(not (("-21" in y) or ("2021" in y))):
            parse_data(parser.name, parser.years[y])
            seasons.append(parser.years[y])
            
        #x = 1
    
    
    #wrongs_comp = []
    
    #for l in wrongs:
        #for i in l:
            #wrongs_comp.append(i)
    
    #list(dict.fromkeys(mylist))
    
    parser.name = parser.name.strip()
    
    return (parser.name, val, list(dict.fromkeys(wrongs)))

    #parser.feed('<html><head t=\'test\' v=\'groo\'><title>Test</title></head>'
                #'<body><h1>Parse me!</h1></body></html>')

def parse_data(name, team):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    url = 'https://stats.ncaa.org/teams/' + str(team)
    r = requests.get(url, allow_redirects=True, headers=headers)
        
    html_content = r.content.decode()
    
    parser = CollegeParser(False)
    parser.feed(html_content)
    
    file = open("Data/" + name.strip() + "/" + str(team) + ".txt", 'w')
    
    for t in parser.schedule:
        file.write(str(t) + "\n")
    
    file.close()

#gets the information already gathered
def restart_info():
    master_path = "C:\\Users\\Kieran\\Documents\\254_Project\\Data"
    valid = {}
    teams = []
    
    file = open('data/teams.txt', 'r')
    
    for line in file:
        teams.append(line.strip())
    
    file.close()
    
    
    #teams = os.listdir(master_path)
    
    #test = "12345.txt"
    #print(test[:-4])
    
    for t in teams:
        if(not(t == "teams.txt") and not(t == '')):
            #print(os.listdir(master_path + "\\" + t))
            for season in os.listdir(master_path + "\\" + t):
                valid[int(season[:-4])] = False
    #print("Done!")
    return valid

def first_restart():
    file = open('data/teams.txt', 'w')
    
    teams = os.listdir("C:\\Users\\Kieran\\Documents\\254_Project\\Data")
    
    for team in teams:
        if(not(team == "teams.txt")):
            file.write(team + "\n")
    
    file.close()

def main():
    #n = 480613 #Women's UCLA 2019
    #n = 441601 #Women's UCLA 2018
    #n = 479473 #Men's UCLA 2019
    #n = 1
    headers = {'Connection':'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    initials = {}
    valid = restart_info()
    teams = {}
    
    #proxies = get_proxies()
    
    #proxy_pool = cycle(proxies)
    
    #21035
    
    print("CONTINUING EXECUTION!")
    start = 10000
    #end = 20001
    end = 520000
    
    for i in range(start, end):
        if(i not in valid.keys()):
            #time.sleep(1)
            #print("Slept")
            #url = 'https://stats.ncaa.org/teams/' + str(n)
            #r = requests.get(url, allow_redirects=True, headers=headers)
        
            #html_content = r.content.decode()
            
            #CYCLING PROXIES
            #proxy = next(proxy_pool)
            
            name, team_id, falses = test_parser(i, headers, 'https://stats.ncaa.org/teams/', valid, teams)
            #initials[test_parser(i, headers, 'https://stats.ncaa.org/teams/')] = True
            #open('test' + str(i + 1) + '.html', 'wb').write(r.content)
            
            if(team_id != -1 and not (name in teams.keys())):
                initials[team_id] = True
        
                for f in falses:
                    valid[f] = False
                
            
                valid[team_id] = True
                
                teams[name] = team_id
                
                #print(teams)
                
                file = open('data/teams.txt', 'a')
                
                file.write(name + "\n")
                
                file.close()
            elif name in teams.keys():
                #we want to add falses to teams
                for f in falses:
                    valid[f] = False
        
                #n = n + 1
                #print(i)
                #2500th prime number
        if(i % 17 == 0 or i < start + 100):
            print(i)
            #print(valid)
     
    #print(teams)
    
   # file = open('data/teams.txt', 'w')
    
    #for t in teams:
        #file.write(t + "\n")
    
    #file.close()
    
    #print(valid)
        
main()
print("DONE!")