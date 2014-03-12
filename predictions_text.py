
f = open('fold5_predictions.txt', 'r')

lines = f.readlines()
for l in range(len(lines)):
    print lines[l][27]