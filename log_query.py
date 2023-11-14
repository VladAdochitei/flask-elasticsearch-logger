import subprocess
import json

# Elasticsearch password
elastic_password = "2GpaWu*RYcvAq7TxuXvk"

# Elasticsearch URL and endpoint for searching
elasticsearch_url = 'https://localhost:9200/my_logs/_search'

# Construct the query payload
query_payload = {
    "query": {
        "match": {
            "message": "Unauthorized"  # Search for logs containing "Unauthorized"
        }
    }
}

# Using subprocess to execute curl command
curl_command = [
    "curl",
    "--cacert",
    "/etc/elasticsearch/certs/http_ca.crt",
    "-XGET",
    "-u",
    f"elastic:{elastic_password}",
    "-H",
    "Content-Type: application/json",
    elasticsearch_url,
    "-d",
    json.dumps(query_payload)
]

# Execute the curl command
result = subprocess.run(curl_command, capture_output=True, text=True)

# Check the result
if result.returncode == 0:
    print("Request successful!")
    print(result.stdout)  # Print the output
else:
    print("Request failed!")
    print(result.stderr)  # Print the error output
