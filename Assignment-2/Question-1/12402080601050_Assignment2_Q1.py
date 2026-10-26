import re

def extract_emails(file_path):
    # Store unique emails for each domain
    email_data = {}

    # Pattern to find valid email addresses
    pattern = r'[A-Za-z0-9._+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.(?:com|edu|org)'

    try:
        # Read the file line by line
        with open(file_path, "r", encoding="utf-8",
                  errors="ignore") as file:

            for line in file:
                # Find email addresses in the current line
                emails = re.findall(pattern, line)

                for email in emails:
                    email = email.lower()

                    # Check for exactly one @ symbol
                    if email.count("@") != 1:
                        continue

                    # Get the domain name
                    domain = email.split("@")[1]

                    # Create a set for a new domain
                    if domain not in email_data:
                        email_data[domain] = set()

                    # Add email (duplicates are ignored)
                    email_data[domain].add(email)

        # Print results in alphabetical order
        for domain in sorted(email_data):
            count = len(email_data[domain])
            smallest = min(email_data[domain])

            print(domain, count, smallest)

    except FileNotFoundError:
        print("Error: File not found.")

    except PermissionError:
        print("Error: Permission denied.")

    except OSError:
        print("Error: Unable to read the file.")

# Main program
file_path = input("Enter the text file path: ").strip()

if file_path == "":
    print("Error: File path cannot be empty.")
else:
    extract_emails(file_path)
