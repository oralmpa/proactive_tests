"""
This script demonstrates a straightforward use case of submitting a Python task to the ProActive Scheduler for execution. The key steps performed in this script include:

1. Initializing a connection with the ProActive Scheduler using the 'getProActiveGateway' function from the 'proactive' library, facilitating the integration of ProActive Scheduler capabilities into Python applications.
2. Creating a new job named "demo_basic_job" through the ProActive gateway. A job serves as a container for one or more tasks, managed and executed by the scheduler.
3. Configuring a Python task named "demo_basic_task" with an inline script. The script prints a greeting message followed by the current Python version. This demonstrates how to directly embed Python code within a task's configuration for quick and flexible task creation.
4. Adding generic information to specify that the Python task should run using Python 3. This ensures that the task is executed in the correct environment, maintaining compatibility and consistency.
5. Adding the configured Python task to the newly created job, assembling the job's structure with its constituent tasks.
6. Submitting the job to the ProActive Scheduler for execution. The scheduler handles the job's lifecycle, including task scheduling, execution, and resource allocation.
7. Retrieving and displaying the job's output upon completion. This step provides immediate insight into the execution results, which is essential for debugging and validation purposes.
8. Closing the gateway connection to the ProActive Scheduler in a graceful manner. This emphasizes the importance of proper resource management and cleanup after job submission and execution.

This script offers a basic example of how to submit and execute a Python task within the ProActive Scheduler environment, focusing on simplicity and user-friendliness. It lays the groundwork for more sophisticated scheduling and task execution scenarios.
"""
from proactive import getProActiveGateway

# Initialize the ProActive gateway
gateway = getProActiveGateway()

# Create a new ProActive job
print("Creating a proactive job...")
job = gateway.createJob("demo_basic_job")

# Create a Python task
print("Creating a proactive task...")
task = gateway.createPythonTask("demo_basic_task")
task.setTaskImplementation("""
import platform
print("Hello from " + variables.get("PA_TASK_NAME"))
print("Python version: ", platform.python_version())
""")

# Add the Python task to the job
print("Adding proactive tasks to the proactive job...")
job.addTask(task)

# Job submission
print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(job)
print("job_id: " + str(job_id))

# Retrieve job output
print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

# Cleanup
gateway.close()
print("Disconnected and finished.")