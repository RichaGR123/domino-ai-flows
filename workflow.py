#!/usr/bin/env python
# coding: utf-8

from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask
from flytekit.types.file import FlyteFile

# Define the Domino tasks

data_merge_task = DominoJobTask(
    name="merge_data",
    domino_job_config=DominoJobConfig(
        #Command="python /mnt/code/scripts/merge-data.py {inputs.data_patha} {inputs.data_pathb}"
        Command="python /mnt/code/scripts/merge-data.py "/mnt/code/data/datasetA.csv" "/mnt/code/data/datasetB.csv""
    ),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    inputs={
        "data_patha": str,
        "data_pathb": str,
    },
    outputs={"merged_data": FlyteFile["csv"]},
    use_latest=True
)


data_prep_task = DominoJobTask(
    name="prepare_data",
    domino_job_config=DominoJobConfig(Command="python /mnt/code/scripts/process-data.py"),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    #inputs={"data_path": str},
    inputs={
        "merged_data": FlyteFile["csv"],
    },
    outputs={"processed_data": FlyteFile["csv"]},
    #use_project_defaults_for_omitted=True,
    use_latest=True
)

training_task = DominoJobTask(
    name="train_model",
    domino_job_config=DominoJobConfig(Command="python /mnt/code/scripts/train-model.py"),
    environment_name="Domino Standard Environment Py3.11 R4.4",
    hardware_tier_name="Small",
    inputs={
        "processed_data": FlyteFile["csv"],
        "epochs": int,
        "batch_size": int,
    },
    outputs={"model": FlyteFile},
    #use_project_defaults_for_omitted=True,
    use_latest=True
)

# Define the workflow
@workflow
def training_workflow() -> FlyteFile:
#def training_workflow(data_patha: str, data_pathb: str) -> FlyteFile:
#def training_workflow(data_patha="/mnt/data/datasetA.csv", data_pathb="/mnt/data/datasetB.csv") -> FlyteFile:
    
     # Run the data Merge task
    #data_merge_results = data_merge_task(data_patha=data_patha, data_pathb=data_pathb)
    #data_merge_results = data_merge_task(data_patha="/mnt/code/data/datasetA.csv", data_pathb="/mnt/code/data/datasetB.csv")
    data_merge_results = data_merge_task()
    
    # Run the data preparation task
    #data_prep_results = data_prep_task(data_path=data_path)
    data_prep_results = data_prep_task(merged_data=data_merge_results.outputs["merged_data"])
    
    # Run the training task
    training_results = training_task(
        processed_data=data_prep_results.outputs["processed_data"],
        epochs=10,
        batch_size=32,
    )
    
    # Return the model file
    return training_results.outputs["model"]
