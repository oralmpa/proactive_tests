from proactive import getProActiveGateway

gateway = getProActiveGateway()

# Create job
job = gateway.createJob("zenoh_file_transfer_job")

# ---- 1. Write to Zenoh Task ----
write_task = gateway.createPythonTask("write_to_zenoh")
write_task.setTaskExecutionScript("""
import zenoh
import time

# Setup
key = "demo/file"
file_path = "my_data/hello.txt"

# Read the file content
with open(file_path, "r") as f:
    content = f.read()

# Put to Zenoh
session = zenoh.open({})
session.put(key, content)
session.close()

print(f"✔ File pushed to Zenoh at key: {key}")
""")

# Input file to send to Zenoh
write_task.addInputFile("my_data/hello.txt")  # Upload a simple file

# ---- 2. Read from Zenoh Task ----
read_task = gateway.createPythonTask("read_from_zenoh")
read_task.setTaskExecutionScript("""
import zenoh
import time

key = "demo/file"
session = zenoh.open({})

# Get from Zenoh
result = session.get(key).wait()
session.close()

# Output
data = result[0].payload.decode("utf-8")
print("📥 Retrieved from Zenoh:")
print(data)
""")

# Add task dependencies
job.addTask(write_task)
job.addTask(read_task).dependsOn(write_task)

# Submit job
job_id = gateway.submitJob(job)
print(f"📨 Job submitted with ID: {job_id}")

# Fetch job output
job_output = gateway.getJobOutput(job_id)
print("📤 Job Output:")
print(job_output)

gateway.close()
