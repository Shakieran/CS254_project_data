# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 02:02:55 2020

@author: Kieran
"""

'''
WE MUST CONVERT THIS:
Abilene Christian Wildcats
['08/21/2015', '@', 'Arizona', 'L 0-4', '1,086']
['08/23/2015', '@', 'UTEP', 'L 0-1', '311']
['08/28/2015', 'UTSA', '@Austin, Texas', 'W 5-3', '0']
#NOTE: (2 OT) MEANS DOUBLE OVERTIME -- T MEANS THEY STILL TIED!
['08/30/2015', 'UC Irvine', '@College Station, Tex', 'T 0-0 (2 OT)', '125']
. . .
    
    
TO THIS (for each season):
No. 17, No. 18, 6, 3
No. 19, No. 22, 3, 3
No. 20, No. 23, 2, 4
. . .
'''

import os
import time
import copy

from data_loader import data_loader
from datetime import datetime

class Load_Game():
    
    def __init__(self):
        self.date = ""
        self.neutral = False
        self.home_team = ""
        self.away_team = ""
        self.home_score = 0
        self.away_score = 0
        
    def set_date(self, date):
        d_save = date
        
        if(date[-1] == ")"):
            date = date.split("(")[0]
            
        try:
            self.date = datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            print(d_save)
            t = 1 + "T"
            
    def equivalent_game(self, game):
        g_temp = copy.deepcopy(game)
        
        if(g_temp.home_team == self.home_team):
            g_temp.away_team = self.away_team.strip()
        else:
            g_temp.home_team = self.home_team.strip()
            
        return self == g_temp
    
    def __eq__(self, g):
        if(not(type(g) == Load_Game)):
            return False
        
        if(self.date == g.date and
           self.neutral == g.neutral and
           self.home_team == g.home_team and
           self.away_team == g.away_team and
           self.home_score == g.home_score and
           self.away_score == g.away_score):
            return True
        
        return False
        
    def __repr__(self):
        if(not(type(self.date) == datetime)):
            self.date = datetime.strptime(self.date, "%m/%d/%Y")
            
        return self.date.strftime("%m/%d/%Y") + ":" + self.home_team + " vs. " + self.away_team + " with a score of " + str(self.home_score) + "-" + str(self.away_score)

class Season():
    
    def __init__(self):
        self.team = ""
        self.games = {}#each year has a list of games in order
        
        self.year = 0
        self.opponents = {}#each opponent is added here
        
    def __repr__(self):
        return self.team
    
    def find_game(self, date):
        for g in self.games:
            if(self.games[g].date == date):
                return g
    
    def first_game_vs_opponent(self, opponent):        
        for g in self.games[self.year]:
            if(g.home_team == opponent or
               g.away_team == opponent):
                return g
        
        return False
    
    def update(self, teams):
        for g in self.games[self.year]:
            if(not(self.team == g.home_team) and
               g.home_team in self.opponents[self.year]):
                #edit opponents to yield the new name
                self.opponents[self.year].remove(g.home_team)
                self.opponents[self.year].append(teams[g.home_team])
            elif(g.away_team in self.opponents[self.year]):
                self.opponents[self.year].remove(g.away_team)
                self.opponents[self.year].append(teams[g.away_team])
            #then we go and edit the game to reflect the new name
            #print(g)
            g.home_team = teams[g.home_team.strip()].strip()
            g.away_team = teams[g.away_team.strip()].strip()
    
    def is_opponent(self, opponent):
        if opponent in self.opponents[self.year]:
            return True
        
        return False
        
    def equivalent_game(self, game):
        #print("Game: " + str(game))
        for g in self.games[self.year]:
            if(g.date == game.date):
                #print("g: " + str(g))
                #print("Game: " + str(game))
                #print("\n")
                #time.sleep(8)
                #the team we want is different otherwise same day one shared team etc.
                g_temp = copy.deepcopy(g)
                if(g_temp.home_team == game.home_team):
                    g_temp.away_team = game.away_team.strip()
                else:
                    g_temp.home_team = game.home_team.strip()
                    
                print("TEAM: " + str(self.team))
                print("Gtemp: " + str(g_temp))
                    
                    #t = 1 + "T"
                    
                if(g_temp == game):
                    return g
            
        return -1
    
    def add_game(self, game):
        #any('*' in entry for entry in line)
        #any(gme.home_team in)
        
        hteam = game[0].home_team
        ateam = game[0].away_team
        #if(hteam == "Ohio Wesleyan Battling Bishops" or
           #ateam == "Ohio Wesleyan Battling Bishops"):
            #print("HERE")
        
        hteam_flag = True
        ateam_flag = True
        for gme in game:
            if(hteam not in (gme.home_team + gme.away_team)):
                hteam_flag = False
                #print("GAME H: " + str(gme))
            
            if(ateam not in (gme.home_team + gme.away_team)):
                ateam_flag = False
                #print("GAME A: " + str(gme))
                
        #print("------------")
        #print(hteam_flag)
        #print(ateam_flag)
        #print("============")
        
        if(hteam_flag):
            self.team = hteam
        
        if(ateam_flag):
            self.team = ateam
            
        if(hteam_flag and ateam_flag):
            if(hteam in ateam):
                self.team = ateam
            elif(ateam in hteam):
                self.team = hteam
            elif(ateam == "Cal St. East Bay" and
                 hteam == "Mills Cyclones"):
                self.team = hteam
            elif(ateam == "Salem (NC) Spirits" and
                 hteam == "William Peace"):
                self.team = ateam
            elif(ateam == "St. Thomas (FL) Bobcats" and
                 hteam == "FGCU"):
                self.team = ateam
            elif(ateam == "Flagler Saints" and
                 hteam == "North Florida"):
                self.team = ateam
            elif(hteam == "Dixie St. Trailblazers" and
                 ateam == "Utah Valley"):
                self.team = hteam
            elif(ateam == "Stanislaus St. Warriors" and
                 hteam == "Sacramento St."):
                self.team = ateam
            elif(hteam == "Hannibal-La Grange" and
                 ateam == "Quincy"):
                self.team = hteam
            elif(hteam == "Dominican (CA)" and
                 ateam == "Grand Canyon"):
                self.team = hteam
            elif(hteam == "Mt. Aloysius" and
                 ateam == "Lancaster Bible"):
                self.team = hteam
            elif(ateam == "Oakland City Lady Oaks" and
                 hteam == "Indiana St."):
                self.team = ateam
            elif(hteam == "Mount Mary Blue Angels" and
                 ateam == "Finlandia"):
                self.team = hteam
            elif(ateam == "Mount Mary Blue Angels" and
                 hteam == "Finlandia"):
                self.team = ateam
            elif(ateam == "Russell Sage Gators" and
                 hteam == "Albany Pharmacy"):
                self.team = ateam
            elif(ateam == "Notre Dame de Namur Argonauts" and
                 hteam == "San Jose St."):
                self.team = ateam
            elif(ateam == "Mary Marauders" and
                 hteam == "North Dakota St."):
                self.team = ateam
            elif(ateam == "Dixie St. Trailblazers" and
                 hteam == "Utah Valley"):
                self.team = ateam
            else:
                pass
                #print("BOTH FLAGS RAISED")
                #print(game)
                #t = 1 + "T"
                
        #only happened once no need to debug since this is the only time it'll occur
        #if(self.team == ''):
            #self.team = "Ohio Wesleyan Battling Bishops"
            
            
        if(type(game) == list):
            #if(self.team == "Ohio Wesleyan Battling Bishops"):
                #print(game[0])
                #print("Game above\n")
            
            for g in game:
                if(self.team == "Ohio Wesleyan Battling Bishops"):
                    pass
                    #print("\nTEST")
                    #print(game[0])
                    #print(g)
                if(self.year == 0):
                    #get year and make a thing in games
                    #print(g)
                    try:
                        self.year = g.date.year
                    except AttributeError:
                        g_date = g.date
                        g.date = datetime.strptime(g_date, "%m/%d/%Y")
                        self.year = g.date.year
                    
                    self.games[self.year] = []
                    self.opponents[self.year] = []
                    
                self.games[self.year].append(g)
                if(self.team == "Ohio Wesleyan Battling Bishops"):
                    pass
                    #print(g)
                    #print(self.games[self.year])
                    
                if(g.home_team == self.team):
                    self.opponents[self.year].append(g.away_team)
                else:
                    if(g.away_team == self.team):
                        self.opponents[self.year].append(g.home_team)
                        
        if(self.team == "Ohio Wesleyan Battling Bishops"):
                #print(self.games)
                pass
        #if(self.team == "Washington Huskies" and self.year == 2019):
            #print(self.games[self.year])
            #print("\n")
            
def hand_written_update():
    teams = data_loader()

    return teams

def read_true_data():
    teams_top = []
    teams_bot = []
    
    TEAMS = hand_written_update()
    
    #data will
    data_load = {}
    count = 0
    
    for season in os.listdir("Data_Final"):
        data_load[season] = []
        try:
            file = open("Data_Final/" + season)
            #SEASON HAS .txt WITH IT! IS STRING! etc.
            first_line = True
            for line in file:
                if(first_line):
                    #if(not(line in teams_top)):
                    '''
                    REMOVE DUPLICATES LATER THIS ALLOWS OUR GAME FUNCTION TO WORK
                    '''
                    teams_top.append(line.strip())
                    first_line = False
                    
                    
                else:
                    #['08/21/2015', '@', 'Arizona', 'L 0-4', '1,086']
                    #'08/21/2015', '@', 'Arizona', 'L 0-4', '1,086'
                    
                    #remove commas where they don't belong
                    running = True
                    while(running):
                        comma_finder = False

                        for i in range(1, len(line)-1):
                            if(not(comma_finder)):
                                if((((line[i]==',' and line[i-1].isdigit() and line[i+1].isdigit())
                                or (line[i]==',' and line[i-1].isalpha() and not(line[i+1] == '\''))
                                or (line[i]==',' and line[i-1] == '.' and not(line[i+1] == '\''))))):
                                    line = line[:i] + line[i+1:]
                                    comma_finder = True
                                    
                        if(not(comma_finder)):
                            running = False
                            
                    #NOTE WE IGNORE ASTERIXES INDEICATING THAT A GAME DOESN'T OCUNT FOR SOMEONE
                    line = line.replace("[", "").replace("]", "").replace("\n", "").replace("*", "").split(',')
                    
                    #if(season == "26602.txt" and line[0] == "'11/27/2017'"):
                    #print(line)
                    
                    for i in range(0, len(line)):
                        #get ride of opening quotes
                        #get ride of leading spaces
                        line[i] = line[i].strip()
                        line[i] = line[i][1:-1]
                        line[i] = line[i].strip()
                        
                    index = 0
                    while(index < len(line)):
                        if(line[index] == ""):
                            line.pop(index)
                        else:
                            index += 1
                    
                    #if(season == "63897.txt"):
                        #print(line)
                    '''
                    TIME TO GET OUR GAME OBJECT AND PUT IT INTO DATA
                    For each pass, below is pasted the value of which would trigger this pass to be true
                    In the if statements with this statement true it will assume that format and parse
                    accordingly
                    '''
                    
                    three_pass_1 = False
                    #['09/19/2015', '@ Cincinnati Christian', 'W 2-0']
                    three_pass_2 = False
                    #['10/24/2015', 'Belhaven', 'W 2-1']
                    
                    four_pass_1 = False
                    #['09/04/2015', 'North Texas', 'L 0-3', '948']
                    four_pass_2 = False
                    #['09/07/2015', '@', 'IIT', 'W 1-0']
                    four_pass_3 = False
                    #['11/27/2017', 'Biola', '@Kissimmee FL', 'L 0-3']
                    
                    five_pass_1 = False
                    #['08/21/2015', "'@", "'Arizona", "'L 0-4", "'", '86']
                    five_pass_2 = False
                    #['09/13/2015', 'Texas Tech', '@Mulcahy Stadiu', 'L 0-1', '108']
                    five_pass_3 = False
                    #['11/07/2019', '#5 Grambling', 'SWAC WSOC Championship', 'L 0-1', '0']
                    
                    six_pass_1 = False
                    #['08/28/2015', 'UTSA', '@Austi', 'exas', 'W 5-3', '0']
                    six_pass_2 = False
                    #['11/03/2019', '@', '#4 Buffalo', 'MAC WSOC Championship', 'L 1-2 (2 OT)', '0']
                    six_pass_3 = False
                    #['09/03/2010', '@', 'Waynesburg', '@Defiance Ohio', 'T 0-0 (2 OT)', '100']
                    #NEUTRAL GROUNDS
                    
                    conference_champ_bs = ["championship",
                                           "champ",
                                           "gliac",
                                           "northeast 10",
                                           "lone star",
                                           "northern sun",
                                           "sunshine state",
                                           "glvc",
                                           "psac",
                                           "east coast",
                                           "ccaa",
                                           "miaa",
                                           "rmac",
                                           "peach belt",
                                           "gulf south",
                                           "great midwest"]
                    
                    cumulative = False
                    
                    game = Load_Game()
                    if(line[0] == '-'):
                        print(season)
                    elif(line[0] == "11/01/-5510" or
                         season == "21216.txt"):
                        #print(season)
                        #print(line)
                        pass
                        
                    if("exempted" in line[0] or
                       any('ppd' == entry.lower() for entry in line) or
                       any('*' in entry for entry in line) or
                       any('\\n' in entry for entry in line) or
                       (any(entry == '@' for entry in line) and len(line) < 4)):
                        #53829.txt
                        pass
                        #OOF
                    elif(len(line) == 3):
                        #PASS 1
                        #['09/19/2015', '@ Cincinnati Christian', 'W 2-0']
                        #PASS 2
                        #['10/24/2015', 'Belhaven', 'W 2-1']
                        try:
                            if(not('@' in line[1][0])):
                                int("T")
                            three_pass_1 = True
                        except ValueError:
                            #onto the next pass
                            try:
                                if(not('-' in line[2])):
                                    int('T')
                                    
                                three_pass_2 = True
                            except ValueError:
                                print("OOF")
                                print(season)
                                print(line)
                                t = 3 + "T"
                            
                        if(three_pass_1):
                            #['09/19/2015', '@ Cincinnati Christian', 'W 2-0']
                            game.set_date(line[0])
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            
                            score = line[2].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[2])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                        
                        elif(three_pass_2):
                            #['10/24/2015', 'Belhaven', 'W 2-1']
                            game.set_date(line[0])
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            score = line[2].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[2])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                    elif(len(line) == 4):
                        #PASS 1
                        #['09/04/2015', 'North Texas', 'L 0-3', '948']
                        #PASS 2
                        #['09/07/2015', '@', 'IIT', 'W 1-0']
                        #PASS 3
                        #['11/27/2017', 'Biola', '@Kissimmee FL', 'L 0-3']
                        try:
                            int(line[3])
                            if(not('-' in line[2])): #and len(line[2]) < 7)):
                                int("T")
                            
                            four_pass_1 = True
                        except ValueError:
                            #onto the next pass
                            try:
                                if(not('@' == line[1])):
                                    int("T")
                                    
                                if(not('-' in line[3])):
                                    int("T")
                                
                                four_pass_2 = True
                                
                            except ValueError:
                                #onto the next pass (numero tres)
                                try:
                                    if(not('-') in line[3]):
                                        int("T")
                                        
                                    if(not('@') in line[2]):
                                        int("T")

                                    four_pass_3 = True
                                except ValueError:
                                    print("OOF")
                                    print(season)
                                    print(line)
                                    t = 4 + "T"
                            
                        if(four_pass_1):
                            #['09/04/2015', 'North Texas', 'L 0-3', '948']
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                                
                            game.set_date(line[0])
                            
                            if(not(game.home_team in teams_bot)):
                                teams_bot.append(game.home_team.strip())
                            
                            score = line[2].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[2])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                            #print(game)
                            #t = 4 + "T"
                        elif(four_pass_2):
                            #['09/07/2015', '@', 'IIT', 'W 1-0']
                            game.set_date(line[0])
                            
                            t_line_num = 2
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            score = line[3].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[3])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                        elif(four_pass_3):
                            #['11/27/2017', 'Biola', '@Kissimmee FL', 'L 0-3']
                            game.set_date(line[0])
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            game.neutral = True
                            
                            score = line[3].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[3])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                        
                    elif(len(line) == 5):
                        #PASS 1
                        #['08/21/2015', "'@", "'Arizona", "'L 0-4", "'", '86']
                        #PASS 2
                        #['09/13/2015', 'Texas Tech', '@Mulcahy Stadiu', 'L 0-1', '108']
                        try:
                            int(line[4])
                            if(not(line[1] == '@')):
                                int("T")
                            
                            five_pass_1 = True
                        except ValueError:
                            
                            #another try
                            try:
                                #['09/13/2015', 'Texas Tech', '@Mulcahy Stadiu', 'L 0-1', '108']
                                int(line[4])
                                if(not('@' == line[2][0])):
                                    int("T")
                                    
                                five_pass_2 = True
                                
                            except ValueError:
                                try:
                                    #['11/07/2019', '#5 Grambling', 'SWAC WSOC Championship', 'L 0-1', '0']
                                    #['11/07/2019', '#6 Oakland', 'Horizon League WSOC Champ', 'W 2-1', '213']
                                    for conf in conference_champ_bs:
                                        cumulative = cumulative or any(conf in entry.lower() for entry in line)
                                    
                                    if(not cumulative):
                                        int("T")
                                    #if(not(any("championship" in entry.lower() for entry in line) or
                                           #any("champ" in entry.lower() for entry in line) or
                                           #any("northeast 10" in entry.lower() for entry in line) or
                                           #any("gliac" in entry.lower() for entry in line)
                                           #or any("northern sun" in entry.lower() for entry in line)
                                           #or any("sunshine state" in entry.lower() for entry in line)
                                           #or any("glvc" in entry.lower() for entry in line))):
                                        #int("T")
                                        
                                    int(line[4])
                                    
                                    if(any(entry == '@' for entry in line)):
                                        int("T")
                                        
                                    five_pass_3 = True
                                    
                                except ValueError:
                                    print("OOF")
                                    print(season)
                                    print(line)
                                    t = 5 + "T"
                            
                        if(five_pass_1):
                            #['08/21/2015', "'@", "'Arizona", "'L 0-4", "'", '86']
                            #we know it's away
                            game.set_date(line[0])
                            
                            t_line_num = 2

                            game.away_team = teams_top[len(teams_top) - 1].strip()
                            game.home_team = line[t_line_num].replace("@", "").strip()
                            
                            if(not(game.home_team in teams_bot)):
                                teams_bot.append(game.home_team.strip())
                            
                            #print(line[3])
                            score = line[3].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[3])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                            #print(game)
                        elif(five_pass_2):
                            #['09/13/2015', 'Texas Tech', '@Mulcahy Stadiu', 'L 0-1', '108']
                            game.set_date(line[0])
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            game.neutral = True
                            
                            score = line[3].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[3])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                        elif(five_pass_3):
                            #['11/07/2019', '#5 Grambling', 'SWAC WSOC Championship', 'L 0-1', '0']
                            game.set_date(line[0])
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(line[t_line_num][0] == '#'):
                                    game.home_team = line[t_line_num][line[t_line_num].find(' '):].strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(line[t_line_num][0] == '#'):
                                    game.home_team = line[t_line_num][line[t_line_num].find(' '):].strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())

                            score = line[3].split(" ")
                            
                            #if season == "480890.txt":
                                #print("score: " + str(score))
                                                        
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[3])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                        else:
                            print(line)
                            print(season)
                            
                            t = 1 + "T"
                    elif(len(line) == 6):
                        #PASS 1
                        #['08/28/2015', 'UTSA', '@Austi', 'exas', 'W 5-3', '0']
                        #PASS 2
                        #['11/03/2019', '@', '#4 Buffalo', 'MAC WSOC Championship', 'L 1-2 (2 OT)', '0']
                        #PASS 3
                        #['09/03/2010', '@', 'Waynesburg', '@Defiance Ohio', 'T 0-0 (2 OT)', '100']
                        
                        try:
                            int(line[5])
                            #print(season)
                            #print(line)
                            if(not('@' == line[2][0])):
                                int("T")
                                
                            if(not any("championship" in entry.lower() for entry in line)):
                                int("T")
                                
                            six_pass_1 = True
                            
                        except ValueError:
                            try:#['11/03/2019', '@', '#4 Buffalo', 'MAC WSOC Championship', 'L 1-2 (2 OT)', '0']
                                for conf in conference_champ_bs:
                                    cumulative = cumulative or any(conf in entry.lower() for entry in line)
                                #if(not(any("championship" in entry.lower() for entry in line)
                                #or any("gliac" in entry.lower() for entry in line) or
                                #any("northeast 10" in entry.lower() for entry in line) or
                                #any("lone star" in entry.lower() for entry in line)
                                #or any("northern sun" in entry.lower() for entry in line)
                                #or any("sunshine state" in entry.lower() for entry in line)
                                #or any("glvc" in entry.lower() for entry in line))):
                                if(not cumulative):
                                    int("T")
                                    
                                if(not('@' == line[1])):
                                    int("T")
                                    
                                six_pass_2 = True
                            except ValueError:
                                try:#['09/03/2010', '@', 'Waynesburg', '@Defiance Ohio', 'T 0-0 (2 OT)', '100']
                                    if(not('@' == line[1] and '@' in line[3])):
                                        int('T')
                                    
                                    six_pass_3 = True
                                except ValueError:
                                    print("OOF")
                                    print(season)
                                    print(line)
                                    t = 6 + "T"
                            
                        if(six_pass_1):
                            #['08/28/2015', 'UTSA', '@Austi', 'exas', 'W 5-3', '0']
                            #Nothing gets here
                            game.set_date(line[0])
                            
                            t_line_num = 1
                            if(not("@" in line[t_line_num])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            score = line[4].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[4])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                            
                            #print(game)
                        elif(six_pass_2):
                            #['11/03/2019', '@', '#4 Buffalo', 'MAC WSOC Championship', 'L 1-2 (2 OT)', '0']
                            game.set_date(line[0])
                            
                            t_line_num = 2
                            if(not("@" in line[1])):
                                game.home_team = teams_top[len(teams_top) - 1].strip()
                                game.away_team = line[t_line_num].replace("@", "").strip()
                                
                                if(line[t_line_num][0] == '#'):
                                   game.home_team = line[t_line_num][line[t_line_num].find(' '):].strip()
                                
                                if(not(game.away_team in teams_bot)):
                                    teams_bot.append(game.away_team.strip())
                            else:
                                game.away_team = teams_top[len(teams_top) - 1].strip()
                                game.home_team = line[t_line_num].replace("@", "").strip()
                                
                                if(line[t_line_num][0] == '#'):
                                    game.home_team = line[t_line_num][line[t_line_num].find(' '):].strip()
                                    
                                if(not(game.home_team in teams_bot)):
                                    teams_bot.append(game.home_team.strip())
                            
                            score = line[4].split(" ")
                                                        
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[4])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                                
                        elif(six_pass_3):
                            #['09/03/2010', '@', 'Waynesburg', '@Defiance Ohio', 'T 0-0 (2 OT)', '100']
                            game.set_date(line[0])
                            game.neutral = True
                            game.home_team = line[2].replace("@", "").strip()
                            
                            if(line[2][0] == '#'):
                               game.home_team = line[2][line[2].find(' '):].strip()
                               
                            game.away_team = teams_top[len(teams_top) - 1].strip()
                            
                            if(not(game.home_team in teams_bot)):
                                teams_bot.append(game.home.replace("@", "").strip())
                            
                            score = line[4].split(" ")
                            
                            active_team_score = 0
                            inactive_team_score = 0
                                                        
                            if(len(score) == 2 or (len(score) == 4 and "OT" in line[4])):
                                score = score[1].split("-")
                                inactive_team_score = score[1]
                                active_team_score = score[0]
                            elif(len(score) == 3):
                                active_team_score = score[0]
                                inactive_team_score = score[2]
                            elif(score[2] == '-'):
                                int(score[1])
                                int(score[3])
                                inactive_team_score = score[1]
                                game.away_score = score[3]
                            else:
                                int("T")
                                
                            if(game.home_team == teams_top[len(teams_top) - 1]):
                                game.home_score = active_team_score
                                game.away_score = inactive_team_score
                            else:
                                game.away_score = active_team_score
                                game.home_score = inactive_team_score
                    else:
                        #print(season)
                        #print(line)
                        #print(len(line))
                        #print("------Oof------")
                        
                        if(not(len(line) == 2)):
                            t = 1 + "T"
                            
                    #there are some doubles at the bottom of files -- this should counter that
                    '''
                    if("exempted" in line[0] or
                       any('ppd' == entry.lower() for entry in line) or
                       any('*' in entry for entry in line) or
                       any('\\n' in entry for entry in line) or
                       (any(entry == '@' for entry in line) and len(line) < 4))
                    '''
                    if(not(len(line) == 2) and
                       (len(data_load[season.strip()]) == 0) or
                        not(game == data_load[season.strip()][-1]) and
                        not("exempted" in line[0] or any('ppd' == entry.lower() for entry in line) or any('*' in entry for entry in line) or any('\\n' in entry for entry in line) or (any(entry == '@' for entry in line) and len(line) < 4))):    
                        add = True
                        filet = open("outputs_generated.txt", 'a')
                        try:
                            #if(game.away_team == "Vanderbilt"):
                                #print("t1")
                            game.away_team = TEAMS[game.away_team.replace("\n", "").strip()]
                            #if(game.away_team == "Vanderbilt"):
                                #print("t2")
                                #print(TEAMS["Vanderbilt"])
                        except KeyError:
                            #print(game.away_team)
                            if(len(game.away_team) > 0):
                                if(game.away_team[0] == '#'):
                                   game.away_team = game.away_team[game.away_team.find(' '):].strip()
                                   
                                filet.write(game.away_team + "\n")
                                TEAMS[game.away_team.replace("\n", "").strip()] = game.away_team.replace("\n", "").strip()
                                
                                if(game.away_team == "Vanderbilt"):
                                    print('oof')
                            else:
                                add = False
                        try:
                            game.home_team = TEAMS[game.home_team.replace("\n", "").strip()]
                        except KeyError:
                            #print(game.home_team)
                            if(len(game.home_team) > 0):
                                if(game.home_team[0] == '#'):
                                   game.home_team = game.home_team[game.home_team.find(' '):].strip()
                                   
                                filet.write(game.home_team + "\n")
                                TEAMS[game.home_team.replace("\n", "").strip()] = game.home_team.replace("\n", "").strip()
                            else:
                                add = False
                                
                        
                        filet.close()
                        
                        #print(TEAMS["Vanderbilt"])
                        
                        if ("unknown" in game.home_team or
                            "unknown" in game.away_team):
                                add = False
                                
                        if( "not_" in game.home_team or
                            "not_" in game.away_team):
                                add = False
                        if(add):
                            data_load[season.strip()].append(game)
                            
                            #if(not(game.home_team) in teams):
                                #teams[game.home_team] = game.home_team
                                
                            #if(not(game.away_team) in teams):
                                #teams[game.home_team] = game.away_team
                            #print(game)
                            #print(season)
                            
                            #just a check to ensure we have numeric values for scores
                            #verify our parsing was correct
                            game.away_score = int(game.away_score)
                            game.home_score = int(game.home_score)
                            count += 1
                            oof = False
                            
                            if(False and
                               season == '21216.txt' and
                               not five_pass_1):
                                    print("HERE")
                                    print(game)
                                    print("3_1: " + str(three_pass_1))
                                    print("3_2: " + str(three_pass_2))
                                    
                                    print("4_1: " + str(four_pass_1))
                                    print("4_2: " + str(four_pass_2))
                                    print("4_3: " + str(four_pass_3))
                                    
                                    print("5_1: " + str(five_pass_1))
                                    print("5_2: " + str(five_pass_2))
                                    print("5_3: " + str(five_pass_3))
                                    
                                    print("6_1: " + str(six_pass_1))
                                    print("6_2: " + str(six_pass_2))
                                    print("6_3: " + str(six_pass_3))
                                    #print()
                            elif(oof):
                                x = 1 + "T"
                        
                            #################################################################
                            if('@' in teams_bot[-1] and teams_bot[-1]):
                                print("---------------")
                                print("OOF")
                                print(teams_bot[-1])
                                print(season)
                                print(game)
                            #print(count)
                            
                            #print("--------------------------")
                            #print(str(count) + ": " + game.__repr__())
                            #time.sleep(.2)
                        #print(len(data_load[season]))
                        
                        #let's literally do this the slow way
                        
                        #t = 1 + "!"
        finally:
            file.close()
            
    #print(len(list(set(teams_top))))
    #print(len(teams_bot))
    
    #return teams
    
    #SOME FINAL PROCESSING BEFORE WE GO
    print("FINAL LOADING")
    
    #dictionary of entries
    #each key directs to the edited version
    edits = {}
  
    for s in data_load:
        for g in data_load[s.strip()]:
            if('#' in g.away_team):
                # '#4 Vanderbilt'
                edits[g.away_team] = g.away_team[g.away_team.find(" "):]
                g.away_team = g.away_team[g.away_team.find(" "):].strip()
            if('#' in g.home_team):
                edits[g.home_team] = g.home_team[g.home_team.find(" "):]
                g.home_team = g.home_team[g.home_team.find(" "):].strip()
                
    teams_bot = list(set(teams_bot))
    
    for key in edits:
        teams_bot.remove(key)
        teams_bot.append(edits[key].strip())
        
    teams_bot = list(set(teams_bot))
    print("DATA LODING")
    
    return data_load, list(set(teams_top)), teams_bot, TEAMS
    

#======================================================================================================

def post_read_processing():
    print("Beginning execution. . .")
    data_raw, teams_top, teams_bot = read_true_data()
    print("Data read into program!")
    print("Beginning data pre-processing. . .")
    teams = {}
    
    t_temp = []
    for t in teams_bot:
        if not(t.strip() == t):
            t_temp.append(t)
            
    for t in t_temp:
        teams_bot.remove(t)
        teams_bot.append(t.strip())
    #so before we change it it can still assign values from here assuming the mapping is correct
    #Season.update() to see why we need to to be applied indistinguishably
    for t in teams_bot:
        teams[t] = t
    
    #FIND OUT WHAT TEAMS EVERY GAME ACTUALLY IS
    #STEPS:
    #1 -- create the seasons ✓
    #2 -- go through each team_bot and if only a substring of one team_top, then pair them in teams ✓
    #3 -- Print out the number of remaining teams and then the teams so that we can see if we a.)
    #     need to automate the final bit or if we can do it by hand and b.) can see what errors might
    #     be (for example #1 UCLA would need to be rewritten as UCLA) ✓
    #4 -- Should we still have a bunch of teams, go through seasons to match up teams with their
    #     games -- each game exists in the home and away season so we can say "akrons and akron zips have
    
    #STEP 1
    seasons = {}
    '''
    for g in data_raw['53863.txt']:
        try:
            print(g)
        except AttributeError:
            t = 1 + "T"
            #'''
    MASTERLIST = []
    for top_team in teams_top:
        seasons[top_team] = {}#put in year, get out season
    
    print("Building seasons. . .")
    
    for season in data_raw:
        s = Season()
        #print(seasons.keys())
        #print(data_raw[season])
        if(len(data_raw[season]) > 0):
            #print(season)
            #print(season)
            #try:
            s.add_game(data_raw[season])
            
            #print(s.team)
            
            #if(s.team == "Ohio Wesleyan Battling Bishops"):
                #print(s.games)
                #print(s.team)
                #print(s.year)
                #pass
            
            #print(s.team)
            #print(s.year)
            if s.team == "Keuka":
                s.team = "Keuka Wolves"
            try:
                
                seasons[s.team][s.year] = s
            except KeyError:
                seasons[s.team] = {}
                seasons[s.team][s.year] = s
                print(len(seasons[s.team]))
                print(s.team)
                print()
            #except ValueError:
                #MASTERLIST.append(season)
        else:
            pass
            
    #print(MASTERLIST)
    #x = 1 + "R"
        #season is constructed
    #print("Season Check 1")
    #print(seasons["Utah Utes"][2019].games)
    #print("-----")
    #print(seasons["Washington St. Cougars"][2019].games)
    #STEP 2
    index = 0
    while(index < len(teams_bot)):
        #we see how many top_teams bot_team is a substraing of
        subs = []
        
        
        for top_team in teams_top:
            if teams_bot[index] in top_team:
                subs.append(top_team)
                
        #we set it so whichever comes through it will return the same output
        if(len(subs) == 1):
            teams[subs[0]] = subs[0]
            teams[teams_bot[index]] = subs[0]
            teams_bot.pop(index)
            
        else:
            index += 1
            
    #print(len(teams_bot))
    #print(teams_bot)
    
    #STEP 4
    #we will start with year = 2019 and work our way backwards
    
    teams = hand_written_update(teams)
    
    t_remove = []
    
    for t in teams_bot:
        if not(teams[t] == t):
            t_remove.append(t)
            
    for t in t_remove:
        teams_bot.remove(t)
    
    #UPDATING TEAMS
    print("Final update before step 4")
    for tm in seasons:
        for yr in seasons[tm]:
            #print(tm)
            #print(yr)
            #print(seasons[tm][yr].games)
            try:
                seasons[tm][yr].update(teams)
            except KeyError:
                print(tm)
                print("Year: " + str(yr))
                print(seasons[tm][yr].games[0].date)
                for g in seasons[tm][yr].games:
                    print(g)
                #print(seasons[tm][yr].games)
                print()
                t = 1 + "T"
    
    year = 2019
    
    print("Step 4 processing on teams")
    
    #print(teams["Washington"])
    #print(teams["Washington St."])
    
    while(len(teams_bot) > 0):
        index = 0
        #if no entries were deleted then we can go to a lower year BUT otherwise newly deleted entries may
        #have yielded previously missing 
        delta = 0
        
        while(index < len(teams_bot)):
            #we get a value to find
            team_bot = teams_bot[index]
            
            #go through each team we've found
            for top_team in teams_top:
                #check if the team plays team_bot
                try:
                    #We check to see if it faces our unknown team
                    if(not(team_bot in top_team) and seasons[top_team][year].is_opponent(team_bot)):
                        #print(team_bot)
                        #print(top_team)
                        #print(seasons[top_team][year].opponents)
                        #print("\n")
                        
                        
                        #so for a team do they play this team?
                        #If we're here, they do!
                        
                        #we get the first game they play against each other
                        game = seasons[top_team][year].first_game_vs_opponent(team_bot)
                        
                        #this is functional
                        
                        #then we need to find every game that is identical to this one after finding this game
                        team_names = []
                        
                        for dummy_team in list(seasons.keys()):
                            if(not(dummy_team == top_team)):
                                try:
                                    #We're looking for a game against the same team, but we don't look at team_bot
                                    #if the teams play the same day with the same score, and both have the same
                                    #opponent at home or away, then we collect those
                                    if(seasons[dummy_team][year].is_opponent(top_team)):
                                        #print("-----------")
                                        #print("YEET")
                                        if(seasons[dummy_team][year].first_game_vs_opponent(top_team).date == game.date):
                                            #print("Team Bot: " + str(team_bot))
                                            #print("Team Top: " + str(top_team))
                                            #print("Dummy: " + str(dummy_team))
                                        #g = seasons[dummy_team][year].equivalent_game(game)
                                            #print(seasons[dummy_team][year].first_game_vs_opponent(top_team))
                                            #print(game)
                                            #print("\n")
                                            #if(dummy_team == "Utah Utes" and
                                               #top_team == "Washington St. Cougars" and
                                               #team_bot == "Utah"):
                                                #print(seasons[dummy_team][year].games)
                                                #t = 1 + "T"
                                            #time.sleep(.8)
                                            
                                            
                                            
                                            if(seasons[dummy_team][year].first_game_vs_opponent(top_team).equivalent_game(game)):
                                        
                                            #if(not(g==-1)):
                                                #print(g)
                                                #print(game)
                                                #print(dummy_team)
                                                #print(top_team)
                                                #print(team_bot)
                                                #print("---------")
                                                #time.sleep(.8)
                                                #if we found an equivalent game
                                                team_names.append(dummy_team)
                                                #store the name
                                except KeyError:
                                    pass
                                
                        #print(len(team_names)) 
                        #now if team_names is of length 1, only one team had the indentical game
                        #therefore, we have ourselves match  mister!
                        if(len(team_names) == 1):
                            #we store the team
                            teams[team_bot] = team_names[0]
                            teams[team_names[0]] = team_names[0]
                            
                            #we pop the previous name
                            teams_bot.pop(index)
                            
                            #update delta
                            delta += 1
                            
                            #and we break out of the for loop since we're done here
                            break
                        elif(len(team_names) > 1):
                            print(len(team_names))
                except KeyError:
                    pass
            
            index += 1
            
        print("CHECKING DELTA")
        print(len(teams_bot))
        
        if(len(teams_bot) == 17):
            break
        
        if(delta == 0):
            year -= 1
            print(year)
            
            if(year < 2008):
                year = 2019
                
            if(len(teams_bot) == 385):
                print(teams)
                print("------")
                print(teams_bot)
                t = 1 + "R"
        else:
            #there was at least 1 change!
                #UPDATING TEAMS
            for tm in seasons:
                for yr in seasons[tm]:
                    seasons[tm][yr].update(teams)
                
    print(teams)
    print(len(teams_bot))
    print(teams_bot)
    
    print("Data preprocessing complete!")
#post_read_processing()
'''
DATA REMOVED BELOW
---------------
26345 -- ['09/08/2017', 'Delta St.']
NOTE: For the above, there was no score online for either team -- for whatever reason it wasn't reported
      to NCAA or included in their database -- either way since we can't do anything with it I removed it
63803 -- ['11/15/2012', '@', 'CCNY']
82858 -- ['12/05/2014', 'Grace (IN)', '@Kissimmee, FL']
21075 -- ['*Contest exempted and does not count toward season record or statistics for Humboldt St. only.']
21081 -- ['*Contest exempted and does not count toward season record or statistics for Lewis only.']
21097 -- ['*Contest exempted and does not count toward season record or statistics for Missouri S&T only.']
21119 -- ['*Contest exempted and does not count toward season record or statistics for St. Cloud St. only.']
Files where I did the above:
    21120
    21429
    
    
479430 -- Aparently they played 2 games in a day so I moved the second game a day later
'''

'''
UNKNOWN TEAMS:
    59292:
['10/25/2008', '@ Unknown team 506282', 'L 0 - 8']
['11/03/2008', '@ Unknown team 506282', 'L 0 - 9']
['11/03/2008', '@ Unknown team 506282', 'L 0 - 9']

59282:
    
['10/18/2008', 'Unknown team 506282', 'W 7 - 0']

59173:
    
['11/01/2008', '@ Unknown team 506282', 'T 0 - 0']

382251:
    ['09/24/2002', 'Unknown team 512', 'L 1 - 5']
    
381901:
    
['10/10/2007', '@ Unknown team 512', 'W 2 - 0']
['10/29/2007', 'Unknown team 512', 'L 0 - 1'] ** MAY BE IN 381827 I FORGET MY B SHOULDN'T MATTER

381827:
    ['09/11/2007', 'Unknown team 506186', 'W 4 - 2']
    
58711:
    
['09/09/2008', '@ Unknown team 512', 'W 3 - 0']

58906:
    
['09/02/2008', '@ Unknown team 512', 'L 1 - 2']

381207:
    
['09/18/2007', '@ Unknown team 512', 'L 0 - 5']

['10/31/2007', 'Unknown team 512', 'L 0 - 2']
['10/31/2007', 'Unknown team 512', 'L 0 - 2']

381248:
    
['09/08/2007', '@ Unknown team 506186', 'L 0 - 3']

381337:
    
['09/03/2007', 'Unknown team 512', 'T 1 - 1']

381345:
    
['09/10/2007', 'Unknown team 506282', 'W 3 - 0']

381783:
    
['10/02/2007', '@ Unknown team 506282', 'W 4 - 1']

381787:
    
['09/15/2007', '@ Unknown team 506282', 'W 6 - 1']

381896:
    
['09/22/2007', '@ Unknown team 512', 'W 2 - 1']
['11/02/2007', 'Unknown team 512', 'W 4 - 1']
['11/02/2007', 'Unknown team 512', 'W 4 - 1']

381823:
    
['09/29/2007', 'Unknown team 512', 'W 3 - 2']
['10/01/2007', 'Unknown team 512', 'L 2 - 3']

381809:
    
['09/22/2007', '@ Unknown team 506282', 'W 3 - 2']

381900:

['10/27/2007', 'Unknown team 512', 'L 0 - 3']

['10/14/2007', '@ Unknown team 512', 'L 1 - 4']

380995:
    
['09/27/2006', 'Unknown team 506282', 'W 5 - 0']

480908.txt:
['08/26/2019', 'South Carolina St.', 'Ppd']
'''