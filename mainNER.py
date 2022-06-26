import spacy
import csv

# Load the model
nlp = spacy.load("en_blackstone_proto")

case1 = open("/home/tristan/Stage/TextesJuridiques/AMGCapitalManagementvFTCBreyer.txt", 'r')
print(type(case1))

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

# Apply the model to the text
result_list = []
for line in processed_text:
    doc = nlp(line)
    for ent in doc.ents:
        res = (ent.text, ent.label_, line)
        result_list.append(res)

# Iterate through the entities identified by the model
for ent in doc.ents:
    print(ent.text, ent.label_)

with open("/home/tristan/Stage/EtudeLogiciels/EtudeLexNLP/BlackstoneNER_AMGvFTCBreyer_Results.csv", "w", newline="") as file_writer:
    fields = ["Text", "Label", "Source"]

    writer=csv.DictWriter(file_writer, fieldnames=fields)

    writer.writeheader()

    for result in result_list:
        writer.writerow({"Text":result[0], "Label":result[1], "Source":result[2]})

case1.close()