import os
import sys
import json
import yaml

workflow_path = '/Users/suderman/Workspaces/JHU/Experiments/variants/variants.yml'

if not os.path.exists(workflow_path):
    print("ERROR: workflow file not found")
else:
    with open(workflow_path) as f:
        benchmark = yaml.safe_load(f)

    for input in benchmark[0]['runs'][0]['inputs']:
        if 'paired' in input:
            for item in input['paired']:
                for key in item.keys():
                    print(key)
        elif 'dataset_id' in input:
            print(f"dataset ID: {input['dataset_id']}")
        elif 'value' in input:
            print(f"literal: {input['value']}")
        else:
            print("Invalid input definition")

