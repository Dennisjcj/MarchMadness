'''
Created on Feb 19, 2014
@author: Dennis
'''
import csv

def read_csvfile(inputfile):
    outputlist = []
    with open(inputfile, mode='r') as infile:
        reader = csv.reader(infile)    
        #reader.next()
        for row in reader:
            outputlist.append(row)
        return outputlist

def make_groups():
    NB_5 = read_csvfile('NB_5folds_sorted.csv')
    data = [[], [], [], []]
    groups =  ['AasA', 'AasB', 'BasA', 'BasB']
    features = NB_5[0]
    
    for row in range(len(NB_5)):
        if NB_5[row][17] == 'A' and NB_5[row][18] == 'A':
            data[0].append(NB_5[row])
        elif NB_5[row][17] == 'A' and NB_5[row][18] == 'B':
            data[1].append(NB_5[row])
        elif NB_5[row][17] == 'B' and NB_5[row][18] == 'A':
            data[2].append(NB_5[row])
        elif NB_5[row][17] == 'B' and NB_5[row][18] == 'B':
            data[3].append(NB_5[row])
            
    return [groups, features, data, NB_5]

def make_feature_lists():
    full_data = make_groups()[3]
    feature_list = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]

    for c in range(len(full_data[0])):
        for i in range(1,len(full_data)):
            feature_list[c][full_data[i][c]] = 0
   
    return feature_list
            
def count_features(g):
    made_groups = make_groups()
    groups = made_groups[0]
    features = made_groups[1]
    data = made_groups[2]
    feature_counts = make_feature_lists()
    print groups[g]
    
    for f in range(len(feature_counts)):
        print features[f]
        for i in range(len(feature_counts[f].keys())):
            num = 0
            for j in range(len(data[g])):
                if data[g][j][f] == feature_counts[f].keys()[i]:
                    num += 1
            feature_counts[f][feature_counts[f].keys()[i]] = num

            #print feature_counts[f].keys()[i], num
            print num
            
    return [groups[g], feature_counts]

def main():
    print 'Running...'
    
    count_features(3)
    
    print 'Done'


if __name__ == '__main__':
    main()