import os
import pandas as pd
import sys

# Read the location of the csv from the task input blob
#input_name = "data_path"
#input_location = f"/workflow/inputs/{input_name}"

datasetA_path = sys.argv[1]
print("this is system argument A",datasetA_path)
#print("these are all args", sys.argv[0],sys.argv[1])

#datasetB_path = sys.argv[1]
#print("this is system argument B",datasetB_path)

#datasetA_path = "/mnt/code/data/datasetA.csv"
#print("This is hard coded path",datasetA_path)

with open(datasetA_path, "r") as file:
    input_csv = file.read()

# Read input csv to dataframe
df = pd.read_csv(input_csv) 


# Write to Flow output
df.to_csv('/workflow/outputs/datasetA.csv', index=False)

