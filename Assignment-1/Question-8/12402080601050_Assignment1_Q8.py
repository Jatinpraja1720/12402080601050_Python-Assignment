import os
import re
import pickle
import zipfile


parts = input().split()

if parts[0] == "BUILD":
    folder = parts[1]
    zip_name = parts[2]

    index = {}
    total_files = 0
    total_lines = 0

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        if not os.path.isfile(file_path):
            continue

        total_files += 1

        with open(file_path, "r", errors="ignore") as file:
            for line_no, line in enumerate(file, 1):
                total_lines += 1

                words = re.findall(r"\b\w+\b", line.lower())

                for word in words:
                    if word not in index:
                        index[word] = []

                    index[word].append((file_name, line_no))

    pickle_file = "log_index.pkl"

    with open(pickle_file, "wb") as file:
        pickle.dump(index, file)

    with zipfile.ZipFile(zip_name, "w") as archive:
        archive.write(pickle_file)

        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)

            if os.path.isfile(file_path):
                archive.write(file_path, arcname=file_name)

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


elif parts[0] == "SEARCH":
    pickle_file = parts[1]
    q = int(parts[2])

    with open(pickle_file, "rb") as file:
        index = pickle.load(file)

    for _ in range(q):
        word = input().strip().lower()

        if word in index:
            for file_name, line_no in index[word]:
                print(file_name + ":" + str(line_no))
