#Need to have py 3.13 or earlier installed in the venv for spaCy to work 


import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")
print([(w.text, w.pos_) for w in doc])
example_scrub = nlp("This is an example of sensitive information: John Doe's email is john.doe@example.com")
for w in example_scrub:
    if w.ent_type_ in ["PERSON", "EMAIL"]:
        print("[REDACTED]", end=" ") #Redacts apostrophes accidentally; fix later
    else:
        print(w.text, end=" ")