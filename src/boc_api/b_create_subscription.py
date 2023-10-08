import requests
import json
from time import time
from uuid import uuid4

url = "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/v1/subscriptions"


def createSubscription(bearerToken):
    payload = json.dumps({
    "accounts": {
        "transactionHistory": True,
        "balance": True,
        "details": True,
        "checkFundsAvailability": True
    },
    "payments": {
        "limit": 99999999,
        "currency": "EUR",
        "amount": 999999999
    }
    })
    headers = {
    'Authorization': f'Bearer {bearerToken}',
    'Content-Type': 'application/json',
    'timeStamp': str(int(time())),
    'journeyId': str(uuid4()),
    'x-client-certificate': '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'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()["subscriptionId"]
    except:
        raise Exception("Error creating subscription (step 2)")
    

# createSubscription('AAIkYmQyMzA2MjAtMWFhNS00NTA5LTg1OGMtODFlOTAyZDVjN2U0qPv4Kd67lbbixS9xlOmOdRUnjN-Fs7tHxCrFs0wmO7Z4ihNLwhs5jqAe5oRBvxgOB2K57niseKCAMpYgxDpStd1B4zoQ0zq3ZD_i4zP5zYZY9mtF3hsHOTkctoLY67mCGKcBCBz9tqPY3Hyfr5DfKQ')