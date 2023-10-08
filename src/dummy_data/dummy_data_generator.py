from random import shuffle
import json

OUTPUT_FILE = "testData.json"

# Defining the categories
my_bank_numb = "BCYPCY2N" # BOC swift code
my_account_number = "351012345671"
my_name = "ANDREAS MICHAEL"

paying_out_to_bank = "BCYPCY2N" # BOC swift code
paying_out_to_account_no = "0"

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
    }
}

final_data = []

# Printing each item based on its frequency
for category, data in categories.items():
    for name, freq in zip(data["names"], data["freqs"]):
        for _ in range(freq):
            final_data.append({
                "debtor": {
                    "bankId": my_bank_numb,
                    "name": my_name,
                    "accountId": my_account_number
                },
                
                "creditor": {
                    "bankId": paying_out_to_bank,
                    "name": name,
                    "accountId": paying_out_to_account_no
                },
                
                "amount": categories[category]["price"],
                "details": "***" + category.upper() + "***" + name
            })



shuffle(final_data)


final_data = {

    "debtor": {
        "bankId": my_bank_numb,
        "name": my_name,
        "accountId": my_account_number
    },
    
    "creditor": {
        "bankId": paying_out_to_bank,
        "name": "Evroulla",
        "accountId": paying_out_to_account_no
    },
    "amount": "20",
    "details": "***" + "TESTCATEGORY" + "***" + "Evroulla"
}


jsonData = json.dumps(final_data, indent=4)

# Writing to json
with open(OUTPUT_FILE, "w") as outfile:
    outfile.write(jsonData)


#       "bankId": "BOFAUS3N",
#       "name": "Christos",
#       "accountId": "898113845429"
