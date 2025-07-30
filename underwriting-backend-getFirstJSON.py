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
    "sec-fetch-site": "same-site",
    "referer": "https://join-dev.foxquilt.com/"
}

query = """
query getFirstJSON($policyFoxdenId: String, $effectiveDate: String, $transactionDate: String, $timezone: String, $transactionType: String!, $country: String, $provinceOrState: String) {
  getFirstJSON(
    policyFoxdenId: $policyFoxdenId
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
    return json.dumps({
        "operationName": "getFirstJSON",
        "variables": {
            "effectiveDate": "2025-07-30",
            "transactionDate": "2025-07-30",
            "timezone": "America/Toronto",
            "transactionType": "New Business",
            "country": "United States of America",
            "provinceOrState": "Florida"
        },
        "query": query
    })

def log_important_response_info(data):
    try:
        result = data["data"]["getFirstJSON"]
        print("[RESULT] isStateActive:", result.get("isStateActive"))

        json_field = result.get("json", {})
        if isinstance(json_field, dict):
            print("[RESULT] json top-level keys:", list(json_field.keys()))
        else:
            print("[WARN] json field is not a dict")

        raw_json = json.dumps(data)
        truncated = (raw_json[:1000] + "...[truncated]") if len(raw_json) > 1000 else raw_json
        print("[TRUNCATED FULL RESPONSE]", truncated)

    except Exception as e:
        print("[ERROR] Unexpected response format:", e)
        print("[RAW]", json.dumps(data, indent=2)[:1000] + "...[truncated]")

def send_request_with_retries(payload, retries=3):
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                return response
            else:
                print(f"[WARN] Attempt #{attempt} failed | Status: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Attempt #{attempt} failed | Error: {e}")
        time.sleep(2)
    return None

def send_request_loop(total_times):
    for i in range(total_times):
        print(f"\n[INFO] ===== Request #{i + 1} | Remaining: {total_times - i - 1} =====")
        start_time = datetime.now()
        payload = build_payload()

        response = send_request_with_retries(payload)
        if response is None:
            print("[ERROR] All retry attempts failed.")
        else:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"[INFO] Response received in {duration:.2f}s | Status: {response.status_code}")
            try:
                data = response.json()
                log_important_response_info(data)
            except Exception as e:
                print("[ERROR] JSON parsing failed:", e)
                print("[RAW]", response.text[:1000] + "...[truncated]")

        time.sleep(5)

send_request_loop(150)
