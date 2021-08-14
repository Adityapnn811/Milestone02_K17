import random
from datetime import datetime
def Random_Motivasi():
    random.seed(datetime.now())
    mot = ["Bisaa gais", "kamu di hati", "i love Bryan", "We love you"]
    return mot[random.randint(0,len(mot)-1)]
test = 10
for i in range(test):
    print(Random_Motivasi())
    wait(10)
