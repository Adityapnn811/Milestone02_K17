import random
def Random_Motivasi():
    f_mot = open("Motivasi.csv", "r")
    lines = f_mot.readlines()
    f_mot.close()
    mot = [line.replace("\n", "") for line in lines]
    return mot[random.randint(0,len(mot)-1)]
test = 10
for i in range(test):
    print(Random_Motivasi())
