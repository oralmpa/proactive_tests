import os
import sys
import pickle
import json
import numpy as np
import io
import requests
import zenoh

def save_datasets(variables, *data):
    for (key, value) in data:
        save_dataset(variables, key, value)


def load_datasets(variables, *keys):
    return [load_dataset(variables, key) for key in keys]


def save_dataset(variables, key, value):
    value_size = sys.getsizeof(value)
    print(f"Saving output data of size {value_size} with key {key}")
    if value_size > 100:
        print("Saving as large dataset")
        save_large_dataset(variables, key, value)
    else:
        print("Saving using the 'variables' object (internal database)")
        variables.put(key, value)


def load_dataset(variables, key):
    print(f"Loading input data with key {key}")
    if key in variables:
        print("Loading using the 'variables' object (internal database)")
        return variables.get(key)
    else:
        print("Loading as large dataset")
        return load_large_dataset(variables, key)


def save_large_dataset(variables, key, value):
    job_id = variables.get("PA_JOB_ID")
    task_id = variables.get("PA_TASK_ID")
    task_folder = os.path.join("/shared", job_id, task_id)
    os.makedirs(task_folder, exist_ok=True)
    output_filename = os.path.join(task_folder, key)
    with open(output_filename, "wb") as outfile:
        pickle.dump(value, outfile)
    variables.put("PREVIOUS_TASK_ID", str(task_id))


def load_large_dataset(variables, key):
    job_id = variables.get("PA_JOB_ID")
    task_id = variables.get("PREVIOUS_TASK_ID")
    task_folder = os.path.join("/shared", job_id, task_id)
    input_filename = os.path.join(task_folder, key)
    with open(input_filename, "rb") as f:
        file_contents = pickle.load(f)
    return file_contents

def create_dir(variables, key):
    job_id = variables.get("PA_JOB_ID")
    task_id = variables.get("PREVIOUS_TASK_ID")
    folder = os.path.join("/shared", job_id, task_id, key)
    os.makedirs(folder, exist_ok=True)

    return folder

def read_data_from_zenoh(zenoh_key_expression):

    # my_url = f'http://127.0.0.1:18000/projects/{project_id}/datasets/{dataset_id}'
    # #requests.get(os.path.join("http://127.0.0.1:18000/projects/", {project_id} , "/datasets/", {dataset_id}))
    # data = requests.get(my_url)
    # print(my_url)
    # print(data)
    # return data
    config = {
        'mode': 'client',
        'connect': {
            'endpoints': ["127.0.0.1:18000"]  
        }
    }

 
    zenoh_session = zenoh.open()

    #zenoh_session = zenoh.open(zenoh.Config.from_file("zenoh-client.json5"))
    #zenoh_key_expr = "projects/{project_id}/datasets/{dataset_id}"
    zenoh_key_expr = zenoh_key_expression
    try:
        replies = zenoh_session.get(zenoh_key_expr, zenoh.ListCollector())
        file_content = None
        for reply in replies():
            if reply.ok:
                file_content = reply.ok.payload
                break
        if file_content:
            return dataset_id, io.BytesIO(file_content)
        else:
            return None
    except Exception as e:
        return e

    zenoh_session.close()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
