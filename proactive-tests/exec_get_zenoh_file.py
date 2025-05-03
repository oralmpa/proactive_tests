"""
This script demonstrates how to submit a Zenoh-based file download task to the ProActive Scheduler.

It follows a similar structure to 'demo_exec_file.py', but instead runs 'zenoh_get_file.py', which pulls a file from a Zenoh key and saves it locally.

Steps:
1. Connect to ProActive Scheduler
2. Create a job and a Python task that runs 'zenoh_get_file.py' with a key and local path
3. Add input dependencies (the script itself + any helper packages)
4. Submit job and fetch output
"""

from proactive import getProActiveGateway
import os

gateway = getProActiveGateway()

print("Creating a proactive job for Zenoh GET...")
job = gateway.createJob("zenoh_get_file_job")

print("Creating the task...")
task = gateway.createPythonTask("zenoh_get_file_task")

# task.setTaskImplementation("""
# import sys, platform
# print("Python version:", platform.python_version(), sys.executable)

# from importlib.metadata import distributions

# for dist in sorted(distributions(), key=lambda d: d.metadata["Name"].lower()):
#     name = dist.metadata["Name"]
#     ver  = dist.version
#     print(f"{name}=={ver}")
# """)

# ✅ Include both the script and any Zenoh config/dependencies
# task.addInputFile("exec_get_zenoh_file/get_file/**")
task.addInputFile("exec_get_zenoh_file/**")

# task.setDefaultPython('python3')
# task.setDefaultPython("/usr/bin/python3")
task.setDefaultPython("/opt/miniconda3/py39/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py310/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py311/bin/python3")
# task.setDefaultPython("/opt/miniconda3/py312/bin/python3")

requirements_path = os.path.join("exec_get_zenoh_file", "requirements.txt").replace("\\", "/")
task.setVirtualEnvFromFile(requirements_file=requirements_path, verbosity=False)

# 👇 Change the arguments to match the key and the path you want inside the worker
zenoh_key = "projects/demo/myfile.txt"
local_target = "downloaded.txt"
task.setTaskExecutionFromFile("exec_get_zenoh_file/main.py", [zenoh_key, local_target])

print("Adding task to the job...")
job.addTask(task)

print("Submitting the job to the scheduler...")
job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
print(f"job_id: {job_id}")

print("Retrieving job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

gateway.close()
print("Disconnected from ProActive. Done.")
