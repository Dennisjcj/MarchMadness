'''
Created on Feb 7, 2014

@author: Dennis
'''
import csv
import Data1
import numpy as np
import random as rn

def write_csvfile(inputlist, outputfile):
    with open(outputfile, 'wb') as infile:
        writer = csv.writer(infile)
        for row in range(len(inputlist)):
            writer.writerow(inputlist[row])
            
def get_records(letter):  
    seeds_dict = Data1.single_season(letter)[5]
    wins_dict = {}
    losses_dict = {}
    scores_dict = {}
    for i in range(len(seeds_dict.items())):
        wins_dict[seeds_dict.keys()[i]] = 0
        losses_dict[seeds_dict.keys()[i]] = 0
        scores_dict[seeds_dict.keys()[i]] = np.array([])
        
    reg_res = Data1.single_season(letter)[1]
    for i in range(len(wins_dict.items())):
        wins = 0
        for row in range(len(reg_res)):
            if reg_res[row][2] == wins_dict.keys()[i]:
                wins += 1
        losses = 0
        for row in range(len(reg_res)):
            if reg_res[row][4] == losses_dict.keys()[i]:
                losses += 1
        for row in range(len(reg_res)):
            if reg_res[row][2] == scores_dict.keys()[i]:
                scores_dict[reg_res[row][2]] = np.append(scores_dict[reg_res[row][2]], [int(reg_res[row][3])])
            if reg_res[row][4] == scores_dict.keys()[i]:
                scores_dict[reg_res[row][4]] = np.append(scores_dict[reg_res[row][4]], [int(reg_res[row][5])])
        wins_dict[wins_dict.keys()[i]] = wins
        losses_dict[losses_dict.keys()[i]] = losses
    
    min_dict = {}
    max_dict = {}
    avg_dict = {}
    std_dict = {}
    for i in range(len(scores_dict.items())):
        min_dict[scores_dict.keys()[i]] = np.min(scores_dict.values()[i])
        max_dict[scores_dict.keys()[i]] = np.max(scores_dict.values()[i])
        avg_dict[scores_dict.keys()[i]] = np.average(scores_dict.values()[i])
        std_dict[scores_dict.keys()[i]] = np.std(scores_dict.values()[i])

    #for i in range(len(scores_dict.items())):
    #    print 'min=', min_dict[scores_dict.keys()[i]], 'max=', max_dict[scores_dict.keys()[i]], 'avg=', avg_dict[scores_dict.keys()[i]], std_dict[scores_dict.keys()[i]]
   
    #print np.min(scores_dict['708'])
    #print len(scores_dict['708'])
    return [wins_dict, losses_dict, min_dict, max_dict, avg_dict, std_dict]

def AtoR_tourneys(outfile):
    lettermap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    games = [['season','winslot','Aslot','Bslot','winner','teamA','teamB','Aseed','Bseed','Aname','Bname','Awins','Bwins','Alosses','Blosses','Ascore','Bscore','daynum','Aregion','Bregion']]
    
    for l in range(len(lettermap)):
        rnd = Data1.build_bracket(lettermap[l], 'real')      
        for row in range(len(rnd)):
            for row2 in range(len(rnd[row])):
                games.append(rnd[row][row2] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        seasonwins = get_records(lettermap[l])[0]
        seasonlosses = get_records(lettermap[l])[1]

    
        seeds_dict = Data1.single_season(lettermap[l])[5]
        team_names = Data1.read_teams()
        tourney_results = Data1.single_season(lettermap[l])[2]
        season_descript = Data1.single_season(lettermap[l])[0][0]
        for row in range(1, len(games)):
            if games[row][0] == lettermap[l]:
                # seeds
                games[row][7] = seeds_dict[games[row][5]][1:3]
                games[row][8] = seeds_dict[games[row][6]][1:3]
                # region
                if seeds_dict[games[row][5]][0] == 'W':
                    games[row][18] = season_descript[3]
                elif seeds_dict[games[row][5]][0] == 'X':
                    games[row][18] = season_descript[4]
                elif seeds_dict[games[row][5]][0] == 'Y':
                    games[row][18] = season_descript[5]
                elif seeds_dict[games[row][5]][0] == 'Z':
                    games[row][18] = season_descript[6]
                
                if seeds_dict[games[row][6]][0] == 'W':
                    games[row][19] = season_descript[3]
                elif seeds_dict[games[row][6]][0] == 'X':
                    games[row][19] = season_descript[4]
                elif seeds_dict[games[row][6]][0] == 'Y':
                    games[row][19] = season_descript[5]
                elif seeds_dict[games[row][6]][0] == 'Z':
                    games[row][19] = season_descript[6]
                                    
                # names
                games[row][9] = team_names[games[row][5]]
                games[row][10] = team_names[games[row][6]]
                # daynum
                for row2 in range(len(tourney_results)):
                    if tourney_results[row2][0] == lettermap[l]:
                        if (tourney_results[row2][2] == games[row][5] and tourney_results[row2][4] == games[row][6]) or (tourney_results[row2][2] == games[row][6] and tourney_results[row2][4] == games[row][5]):
                            games[row][17] = tourney_results[row2][1]
                            if tourney_results[row2][2] == games[row][5]:
                                games[row][15] = tourney_results[row2][3]
                                games[row][16] = tourney_results[row2][5]
                            else:
                                games[row][15] = tourney_results[row2][5]
                                games[row][16] = tourney_results[row2][3]
                # record
                games[row][11] = seasonwins[games[row][5]]
                games[row][12] = seasonwins[games[row][6]]
                games[row][13] = seasonlosses[games[row][5]]
                games[row][14] = seasonlosses[games[row][6]]
                
    for row in range(len(games)):
        if games[row][4] == games[row][5]:
            games[row][4] = 'A'
        if games[row][4] == games[row][6]:
            games[row][4] = 'B'
            
    for row in range(len(games)):
        print games[row]
    write_csvfile(games, outfile)
    
def AtoR_tourneys_full():
    lettermap = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    #games = [['season','winslot','Aslot','Bslot','winner','teamA','teamB','Aseed','Bseed','Aname','Bname','Awins','Bwins','Alosses','Blosses','Ascore','Bscore','daynum','Aregion','Bregion']]
    games = [['season','winslot','Aslot','Bslot','Aseed','Bseed','Aname','Bname','Awins','Bwins','Alosses','Blosses','daynum','Aregion','Bregion', 'winner', 'teamA','teamB', 'Aminscore', 'Bminscore', 'Amaxscore', 'Bmaxscore', 'Aqvgscore', 'Bqvgscore', 'Astdscore', 'Bstdscore', 'Agamescore', 'Bgamescore']]
    #games =      0        1        2       3        4      5       6       7        8      9        10         11       12       13        14        15        16       17        18         19          20             21           22           23            24           25           26            27

    for l in range(len(lettermap)):
        rnd = Data1.build_bracket(lettermap[l], 'real')      
        for row in range(len(rnd)):
            for row2 in range(len(rnd[row])):
                games.append([rnd[row][row2][0], rnd[row][row2][1], rnd[row][row2][2], rnd[row][row2][3], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, rnd[row][row2][4], rnd[row][row2][5], rnd[row][row2][6], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        records = get_records(lettermap[l])
        seasonwins = records[0]
        seasonlosses = records[1]
        seasonmin = records[2]
        seasonmax = records[3]
        seasonavg = records[4]
        seasonstd = records[5]

        seeds_dict = Data1.single_season(lettermap[l])[5]
        team_names = Data1.read_teams()
        tourney_results = Data1.single_season(lettermap[l])[2]
        season_descript = Data1.single_season(lettermap[l])[0][0]
        for row in range(1, len(games)):
            if games[row][0] == lettermap[l]:
                # seeds
                games[row][4] = seeds_dict[games[row][16]][1:3]
                games[row][5] = seeds_dict[games[row][17]][1:3]
                # A region
                if seeds_dict[games[row][16]][0] == 'W':
                    games[row][13] = season_descript[3]
                elif seeds_dict[games[row][16]][0] == 'X':
                    games[row][13] = season_descript[4]
                elif seeds_dict[games[row][16]][0] == 'Y':
                    games[row][13] = season_descript[5]
                elif seeds_dict[games[row][16]][0] == 'Z':
                    games[row][13] = season_descript[6]
                # B region
                if seeds_dict[games[row][17]][0] == 'W':
                    games[row][14] = season_descript[3]
                elif seeds_dict[games[row][17]][0] == 'X':
                    games[row][14] = season_descript[4]
                elif seeds_dict[games[row][17]][0] == 'Y':
                    games[row][14] = season_descript[5]
                elif seeds_dict[games[row][17]][0] == 'Z':
                    games[row][14] = season_descript[6]
                                    
                # names 
                games[row][6] = team_names[games[row][16]]
                games[row][7] = team_names[games[row][17]]
                # daynum and scores
                for row2 in range(len(tourney_results)):
                    if tourney_results[row2][0] == lettermap[l]:
                        if (tourney_results[row2][2] == games[row][16] and tourney_results[row2][4] == games[row][17]) or (tourney_results[row2][2] == games[row][17] and tourney_results[row2][4] == games[row][16]):
                            games[row][12] = tourney_results[row2][1] # daynum
                            if tourney_results[row2][2] == games[row][16]: # scores
                                games[row][26] = tourney_results[row2][3]
                                games[row][27] = tourney_results[row2][5]
                            else:
                                games[row][26] = tourney_results[row2][5]
                                games[row][27] = tourney_results[row2][3]
                # record
                games[row][8] = seasonwins[games[row][16]] # Awins
                games[row][9] = seasonwins[games[row][17]] # Bwins
                games[row][10] = seasonlosses[games[row][16]] # Alosses
                games[row][11] = seasonlosses[games[row][17]] # Blosses
                
                games[row][18] = seasonmin[games[row][16]] # Amin
                games[row][19] = seasonmin[games[row][17]] # Bmin
                games[row][20] = seasonmax[games[row][16]] # Amax
                games[row][21] = seasonmax[games[row][17]] # Bmax
                games[row][22] = seasonavg[games[row][16]] # Aavg
                games[row][23] = seasonavg[games[row][17]] # Bavg
                games[row][24] = seasonstd[games[row][16]] # Astd
                games[row][25] = seasonstd[games[row][17]] # Bstd
                
                
                
    for row in range(len(games)):
        if games[row][15] == games[row][16]:
            games[row][15] = 'A'
        if games[row][15] == games[row][17]:
            games[row][15] = 'B'
    return games

def shuffled_separated():
    games = AtoR_tourneys_full()
    newgames = games[1:]
    rn.shuffle(newgames) # shuffle all the rows besides the row 0
    games = [games[0]]
    for row in newgames:
        games.append(row)

    finaltest = [['season','winslot','Aslot','Bslot','Aseed','Bseed','Aname','Bname','Awins','Bwins','Alosses','Blosses','daynum','Aregion','Bregion', 'winner', 'teamA','teamB', 'Aminscore', 'Bminscore', 'Amaxscore', 'Bmaxscore', 'Aqvgscore', 'Bqvgscore', 'Astdscore', 'Bstdscore', 'Agamescore', 'Bgamescore']]
    devdata = [['season','winslot','Aslot','Bslot','Aseed','Bseed','Aname','Bname','Awins','Bwins','Alosses','Blosses','daynum','Aregion','Bregion', 'winner', 'teamA','teamB', 'Aminscore', 'Bminscore', 'Amaxscore', 'Bmaxscore', 'Aqvgscore', 'Bqvgscore', 'Astdscore', 'Bstdscore', 'Agamescore', 'Bgamescore']]
    crossval = [['season','winslot','Aslot','Bslot','Aseed','Bseed','Aname','Bname','Awins','Bwins','Alosses','Blosses','daynum','Aregion','Bregion', 'winner', 'teamA','teamB', 'Aminscore', 'Bminscore', 'Amaxscore', 'Bmaxscore', 'Aqvgscore', 'Bqvgscore', 'Astdscore', 'Bstdscore', 'Agamescore', 'Bgamescore']]

    for row in range(1,51): # 50 # 1:51
        finaltest.append(games[row])
    for row in range(51,251): # 200 # 51:251
        devdata.append(games[row])
    for row in range(251,1157): # 906 # 251:1157
        crossval.append(games[row])

    print 'finaltest'
    for row in range(len(finaltest)):
        print finaltest[row]
    print "devdata"
    for row in range(len(devdata)):
        print devdata[row]
    print 'crossval'
    for row in range(len(crossval)):
        print crossval[row]
    print len(finaltest), len(devdata), len(crossval)
    
    write_csvfile(games, 'shuffledgames1.csv')
    write_csvfile(finaltest, 'finaltest.csv')
    write_csvfile(devdata, 'devdata.csv')
    write_csvfile(crossval, 'crossval.csv')
    

def main():
    print 'Running...'
    
    games = AtoR_tourneys_full()
    
    for row in range(len(games)):
        print games[row]
    write_csvfile(games, 'games.csv')

    print 'Done'
    # Remember! Weka cannot handle apostraphies


if __name__ == '__main__':
    main()