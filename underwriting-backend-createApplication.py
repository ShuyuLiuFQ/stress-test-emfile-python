import requests
import json
import time
from datetime import datetime

URL = "https://foxden-dev.api.foxquilt.com/underwriting/2022-06-30/graphql"

HEADERS = {
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

PAYLOAD_TEMPLATE = {
    "operationName": "createApplication",
    "variables": {
        "answersInfo": {
            "BusinessInformation_100_Country_WORLD_EN": "BusinessInformation_100_Country_01_WORLD_EN",
            "BusinessInformation_100_Province_WORLD_EN": "BusinessInformation_100_Province_01_WORLD_EN",
            "BusinessInformation_100_EffectiveDate_WORLD_EN": "2025-07-30",
            "BusinessInformation_100_PrimaryProfession_WORLD_EN": "BusinessInformation_100_Profession_9219_1820001_WORLD_EN",
            "BusinessInformation_100_CustomerInfo_WORLD_EN": {
                "firstName": "tom",
                "lastName": "smith",
                "email": "hestergong@foxquilt.com",
                "phoneNumber": "13453425345"
            },
            "primaryProfessionLabel": "Yoga Instructors"
        },
        "hubspotTracker": "3391f76e1046a933ac7e83a2ac6611e8",
        "pageName": "BusinessInformationCountry_100",
        "effectiveDateUTC": "Wed Jul 30 2025 00:00:00 GMT-0400 (Eastern Daylight Time)",
        "transactionType": "New Business",
        "transactionDateUTC": "Wed Jul 30 2025 11:37:12 GMT-0400 (Eastern Daylight Time)",
        "country": "Canada",
        "provinceOrState": "Ontario"
    },
    "query": """mutation createApplication($answersInfo: createApplicationAnswersInput!, $pageName: String!, $groupName: String, $hubspotTracker: String, $policyFoxdenId: String, $cancellationReason: String, $cancellationTrigger: String, $effectiveDateUTC: String, $transactionDateUTC: String, $transactionType: String!, $country: String!, $provinceOrState: String!) {
  createApplication(
    answersInfo: $answersInfo
    pageName: $pageName
    groupName: $groupName
    hubspotTracker: $hubspotTracker
    policyFoxdenId: $policyFoxdenId
    cancellationReason: $cancellationReason
    cancellationTrigger: $cancellationTrigger
    effectiveDateUTC: $effectiveDateUTC
    transactionDateUTC: $transactionDateUTC
    transactionType: $transactionType
    country: $country
    provinceOrState: $provinceOrState
  ) {
    ... on ApplicationSuccess {
      applicationId
      __typename
    }
    ... on ApplicationFailure {
      error
      __typename
    }
    __typename
  }
}"""
}

def send_request(payload, idx, retries=3):
    for attempt in range(1, retries + 1):
        try:
            ts = datetime.now()
            response = requests.post(URL, headers=HEADERS, data=payload, timeout=10)
            if response.status_code == 200:
                return idx, ts, response.status_code, response
            else:
                print(f"[WARN] #{idx} | Attempt #{attempt} failed | Status: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] #{idx} | Attempt #{attempt} failed | Error: {e}")
        time.sleep(1)
    return idx, datetime.now(), "ERROR", None

def format_response(idx, ts, status, response):
    if status == "ERROR":
        print(f"[{idx}] {ts.isoformat()} | Status: ERROR | Result: {response}")
        return

    try:
        data = response.json()
        result = data.get("data", {}).get("createApplication", {})

        if result.get("__typename") == "ApplicationSuccess":
            app_id = result.get("applicationId", "UNKNOWN")
            print(f"[{idx}] {ts.isoformat()} | Status: {status} | ApplicationId: {app_id}")
        elif result.get("__typename") == "ApplicationFailure":
            error_msg = result.get("error", "Unknown error")
            print(f"[{idx}] {ts.isoformat()} | Status: FAILURE | Error: {error_msg}")
        else:
            print(f"[{idx}] {ts.isoformat()} | Status: {status} | Unexpected typename: {result.get('__typename')}")
    except Exception as e:
        print(f"[{idx}] {ts.isoformat()} | Status: {status} | JSON parse error: {e}")
        try:
            print("Raw:", response.text[:500] + "...[truncated]")
        except Exception:
            pass

def run_stress_test(total_requests=200):
    iso_start = datetime.now()
    start_time = time.time()

    for i in range(total_requests):
        payload = json.dumps(PAYLOAD_TEMPLATE)
        idx, ts, status, response = send_request(payload, i)
        format_response(idx, ts, status, response)

    iso_end = datetime.now()
    end_time = time.time()
    total_duration = end_time - start_time

    print(f"\n[START] Sequential Requests for createApplication | Total Requests: {total_requests}")
    print(f"[START TIME]: {iso_start.isoformat()}")
    print(f"[END TIME]:   {iso_end.isoformat()}")
    print(f"[DURATION]:   {total_duration:.2f} seconds")

if __name__ == "__main__":
    run_stress_test(total_requests=150)
