#import random
import time
import math
import numpy as np

from numpy import random
from scipy.stats import poisson

class Team:
    def __init__(self):
        self.power = 50.0
        #randomize to be around 1.5 goals in both scenarios
        self.attack = 5.0
        self.defense = 5.0
        #for me
        self.name = ""
        
    def set_name(self, nm):
        self.name = nm
        
    def get_name(self):
        return self.name
    
    def get_attacK(self):
        return self.attack
    
    def set_attacK(self, attck):
        self.attack = attck
    
    def get_defense(self):
        return self.defense
    
    def set_defense(self, defn):
        self.defense = defn
    
    #gets the harmonic mean of 
    def game_lambda(self, defense):
        return harmonic_mean(self.attack, defense)

    def harmonic_mean(a, b):
        return 2/(a**-1 + b**-1)
    
class Team_Staged(Team):
    def __init__(self, attack, defense):
        Team.__init__(self)

        #True Values
        self.true_values = True
        self.true_attack = attack
        self.true_defense = defense

class Game:
    def __init__(self):
        #home is the team who is hosting index
        self.home = -1
        self.away = -1
        
        self.home_score = 0
        self.away_score = 0
        
        #for tournamnet pen shootouts
        self.home_pens = 0
        self.away_pens = 0

class Conference:
    def __init__(self, nm, attk_mu=2.5, attk_std=1.0, def_mu=1.5, def_std=.65, master_path="Test_Results/"):
        self.teams = []
        self.name = nm
        
        #for each matchday a dictionary holds who a team plays by index
        self.schedule = []
        self.games = []
        self.iteration = 1
        
        self.attacking_mu = attk_mu
        self.attacking_std = attk_std
        self.defensive_mu = def_mu
        self.defensive_std = def_std
        
        #amount added to home games
        self.home_field_advantage = 0.4
        
        self.master_path = master_path
        
    def gen_standard_conference(self, size, names):
        for i in range(0, size):
            team = Team_Staged(max(random.normal(self.attacking_mu, self.attacking_std), .1),
                               max(random.normal(self.defensive_mu, self.defensive_std), .1))
            team.set_name(names[i])
            self.teams.append(team)
            
            #print(str(chr(65 + i)) + ": Attack=" + str(team.true_attack) + ", Defense=" + str(team.true_defense))
    def reset(self):
        self.games = []
        self.schedule = []
        self.iteration += 1
        
    def gen_schedule(self):
        days = len(self.teams) - 1
        master_days = []
        master_teams = []
        for i in range(0, len(self.teams)):
            master_days.append(list(range(0, days)))
            master_teams.append(list(range(0, days + 1)))
            master_teams[i].remove(i)
        
        match_days = {}
        for i in range(0, days):
            match_days[i] = {}
            
        #just start from 1 and work your way up
        index = 0
        while(len(master_teams[days]) > 0):
            if(len(master_teams[index]) == 0):
                #then we gucci all paired up
                index += 1
            else:
                #still values to be had
                #go through and see which has the fewest days it can work
                minimum = days + 2
                min_val = days + 2
                for i in range(0, len(self.teams)):
                    if(i in master_teams[index]):
                        t = len(list(set(master_days[index]).intersection(master_days[i])))
                        if(t < min_val):
                            min_val = t
                            minimum = i
                            
                #we now how minimum as the index of the team with the fewest days that it can be paired with index team
                valid_days = list(set(master_days[index]).intersection(master_days[minimum]))
                mtch_day = valid_days[0]
                
                try:
                    #we have our day, now lets update our deliverable
                    match_days[mtch_day][index] = minimum
                    match_days[mtch_day][minimum] = index
                    #update our masters
                    master_teams[index].remove(minimum)
                    master_teams[minimum].remove(index)
                    
                    master_days[index].remove(mtch_day)
                    master_days[minimum].remove(mtch_day)
                except TypeError:
                    print("match_days: " + str(match_days))
                    print("master_teams: " + str(master_teams))
                    print("master_days: " + str(master_days))
                    print("mtch_day: " + str(mtch_day))
                    print("index: " + str(index))
                    
                    t = 1 + "T"

        for i in match_days:
            self.schedule.append(match_days[i])
        
        #SELF.SCHEDULE IS A LIST OF DICTIONARIES WITH A GIVEN MATCH'S MATCHES
        
    #basically at the end of a season the team may get stronger or weaker
    def adjust_teams(self):
        for team in self.teams:
            t = team.true_attack + random.normal(0, .2)
            team.true_attack = max(t, .1)
            
            t = team.true_defense + random.normal(0, .3)
            team.true_defense = max(t, .1)
            
    def write_team_powers(self):
        file = open(self.master_path + self.name + str(self.iteration) + "_summaries.txt", 'w')
        for team in self.teams:
            file.write(str(team.name) + ", " + str(team.true_attack) + ", " + str(team.true_defense) + "\n")
            
        file.close()
        
    def write_summaries(self):
        file = open(self.master_path + self.name + str(self.iteration) + "_games.txt", 'w')
        for game in self.games:
            #keeping it the same style as with tournamnet sans penalty kick shootout
            file.write((str(self.teams[game.home].name) + ", " +
                        str(self.teams[game.away].name) + ", " +
                        str(game.home_score) + ", " +
                        str(game.away_score) + "\n"))
        file.close()
        
    def run_season(self):
        self.gen_schedule()
        
        for i in range(0, len(self.schedule)):
            self.play_matchday(i)
        
        self.write_summaries()
        self.write_team_powers()
        self.adjust_teams()
        
    def play_matchday(self, day):
        #print("------------------")
        #print("MATCHDAY " + str(day + 1))
        free_teams = {}
        
        for i in range(0, len(self.teams)):
            free_teams[i] = True
            
        for i in range(0, len(self.teams)):
            if(free_teams[i] and free_teams[self.schedule[day][i]]):
                game = Game()
                game.home = i
                game.away = self.schedule[day][game.home]
                
                game.home_score = random.poisson(harmonic_mean(self.teams[game.home].true_attack + self.home_field_advantage,
                                                                  self.teams[game.away].true_defense))
                
                game.away_score = random.poisson(harmonic_mean(max(self.teams[game.home].true_defense - self.home_field_advantage, .1) ,
                                                                  self.teams[game.away].true_attack))
                
                free_teams[game.home] = False
                free_teams[game.away] = False
                
                self.games.append(game)
                
        '''
        for g in self.games[-1*int((len(self.teams)/2)):]:
            print(self.teams[g.home].name + " vs. " + self.teams[g.away].name)
            print(str(g.home_score) + ":" + str(g.away_score))
            #'''
            
    def calculate_expected_powers(self, game, home):
        team = 0
        opp = 0
        team_forced = 0
        team_accepted = 0
        
        if(home):
            team = game.home
            team_forced = game.home_score
            team_accepted = game.away_score
            opp = game.away
        else:
            team = game.away
            team_forced = game.away_score
            team_accepted = game.home_score
            opp = home.away
            
            
        print("Home: " + str(home))
        print("Forced: " + str(team_forced))
        print("Accepted: " + str(team_accepted))
        print("Attack: " + str(self.teams[team].attack))
        print("Defense: " + str(self.teams[opp].defense))
        #first we do attack
        #step one
        #value then lambda
        #also I use x so it matches my notes
        x = team_forced
        f = poisson.pmf(team_forced, get_lambda(self.teams[team].attack,
                                                self.teams[opp].defense))
        
        print("Step 1: " + str(f))
        #step two
        #we want to get the gamma function which is a constant in our equation
        #gamma = c to match my notes
        #c = math.exp(-1*self.teams[team].attack)
        #c *= (self.teams[team].attack)**x
        #c /= f
        
        c = math.factorial(team_forced)
        
        print("Step 2: " + str(c))
        
        
        #step three
        #part a construct the polynomial
        poly_coefs = [1]
        val = 1
        
        for i in range(x, 0, -1):
            val *= i
            poly_coefs.append(val)
            
        poly = Polynomial(poly_coefs)
        
        #part b now we have the poly let's do the heavy lifting
        #initial is what we subtract from the poly at b times c
        
        initial = poly.get_value(0)
        #e^0 = 1
        initial *= math.exp(0)
        #initial *= c
        #'''
        b = x
        prev_val = poly.get_value(b-1)*math.exp(-b + 1)*c*-1 - initial
        val = poly.get_value(b)*math.exp(-b)*c*-1 - initial
        threshold = .0005
        
        #random threshold
        while(abs(val - prev_val) > threshold):
            b += 1
            prev_val = val
            val = poly.get_value(b)*math.exp(-b)*c*-1 - initial
        
        overall = val - initial
        print("Overall: " + str(overall))
        #what we did above was get the value of b where the integral converges
        #'''
        
        #step 4
        #time to get the b such that we get half of overall for the 50th percentile
        value = 1/2*overall
        #then we divide by c so we don't need to deal with it anymore
        value /= c
        #then subtract initial once again cleaning the side of the equation with
        #the unknown
        value -= initial
        
        #we use binary search to find the value within a given threshold
        b = find_b(0, b, value, poly, threshold)
        
        print(b)
        t = 1 + "T"
        t += t
        
class Tournament:
    #size must be multiple of 2
    def __init__(self, nm, sz=16, master_path="Test_Results/"):
        self.name = nm
        self.games = []
        self.teams = []
        self.instantiation = 1
        self.size = sz
        self.home_field_advantage = .4
        self.first_half = True
        while(sz > 2):
            sz /= 2
            
        if(not(sz==2)):
            sz = 16
            #basically if you don't make it a power of 2 I WILL
        
        self.cur_size = self.size
        #determine match dat etc.
        
        self.master_path = master_path
    
    def reset(self):
        self.cur_size = self.size
        self.first_half = True
        self.instantiation += 1
        self.teams = []
    
    def add_team(self, team):
        if(self.size >= len(self.teams) and self.size == self.cur_size):
            self.teams.append(team)
            
    def add_teams(self, teams):
        for team in teams:
            self.add_team(team)
            
    def write_game_line(self, game):
        t1 = self.teams[game.home].name
        t2 = self.teams[game.away].name
        t1_score = game.home_score
        t2_score = game.away_score
        
        appropos = ""
        
        if(t1_score == t2_score):
            appropos = ", " + str(game.home_pens) + ", " + str(game.away_pens)
            
        line = (str(t1) + ", " + str(t2) + ", " + str(t1_score) + ", " + str(t2_score)) + appropos
        
        return (line + "\n")
        
    def play_matchday(self):
        #print(len(self.teams))
        file = ""
        if(self.cur_size == self.size and self.first_half):
            file = open(self.master_path + self.name + "_" + str(self.instantiation) + ".txt", 'w')
        else:
            file = open(self.master_path + self.name + "_" + str(self.instantiation) + ".txt", 'a')
            
        home_adv = self.home_field_advantage
        
        #tournaments tend to end with neutral grounds
        if(self.cur_size < 4):
            home_adv = 0
        else:
            #because right now we do random home assignment etc etc
            home_adv = 0
            
        if(not self.first_half):
            start = len(self.teams) - int(3*self.cur_size/4.0)
            end = len(self.teams) - int(1/4.0 * self.cur_size)
            self.first_half = True
            self.cur_size /= 2.0
        else:
            start = len(self.teams) - self.cur_size
            end = len(self.teams) - int(self.cur_size/2.0)
            self.first_half = False
        
        start = int(start)
        end = int(end)
        
        #print("start: " + str(start))
        #print("end: " + str(end))
        #print(str(range(start, end, 2)))
        #print(str(list(range(start, end, 2))))
            
        for i in range(start, end, 2):
            game = Game()
            game.home = i
            game.away = i + 1
            
            game.home_score = random.poisson(harmonic_mean(self.teams[game.home].true_attack + home_adv,
                                                              self.teams[game.away].true_defense))
            
            game.away_score = random.poisson(harmonic_mean(max(self.teams[game.home].true_defense - home_adv, .1),
                                                              self.teams[game.away].true_attack))
            #THAT PENALTY SHOOTOUT THOUGH!
            done = False
            if(game.home_score == game.away_score):
                for i in range(0, 5):
                    #.28 was just a hyperparameter I chose looking at the harmonic mean of it
                    #should be roughly decent
                    if(not done and harmonic_mean_three(self.teams[game.home].true_attack + home_adv,
                                  self.teams[game.away].true_defense,
                                  .28) > np.random.random()):
                        game.home_pens += 1
                        
                        if(game.home_pens > 5-i + game.away_pens):
                            done = True
                            
                    if(not done and harmonic_mean_three(self.teams[game.home].true_defense - home_adv,
                                  self.teams[game.away].true_attack,
                                  .28) > np.random.random()):
                        game.away_pens += 1
                        
                        if(game.away_pens > 5-i + game.home_pens):
                            done = True
                            
                #we have done 5 penalties
                #do sudden death penalties
                while(game.home_pens == game.away_pens):
                    if(not done and harmonic_mean_three(self.teams[game.home].true_attack + home_adv,
                                  self.teams[game.away].true_defense,
                                  .28) > np.random.random()):
                        game.home_pens += 1
                        
                    if(not done and harmonic_mean_three(self.teams[game.home].true_defense - home_adv,
                                  self.teams[game.away].true_attack,
                                  .28) > np.random.random()):
                        game.away_pens += 1
            
            
            if(game.home_score > game.away_score or game.home_pens > game.away_pens):
                self.teams.append(self.teams[game.home])
            else:
                self.teams.append(self.teams[game.away])
            
            file.write(self.write_game_line(game))
            
        self.games.append(game)
        file.close()
    

class Polynomial():
    def __init__(self):
        self.coefficients = []
        
    def __init__(self, coeffs):
        self.coefficients = coeffs
        
    def get_degree(self):
        return len(self.coefficients) - 1
    
    def get_value(self, x):
        value = 0
        #x^6 * coef[0] + x^5 * coef[1] . . . + x^0 + coef[6]
        #  0               -1                    -6
        for i in range(len(self.coefficients) - 1, -1, -1):
            value += (x**i) * self.coefficients[abs(i - (len(self.coefficients) - 1))]
            
        return value
    
    def get_roots(self, max_num):
        roots = np.roots(self.coefficients)
        
        print(roots)
        
        if(len(roots) > 1):
            for i in roots:
                try:
                    if(i >= 0 and i <= max_num):
                        return roots[i]
                except ValueError:
                    x = 1
        else:
            return roots[0]

#takes in input a and result c to calculate the other input b
def reverse_harmonic(a, c):
    b = 2/c
    b -= a**-1
    b = b**-1
    
    return b

#computes the harmonic mean of a and b
def harmonic_mean(a, b):
    a = a**-1
    b = b**-1
    
    return(2/(a+b))
    
def harmonic_mean_three(a, b, c):
    return 3/(a**-1 + b**-1 + c**-1)
    
def get_lambda(att, defense):
    return harmonic_mean(att, defense)

def find_b(a, b, value, poly, threshold):
    val = 0
    print("a: " + str(a))
    print("b: " + str(b))
    print("value: " + str(value))
    print("PRE-LOOP")
    print("--------")
    while(abs(value-val) > threshold):
        inter = (a+b)/2.0
        val = -1*poly.get_value(inter)*math.exp(-inter)
        
        print("a: " + str(a))
        print("b: " + str(b))
        print("inter: " + str(inter))
        print("val: " + str(val) + "\n")
        
        if(val > value):
            b = inter
        #val < value
        else:
            a = inter
            
        time.sleep(1)
        
    return inter

def tester():
    conf = Conference("Testa")
    conf.gen_standard_conference(8)
    conf.gen_schedule()
    for i in range(0, len(conf.schedule)):
        #print("--" + "MATCHDAY " + str(i) + "--")
        conf.play_matchday(i)

def get_names(num, start_num):
    names = []
    for i in range(start_num, start_num + num):
        names.append("No. " + str(i))
        
    return names

def main():
    #random.seed(1)
    for data_set in range(101, 1000):
        MASTERPATH = "Test_Results/" + str(data_set)
        try:
            os.mkdir(MASTERPATH)
        except FileExistsError:
            pass
        
        MASTERPATH += "/"
        
        print(MASTERPATH)
        
        conf_counter = 1
        conferences = []
        conference_names = ["Valley High",
                         "Longhorn",
                         "Big Sky",
                         "Rocky",
                         "Desert",
                         "Gulf Coast",
                         "Panhandle",
                         "South",
                         "North",
                         "East",
                         "West",
                         "Lowland",
                         "Highland",
                         "Heartland",
                         "Southland",
                         "Pac-Ten"]
        
        #conf = Conference("Testa")
        
        #conf.gen_standard_conference(8, get_names(8, 1))
        
        #create conferences
        for name in conference_names:
            conferences.append(Conference(name, attk_mu=3.25 + random.normal(0, .75),
                                          attk_std=1.0 + random.normal(0, .12),
                                          def_mu=1.5 + random.normal(0, .5),
                                          def_std=.65 + random.normal(0, .12),
                                          master_path = MASTERPATH))
            conferences[len(conferences)-1].gen_standard_conference(8, get_names(8, conf_counter))
            conf_counter += 8
        
        nationals = Tournament("NCAA Nationals", master_path=MASTERPATH)
        
        for seasons in range(0, 15):
            for conf in conferences:
                conf.run_season()
                nationals.add_team(conf.teams[np.random.randint(0, 8)])
            #print(len(nationals.teams))
            for i in range(0, 7):
                nationals.play_matchday()
                
            for conf in conferences:
                conf.reset()
                
            nationals.reset()
            
    
#def __init__(self, nm, attk_mu=2.5, attk_std=1.0, def_mu=1.5, def_std=.65):
    
    

main()
#tester()
print("COMPLETE")
