'''
Problem Statement: A CSV file contains transaction_id, account_id, type, amount and timestamp. Create a program that reads the file,
validates every row, writes valid credit and debit transactions into separate CSV files, writes rejected rows into error.csv with reason,
and finally prints account-wise balance changes. The program must continue processing after invalid rows using exception handling.
'''

import csv

file_path = input()

balances = {}

with open(file_path, "r", newline="") as file:
    reader = csv.DictReader(file)

    with open("credit.csv", "w", newline="") as credit_file:
        with open("debit.csv", "w", newline="") as debit_file:
            with open("error.csv", "w", newline="") as error_file:

                credit_writer = csv.writer(credit_file)
                debit_writer = csv.writer(debit_file)
                error_writer = csv.writer(error_file)

                credit_writer.writerow(reader.fieldnames)
                debit_writer.writerow(reader.fieldnames)
                error_writer.writerow(reader.fieldnames + ["reason"])

                for row in reader:

                    try:
                        transaction_id = row["tid"]
                        account_id = row["acc"]
                        transaction_type = row["type"]
                        amount = float(row["amount"])
                        timestamp = row["time"]

                        if transaction_type not in ["CREDIT", "DEBIT"]:
                            raise Exception("Invalid transaction type")

                        if amount <= 0:
                            raise Exception("Invalid amount")

                        if len(timestamp) != 19 or timestamp[4] != "-" or timestamp[7] != "-" or timestamp[10] != "T":
                            raise Exception("Invalid timestamp")

                        if account_id not in balances:
                            balances[account_id] = 0

                        if transaction_type == "CREDIT":
                            balances[account_id] += amount
                            credit_writer.writerow(row.values())

                        else:
                            balances[account_id] -= amount
                            debit_writer.writerow(row.values())

                    except Exception as e:
                        error_writer.writerow(list(row.values()) + [str(e)])

print("")

result = []

for account in balances:
    result.append((account, balances[account]))

result.sort(key=lambda x: (-abs(x[1]), x[0]))

for account, balance in result:
    if balance.is_integer():
        balance = int(balance)

    print(account, balance)
