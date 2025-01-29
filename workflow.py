#!/usr/bin/env python
# coding: utf-8

from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from flytekit.types.file import FlyteFile

# Define the Domino tasks

data_load_taskA = DominoJobTask(
    name='Load_Data_A',
    domino_job_config=DominoJobConfig(
         #Command='python /mnt/code/scripts/load-data-A.py {data_patha}',
         #Command='python /mnt/code/scripts/load-data-A.py {sys.argv[1]}',
         Command=f'python /mnt/code/scripts/load-data-A.py /mnt/code/data/datasetA.csv',
    ),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    
    #comment it when hardcoding
    #inputs={
        #"data_patha": str,
    #},
    
#     inputs={
#         "data_patha": str,
#     },
    
    outputs={"datasetA": FlyteFile["csv"]},
    use_latest=True
)

data_load_taskB = DominoJobTask(
    name='Load_Data_B',
    domino_job_config=DominoJobConfig(
        #Command='python /mnt/code/scripts/load-data-B.py {data_pathb}',
        #Command='python /mnt/code/scripts/load-data-B.py {sys.argv[1]}',
        Command=f'python /mnt/code/scripts/load-data-B.py /mnt/code/data/datasetB.csv',
    ),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    
#     inputs={
#         "data_pathb": str,
#     },
    
    outputs={"datasetB": FlyteFile["csv"]},
    use_latest=True
)

data_merge_task = DominoJobTask(
    name="merge_data",
    domino_job_config=DominoJobConfig(
         Command="python /mnt/code/scripts/merge-data.py {datasetA} {datasetB}",
#         Command=f"python /mnt/code/scripts/merge-data.py /workflow/outputs/datasetA.csv /workflow/outputs/datasetB.csv",
    ),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    
     inputs={
        "datasetA": FlyteFile["csv"],
        "datasetB": FlyteFile["csv"],
    },
    
    outputs={"merged_data": FlyteFile["csv"]},
    use_latest=True
)


data_prep_task = DominoJobTask(
    name="prepare_data",
    domino_job_config=DominoJobConfig(Command="python /mnt/code/scripts/process-data.py {merged_data}"),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    inputs={
        "merged_data": FlyteFile["csv"],
    },
    outputs={"processed_data": FlyteFile["csv"]},
   
    use_latest=True
)

training_task = DominoJobTask(
    name="train_model",
    domino_job_config=DominoJobConfig(Command="python /mnt/code/scripts/train-model.py {processed_data}"),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    inputs={
        "processed_data": FlyteFile["csv"],
        "epochs": int,
        "batch_size": int,
    },
    outputs={"model": FlyteFile},
    use_latest=True
)

# Define the workflow
@workflow
#def training_workflow(data_patha: str, data_pathb: str) -> FlyteFile:

#uncomment below while hardcoding
def training_workflow() -> FlyteFile: 
    
    #data_load_taskA
    #data_load_A = data_load_taskA(data_patha=data_patha)
    #uncomment below while hardcoding
    data_load_A = data_load_taskA()
    data_load_B = data_load_taskB()
    #data_load_B = data_load_taskB(data_pathb=data_pathb)
    
     # Run the data Merge task
    #data_merge_results = data_merge_task(datasetA=data_load_A, datasetB=data_load_B)
    data_merge_results = data_merge_task(datasetA=data_load_A.outputs["datasetA"], datasetB=data_load_B.outputs["datasetB"])
    
    #data_merge_results = data_merge_task()
    
    
    # Run the data preparation task
    #data_prep_results = data_prep_task(data_path=data_path)
    
    #to be done
    data_prep_results = data_prep_task(merged_data=data_merge_results.outputs["merged_data"])
    
    # Run the training task
    training_results = training_task(
        processed_data=data_prep_results.outputs["processed_data"],
        epochs=10,
        batch_size=32,
    )
    
    # Return the model file
    return training_results.outputs["model"]
