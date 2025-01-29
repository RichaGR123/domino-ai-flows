import os
import pandas as pd
import sys

# Read the location of the csv from the task input blob
#input_name = "data_path"
#input_location = f"/workflow/inputs/{input_name}"

datasetB_path = sys.argv[1]

# with open(datasetB_path, "r") as file:
#     input_csv = file.read()

# Read input csv to dataframe
# df = pd.read_csv(input_csv) 

df = pd.read_csv(datasetB_path)


# Write to Flow output
df.to_csv('/workflow/outputs/datasetB.csv', index=False)
#df.to_csv('/mnt/code/outputs/datasetB.csv', index=False)