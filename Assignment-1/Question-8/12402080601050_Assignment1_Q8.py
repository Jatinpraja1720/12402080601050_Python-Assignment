'''
Problem Statement: A server produces several text log files. Create a program that scans all files in a folder, builds an inverted index
mapping each normalized token to the list of file names and line numbers where it appears, stores the index using pickle, and
compresses both original logs and index into a zip file. The program must also support a search mode that loads the pickle index and
answers token queries.
'''

import os
import pickle
import zipfile
import re

parts = input().split()

mode = parts[0]

if mode == "BUILD":

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

        with open(file_path, "r", encoding="utf-8") as file:

            line_number = 0

            for line in file:

                line_number += 1
                total_lines += 1

                words = re.findall(r"\b\w+\b", line.lower())

                for word in words:

                    if word not in index:
                        index[word] = []

                    index[word].append((file_name, line_number))

    pickle_file = folder + "_index.pkl"

    with open(pickle_file, "wb") as file:
        pickle.dump(index, file)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as archive:

        for file_name in os.listdir(folder):

            file_path = os.path.join(folder, file_name)

            if os.path.isfile(file_path):
                archive.write(file_path, file_name)

        archive.write(pickle_file, os.path.basename(pickle_file))

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))

else:

    pickle_file = parts[1]
    q = int(input())

    with open(pickle_file, "rb") as file:
        index = pickle.load(file)

    for i in range(q):

        token = input().lower()

        if token in index:

            result = []

            for file_name, line_number in index[token]:
                result.append(f"{file_name}:{line_number}")

            print(" ".join(result))

        else:
            print()
