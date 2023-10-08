from flask import Flask, request
import sys
import json
from time import sleep

print()

from a_get_bearer_token import getBearerToken
from b_create_subscription import createSubscription
from c_oauth_auth_code import authenticate
from d_retrieve_subscription import retrieveSubscription
from e_update_subscription import updateSubscription

from inspect_balance import retrieveAvailableBalance
from inspect_statement import retrieveStatement

from pay_initiate_payment import initiatePayment
from pay_sign_payment_req import signPaymentRequest

import webbrowser

from utils import getUserData, getPaymentData

SUBSCRIPTION_REDIRECT_URI = 'https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/oauth2/authorize?response_type=code&redirect_uri=http://localhost&scope=UserOAuth2Security&client_id=bd230620-1aa5-4509-858c-81e902d5c7e4&subscriptionid='
PAYMENTS_REDIRECT_URI = 'https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/oauth2/authorize?response_type=code&redirect_uri=http://localhost&scope=UserOAuth2Security&client_id=bd230620-1aa5-4509-858c-81e902d5c7e4&paymentid='

app = Flask(__name__)

userData = getUserData()
bearer_token = ''

subscription_id = userData['subscriptionId']
accountNo = userData['accountNumber']
altAccount = userData['altAccount']
auth_bearer_token = userData['bearerToken']
subscriptionDataDump = userData['subscription']

creatingSubscriber = (subscription_id == '')

@app.route("/")
def hello_world():
    if request.method == "GET":
        code = request.args.get('code')
        # print("Got code from localhost", code)
        auth_bearer_token = authenticate(code, subscription_id)
        print("Got token after OAuth authorization ", auth_bearer_token)
        sleep(3)
        subscription = retrieveSubscription(bearer_token, subscription_id)
        print("Retrieved subscription: ", subscription)
        updatedSubs = updateSubscription(subscription[0], auth_bearer_token['access_token'])
        print("Updated subs: ", updatedSubs.text)
        # retrieveAvailableBalance(subscription_id, )
        balance = retrieveAvailableBalance(subscription_id, bearer_token, accountNo)
        print("Balance", balance)
        input()
        

    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    bearer_token = getBearerToken()
    print("Got new bearer token, ", bearer_token, "\n")
    

    if creatingSubscriber:
        subscription_id = createSubscription(bearer_token)
        print(subscription_id)
        input("Press enter to continue")
        webbrowser.open(SUBSCRIPTION_REDIRECT_URI + subscription_id)
        # start listening for a response
        app.run(host='0.0.0.0', port=80)
    
    updatedSubs = updateSubscription(subscriptionDataDump, auth_bearer_token)
    print("Updated subs", updatedSubs.text, "\n") # can be error 400

    subscription = retrieveSubscription(auth_bearer_token, subscription_id)
    print("Retrieved subscription: ", subscription, "\n")

    balance = retrieveAvailableBalance(subscription_id, bearer_token, accountNo)
    print("Retrieved balance: ", balance, "\n")

    statement = retrieveStatement(subscription_id, bearer_token, accountNo)
    print("Retrieved statement: ", statement, "\n")

    ####

    # Load payment data
    paymentData = getPaymentData()
    print("Payment data: ", paymentData, '\n')

    # Sign payment request
    signedResponse = signPaymentRequest(paymentData['debtor'], paymentData['creditor'], paymentData['amount'], paymentData['details'])
    print("Signed response: ", signedResponse, '\n')

    # Initiate Payment
    payment_initiated = initiatePayment(signedResponse, bearer_token, subscription_id)
    print("Payment initialized: ", payment_initiated, '\n')

    
    



    
