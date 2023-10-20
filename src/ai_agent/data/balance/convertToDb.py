import sqlite3
import json

def create_database_and_table(connection):
    # Create the table
    with connection:
        connection.execute('''
        CREATE TABLE IF NOT EXISTS daily_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE UNIQUE NOT NULL,
            checkingAccountBalance DECIMAL(20, 2) NOT NULL,
            savingsAccountBalance DECIMAL(20, 2) NOT NULL
        );
        ''')

def insert_into_database(connection, current_data, savings_data):
    # Convert both datasets into dictionaries with date as the key
    current_dict = {entry['date']: format(float(entry['amount']), '.2f') for entry in current_data['data']}
    savings_dict = {entry['date']: format(float(entry['amount']), '.2f') for entry in savings_data['data']}
    
    # Merge both datasets based on the date and sort them
    all_dates = sorted(set(current_dict.keys()) | set(savings_dict.keys()))
    
    with connection:
        for date in all_dates:
            checking_balance = current_dict.get(date, '0.00')
            savings_balance = savings_dict.get(date, '0.00')

            connection.execute(
                "INSERT OR REPLACE INTO daily_balances (date, checkingAccountBalance, savingsAccountBalance) VALUES (?, ?, ?)", 
                (date, checking_balance, savings_balance)
            )

if __name__ == "__main__":
    # Load the JSON data
    with open('current_daily.json', 'r') as file:
        current_data = json.load(file)
    
    with open('savings_daily.json', 'r') as file:
        savings_data = json.load(file)

    # Connect to the SQLite database (will create the file if it doesn't exist)
    conn = sqlite3.connect('dailyBalanceDB.sqlite3')
    
    # Create the table
    create_database_and_table(conn)

    # Insert data into the table
    insert_into_database(conn, current_data, savings_data)

    # Close the connection
    conn.close()
