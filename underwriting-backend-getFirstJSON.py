import requests
import time
import json
from datetime import datetime

url = "https://foxden-dev.api.foxquilt.com/underwriting/2022-06-30/graphql"

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}

query = """
query getFirstJSON($effectiveDate: String, $transactionDate: String, $timezone: String, $transactionType: String!, $country: String, $provinceOrState: String) {
  getFirstJSON(
    effectiveDate: $effectiveDate
    transactionDate: $transactionDate
    timezone: $timezone
    transactionType: $transactionType
    country: $country
    provinceOrState: $provinceOrState
  ) {
    json
    previousAnswers
    policyStartDateStr
    policyExpiryDateStr
    isStateActive
    __typename
  }
}
"""

def build_payload():
    variables = {
        "effectiveDate": "2025-07-30",
        "transactionDate": "2025-07-30",
        "timezone": "America/Toronto",
        "transactionType": "New Business",
        "country": "Canada",
        "provinceOrState": "Ontario"
    }
    print(f"\n[INFO] Building request with variables:\n{json.dumps(variables, indent=2)}")
    return json.dumps({
        "operationName": "getFirstJSON",
        "variables": variables,
        "query": query
    })

def send_request_recursively(times_left):
    if times_left <= 0:
        print("[INFO] All requests completed.")
        return

    print(f"\n[INFO] ----- Request #{1001 - times_left} | Remaining: {times_left} -----")
    start_time = datetime.now()
    payload = build_payload()

    try:
        response = requests.post(url, headers=headers, data=payload)
        duration = (datetime.now() - start_time).total_seconds()
        print(f"[INFO] Response received in {duration:.2f} seconds. Status code: {response.status_code}")

        try:
            data = response.json()
            print(f"[INFO] Response data (truncated):\n{json.dumps(data, indent=2)[:1000]}")
        except Exception as parse_err:
            print("[ERROR] Failed to parse JSON response.")
            print("Raw response text:\n", response.text)
    except Exception as err:
        print(f"[ERROR] Request failed: {err}")

    time.sleep(5)
    send_request_recursively(times_left - 1)

send_request_recursively(1000)
