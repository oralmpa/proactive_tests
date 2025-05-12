from proactive import getProActiveGateway

# Connect to ProActive
gateway = getProActiveGateway()
job = gateway.createJob("download_datasets_job")

# Filenames to download (upload_filename in the catalog)
dataset_filenames = ["titanic.json", "titanic-test.json"]

# The correct inline Python script
task_code = '''
import requests

dataset_filenames = ["titanic.json", "titanic-test.json"]
base_url = "http://146.124.106.200/api"
catalog_url = f"{base_url}/catalog"
file_url_template = f"{base_url}/file/{{}}"

for fname in dataset_filenames:
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
        file_type = entry.get("file_type") or "bin"
        save_name = fname  # use given name to save

        file_url = file_url_template.format(file_id)
        print("Downloading:", file_url)
        f_response = requests.get(file_url)
        f_response.raise_for_status()

        with open(save_name, "wb") as f:
            f.write(f_response.content)
        print("Saved:", save_name)

    except Exception as e:
        print(f"Error processing {{fname}}:", str(e))
'''

# Inject script and submit
task = gateway.createPythonTask("download_dataset_task")
task.setTaskImplementation(task_code)
job.addTask(task)
job_id = gateway.submitJob(job)
print(f"Job submitted: {job_id}")
print("Job output:")
print(gateway.getJobOutput(job_id))
gateway.close()
print("Disconnected.")
