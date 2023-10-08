# convert statements into summary data that is useful
import json
import os
import calendar
from datetime import datetime
from collections import defaultdict


def getTotalMonthlySpending(JSON_FOLDER='dummy_data/monthly_statements'):
    """
    Get total monthly moneyMade, moneySpent, and leftoverMoney values.

    Parameters:
    - JSON_FOLDER: The folder containing the monthly statement JSON files.

    Returns:
    - Prints a table of the monthly moneyMade, moneySpent, and leftoverMoney values.
    - Generates JSON file of data as well
    """

    # Function to read JSON file content
    def read_json_file(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def print_row(month, indicator, moneyMade, moneyMade_change_pct, moneySpent, moneySpent_change_pct, leftoverMoney, leftoverMoney_change_pct):
        moneyMade_change_pct_str = '--'.center(7) if moneyMade_change_pct is None else f"{moneyMade_change_pct:7.2f}%"
        moneySpent_change_pct_str = '--'.center(7) if moneySpent_change_pct is None else f"{moneySpent_change_pct:7.2f}%"
        leftoverMoney_change_pct_str = '--'.center(7) if leftoverMoney_change_pct is None else f"{leftoverMoney_change_pct:7.2f}%"
        
        # Do not display % change for "Curr" rows
        if indicator == "(Curr)":
            moneyMade_change_pct_str = '--'.center(7)
            moneySpent_change_pct_str = '--'.center(7)
            leftoverMoney_change_pct_str = '--'.center(7)
        
        print(f"{month:9}{indicator:7} | {moneyMade:8.2f} | {moneyMade_change_pct_str} | {moneySpent:8.2f} | {moneySpent_change_pct_str} | {leftoverMoney:8.2f} | {leftoverMoney_change_pct_str}")

    # Load monthly data
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
    monthly_data = {f.split('.')[0]: read_json_file(os.path.join(JSON_FOLDER, f)) for f in files}

    monthly_totals = {}
    previous_totals = None

    # Project values for the current month
    today = datetime.today()
    current_month = f"Month {today.month}"
    days_passed = today.day
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    projection_factor = days_in_month / days_passed if days_passed != 0 else 1

    for month, data in sorted(monthly_data.items(), key=lambda x: int(x[0].split()[1])):
        moneyMade = sum(t['transactionAmount']['amount'] for t in data['transaction'] if t['dcInd'] == 'CREDIT')
        moneySpent = sum(t['transactionAmount']['amount'] for t in data['transaction'] if t['dcInd'] == 'DEBIT')
        leftoverMoney = moneyMade - moneySpent

        monthly_totals[month] = {
            'moneyMade': moneyMade,
            'moneySpent': moneySpent,
            'leftoverMoney': leftoverMoney,
            'moneyMade_change_pct': None,
            'moneySpent_change_pct': None,
            'leftoverMoney_change_pct': None
        }

        if month != current_month:
            if previous_totals:
                for key in ['moneySpent', 'leftoverMoney']:
                    if previous_totals[key] != 0:
                        change = round(((monthly_totals[month][key] - previous_totals[key]) / previous_totals[key]) * 100, 2)
                        monthly_totals[month][f"{key}_change_pct"] = change
            previous_totals = monthly_totals[month]

    if current_month in monthly_totals:
        rent_housing = sum(t['transactionAmount']['amount'] for t in monthly_data[current_month]['transaction'] if t['dcInd'] == 'DEBIT' and any(keyword in t.get('description', '').lower() for keyword in ['rent', 'housing', 'home']))
        other_spending = monthly_totals[current_month]['moneySpent'] - rent_housing
        projected_other_spending = other_spending * projection_factor
        
        monthly_totals[current_month]['projected_moneySpent'] = rent_housing + projected_other_spending
        monthly_totals[current_month]['projected_leftoverMoney'] = monthly_totals[current_month]['moneyMade'] - monthly_totals[current_month]['projected_moneySpent']
        for key in ['moneySpent', 'leftoverMoney']:
            if previous_totals[key] != 0:
                change = round(((monthly_totals[current_month][f'projected_{key}'] - previous_totals[key]) / previous_totals[key]) * 100, 2)
                monthly_totals[current_month][f"proj_{key}_change_pct"] = change

    # Dump monthly_totals to a JSON file
    with open('total_monthly_spending.json', 'w') as file:
        json.dump(monthly_totals, file, indent=4)

    # Print table
    header = "Month            | MoneyMade | %Change  | MoneySpent | %Change  | Leftover | % Change  "
    print(header)
    print('-' * len(header))

    for month, totals in sorted(monthly_totals.items(), key=lambda x: int(x[0].split()[1])):
        if month == current_month:
            print_row(month, "(Proj)", totals['moneyMade'], totals['moneyMade_change_pct'], totals['projected_moneySpent'], totals['proj_moneySpent_change_pct'], totals['projected_leftoverMoney'], totals['proj_leftoverMoney_change_pct'])
            print_row(month, "(Curr)", totals['moneyMade'], totals['moneyMade_change_pct'], totals['moneySpent'], totals['moneySpent_change_pct'], totals['leftoverMoney'], totals['leftoverMoney_change_pct'])
        else:
            print_row(month, "", totals['moneyMade'], totals['moneyMade_change_pct'], totals['moneySpent'], totals['moneySpent_change_pct'], totals['leftoverMoney'], totals['leftoverMoney_change_pct'])

    print('-' * len(header))


def getSpendingByCategory(JSON_FOLDER='dummy_data/monthly_statements'):
    """
    Get total monthly spending broken down by category.

    Parameters:
    - JSON_FOLDER: The folder containing the monthly statement JSON files.

    Returns:
    - Prints a table of the monthly spending for each category with % change.
    """

    # Categories
    CATEGORIES = ["transport", "groceries", "restaurants", "shopping", "home"]

    # Function to read JSON file content
    def read_json_file(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Read all JSON files
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
    monthly_data = {f.split('.')[0]: read_json_file(os.path.join(JSON_FOLDER, f)) for f in files}

    # Determine the running month and today's date
    today = datetime.today()
    current_month = f"Month {today.month}"
    days_passed = today.day
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    projection_factor = days_in_month / days_passed if days_passed != 0 else 1

    # Compute spending by category for each month
    monthly_category_totals = {}
    monthly_totals = {}
    previous_category_totals = None

    for month, data in sorted(monthly_data.items(), key=lambda x: int(x[0].split()[1])):
        category_totals = {category: 0 for category in CATEGORIES}

        for transaction in data['transaction']:
            if transaction['dcInd'] == 'DEBIT':
                for category in CATEGORIES:
                    if f"***{category.upper()}***" in transaction['description']:
                        category_totals[category] += transaction['transactionAmount']['amount']
                        break

        # Calculate % changes for actual data
        if previous_category_totals:
            for category in CATEGORIES:
                if month == current_month:
                    category_totals[f"{category}_change"] = None
                else:
                    diff = category_totals[category] - previous_category_totals[category]
                    percent_change = (diff / previous_category_totals[category]) * 100 if previous_category_totals[category] != 0 else 0
                    category_totals[f"{category}_change"] = percent_change
        else:
            for category in CATEGORIES:
                category_totals[f"{category}_change"] = None

        monthly_total = sum([category_totals[category] for category in CATEGORIES])
        for category in CATEGORIES:
            category_totals[f"{category}_percent_of_total"] = (category_totals[category] / monthly_total) * 100 if monthly_total else 0

        if month == current_month:
            # If it's the running month, project the total for categories other than "home"
            for category in CATEGORIES:
                if category != "home":
                    category_totals[f"projected_{category}"] = category_totals[category] * projection_factor

            projected_total = sum([category_totals[f"projected_{category}"] for category in CATEGORIES if category != "home"]) + category_totals["home"]

            # Compute percent of total for projected values
            for category in CATEGORIES:
                if category != "home":
                    category_totals[f"projected_{category}_percent_of_total"] = (category_totals[f"projected_{category}"] / projected_total) * 100 if projected_total else 0
                else:
                    category_totals[f"{category}_percent_of_total"] = (category_totals[category] / projected_total) * 100 if projected_total else 0

            # Calculate % changes for projected data based on last month's finalized data
            for category in CATEGORIES:
                if category != "home":
                    diff = category_totals[f"projected_{category}"] - previous_category_totals[category]
                    percent_change = (diff / previous_category_totals[category]) * 100 if previous_category_totals[category] != 0 else 0
                    category_totals[f"projected_{category}_change"] = percent_change
                else:
                    category_totals[f"{category}_change"] = None

        monthly_category_totals[month] = category_totals
        monthly_totals[month] = monthly_total
        previous_category_totals = {category: category_totals[category] for category in CATEGORIES}

    # Dump monthly_totals to a JSON file
    with open('category_spending.json', 'w') as file:
        json.dump(monthly_category_totals, file, indent=4)

    # Display table
    header_parts = [f"{cat.capitalize():^12} | % Change | % Total " for cat in CATEGORIES]
    header = "Month           | " + " | ".join(header_parts)
    print(header)
    print('-' * len(header))

    for month, category_totals in sorted(monthly_category_totals.items(), key=lambda x: int(x[0].split()[1])):
        monthly_total = monthly_totals[month]

        if month != current_month:
            row = [f"{month:11}    "]
            for category in CATEGORIES:
                value = category_totals[category]
                percent_change = f"{category_totals[f'{category}_change'] if category_totals[f'{category}_change'] is not None else '--':8}"
                percent_of_total = f"{category_totals[f'{category}_percent_of_total']:7.2f}%"
                row.append(f"{value:12.2f} | {percent_change} | {percent_of_total}")
            print(" | ".join(row))
        else:
            # Projected
            projected_total = sum([category_totals[f"projected_{category}"] for category in CATEGORIES if category != "home"]) + category_totals["home"]

            row = [f"{current_month:6} (Proj)"]
            for category in CATEGORIES:
                if category != "home":
                    value = category_totals[f"projected_{category}"]
                    percent_change = f"{category_totals[f'projected_{category}_change']:8.2f}"
                    percent_of_total = f"{category_totals[f'projected_{category}_percent_of_total']:7.2f}%"
                else:
                    value = category_totals[category]
                    percent_change = "--      "
                    percent_of_total = f"{category_totals[f'{category}_percent_of_total']:7.2f}%"
                row.append(f"{value:12.2f} | {percent_change} | {percent_of_total}")
            print(" | ".join(row))

            # Current
            row = [f"{current_month:11}    "]
            for category in CATEGORIES:
                value = category_totals[category]
                percent_change = "--      "
                percent_of_total = f"{category_totals[f'{category}_percent_of_total']:7.2f}%"
                row.append(f"{value:12.2f} | {percent_change} | {percent_of_total}")
            print(" | ".join(row))

    print('-' * len(header))


import os
import json
from collections import defaultdict

def generate_category_table(JSON_FOLDER='dummy_data/monthly_statements', OUTPUT_JSON='category_tables.json'):
    """
    For each category, generates a table where:
    - Each row is a month
    - Each column is an establishment (deduced from the transaction description)
    - The value is the total amount spent at that establishment in that month

    Parameters:
    - JSON_FOLDER: The folder containing the monthly statement JSON files.
    - OUTPUT_JSON: The name of the output JSON file to save the tables.

    Returns:
    - A dictionary of tables for each category.
    """

    # Categories
    CATEGORIES = ["transport", "groceries", "restaurants", "shopping", "home"]

    # Function to read JSON file content
    def read_json_file(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Read all JSON files
    files = [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
    monthly_data = {f.split('.')[0]: read_json_file(os.path.join(JSON_FOLDER, f)) for f in files}

    # Dictionary to store tables for each category
    category_tables = {category: defaultdict(lambda: defaultdict(float)) for category in CATEGORIES}

    for month, data in sorted(monthly_data.items(), key=lambda x: int(x[0].split()[1])):
        for transaction in data['transaction']:
            if transaction['dcInd'] == 'DEBIT':
                for category in CATEGORIES:
                    if f"***{category.upper()}***" in transaction['description']:
                        # Extracting establishment name from the transaction description
                        establishment = transaction['description'].replace(f"***{category.upper()}***", '').strip()
                        amount = transaction['transactionAmount']['amount']
                        category_tables[category][month][establishment] += amount
                        break

    # Convert defaultdict to dict for JSON serialization
    output_tables = {category: dict(month_data) for category, month_data in category_tables.items()}

    # Calculate and insert totals into output_tables
    for category, table in output_tables.items():
        for month, establishments in table.items():
            monthly_total = sum(establishments.values())
            table[month]['Total'] = round(monthly_total, 2)

    # Save to JSON
    with open(OUTPUT_JSON, 'w') as file:
        json.dump(output_tables, file, indent=4)

    # Display tables
    for category, table in category_tables.items():
        print(f"\nTable for {category.capitalize()}:")
        header = ['Month'] + sorted(table[next(iter(table))].keys()) + ['Total']
        print(" | ".join(header))
        print('-' * (sum([len(h) for h in header]) + len(header) - 1))
        
        for month, establishments in sorted(table.items(), key=lambda x: int(x[0].split()[1])):
            monthly_total = sum(establishments.values())
            row = [month] + [f"{establishments[est]:.2f}" for est in header[1:-1]] + [f"{monthly_total:.2f}"]
            print(" | ".join(row))

    return output_tables


print("SPENDING BY CATEGORY")
getSpendingByCategory()

print("\n" * 3)
print("TOTAL MONTHLY SPENDING")
getTotalMonthlySpending()

# Call the function
tables = generate_category_table()
