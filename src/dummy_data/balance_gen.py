import json
from datetime import date, timedelta
import random
import datetime

STARTING_BALANCE = 400  # Initial amount in the account
FLUCTUATION_RANGE = 6  # Variability in daily change
SAVINGS_MODIFIER = 30  # Average daily change for savings account
CURRENT_MODIFIER = 10  # Average daily change for current account

def generate_daily_data(account_number, account_type):
    start_date = date.today().replace(month=1, day=1)  # Beginning of the current year
    end_date = date.today()
    current_date = start_date
    data_list = []
    current_balance = STARTING_BALANCE
    modifier = SAVINGS_MODIFIER if account_type == "savings" else CURRENT_MODIFIER

    while current_date <= end_date:
        delta = modifier + random.uniform(-FLUCTUATION_RANGE, FLUCTUATION_RANGE)
        current_balance += delta
        data_list.append({
            "date": str(current_date),
            "amount": round(current_balance, 2),
            "changeFromYesterday": round(delta, 2)
        })
        current_date += timedelta(days=1)
    
    return data_list

def generate_weekly_data(data_dict):
    weekly_data = []
    first_entry_amount = data_dict[0]["amount"]  # Get the amount of the first entry

    for index in range(0, len(data_dict), 7):  # Iterate every 7 days
        entry = data_dict[index]
        
        # Calculate the change from the first entry for the first week
        # For subsequent weeks, calculate the change from 7 days prior
        if index == 0:
            change = 0
        else:
            change = entry["amount"] - data_dict[index-7]["amount"]
        change = round(change, 2)
        
        weekly_data.append({
            "date": entry["date"],
            "amount": entry["amount"],
            "changeFromLastWeek": change
        })

    return weekly_data


def generate_monthly_data(data_dict):
    # Parse the input JSON if it's a string
    monthly_data = []
    last_month_amount = None
    for entry in data_dict:
        date_parts = entry["date"].split("-")
        year, month, day = map(int, date_parts)

        # Check if the day is the first day of the month
        if day == 1:
            change = 0 if last_month_amount is None else entry["amount"] - last_month_amount
            change = round(change, 2)
            monthly_data.append({
                "date": entry["date"],
                "amount": entry["amount"],
                "changeFromLastMonth": change
            })
            last_month_amount = entry["amount"]

    return monthly_data

def main():
    account_number = "1234567890"
    account_type = input("Choose account type (savings or current): ").lower()

    if account_type not in ["savings", "current"]:
        print("Invalid account type selected. Exiting...")
        return
    
    daily_data = generate_daily_data(account_number, account_type)
    with open(f"{account_number}_{account_type}_daily.json", "w") as f:
        json.dump({"account_number": account_number, "type": account_type, "frequency": "daily", "data": daily_data}, f, indent=4)

    weekly_data = generate_weekly_data(daily_data)
    with open(f"{account_number}_{account_type}_weekly.json", "w") as f:
        json.dump({"account_number": account_number, "type": account_type, "frequency": "weekly", "data": weekly_data}, f, indent=4)

    monthly_data = generate_monthly_data(daily_data)
    with open(f"{account_number}_{account_type}_monthly.json", "w") as f:
        json.dump({"account_number": account_number, "type": account_type, "frequency": "monthly", "data": monthly_data}, f, indent=4)

main()
