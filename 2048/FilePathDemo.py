from pathlib import Path
import os
import os.path 
import shelve

folderPath = os.path.join(Path.home(),"2048Vision")
filePath = os.path.join(folderPath, "data")

print("File      Path:", Path(__file__).absolute())
print("Directory Path:", Path().absolute()) 

#with shelve.open(filePath, 'c') as rw:
    #rw['color'] = 'blue'
 #   for x in rw.keys():
      #  print(x)
  #  for x in rw:
      #  print(x, rw[x])
