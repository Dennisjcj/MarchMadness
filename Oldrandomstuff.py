'''
Created on Feb 7, 2014

@author: Dennis
'''
by_seed_features = ['season', 'winning team', 'winning seed', 'winning score', 'losing team', 'losing seed', 'losing score', 'winning seed']
by_seed_data = []
def by_seed():
    # Higher seed wins, 
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
    
    
   