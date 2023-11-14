import subprocess
import os
import json

# Assuming each line of the log file is in the format: timestamp - [LEVEL] - Message - IP:...
log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs/app.log')

elastic_password = "2GpaWu*RYcvAq7TxuXvk"

with open(log_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.split(' - ')
    if len(parts) >= 4:
        timestamp = parts[0].strip()
        log_level = parts[1].strip().strip('[]')
        message = ' - '.join(parts[2:-1]).strip()
        ip_address = parts[-1].split(':')[-1].strip()

        # Constructing the JSON payload for Elasticsearch
        json_payload = {
            "timestamp": timestamp,
            "loglevel": log_level,
            "message": message,
            "ip_address": ip_address
            # Add other fields if needed
        }

        # Using subprocess to execute curl command
        # Replace with your Elasticsearch URL and credentials

        curl_command = [
            "curl",
            "--cacert",
            "/etc/elasticsearch/certs/http_ca.crt",
            "-XPOST",
            "-u",
            f"elastic:{elastic_password}",
            "-H",
            "Content-Type: application/json",
            "https://localhost:9200/my_logs/_doc",
            "-d",
            json.dumps(json_payload)  # Properly format the JSON payload
        ]

        # Print JSON payload for debugging purposes
        # print(json.dumps(json_payload)) 

        # Print JSON payload for debugging purposes
        # print("Executing command:", ' '.join(curl_command))

        # Execute the curl command
        subprocess.run(curl_command)
