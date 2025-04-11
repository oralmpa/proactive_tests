"""
This script showcases an advanced ProActive Scheduler use case focused on executing Python tasks that require pre-execution setup, post-execution cleanup, and access to external files or resources. The workflow includes the following steps:

1. Establish a connection with the ProActive Scheduler using the proactive library, demonstrating the SDK's capability to interact with the scheduler.
2. Create a ProActive job named "demo_exec_file_job," serving as a container for the tasks.
3. Define a Python task "demo_exec_file_task," configured to execute a Python script ('main.py') with parameters ('param1' and 'param2'), demonstrating how to run complex scripts with arguments.
4. Configure the task to include a directory ('demo_exec_file/hellopkg/**') as input files, illustrating the scheduler's handling of tasks with external dependencies.
5. Set the task to execute using Python 3 by specifying the Python command in the task's generic information, highlighting the SDK's support for different Python versions.
6. Add the configured task to the job, preparing it for submission.
7. Submit the job to the ProActive Scheduler, capturing the job ID for reference, and demonstrating the scheduler's job management capabilities.
8. Fetch and print the job's output, providing insights into the task's execution results.

The script concludes by disconnecting from the gateway, emphasizing the importance of clean disconnection and resource management after job execution.

This demonstration highlights the ProActive Scheduler's versatility in managing Python tasks, especially those requiring specific pre- and post-execution steps or dependent on external resources.
"""
from proactive import getProActiveGateway

gateway = getProActiveGateway()

print("Creating a proactive job...")
job = gateway.createJob("demo_exec_file_job")

print("Creating a proactive task...")
task = gateway.createPythonTask("demo_exec_file_task")
task.setTaskExecutionFromFile('demo_exec_file/main.py', ['param1', 'param2'])
task.addInputFile('demo_exec_file/hellopkg/**')

print("Adding proactive tasks to the proactive job...")
job.addTask(task)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
print("job_id: " + str(job_id))

print("Getting job output...")
job_output = gateway.getJobOutput(job_id)
print(job_output)

gateway.close()
print("Disconnected and finished.")