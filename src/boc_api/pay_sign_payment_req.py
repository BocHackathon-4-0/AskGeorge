import requests
import json

url = "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/jwssignverifyapi/sign"

#       "bankId": "BOFAUS3N",
#       "name": "Christos",
#       "accountId": "898113845429"


def signPaymentRequest(debtor, creditor, amount, paymentDetails):

    dataDict = {
        "debtor": debtor, # ie me,
        "creditor": creditor,
        "transactionAmount": {
            "amount": amount,
            "currency": "EUR"
        },
        "paymentDetails": paymentDetails
    }

    payload = json.dumps(dataDict)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()
