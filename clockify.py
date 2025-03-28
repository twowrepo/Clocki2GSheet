import json
import requests
from datetime import datetime

def get_timeentries_raw(start, end, config):
    url = f"https://reports.api.clockify.me/v1/workspaces/{config.CLOCKIFY_WORKSPACE_ID}/reports/detailed"
    headers = {
        "X-Api-Key": config.CLOCKIFY_API_KEY,
        "Content-Type": "application/json"
    }

    all_entries = []
    page = 1
    while True:
        payload = {
            "dateRangeStart": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "dateRangeEnd": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "detailedFilter": {"page": page, "pageSize": 200},
            "exportType": "JSON",
            "rounding": False
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        entries = data.get("timeentries", [])
        if not entries:
            break

        all_entries.extend(entries)

        if len(entries) < 200:
            break
        page += 1

    return {"timeentries": all_entries}
