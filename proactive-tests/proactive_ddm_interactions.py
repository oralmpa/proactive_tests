from proactive import getProActiveGateway

# Connect to ProActive
gateway = getProActiveGateway()
job = gateway.createJob("download_and_upload_datasets_job")

task_code = '''
import requests
import json
from io import BytesIO

# Configuration
dataset_filenames = ["titanic.json", "titanic-test.json"]
base_url = "http://146.124.106.200/api"
catalog_url = f"{base_url}/catalog"
file_url_template = f"{base_url}/file/{{}}"
upload_url = f"{base_url}/files/upload"
project_id = "demo_project_001"

# Metadata for upload
user_filenames = ["titanic_custom", "titanic_test_custom"]
descriptions = ["Titanic training data", "Titanic test data"]
metadata_entries = [{"source": "kaggle"}, {"source": "kaggle"}]

# Collect files in memory
upload_files = []
metadata_files = []

for i, fname in enumerate(dataset_filenames):
    try:
        print("Looking up:", fname)
        r = requests.get(
            catalog_url,
            params={
                "filename": fname,
                "sort": "created,desc",
                "page": 1,
                "perPage": 1
            }
        )
        r.raise_for_status()
        results = r.json().get("data", [])
        if not results:
            print("Not found:", fname)
            continue

        entry = results[0]
        file_id = entry.get("id")
        file_url = file_url_template.format(file_id)

        print("Downloading:", file_url)
        f_response = requests.get(file_url)
        f_response.raise_for_status()

        file_bytes = BytesIO(f_response.content)
        upload_files.append(("files", (fname, file_bytes, "application/octet-stream")))

        # Add matching metadata as a file-like object
        metadata_json = json.dumps(metadata_entries[i])
        metadata_bytes = BytesIO(metadata_json.encode("utf-8"))
        metadata_files.append(("metadata-files", (f"meta_{fname}", metadata_bytes, "application/json")))

    except Exception as e:
        print(f"Error processing {fname}:", str(e))

# Prepare form fields
form_data = {
    "project_id": project_id,
    "user_filenames": json.dumps(user_filenames),
    "descriptions": json.dumps(descriptions),
}

# Combine all files
all_files = upload_files + metadata_files

# POST to upload endpoint
print("Uploading to:", upload_url)
response = requests.post(upload_url, files=all_files, data=form_data)

print("Status:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw response:", response.text)
'''

# Submit ProActive task
task = gateway.createPythonTask("download_and_upload_task")
task.setTaskImplementation(task_code)
job.addTask(task)

job_id = gateway.submitJob(job)
print(f"Job submitted: {job_id}")
print("Job output:")
print(gateway.getJobOutput(job_id))

gateway.close()
print("Disconnected.")
