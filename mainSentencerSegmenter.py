import spacy
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules import CITATION_PATTERNS
from pathlib import Path

nlp = spacy.load("en_blackstone_proto")

# add the Blackstone sentence_segmenter to the pipeline before the parser
sentence_segmenter = SentenceSegmenter(nlp.vocab, CITATION_PATTERNS)
nlp.add_pipe(sentence_segmenter, before="parser")

#We ask the user the path to the file he wants to use.
file_path = Path(input("Enter the file path: ").strip())
file_name = input("Enter the file name with extension (.txt): ".strip())
file_full_path = file_path / file_name
case1 = open(file_full_path, 'r')
text = case1.read()

#We process the text and use the segmenter of the Blackstone model. The result is printed in the terminal.
text = text.replace("\n"," " )
text = text.replace("\t"," " )
text = text.replace("\xa0","" )

doc = nlp(text)

for sent in doc.sents:
    print (sent.text)