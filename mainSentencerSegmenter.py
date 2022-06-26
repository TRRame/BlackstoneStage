import spacy
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules import CITATION_PATTERNS

nlp = spacy.load("en_blackstone_proto")

# add the Blackstone sentence_segmenter to the pipeline before the parser
sentence_segmenter = SentenceSegmenter(nlp.vocab, CITATION_PATTERNS)
nlp.add_pipe(sentence_segmenter, before="parser")

case1 = open("/home/tristan/Stage/TextesJuridiques/BordenvUnitedStatesKagan.txt", 'r')
text = case1.read()

text = text.replace("\n"," " )
text = text.replace("\t"," " )
text = text.replace("\xa0","" )

doc = nlp(text)

for sent in doc.sents:
    print (sent.text)