# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:46:32 2020

@author: Kieran
"""

import os
import true_data_prep as TDP
from datetime import datetime
from data_loader import data_loader

class Game:
    def __init__(self, h, a, h_score, a_score, h_pens=0, a_pens=0, neut=False):
        self.home = h
        self.away = a
        
        self.home_score = int(h_score)
        self.away_score = int(a_score)
        
        self.home_pens = int(h_pens)
        self.away_pens = int(a_pens)
        self.neutral = neut
        
    def __repr__(self):
        return self.home + " " + str(self.home_score) + " vs. " + str(self.away_score) + " " + self.away

class Input_Data():
    #FOR THE TIME BEING NO DIVISION
    def __init__(self):
        #X DATA
        self.pass_num_h = 1
        self.pass_num_a = 1
        self.game_num_h = 1
        self.game_num_a = 1
        #for the time being we aren't using division but to be implemented!
        self.division_h = 1
        self.division_a = 1
        
        #None means we need to get if from a previous instance etc.
        self.attack_home = None
        self.defense_home = None
        self.attack_away = None
        self.defense_away = None
        
        #is it a neutral field
        self.neutral_field = False
        
        self.goals_home = 0
        self.goals_away = 0
        self.pens_home = 0
        self.pens_away = 0
        
        #Y DATA
        self.true_attack_h = None
        self.true_defense_h = None
        self.true_attack_a = None
        self.true_defense_a = None
        
        #ADDED DATA FOR TRUE DATA
        self.home = ""
        self.away = ""
        
    #CURRENTLY 14 FEATURES
    #15 WHEN WE ADD IN DIVISION
    def data_representation(self):
        data = str(self.pass_num_h) + "," + str(self.pass_num_a) + "," + str(self.game_num_h) + "," + str(self.game_num_a) + ","
        data += str(self.attack_home) + "," + str(self.defense_home) + "," + str(self.attack_away) + "," + str(self.defense_away) + ","
        data += str(self.goals_home) + "," + str(self.goals_away) + "," + str(self.pens_home) + "," + str(self.pens_away) + ","
        #WE MAKE A VARIABLE TO REPRESENT WHETHER OR NOT THERE WERE PENALTIES AND ENCODE IT TO 1 OR 0
        if(self.pens_away + self.pens_home > 0):
            data += "1,"
        else:
            data += "0,"
            
        #WE ENCODE THE BOOLEAN TO 1 OR 0
        if(self.neutral_field):
            data += "1"
        else:
            data += "0"
            
        return data
    
    def y_data_representation(self):
        data = str(self.true_attack_h) + "," + str(self.true_defense_h) + "," + str(self.true_attack_a) + "," + str(self.true_defense_a)
        
        return data
        
    def __repr__(self):
        name = ""
        
        name += "Passes: " + str(self.pass_num_h) + " " + str(self.pass_num_a) + " ; Games: " + str(self.game_num_h) + " " + str(self.game_num_a) + "\n"
        name += "Score: " + str(self.goals_home) + "-" + str(self.goals_away)
        if(self.pens_home + self.pens_away > 0):
            name += "(" + str(self.pens_home) + "-" + str(self.pens_away) + ")"
            
        name += "\n"
        
        name += "Attacks: " + str(self.attack_home) + ", " + str(self.attack_away) + "; Defense: " + str(self.defense_home) + ", " + str(self.defense_away) + "\n"
        name += "TRUE Attacks: " + str(self.true_attack_h) + ", " + str(self.true_attack_a) + "; TRUE Defense: " + str(self.true_defense_h) + ", " + str(self.true_defense_a) + "\n"
        
        return name

"""
print(p[1][1][1][0].data_representation())
print(p[1][1][1][0].y_data_representation())
print(t[1][1][1][0])
1,1,1,1,2.6,2.6,2.6,2.6,3,1,0,0,0,0
1.235948663632983,1.6561187321832838,2.8623776301601063,1.5936604425287078
('No.17', 'No.18')
"""
def write_batch_data_2():
    data, team_pairs, teams = prep_data()

def write_true_data():
    data_raw, teams_top, teams_bot, teams = TDP.read_true_data()
    #print("LEGGO")
    batch = 1
    
    #teams = data_loader()
    '''
    seasons = {}
    for top_team in teams:
        seasons[top_team] = {}#put in year, get out season

    for season in data_raw:
        s = Season()
        if(len(data_raw[season]) > 0):
            s.add_game(data_raw[season])
            
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
        else:
            pass'''
    #data is as such: data[team][year] returns a season which we can use to get 
    
    
    
    #1.) first we put games into lists by the day they're played
    #days are sorted by year for obvious reasons
    #2.) Then, we made teh data_representation objects for each game
    #3.) Then we write them to file
    
    print("Data Gotten: BATCH TIME")
    
    #data is as such: data[text file] returns a list of games which we can use to get information
    schedule = {}
    #schedule holds the games in a list for each date
    sched = {}
    #sched holds the list of dates for a year so we can order them
    sched_mappings = {}
    #sched holds the mappings from date to number
    input_objects = {}
    #holds the input objects
    pass_nums = {}
    #takes in a team and returns (game #, pass #)
    for season in data_raw:
        if(len(data_raw[season]) > 0):
            #we can get a list of Load_Games
            #datetime.strptime(date, "%m/%d/%Y")
            year = data_raw[season][0].date.year
            #year = datetime.strptime(data_raw[season][0].date, "%m/%d/%Y").year
            schedule[year] = {}
            sched[year] = []
            input_objects[year] = {}
            
            
    for team in teams:
        pass_nums[teams[team]] = (1, 1)
    
    for season in data_raw:
        if(len(data_raw[season]) > 0):
            file = open("Data_Final/" + season, 'r')
            
            team = file.readline().strip()
            
            file.close()
            
            year = data_raw[season][0].date.year
            
            for game in data_raw[season]:
                try:
                    schedule[year][game.date].append(game)
                except KeyError:
                    schedule[year][game.date] = [game]
                    
                sched[year].append(game.date)
            
    for year in sched:
        sched[year].sort()
        
        for n in range(0, len(sched[year])):
            sched_mappings[sched[year][n]] = n + 1
            input_objects[year][n + 1] = []

                
    #now we need to make the games and then we should be good to go
    counter = 1
    for year in schedule:
        for date in schedule[year]:
            for game in schedule[year][date]:
                i = Input_Data()
                
                i.home = game.home_team
                i.away = game.away_team
                
                i.game_num_a, i.pass_num_a = pass_nums[i.away]
                pass_nums[i.away] = (i.game_num_a + 1, i.pass_num_a + 1)
                i.game_num_h, i.pass_num_h = pass_nums[i.home]
                pass_nums[i.home] = (i.game_num_h + 1, i.pass_num_h + 1)
                
                i.neutral_field = game.neutral
                
                i.goals_home = game.home_score
                i.goals_away = game.away_score
                
                #now add it to the final schedule and we gucci
                sched_mappings[game.date]
                
                if(i.pass_num_h < counter and
                   i.pass_num_a < counter):
                    try:
                        input_objects[year][sched_mappings[game.date]].append(i)
                    except KeyError:
                        input_objects[year][sched_mappings[game.date]] = [i]
                #print(game)
                #print(i.data_representation())
            counter += 1
            #counter COUNTERS duplicate days
        
        for team in pass_nums:
            #we must update as now we'll be at game 1 but the same number of passes
            pass_nums[team] = (1, pass_nums[team][1])
                
                
    #t = 1 + "T"
    
    count = 1
    
    for year in input_objects:
        for mapping in input_objects[year]:
            if(len(input_objects[year][mapping]) > 0):
                try:
                    file_x = open("Final_Prepared_Data/x_" + str(count) + ".txt", 'w')
                    file_t = open("Final_Prepared_Data/t_" + str(count) + ".txt", 'w')
                    
                    for input_obj in input_objects[year][mapping]:
                        file_x.write(input_obj.data_representation() + "\n")
                        file_t.write(input_obj.home + "," + input_obj.away + "\n")
                        
                finally:
                    file_x.close()
                    file_t.close()
                    
                    count += 1
             
print("COMPLETED!")
            
'''            
    for data_set in data.keys():
        print("Data set " + str(data_set))
        seasons = list(data[data_set].keys())
        seasons.sort()
        
        batch = 1
        
        for season in seasons:
            match_days = list(data[data_set][season].keys())
            match_days.sort()
            
            for match_day in match_days:
                try:
                    try:
                        os.mkdir("Final_Neural_Net_Data/" + str(data_set))
                    except FileExistsError:
                        pass
                    file_x = open("Neural_Net_Data/" + str(data_set) + "/batch_x_" + str(batch) + ".txt", 'w')
                    file_teams = open("Neural_Net_Data/" + str(data_set) + "/batch_t_" + str(batch) + ".txt", 'w')
                    
                    for match in range(0, len(data[data_set][season][match_day])):
                        file_x.write(data[data_set][season][match_day][match].data_representation() + "\n")
                        file_teams.write(str(team_pairs[data_set][season][match_day][match][0]) + "," +
                                         str(team_pairs[data_set][season][match_day][match][1]) + "\n")
                        
                    
                finally:
                    file_x.close()
                    file_teams.close()
                    
                    #each match_day is a single batch
                    #NOTE: As of right now there are going to be some small batches, the final batch of a season being a single game (a tournament game)
                    batch += 1
'''
def write_batch_data():
    #data is data (see above prints -- p)
    #team_pairs is for each match the two teams, home and away, that are participating
    #teams is a dictionary you put in the team and get back a dictionary with "Attack" and "Defense" that is 2.6 and will be the outputs and etc.
    data, team_pairs, teams = prep_data()
    #print("LEGGO")
    batch = 1
    
    print("Data Gotten: Time To Write Batches")
    
    for data_set in data.keys():
        print("Data set " + str(data_set))
        seasons = list(data[data_set].keys())
        seasons.sort()
        
        batch = 1
        
        for season in seasons:
            match_days = list(data[data_set][season].keys())
            match_days.sort()
            
            for match_day in match_days:
                try:
                    try:
                        os.mkdir("Neural_Net_Data/" + str(data_set))
                    except FileExistsError:
                        pass
                    file_x = open("Neural_Net_Data/" + str(data_set) + "/batch_x_" + str(batch) + ".txt", 'w')
                    file_y = open("Neural_Net_Data/" + str(data_set) + "/batch_y_" + str(batch) + ".txt", 'w')
                    file_teams = open("Neural_Net_Data/" + str(data_set) + "/batch_t_" + str(batch) + ".txt", 'w')
                    
                    for match in range(0, len(data[data_set][season][match_day])):
                        #each individual datum
                        #print("[" + str(data_set) + "]" + "[" + str(season) + "]" + "[" + str(match_day) + "]" + "[" + str(match) + "]")
                        #if(batch == 8):
                            #print(team_pairs[data_set][season][match_day][match])
                            #print(data[data_set][season][match_day][match].pens_home)
                            #print(data[data_set][season][match_day][match].pens_away)
                            #print(data[data_set][season][match_day][match])
                        
                        file_x.write(data[data_set][season][match_day][match].data_representation() + "\n")
                        file_y.write(data[data_set][season][match_day][match].y_data_representation() + "\n")
                        file_teams.write(str(team_pairs[data_set][season][match_day][match][0]) + "," +
                                         str(team_pairs[data_set][season][match_day][match][1]) + "\n")
                        
                    
                finally:
                    file_x.close()
                    file_y.close()
                    file_teams.close()
                    
                    #each match_day is a single batch
                    #NOTE: As of right now there are going to be some small batches, the final batch of a season being a single game (a tournament game)
                    batch += 1
    

#home = boolean --> We are looking for home team
#num_game = number --> this game in the opponent's schedule
#RETURNS TUPLE (pass, game)
def get_game_pass_nums(games, data_set, season, game, num_game, home):
    #1.) see how many times these teams played in this season
    #2.) If this is the nth time they've played, find the nth game they've played together
    #3.) count how many games have been played up to that point for games, for passes also add all previous lists of games
    #4.) return this stuff
    
    #step 0 -- get ready for other steps
    index = num_game - 1
    occurances = 0
    team = ""
    opponent = ""
    
    if(home):
        team = game.home
        opponent = game.away
    else:
        team = game.away
        opponent = game.home
    
    #step 1
    while(index > -1):
        g = games[data_set][season][opponent][index]
        
        #one of them IS team opponent so we just need to see if the other team is our boi
        if(g.home == team or g.away == team):
            #should it be our boi, occurances +1
            #we start at the index so we +1 even if we know pre-emptively yeet it's a go
            #note this is done because if it's the first game we don't want to start with index = num_game - 2 if that would result in an index of -1
            occurances += 1
            
        index -= 1
    
    index = 0
    running = True
    #step 2
    while(running):
        g  = games[data_set][season][team][index]
        if(g.home == opponent or g.away == opponent):
            occurances -= 1
            
        if(occurances == 0):
            running = False
            
        #so we preserve index if this is THE game
        if(occurances > 0):
            index += 1
            
    #step 3 -- index is the game number
    game_num = index + 1#index starts at 0 game num starts at 1
    
    pass_num = game_num
    
    #we have to sum the previous lists to get our pass_num
    for s in range(season-1, 0, -1):
        pass_num += len(games[data_set][s][team])
        
    #step 4 -- RETURN THAT DATA MOFO
    return (pass_num, game_num)
        
    

"""
prep_data() basically converts all the data into a Input_Data object so it is ready to be used in the neural network

"""
def prep_data():
    true_values, games = read_data()
    #dataset
    #------ season
    #------ ------ match-day
    data = {}
    valid = {}
    team_pairings = {}
    all_teams = {}
    
    #For valid
    #now we recreate games EXCEPT we have booleans and whenever we make a game we set that
    for data_set in games.keys():
        valid[data_set] = {}
        team_pairings[data_set] = {}
        for season in games[data_set].keys():
            valid[data_set][season] = {}
            team_pairings[data_set][season] = {}
            for team in games[data_set][season].keys():
                valid[data_set][season][team] = []
                
                for game in games[data_set][season][team]:
                    valid[data_set][season][team].append(True)
                
    
    
    #NOTE: FOR A HOT SEC THESE BOTH HAVE THE SAME SHAPE!
    for data_set in games.keys():
        data[data_set] = {}
        
        for s in games[data_set].keys():
            data[data_set][s] = {}
        #Why start here?
        #basically because of the num_passes we want to start here and iterate over each team THEN by season so we can easily keep track of
        #the number of passes
        for team in games[data_set][1].keys():
            all_teams[team] = {"Attack":2.6, "Defense":2.6}
            num_game = 1
            num_pass = 1
            
            #basically with  keys it isn't sorted and our code needs to move in order of occurances
            seasons = list(games[data_set].keys())
            seasons.sort()
            
            for season in seasons:
                #now we have our 3 constants
                #NOW we cycle through each game in a given season
                num_game = 1
                
                for game in games[data_set][season][team]:
                    if(valid[data_set][season][team][num_game - 1]):
                        valid[data_set][season][team][num_game - 1] = False
                        
                        datum = Input_Data()
                        datum.goals_home = game.home_score
                        datum.goals_away = game.away_score
                        datum.pens_home = game.home_pens
                        datum.pens_away = game.away_pens
                        
                        datum.neutral_field = game.neutral
                        
                        if(game.home == team):
                            datum.pass_num_h = num_pass
                            datum.game_num_h = num_game
                            #(games, data_set, season, game, num_game, home)
                            datum.pass_num_a, datum.game_num_a = get_game_pass_nums(games, data_set, season, game, num_game, False)
                            
                            #set that game to invalid because it isn't valid anymore -- NO DUPLICATES PLEASE
                            valid[data_set][season][game.away][datum.game_num_a - 1] = False
                            
                            #print("[" + str(data_set) + "]" + "[" + str(season) + "]" + "[" + str(team) + "]" + "[" + str(num_game - 1) + "]")
                            #print("[" + str(data_set) + "]" + "[" + str(season) + "]" + "[" + str(game.away) + "]" + "[" + str(datum.game_num_a - 1) + "]")
                            
                            #t = 1 + "T"
                            
                            #initial i.e. we have no attack or defense scores yet
                            if(num_pass == 1):
                                datum.attack_home = 2.6
                                datum.defense_home = 2.6
                                
                            if(datum.pass_num_a == 1):
                                datum.attack_away = 2.6
                                datum.defense_away = 2.6
                                
                            #NOW IMPUT THE TRUE ATTACKS AND DEFENSES
                            datum.true_attack_h = true_values[data_set][season][team]["Attack"]
                            datum.true_defense_h = true_values[data_set][season][team]["Defense"]
                            datum.true_attack_a = true_values[data_set][season][game.away]["Attack"]
                            datum.true_defense_a = true_values[data_set][season][game.away]["Defense"]
                        else:
                            datum.pass_num_a = num_pass
                            datum.game_num_a = num_game
                            #(games, data_set, season, game, num_game, home)
                            datum.pass_num_h, datum.game_num_h =  get_game_pass_nums(games, data_set, season, game, num_game, True)
                            
                            #set that game to invalid because it isn't valid anymore -- NO DUPLICATES PLEASE
                            #print("Master: " + str(valid[data_set][season][game.away]))
                            #print("Value: " + str(valid[data_set][season][game.away][datum.game_num_h - 1]))
                            valid[data_set][season][game.away][datum.game_num_h - 1] = False
                            
                            #initial i.e. we have no attack or defense scores yet
                            if(num_pass == 1):
                                datum.attack_away = 2.6
                                datum.defense_away = 2.6
                                
                            if(datum.pass_num_h == 1):
                                datum.attack_home = 2.6
                                datum.defense_home = 2.6
                                
                            #NOW IMPUT THE TRUE ATTACKS AND DEFENSES
                            datum.true_attack_h = true_values[data_set][season][game.home]["Attack"]
                            datum.true_defense_h = true_values[data_set][season][game.home]["Defense"]
                            datum.true_attack_a = true_values[data_set][season][team]["Attack"]
                            datum.true_defense_a = true_values[data_set][season][team]["Defense"]
                        
                        #add it to the data
                        try:
                            data[data_set][season][num_game].append(datum)
                            team_pairings[data_set][season][num_game].append((game.home, game.away))
                        except KeyError:
                            data[data_set][season][num_game] = []
                            data[data_set][season][num_game].append(datum)
                            
                            team_pairings[data_set][season][num_game] = []
                            team_pairings[data_set][season][num_game].append((game.home, game.away))
                            
                        
                    
                    #increment because we've gotten past one game
                    num_pass += 1
                    num_game += 1
    return (data, team_pairings, all_teams)

"""
read_data() will read in all the dummy data in the files so that it can be processed for the neural network
returns a tuple of two dictionaries as described below
"""
#Tuple 0 = True Attacks/Defense
#[dataset][season][team name(STRIPED)]
#ex.[1][9]["No.5"] is team No. 5 in season 9 in dataset 1, returns a dictionary with "Attack" and "Defense"
#Tuple 1 = games
#[dataset][season][team name(STRIPED)]
#ex. [1][9]["No.5"] is team No. 5 in season 9 in dataset 1, returns a list of all games IN THE ORDER THEY OCCUR
def read_data():
    data_sets = os.listdir("Dummy_Data")
    
    true_values = {}
    games = {}
    #data_set
    #team
    #season
    #values
    #ex: 1
    #       1
    #          No. 1
    #                Attack, Defense
    #in dataset 1, the team "No. 1" in Season one attack and defense
    #for data_set in data_sets:
    for data_set in ['101']:
        #we have a number for each set
        #1 is comprised of a single set of conferences and etc. through 16 seasons
        data_set_data = os.listdir("Dummy_Data/" + data_set)
        
        true_values[int(data_set)] = {}
        games[int(data_set)] = {}
        season = 1
        for data in data_set_data:
            #data is a file in the data
            try:
                file = open("Dummy_Data/" + data_set + "/" + data)
                
                #season = 1
                if(data.split('_')[0][-2] == '1'):
                    season = int(data.split('_')[0][-2:])
                elif(not("NCAA" in data)):
                    #print(data.split('_')[0])
                    season = int(data.split('_')[0][-1])
                else:
                    season = int(data.split('_')[1].split('.')[0])
                
                try:
                    x = games[int(data_set)][season]
                except KeyError:
                    games[int(data_set)][season] = {}
                
                try:
                    x = true_values[int(data_set)][season]
                except KeyError:
                    true_values[int(data_set)][season] = {}
                #first we skip tournament since that is the LAST event of the season
                if(not("NCAA") in data):
                    #conference NOT tournamnet
                    if("_games" in data):
                        #this is the list of games
                        for line in file:
                            row = get_row_from_line(line)
                            game = Game(row[0], row[1], row[2], row[3])
                            
                            try:
                                games[int(data_set)][season][row[0]].append(game)
                            except KeyError:
                                games[int(data_set)][season][row[0]] = []
                                games[int(data_set)][season][row[0]].append(game)
                                
                            try:
                                games[int(data_set)][season][row[1]].append(game)
                            except KeyError:
                                games[int(data_set)][season][row[1]] = []
                                games[int(data_set)][season][row[1]].append(game)
                                
                    elif("_summaries" in data):
                        #this is a list of teams and their true values
                        #print(data)
                        for line in file:
                            row = get_row_from_line(line)
                                
                            true_values[int(data_set)][season][row[0]] = {"Attack": row[1], "Defense": row[2]}
            finally:
                #print(games)
                #print("FINALLY\n")
                file.close()
        try:
            for season in range(1, 16):
                file = open("Dummy_Data/" + data_set + "/NCAA Nationals_" + str(season) + ".txt.")
                #print(data)
                for line in file:
                    row = get_row_from_line(line)
                    
                    #print(row)
                    #print(file)
                    
                    game = ""
                    
                    try:
                        game = Game(row[0], row[1], row[2], row[3], row[4], row[5])
                    except IndexError:
                        game = Game(row[0], row[1], row[2], row[3])
                        
                    game.neutral = True
                    
                    #print(games)
                    #we know these arrays are made so we can just add them
                    games[int(data_set)][season][row[0]].append(game)
                    games[int(data_set)][season][row[1]].append(game)
        finally:
            file.close()
            #print(games)
    
    return (true_values, games)

#no need to csv parse when we can easily convert to the list of entries from
#standard io libraries
def get_row_from_line(line):
    line = line.strip()
    row = line.replace(" ", "")
    row = row.split(',')
    
    return row
#Tuple 0 = True Attacks/Defense
#[dataset][season][team name(STRIPED)]
#ex.[1][9]["No.5"] is team No. 5 in season 9 in dataset 1, returns a dictionary with "Attack" and "Defense"
#Tuple 1 = games
#[dataset][season][team name(STRIPED)]
#ex. [1][9]["No.5"] is team No. 5 in season 9 in dataset 1, returns a list of all games IN THE ORDER THEY OCCUR
#print(p[1][1][9]["No.5"])
#print(p[0][1][9]["No.5"])

    #dataset
    #------ season
    #------ ------ match-day
#print(prep_data()[1][1][1])
#d = prep_data()
#p = d[0]
#t = d[1]
#print(p[1][1][1][0].data_representation())
#print(p[1][1][1][0].y_data_representation())
#print(p[1][1][2][4].data_representation())
#print(p[1][1][2][4].y_data_representation())
#print(p[1][2][3][16].data_representation())
#print(p[1][2][3][16].y_data_representation())

#print(t[1][1][1][0])
#print(t[1][1][2][4])
#print(t[1][2][3][16])
#print(len(prep_data()[1][1][1]))
#write_batch_data()
#x = read_data()
#print(x[0])
#print("\n-----------\n")
#print(x[1])
#print("COMPLETED")
    
    
write_true_data()