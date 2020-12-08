# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 12:41:35 2020

@author: Kieran
"""

import os
import csv
import requests

from html.parser import HTMLParser

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
        self.row = False
        self.row_col = 1
        self.row_col_pst = 1
        self.row_txt = ""
        
        self.match = []
        self.schedule = []
        
        self.testing = False
        self.running = True
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
            self.row_col = 0
            self.row_col_pst = 0
            self.match = []
            
        elif(self.counter == 8 and tag == 'td'):
            self.row_col = self.row_col + 1

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
                for i in self.years:
                    if "2019-" in i:
                        self.success = self.years[i]
                        self.fail_type = 1
                        #self.running = False
        elif(self.counter == 5 and tag == 'select'):
            self.counter = 6
            if(self.success == 56):
                for i in self.teams:
                    if "Women" in i and "Soccer" in i:
                        self.success = self.teams[i]
                        self.fail_type = 2
                        #self.running = False
            elif(self.initial):
                x = 1
                        
        elif(self.counter == 8 and tag == 'tr'):
            self.row = False
            if(len(self.match) > 0):
                self.schedule.append(self.match)
            
            if(self.testing):
                self.schedule.append(self.match)

    def handle_data(self, data):
        if(not self.running):
            pass
        
        elif(self.push_data):
            if(self.counter == 1):
                self.name = data
            
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
                    if("Women" in data and "Soccer" in data):
                        self.selected = False
                    else:
                        self.success = 56
                        self.selected = False
            elif(self.counter == 6 and "Schedule" in data):
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
                        
                    if(data.strip() != ''):
                        self.match.append(data.strip())

                    
        elif(self.initial and "page you were looking for" in data):
            self.running = False
            
class VerifyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.legit = False
        self.ready = False
        
    def handle_starttag(self, tag, attrs):
        if(tag == "fieldset"):
            self.ready = True
            
        if self.ready and tag == "option" and len(attrs) >= 2 and attrs[1][1] == "selected":
            self.flag = True
            
    def handle_data(self, data):
        if(self.ready and self.flag):
            #print(data)
            if not '-' in data:
                if(("Women" in data or "women" in data) and ("Soccer" in data or "soccer" in data)):
                    self.legit = True
            self.flag = False

def double_check(headers, team, season):
    url = 'https://stats.ncaa.org/teams/' + team
    
    r = requests.get(url, allow_redirects=True, headers=headers)
    
    html_content = r.content.decode()
    
    #file = open("INVALIDS/" + team + ".html", 'w')
    
    #file.write(html_content)
    
    #file.close()
    
    #file = open("Data/" + team + "/" + season, 'r')
    
    parser = VerifyParser()
    
    parser.feed(html_content)
    
    #file.close()
    
    return parser.legit
    #return True
    
def double_check(content):
    parser = VerifyParser()
    
    parser.feed(content)
    
    return parser.legit
    
def main():
    headers = {'Connection':'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    starts = [381091, 58690, 94188, 53822, 73267, 63256, 35563, 81844, 20699, 41338, 26011, 440819, 479431]
    
    for start in starts:
        #name, team_id, falses = test_parser(i, headers, 'https://stats.ncaa.org/teams/', valid, teams)
        url = 'https://stats.ncaa.org/teams/' + str(start) 
        r = requests.get(url, allow_redirects=True, headers=headers)
        html_content = r.content.decode()
        
        parser = CollegeParser(False)
            
        parser.feed(html_content)
            
        file = open("Data_Final/" + str(start) + ".txt", "w")
        file.write(parser.name)
        for match in parser.schedule:
            file.write("\n")
            file.write(str(match))
                
        file.close()
        
        start = start - 1
        
        #while's it's womens soccer and not another batch of seasons
        while(double_check(html_content) and not(start in starts)):
            #if it's a women's soccer game
            if(not((str(start) + ".txt") in os.listdir("Data_Final"))):
                print(start)
                parser = CollegeParser(False)
                
                url = 'https://stats.ncaa.org/teams/' + str(start)
                r = requests.get(url, allow_redirects=True, headers=headers)
                html_content = r.content.decode()
                
                parser.feed(html_content)
                
                file = open("Data_Final/" + str(start) + ".txt", "w")
                file.write(parser.name)
                for match in parser.schedule:
                    file.write("\n")
                    file.write(str(match))
                    
                file.close()
            
            start = start - 1
            
        print("A SEASON IS DONE!")
            
def last_go():
    for file in os.listdir("Competitions/Final_Data/"):
        pass
        
#main()