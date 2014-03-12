'''
Created on Feb 6, 2014
@author: Dennis
'''
import csv

def read_teams():
    with open('teams.csv', mode='r') as infile:
        reader = csv.reader(infile)    
        teams = {rows[0]:rows[1] for rows in reader}
    return teams
    
def read_csvfile(inputfile):
    outputlist = []
    with open(inputfile, mode='r') as infile:
        reader = csv.reader(infile)    
        reader.next()
        for row in reader:
            outputlist.append(row)
        return outputlist

def read_all_files():
    seasons = read_csvfile('seasons.csv')
    regular_season_results = read_csvfile('regular_season_results.csv')
    tourney_results = read_csvfile('tourney_results.csv')
    tourney_seeds = read_csvfile('tourney_seeds.csv')
    tourney_slots = read_csvfile('tourney_slots.csv')
    return [read_teams(), seasons, regular_season_results, tourney_results, tourney_seeds, tourney_slots]

def single_season(s):
    files = read_all_files();
    
    seasons = files[1]
    regular_season_results = files[2]
    tourney_results = files[3]
    tourney_seeds = files[4]
    tourney_slots = files[5]
    
    local_seasons = []
    local_regular_season_results = []
    local_tourney_results = []
    local_tourney_seeds = []
    local_tourney_slots = []
    local_seeds_dict = {}
    local_reverse_seeds_dict = {}
    
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
    for row in range(len(tourney_seeds)):
        if tourney_seeds[row][0] == s:
            local_seeds_dict[tourney_seeds[row][2]] = tourney_seeds[row][1]
    for row in range(len(tourney_seeds)):
        if tourney_seeds[row][0] == s:
            local_reverse_seeds_dict[tourney_seeds[row][1]] = tourney_seeds[row][2]
    return [local_seasons, local_regular_season_results, local_tourney_results, local_tourney_seeds, local_tourney_slots, local_seeds_dict, local_reverse_seeds_dict]
    # 0=seasons, 1=regular_season_results, 2=tourney_results, 3=tourney_seeds, 4=tourney_slots, 5=local_seeds_dict, 6=local_reverse_seeds_dict

def winner(teama, teamb, season, algorithm):
    if algorithm == 'real':
        real_tourney_results = season[2]
        whowon = 0
        for row in range(len(real_tourney_results)):
            if real_tourney_results[row][2] == teama and real_tourney_results[row][4] == teamb:
                whowon = teama
            elif real_tourney_results[row][2] == teamb and real_tourney_results[row][4] == teama:
                whowon = teamb
        if whowon == teama:
            return teama
        elif whowon == teamb:
            return teamb
        else: print 'somthings is wrong with game ' + str(real_tourney_results[row])
    elif algorithm == 'seed': # picks the highest seed or flips a coin if even
        seeds_dict = season[5]
        if int(seeds_dict[teama][1:3]) < int(seeds_dict[teamb][1:3]):
            return teama
        elif int(seeds_dict[teama][1:3]) > int(seeds_dict[teamb][1:3]):
            return teamb
        else: 
            return teama
        
def write_csvfile(inputlist, outputfile):
    with open(outputfile, 'wb') as infile:
        writer = csv.writer(infile)
        for row in range(len(inputlist)):
            writer.writerow(inputlist[row])

def build_bracket(season, algorithm):
    teams = read_teams()
    this_season = single_season(season)
    these_tourney_slots = this_season[4]
    these_reverse_seeds_dict = this_season[6]
    
    rnd = [[], [], [], [], [], [], []]
    for row in range(len(these_tourney_slots)):
        if these_tourney_slots[row][1][0] != 'R':
            rnd[0].append([these_tourney_slots[row][0], these_tourney_slots[row][1], these_tourney_slots[row][2], these_tourney_slots[row][3], 0, 0, 0])
        else:
            for i in range(1, 7):
                if these_tourney_slots[row][1][0:2] == 'R' + str(i):
                    rnd[i].append([these_tourney_slots[row][0], these_tourney_slots[row][1], these_tourney_slots[row][2], these_tourney_slots[row][3], 0, 0, 0]) 
    # Start round 0
    r = 0
    for i in range(len(rnd[r])): # start rnd 0
        rnd[r][i][5] = these_reverse_seeds_dict[rnd[r][i][2]]
        rnd[r][i][6] = these_reverse_seeds_dict[rnd[r][i][3]]
    for row in range(len(rnd[r])): # find winners
        thewinner = winner(rnd[r][row][5], rnd[r][row][6], this_season, algorithm)
        if  thewinner == rnd[r][row][5]:
            rnd[r][row][4] = rnd[r][row][5]
        elif thewinner == rnd[r][row][6]:
            rnd[r][row][4] = rnd[r][row][6]
        else: print 'Row ' + str(row) + ' error: ' + str(rnd[r][row])
    for i in range(len(rnd[r])): # move play in games into round 1
        for j in range(len(rnd[r+1])):
            if rnd[r][i][1] == rnd[r+1][j][2]:
                rnd[r+1][j][5] = rnd[r][i][4]
            if rnd[r][i][1] == rnd[r+1][j][3]:
                rnd[r+1][j][6] = rnd[r][i][4]
    r=1
    for i in range(len(rnd[r])): # start round 1
        if rnd[r][i][5] == 0:
            rnd[r][i][5] = these_reverse_seeds_dict[rnd[r][i][2]]
        if rnd[r][i][6] == 0:
            rnd[r][i][6] = these_reverse_seeds_dict[rnd[r][i][3]]
    for row in range(len(rnd[r])): # find winners
        thewinner = winner(rnd[r][row][5], rnd[r][row][6], this_season, algorithm)
        if  thewinner == rnd[r][row][5]:
            rnd[r][row][4] = rnd[r][row][5]
        elif thewinner == rnd[r][row][6]:
            rnd[r][row][4] = rnd[r][row][6]
    
    for r in range(1, 6):
        for i in range(len(rnd[r])): # move winners to next round
            for j in range(len(rnd[r+1])):
                if rnd[r][i][1] == rnd[r+1][j][2]:
                    rnd[r+1][j][5] = rnd[r][i][4]
                if rnd[r][i][1] == rnd[r+1][j][3]:
                    rnd[r+1][j][6] = rnd[r][i][4]
        r=r+1
        for row in range(len(rnd[r])): # find winners
            thewinner = winner(rnd[r][row][5], rnd[r][row][6], this_season, algorithm)
            if  thewinner == rnd[r][row][5]:
                rnd[r][row][4] = rnd[r][row][5]
            elif thewinner == rnd[r][row][6]:
                rnd[r][row][4] = rnd[r][row][6]
    
    """for f in range(0, 7):
        print 'rnd ' + str(f)
        for row in range(len(rnd[f])):
            print rnd[f][row], teams[rnd[f][row][5]], 'vs.', teams[rnd[f][row][6]]
    print teams[rnd[6][0][4]] + ' wins it all ' + rnd[6][0][4]
    """
    
    return rnd

def compare_brackets(predicted, real):
    numcorrect = [0, 0, 0, 0, 0, 0, 0]
    numtotal = [0, 0, 0, 0, 0, 0, 0]
    accuracy = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for r in range(0, 7):
        for row in range(len(predicted[r])):
            numtotal[r] += 1
            if predicted[r][row] == real[r][row]:
                numcorrect[r] += 1
        if numtotal[r] == 0:
            accuracy[r] = 'n/a '
        else:
            accuracy[r] = round(float(numcorrect[r])/numtotal[r]*100, 1) # round accuracy
    accuracy[7] = float(sum(numcorrect))/sum(numtotal)*100 # overall accuracy
      
    for f in range(0, 7):
        print 'Round ' + str(f) + ': ' + str(numcorrect[f]) + '/' + str(numtotal[f]) + ' = ' + str(accuracy[f]) + '%'
    print 'Total: ' + str(sum(numcorrect)) + '/' + str(sum(numtotal))  + ' = ' + str(round(accuracy[7], 1)) + '%'
    
    return accuracy

def all_season_performance(algorithm):
    lettermap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    real_bracket = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    all_seasons_averages = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    average_rounds = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i in range(len(lettermap)):
        real_bracket[i] = build_bracket(lettermap[i], 'real') 
        print 'Season ' + lettermap[i]
        all_seasons_averages[i] = compare_brackets(build_bracket(lettermap[i], algorithm), real_bracket[i])
    
    for i in range(len(average_rounds)):
        for j in range(len(lettermap)):
            if all_seasons_averages[j][i] != 'n/a ':
                average_rounds[i] += all_seasons_averages[j][i]
        average_rounds[i] = average_rounds[i]/len(lettermap)
        
    print 'Overall'
    for f in range(0, 7):
        print 'Round ' + str(f) + ': ' + str(round(average_rounds[f], 1)) + '%'
    print 'Total: ' +  str(round(average_rounds[7], 1)) + '%'

def get_records(letter):
    reg_results = single_season(letter)[1]
    for row in range(len(reg_results)):
        pass
    
    for row in range(len(reg_results)):
        print reg_results[row]

def main():  
    get_records('A')
    
    print 'Done'
    
if __name__ == '__main__':
    main()