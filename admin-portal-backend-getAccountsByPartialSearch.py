import requests
import time

policy_numbers = ['XIT20250522FKLVMT', 'XIT20250522NQEBGV', 'XIT202505227KUSN5', 'XIT20250522YZQ4ED', 'XIT202505213GFYQA',
                  'XIT20250521X22B34', 'XIT20250521C3JVZA', 'XIT20250521LBALKR', 'XIT20250521S6AGV9', 'XIT20250521EAAWSY', 'XIT202505225IGJRU']

url = "http://localhost:4005/local/graphql"

payload_template = (
    "{\"query\":\"query getAccountsByPartialSearch($searchInput: String!, $pageNo: NonNegativeInt!, $pageSize: NonNegativeInt!) "
    "{\\n  getAccountsByPartialSearch(\\n    searchInput: $searchInput\\n    pageNo: $pageNo\\n    pageSize: $pageSize\\n  ) "
    "{\\n    data {\\n      accountNumber\\n      businessName\\n      primaryContactFullName\\n      phoneNumber\\n      emailAddress\\n      "
    "dateCreated\\n      country\\n      agencyName\\n      __typename\\n    }\\n    totalCount\\n    __typename\\n  }\\n}\\n\","
    "\"variables\":{\"searchInput\":\"REPLACE_ME\",\"pageNo\":0,\"pageSize\":10}}"
)

headers = {
  'Cookie': '__hstc=181257784.de8fa7c4923521a4969e7d20a7645957.1753403429789.1753403429789.1753403429789.1; hubspotutk=de8fa7c4923521a4969e7d20a7645957; __hssrc=1; __hssc=181257784.1.1753403429789; messagesUtk=a57c6f1a74dc4d2f92eb7b7dc2991c06; foxden.platform.local=s%3AdWM1p2-ljHWMTXDOGdZuKQYv4d4y66SB.Nn3L6ibax1vzvo2zgzBVMY8Axa4FJH7z%2Bql6JigAPIA; Cookie_1=value; foxden.platform.local=s%3AdWM1p2-ljHWMTXDOGdZuKQYv4d4y66SB.Nn3L6ibax1vzvo2zgzBVMY8Axa4FJH7z%2Bql6JigAPIA',
  'Content-Type': 'application/json'
}

def retrieve_next_payload(t):
  t = t % len(policy_numbers)
  policy_number = policy_numbers[t]
  print(f"sending request for {policy_number}")
  return payload_template.replace("REPLACE_ME", policy_number)


def send_request_recursively(times_left):
  if times_left <= 0:
    return

  payload = retrieve_next_payload(times_left)
  response = requests.request("POST", url, headers=headers, data=payload)
  data = response.json()
  business_name = data["data"]["getAccountsByPartialSearch"]["data"][0]["businessName"]
  print(f"business name received: {business_name}\n, times left: {times_left}")
  time.sleep(5)
  send_request_recursively(times_left - 1)

send_request_recursively(1000)