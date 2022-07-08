import csv
import os
import spacy
from pathlib import Path
nlp = spacy.load("en_blackstone_proto")

#We ask the user the path to the file he wants to use.
file_path = Path(input("Enter the file path: ").strip())
file_name = input("Enter the file name with extension (.txt): ".strip())
file_full_path = file_path / file_name
case = open(file_full_path, 'r')

#This function process the given text to remove line break, tabulation, and non-breaking space.
def process_text(textToProcess):
    processed_text = []
    for line in textToProcess:
        
        unprocessed_line = line

        processed_line = unprocessed_line.replace("\n", "")
        processed_line = processed_line.replace("\t", " ")
        processed_line = processed_line.replace("\xa0", " ")

        processed_text.append(processed_line)
    return processed_text

processed_text = process_text(case)

# Apply the model to the text.
# Replace ent.label_ value to "COURTS" or "INSTRUMENTS" to only get courts and instruments results
def get_result_per_line(text) :
    i = 0
    result_list = []
    for line in processed_text:
        i = i + 1
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == 'CITATION' :
                result_list.append((i, ent.text))
    return result_list

results_list = get_result_per_line(processed_text)

#We write the result in a csv file using another path given by the user
# This file will be used with a result file from lexnlp to fuse them and compare the performance.
# When writing results for "Courts" or "Instruments", change the second value in fields, and the string with the same name in writerow.
csv_file_path = Path(input("Enter the file path: ").strip())
csv_file_name = input("Enter the file name with extension (.csv): ".strip())
csv_file_full_path = csv_file_path / csv_file_name
with open(csv_file_full_path, "w", newline="") as file_writer:
    fields = ["Line", "Citation"]

    writer=csv.DictWriter(file_writer, fieldnames=fields)

    writer.writeheader()

    for result in results_list:
        writer.writerow({"Line": result[0], "Citation": result[1]})