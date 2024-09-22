import requests
import json

# Authentication
bearer_token = 'YOUR_DATABRICKS_BEARER_TOKEN'
base_url = 'https://YOUR_DATABRICKS_INSTANCE'

# Payload to run the notebook
payload = {
    "run_name": "MyNotebookRun",
    "existing_cluster_id": "YOUR_CLUSTER_ID",
    "notebook_task": {
        "notebook_path": "/path/to/your/notebook"
    }
}

# Headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {bearer_token}'
}

# Submit the request
response = requests.post(f"{base_url}/api/2.0/jobs/runs/submit", headers=headers, data=json.dumps(payload))

# Handle the response
if response.status_code == 200:
    print("Notebook run successfully")
else:
    print(f"Failed to run notebook: {response.text}")