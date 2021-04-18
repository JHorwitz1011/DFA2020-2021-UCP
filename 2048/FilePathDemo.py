from pathlib import Path
import os
import os.path 
import shelve

home = str(Path.home())
path = os.path.join(home,"2048Vision")
threshold = 10


if(not os.path.exists(path)):
            os.makedirs(path)
        
if (not len(os.listdir(path)) == 0):    
    with shelve.open(os.path.join(path,"data")) as dataFile:
        threshold = dataFile['threshold']
else: 
    with shelve.open(os.path.join(path,"data")) as dataFile:
        dataFile['threshold'] = threshold

print(home)
print(path)