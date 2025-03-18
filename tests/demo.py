import os
log_dir = "logs"
#os.makedirs(log_dir, exist_ok=True)  # Creates 'logs' if it doesn't exist
log_file = os.path.join(log_dir, "test_execution.log")
print(log_file)