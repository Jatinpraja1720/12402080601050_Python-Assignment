import csv
from datetime import datetime

file_name = input().strip()

balances = {}

with open(file_name, "r", newline="") as file:
    reader = csv.DictReader(file)

    credit_file = open("credit.csv", "w", newline="")
    debit_file = open("debit.csv", "w", newline="")
    error_file = open("error.csv", "w", newline="")

    credit_writer = csv.writer(credit_file)
    debit_writer = csv.writer(debit_file)
    error_writer = csv.writer(error_file)

    header = ["tid", "acc", "type", "amount", "time"]

    credit_writer.writerow(header)
    debit_writer.writerow(header)
    error_writer.writerow(header + ["reason"])

    for row in reader:
        try:
            tid = row["tid"]
            acc = row["acc"]
            trans_type = row["type"].upper()
            amount = float(row["amount"])
            time = row["time"]

            if amount <= 0:
                raise ValueError("Invalid amount")

            if trans_type not in ["CREDIT", "DEBIT"]:
                raise ValueError("Invalid type")

            datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

            if acc not in balances:
                balances[acc] = 0

            if trans_type == "CREDIT":
                balances[acc] += amount
                credit_writer.writerow(row.values())
            else:
                balances[acc] -= amount
                debit_writer.writerow(row.values())

        except Exception as e:
            error_writer.writerow(list(row.values()) + [str(e)])

    credit_file.close()
    debit_file.close()
    error_file.close()


result = sorted(
    balances.items(),
    key=lambda x: abs(x[1]),
    reverse=True
)

for acc, amount in result:
    if amount == int(amount):
        amount = int(amount)

    print(acc, amount)

print("Files created: credit.csv, debit.csv, error.csv")
