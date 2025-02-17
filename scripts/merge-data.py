import os
import sys
import pandas as pd

# Read inputs from command-line arguments

print("Files in /workflow/outputs:", os.listdir('/workflow/outputs'))
#print("Files in /mnt/data:", os.listdir('/mnt/data/'))

datasetA_path = sys.argv[1]
datasetB_path = sys.argv[2]

print(f"Loading dataset A from: {datasetA_path}")
print(f"Loading dataset A from: {datasetB_path}")

#datasetA_path = "/mnt/code/outputs/datasetA"
#datasetB_path = "/mnt/code/outputs/datasetB"

#datasetA_path = "/workflow/outputs/datasetA.csv"
#datasetB_path = "/workflow/outputs/datasetB.csv"

# Load data
#print(f"Loading dataset A from: {datasetA_path}")
#a = pd.read_csv(datasetA_path, index_col='Id')
a = pd.read_csv(datasetA_path)

#print(f"Loading dataset B from: {datasetB_path}")
#b = pd.read_csv(datasetB_path, index_col='Id')
b = pd.read_csv(datasetB_path)

#print(f"Received dataset A path: {datasetA_path}")
#print(f"Received dataset B path: {datasetB_path}")



# Merge data
print('Merging data...')
merged = pd.concat([a, b], axis=0).reset_index(drop=True)


# Ensure output directory exists
# output_dir = '/mnt/code/outputs/'
# os.makedirs(output_dir, exist_ok=True)

# Write output
# output_path = os.path.join(output_dir, 'merged_data.csv')
# merged.to_csv(output_path, index=False)
# print(f"Merged data saved to: {output_path}")

#/mnt/data/merged_data.csv

# Write output
#output_path = '/mnt/data/merged_data.csv'

output_path = '/workflow/outputs/merged_data.csv'

#output_path = '/mnt/code/outputs/merged_data.csv'
merged.to_csv(output_path, index=False)
#print(f"Merged data saved to: {output_path}")
