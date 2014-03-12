'''
Created on Feb 6, 2014
@author: Dennis
'''
import csv

teams = []
seasons = []
regular_season_results = []
tourney_results = []
tourney_seeds = []
tourney_slots = []

by_seed_features = ['season', 'winning team', 'winning seed', 'winning score', 'losing team', 'losing seed', 'losing score', 'winning seed']
by_seed_data = []

def read_teams():
    global teams
    with open('teams.csv', mode='r') as infile:
        reader = csv.reader(infile)    
        teams = {rows[0]:rows[1] for rows in reader}
    
def read_csvfile(inputfile):
    outputlist = []
    with open(inputfile, mode='r') as infile:
        reader = csv.reader(infile)    
        reader.next()
        for row in reader:
            outputlist.append(row)
        return outputlist

def read_all_files():
    global teams
    global seasons
    global regular_season_results
    global tourney_results
    global tourney_seeds
    global tourney_slots
    read_teams()
    seasons = read_csvfile('seasons.csv')
    regular_season_results = read_csvfile('regular_season_results.csv')
    tourney_results = read_csvfile('tourney_results.csv')
    tourney_seeds = read_csvfile('tourney_seeds.csv')
    tourney_slots = read_csvfile('tourney_slots.csv')

def by_seed():
    read_all_files()
    by_seed_data.append(by_seed_features)
    for row in range(1, len(tourney_results)):
        by_seed_data.append([tourney_results[row][0], tourney_results[row][2], 0, tourney_results[row][3], tourney_results[row][4], 0, tourney_results[row][5], 0])
    
    for i in range(1, len(by_seed_data)):
        for j in range(0, len(tourney_seeds)):
            if by_seed_data[i][0] == tourney_seeds[j][0]:
                if by_seed_data[i][1] == tourney_seeds[j][2]:
                    by_seed_data[i][2] = tourney_seeds[j][1]
                elif by_seed_data[i][4] == tourney_seeds[j][2]:
                    by_seed_data[i][5] = tourney_seeds[j][1]
    
    for row in range(1, len(by_seed_data)):
        if int(by_seed_data[row][2][1:3]) < int(by_seed_data[row][5][1:3]):
            by_seed_data[row][7] = 'high seed won'
        elif int(by_seed_data[row][2][1:3]) > int(by_seed_data[row][5][1:3]):
            by_seed_data[row][7] = 'low seed won'
        else:
            by_seed_data[row][7] = 'seeds are even'
    
    highseedswon = 0
    lowseedswon = 0
    seedsareeven = 0
    for row in range(1, len(by_seed_data)):
        if by_seed_data[row][7] == 'high seed won':
            highseedswon = highseedswon + 1
        elif by_seed_data[row][7] == 'low seed won':
            lowseedswon = lowseedswon + 1
        else:
            seedsareeven = seedsareeven + 1
    
    print 'Given you know the 2 teams in each game:'
    print 'high = ' + str(highseedswon) + ' = ' + str(round(float(highseedswon)/(highseedswon+lowseedswon+seedsareeven)*100, 1)) + '%'
    print 'low = ' + str(lowseedswon) + ' = ' + str(round(float(lowseedswon)/(highseedswon+lowseedswon+seedsareeven)*100, 1)) + '%'
    print 'even = ' + str(seedsareeven) + ' = ' + str(round(float(seedsareeven)/(highseedswon+lowseedswon+seedsareeven)*100, 1)) + '%'
            
    """If you always picked the high seed, 
    and randomly guessed when seeds where even, 
    you would accurately predict 70.6% of the outcome of all games.
    
    But this assumes you already know which 2 teams will be in any game.  
    In reality if you get one wrong in an round, you will get another wrong in a subsequent round.
    So for the over all bracket, the accuracy of prediction by seeds is much lower.

    """

def single_season(s):
    read_all_files();
    
    local_seasons = []
    local_regular_season_results = []
    local_tourney_results = []
    local_tourney_seeds = []
    local_tourney_slots = []
    
    for row in range(len(seasons)):
        if seasons[row][0] == s:
            local_seasons.append(seasons[row])
    for row in range(len(regular_season_results)):
        if regular_season_results[row][0] == s:
            local_regular_season_results.append(regular_season_results[row])
    for row in range(len(tourney_results)):
        if tourney_results[row][0] == s:
            local_tourney_results.append(tourney_results[row])
    for row in range(len(tourney_seeds)):
        if tourney_seeds[row][0] == s:
            local_tourney_seeds.append(tourney_seeds[row])
    for row in range(len(tourney_slots)):
        if tourney_slots[row][0] == s:
            local_tourney_slots.append(tourney_slots[row])
    return [local_seasons, local_regular_season_results, local_tourney_results, local_tourney_seeds, local_tourney_slots]
    # 0=seasons, 1=regular_season_results, 2=tourney_results, 3=tourney_seeds, 4=tourney_slots

def main():  
    by_seed()
    
    print 'Done'
    
if __name__ == '__main__':
    main()