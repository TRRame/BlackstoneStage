#DISCLAIMER: THIS FILE MAINLY USE THE WORK OF TRISTAN KOH, AVAILABLE HERE : https://github.com/TristanKoh/blackstone-legal-cat/blob/master/code/blackstone_text_cat.ipynb
from pathlib import Path
import pandas as pd

# DatafilePath is a string that contains the relative file path to the data file
home = Path.home()
dataFilePath = Path(home, "Stage/TextesJuridiques", "AmericansForProsperityFoundationvBontaSyllabus.txt")

# Import the case as text
case = open(dataFilePath, "r", encoding= "utf8")

# .readlines() returns a stream (ie. the text is not saved in memory), hence we save it as a string called "text" which is saved in memory
text = case.readlines()

# This code loads the blackstone NLP model, and saves it into the object called NLP
import blackstone
import en_blackstone_proto
nlp = en_blackstone_proto.load()



# Text preprocessing
def text_preprocessing(text):
    """ Accepts a list of unprocessed strings, returns a list of strings without string and tab breaks and empty strings """
    
    # This creates an empty list
    processed_text = []

    # This is a for loop; it iterates through the strings in the text, and performs some operations on each string. Hence the name for loop: "For" each string, apply X operations on the string.

    # In this case, for each string, we replace new lines ("\n") with an empty string, and replace tabs ("\t") with a space.
    for string in text:
        string = string.replace("\n", "")
        string = string.replace("\t", " ")
        processed_text.append(string)
    
    # This is a list comprehension; a more concise way of expressing a for loop.
    # We iterate through each string in the processed text, and we only retain strings which are not empty strings (since empty strings are meaningless in this context)

    processed_text = [string for string in processed_text if string != ""]

    return processed_text


# Run the function on the string
text = text_preprocessing(text)


def legal_cats(sentences):
    """
    Function to identify the highest scoring category prediction generated by the text categoriser. 

    Arguments: 
    a list of strings
    
    converts to spacy generator object, splits into sentences using spacy's sentence detector

    returns a tuple of: 
    a list of the split sentences,
    a list of the max cat and max score for each doc in tuples
    """
    doc_sentences = []

    # This passes the input string through the nlp model, and converts it to doc object
    # This doc object contains both the original text, and tags the sentences with certain attributes, such as the sentence boundary detector.
    # A doc corresponds to a string.

    docs = nlp.pipe(sentences, disable = ["tagger", "ner", "textcat"])

    # We loop through each document in the documents, and loop again through each sentence in the document, and append the sentence to doc_sentences, an empty list
    for doc in docs:
        for sentence in doc.sents:
            doc_sentences.append(sentence.text)
    
    # We can now categorise each sentence into one of the five abovementioned categories.

    # We convert the newly detected sentences into a doc object again, as it contains the categoriser attribute that we can use to predict
    
    docs = nlp.pipe(doc_sentences, disable = ["tagger", "parser", "ner"])

    # We create a list to store the corresponding category and the score (ie the likelihood of the category that blackstone predicts the sentence to be)
    # This index of the list corresponds to doc_sentences (ie. the first item in cats_list contains the predicted category and score for the first sentence in doc_sentences, the second item in cats_list contains the predicted category and score for the second sentence, so on and so forth)

    cats_list = []

    # We loop through the doc (sentence) in the documents, and return the highest probability category and its score for each sentence

    # We have to select the highest scoring category because blackstone provides the probability of all five categories which the sentence can fall under.

    # We are only concerned with blackstone's best prediction, and hence we only save the highest scoring category.
    for doc in docs:
        cats = doc.cats
        max_score = max(cats.values()) 
        max_cats = [k for k, v in cats.items() if v == max_score]
        max_cat = max_cats[0]
        cats_list.append((max_cat, max_score))

    return doc_sentences, cats_list

cats = legal_cats(text)



# This creates a new dataframe with the three columns
df_results = pd.DataFrame({"sentence" : cats[0], "category": [cat[0] for cat in cats[1]], "score": [cat[1] for cat in cats[1]]})

# The first 5 rows of the new dataframe.



print(df_results["category"].value_counts())


print("\n")
print("CONCLUSION")
print("_" * 60)


for sentence in df_results.loc[df_results["category"] == "CONCLUSION", "sentence"][:40]:
    print(sentence)
    print("-" * 40)


print("\n")
print("LEGAL_TEST")
print("_" * 60)


for sentence in df_results.loc[df_results["category"] == "LEGAL_TEST", "sentence"][:40]:
    print(sentence)
    print("-" * 40)


print("\n")
print("AXIOM")
print("_" * 60)


for sentence in df_results.loc[df_results["category"] == "AXIOM", "sentence"][:40]:
    print(sentence)
    print("-" * 40)


print("\n")
print("ISSUE")
print("_" * 60)


for sentence in df_results.loc[df_results["category"] == "ISSUE", "sentence"][:40]:
    print(sentence)
    print("-" * 40)


