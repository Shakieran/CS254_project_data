# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:22:25 2020

To check the data to ensure none of it is missing, and none present isn't actually soccer data.

@author: Kieran
"""
import os
import csv
import requests

from html.parser import HTMLParser

class InvalidPermissionParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        
    def handle_data(self, data):
        if "You don't have permission" in data:
            self.flag = True

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
            self.flag

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
    
def test_invalid_htmls():
    #NOTE: EL JEFE CONTAINS DATA TO BE DELETED
    eljefe = open("INVALIDS/ElJefe.txt", "w")
    elvalid = open("INVALIDS/ElValid.txt", "w")
    
    #print(os.listdir("INVALIDS/"))
    
    for season in os.listdir("INVALIDS/"):
        #print(season)
        if("html" in season):
            #if it is an html file
            #print(season[:-5])
            #t = 1 + "T"
            
            if(not double_check([], season[:-5])):
                eljefe.write(season[:-5] + "\n")
            else:
                elvalid.write(season[:-5] + "\n")
                
    print("CLOSING")
    eljefe.close()
    elvalid.close()
            

def tester_invalids():
    headers = {'Connection':'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    
    file = open("INVALIDS.txt", "r")
    
    for line in file:
        #print(line)
        #print(line[:-5])
        #t = 1 + "T"
        #print(double_check(headers, line[:-5]))
        double_check(headers, line[:-5])
        
    file.close()
    
    file = open("INVALID_permissions.txt", "w")
    
#    for season in os.listdir()
    
    file.close()
    #InvalidPermissionParser
    
def tester_index_error():
    #headers = {'Connection':'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    
    files = {}
    file_locations = {}
    for team in os.listdir("Data"):
        if(".txt" not in team):
            seasons = []
            for season in os.listdir("Data/" + team):
                seasons.append(season[:-4])
                file_locations[season] = team
                
            files[team] = seasons.copy()
            
    ##WE NOW HAVE WHERE EACH FILE IS
    #master_file = open("FAILED_TO_PROCESS_index.txt", 'r')
    
    return file_locations
    
def delete_files():
    #basically gets us the team for a given file etc.
    files = tester_index_error()
    
    file = open("INVALIDS.txt", "r")
    key_error = open("keyerror_delete.txt", "w")
    
    for line in file:
        try:
            #print("Data/" + files[line.strip()] + "/" + line.strip())
            #t = 1 + "T"
            try:
                os.remove("Data/" + files[line.strip()] + "/" + line.strip())
            except FileNotFoundError:
                x = 1
        except KeyError:
            key_error.write(line.strip())
            
    file.close()
    file = open("INVALIDS/ElJefe.txt", "r")
    #remove files in ElJefe
    for line in file:
        #print("Data/" + files[line.strip()] + "/" + line.strip())
        #t = 1 + "T"
        try:
            os.remove("Data/" + files[line.strip()] + "/" + line.strip() + ".txt")
        except FileNotFoundError:
            x = 1
        except KeyError:
            key_error.write(line.strip())
            
    file.close()
    
    
    #now just remove all files of size 0
    for team in os.listdir("Data"):
        if(not ".txt" in team):
            for season in os.listdir("Data/" + team):
                if(os.path.getsize("Data/" + team + "/" + season) == 0):
                    os.remove("Data/" + team + "/" + season)
                    
    print("WE'RE DONE HERE!")
    
    key_error.close()
    
def main():
    #2 tasks
    #1.) make sure that all data present is soccer data
    #--if high scoring matches, double check that it's women's soccer by finding the tag 
    #with the select and ensuring it's women's soccer
    #2.) make sure no data is missing
    #keep track of all seasons missing (i.e. Iowa St. played UCLA in 2013 but no data from
    #UCLA in 2013, etc.) and then find it later manually or automated if a lot of teams which I doubt
    
    #1
    master_path = "Data"
    high_score = 4
    headers = {'Connection':'keep-alive','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    TestFlag = False
    Team_Begin = "Wyoming Cowboys"
    legit_files = tester_index_error()
    
    for team in os.listdir(master_path):
        if((TestFlag or team == Team_Begin) and not(".txt" in team)):
            print(team)
            
            if(team == Team_Begin):
                TestFlag = True
                
            cur_dir = master_path + "/" + team
            for season in os.listdir(cur_dir):
                if(legit_files[season]):
                    try:
                        #print(season)
                        #for each file we open it and check the scores
                        cur_file = open(cur_dir + "/" + season, "r")
                        file_reader = csv.reader(cur_file, delimiter=',', quotechar='\'')
                        
                        running = True
                        high_scoring = False
                        
                        for row in file_reader:
                            while(not( '-' in row[-1])):
                                row = row[:-1]
                               
                            score_unedited = row[-1].split()
                            #score = score_unedited.copy()
                            score = score_unedited[-1]
                            
                            try:
                                #print(score)
                                x = -2
                                #print("SCORE:" + score)
                                #print('-' in score)
                                while(not( '-' in score)):
                                    score = score_unedited[len(score_unedited)+x]
                                    x = x - 1
                                   
                                   
                                score = score.replace('\'','').split('-')
                                #print("Test" + str(score))
                                score = [int(score[0]), int(score[1])]
                            except ValueError:
                                #we assume spaces such as "W 1 - 0" etc.
                                #[W, 1, -, 0]
                                score = score_unedited.copy()
                                if(len(score_unedited) == 4):
                                    #print(score)
                                    if(season == "21295.txt"):
                                        print("PRINT STMT")
                                        print(score)
                                    flag = True
                                    while(flag):
                                        try:
                                            int(score[3])
                                            flag = False
                                        except ValueError:
                                            #print(score)
                                            score[3] = score[3][:-1]
                                            
                                    score = [int(score[1]), int(score[3])]
                                    
                                elif(len(score_unedited) == 2):
                                    #print(row)
                                    #print(season)
                                    #print(score)
                                    score = score_unedited[-1]
                                    #print(score)
                                    score = score.split('-')
                                    #print(score)
                                    score = [int(score[0]), int(score[-1].replace("'", "").replace("]", ""))]
                                    #print(score)
                                elif(len(score_unedited) == 3):
                                    score = [int(score[0].replace("'", "").replace("]", "")), int(score[-1].replace("'", "").replace("]", ""))]
                                else:
                                    #I couldn't think of another error
                                    print(season)
                                    print(row)
                                    print(score_unedited)
                                    print(score)
                                    raise SyntaxError
                           
                            #print(score)
                            #if(season == "381091.txt"):
                                #print(score)
                                        
                            if(score[0] > high_score or score[1] > high_score):
                                high_scoring = True
                                running = False
                               
                            if(not(running)):
                                break;
                                
                        if(high_scoring):
                            if(not double_check(headers, team, season[:-4])):
                                #i.e. if this ISN'T a women's soccer season
                                #print(season)
                                
                                #print(season)
                                #t = 1 + "T"
                                x = 1
                                
                                #file = open("INVALIDS.txt", 'a')
                                
                                #file.write(season + "\n")
                                
                                #file.close()
                            else:
                                print(season)
                     
                           
                       
                        cur_file.close()
                    except ValueError:
                        #file = open("FAILED_TO_PROCESS_value.txt", 'a')
                        
                        #file.write(season + "\n")
                        
                        #file.close()
                        x = 1
                    #except IndexError:
                        #file = open("FAILED_TO_PROCESS_index.txt", 'a')
                        #print("FAILED TO PROCESS")
                        #file.write(season + "\n")
                        
                        #file.close()
                        #x = 1
    
#main()
#test_invalid_htmls()
#tester_index_error()
delete_files()
#---------------------------------
#IN 36082:
#First match 9/01 vs South Dakkota DOESN'T COUNT towards stats for UC Colorado Springs etc.
#IN 442174: 
#['09/20/2018', 'Northwestern-St. Paul', 'Ppd']