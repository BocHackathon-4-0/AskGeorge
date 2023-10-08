import random
import uuid
from datetime import datetime, timedelta
import os
import json


current_date = datetime.now()
current_month = current_date.month
current_day = current_date.day
monthly_wage = 8000

categories = {
    "transport": {
        "names": ["ESSO", "Petrolina", "Panikos Car Mechanic"],
        "freqs": [6, 3, 1],
        "price": 30
    },
    "groceries": {
        "names": ["Alphamega Hypermarket", "Athienitis"],
        "freqs": [3, 1],
        "price": 125
    },
    "restaurants": {
        "names": ["Evroulla", "Foukou tou Yiakoumi", "Etsi Apla Opos Palia", "Deliyard", "TGI Fridays"],
        "freqs": [12, 4, 1, 5, 8],
        "price": 15
    },
    "shopping": {
        "names": ["ZARA", "Amazon", "Ebay"],
        "freqs": [4, 1, 1],
        "price": 50
    },
    "home": {
        "names": ["Rent", "Electricity"],
        "freqs": [2, 1],
        "price": 2000
    }
}

VARIANCE_PERCENTAGE = 0.10  # This will cause a -10% to 10% variance.


def random_date_in_month(year=2023, month=1, max_day=None):
    start_date = datetime(year, month, 1)
    if max_day:
        end_date = datetime(year, month, max_day)
    elif month == 12:
        end_date = datetime(year+1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month+1, 1) - timedelta(days=1)
    
    random_date = start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    return random_date.strftime('%d/%m/%Y')

def apply_variance(value):
    variance = random.uniform(-VARIANCE_PERCENTAGE, VARIANCE_PERCENTAGE)
    return round(value * (1 + variance))

def generate_dummy_data_for_month(categories, month):
    transactions = []

    for category, details in categories.items():
        for store, freq in zip(details['names'], details['freqs']):
            for _ in range(freq):
                transaction = {
                    'id': str(uuid.uuid4().hex),  # generates a unique hexadecimal ID
                    'dcInd': 'DEBIT',
                    'transactionAmount': {
                        'amount': apply_variance(details['price']),
                        'currency': 'EUR'
                    },
                    'description': f"***{category.upper()}***{store}",
                    'postingDate': random_date_in_month(month=month),
                    'valueDate': random_date_in_month(month=month),
                    'transactionType': 'PAYMENT'
                }
                transactions.append(transaction)
    
    transaction = {
        'id': str(uuid.uuid4().hex),  # generates a unique hexadecimal ID
        'dcInd': 'CREDIT',
        'transactionAmount': {
            'amount': monthly_wage,
            'currency': 'EUR'
        },
        'description': f"***WAGES***Software Programming Job",
        'postingDate': random_date_in_month(month=month),
        'valueDate': random_date_in_month(month=month),
        'transactionType': 'PAYMENT'
    }
    transactions.append(transaction)
    
    return transactions


def generate_dummy_data_for_running_month(categories, month, day):
    transactions = []

    current_date_factor = day/30.0  # Assuming average month length as 30 days

    for category, details in categories.items():
        for store, freq in zip(details['names'], details['freqs']):
            # For Rent, Electricity, and Wages, we don't want to change the frequency.
            if category in ["home"] and store in ["Rent", "Electricity"]:
                adjusted_freq = freq
            else:
                adjusted_freq = round(freq * current_date_factor)
                
            for _ in range(adjusted_freq):
                transaction = {
                    'id': str(uuid.uuid4().hex),
                    'dcInd': 'DEBIT',
                    'transactionAmount': {
                        'amount': apply_variance(details['price']),
                        'currency': 'EUR'
                    },
                    'description': f"***{category.upper()}***{store}",
                    'postingDate': random_date_in_month(month=month, max_day=day),
                    'valueDate': random_date_in_month(month=month, max_day=day),
                    'transactionType': 'PAYMENT'
                }
                transactions.append(transaction)

    transaction = {
        'id': str(uuid.uuid4().hex),
        'dcInd': 'CREDIT',
        'transactionAmount': {
            'amount': monthly_wage,
            'currency': 'EUR'
        },
        'description': f"***WAGES***Software Programming Job",
        'postingDate': random_date_in_month(month=month, max_day=day),
        'valueDate': random_date_in_month(month=month, max_day=day),
        'transactionType': 'PAYMENT'
    }
    transactions.append(transaction)
    
    return transactions


# Create monthly statements for Jan to Aug
monthly_statements = {}
for month in range(1, current_month + 1):  # Adjusted range to include October
    if month == current_month:  # If it's October
        monthly_statements[f"Month {month}"] = {
            'account': {
                'bankId': '12345671',
                'accountId': '351012345671',
                'accountAlias': 'ANDREAS',
                'accountType': 'CURRENT',
                'accountName': 'ANDREAS LORDOS',
                'IBAN': 'CY99999999999999999999999999',
                'currency': 'EUR',
                'infoTimeStamp': '1511779237'},
            'transaction': generate_dummy_data_for_running_month(categories, month, current_day)
        }
    else:
        monthly_statements[f"Month {month}"] = {'account': 
                                            {'bankId': '12345671', 
                                            'accountId': '351012345671', 
                                            'accountAlias': 'ANDREAS', 
                                            'accountType': 'CURRENT', 
                                            'accountName': 'ANDREAS LORDOS', 
                                            'IBAN': 'CY99999999999999999999999999', 
                                            'currency': 'EUR', 
                                            'infoTimeStamp': '1511779237'}, 
                                        'transaction': generate_dummy_data_for_month(categories, month)}
        

    

# Save each statement as a JSON in a subfolder
subfolder = 'monthly_statements'
if not os.path.exists(subfolder):
    os.makedirs(subfolder)

for month, statement in monthly_statements.items():
    filename = os.path.join(subfolder, f"{month}.json")
    with open(filename, 'w') as file:
        json.dump(statement, file, indent=4)




