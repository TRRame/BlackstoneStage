import spacy
import csv
from pathlib import Path
# Load the model
nlp = spacy.load("en_blackstone_proto")

#We ask the user the path to the file he wants to use.
file_path = Path(input("Enter the file path: ").strip())
file_name = input("Enter the file name with extension (.txt): ".strip())
file_full_path = file_path / file_name
case1 = open(file_full_path, 'r')

#This function process the given text to remove line break, tabulation, and non-breaking space.
def process_text(textToProcess):
    processed_text = []
    for line in case1:
        
        unprocessed_line = line

        processed_line = unprocessed_line.replace("\n", " ")
        processed_line = processed_line.replace("\t", " ")
        processed_line = processed_line.replace("\xa0", " ")

        processed_text.append(processed_line)
    return processed_text

processed_text = process_text(case1)

# Apply the NER model to the text
result_list = []
for line in processed_text:
    doc = nlp(line)
    for ent in doc.ents:
        res = (ent.text, ent.label_, line)
        result_list.append(res)

# Iterate through the entities identified by the model
for ent in doc.ents:
    print(ent.text, ent.label_)

#We write the result in a csv file using another path given by the user
csv_file_path = Path(input("Enter the file path: ").strip())
csv_file_name = input("Enter the file name with extension (.csv): ".strip())
csv_file_full_path = csv_file_path / csv_file_name
with open(csv_file_full_path, "w", newline="") as file_writer:
    fields = ["Text", "Label", "Source"]

    writer=csv.DictWriter(file_writer, fieldnames=fields)

    writer.writeheader()

    for result in result_list:
        writer.writerow({"Text":result[0], "Label":result[1], "Source":result[2]})

case1.close()