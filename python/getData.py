import sys
import pandas as pd

filePath = sys.argv[1]

dataFile = pd.read_csv(filePath)
jsonData = dataFile.to_json(orient='records')
print(jsonData)
sys.stdout.flush()
