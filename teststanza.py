#!/usr/bin/python3

import stanza

class Statement:
    def __init__(self):
        self.subject = ""
        self.verb = ""
        self.object = ""
        self.noun = ""

    def print(self):
#        print(self.subject+" "+self.verb+" "+self.object+" "+self.noun)
        out = ""
        if self.verb != "" and (self.subject != "" or self.object != ""):
            if self.subject == "":
                if self.noun != "":
                    out = self.verb+"("+self.object+","+self.noun+")."
                else:
                    out = self.verb+"("+self.object+")."
            elif self.object == "":
                if self.noun != "":
                    out = self.verb+"("+self.subject+","+self.noun+")."
                else:
                    out = self.verb+"("+self.subject+")."
            else: 
                out = self.verb+"("+self.subject+","+self.object+self.noun+")."
            out = out.replace(" ","").replace("’","")
            print(out)

text = 'Well, I wouldn’t really call it a “date” – at least not if I don’t want to end up as a coat for Miss Piggy. Y\'see, I just gave Lady Gaga a ride to the VMAs, and when Lady Gaga left her credentials in the limo, I had to bring them to her. (On the off-chance security didn t recognize her. Hey, it could happen.) Of course, after Lady Gaga and I were seen on the red carpet together, well Miss Piggy got a little jealous. But I definitely did get a ride home – in the trunk!'


nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,ner')
doc = nlp(text)
res = []

for s in doc.sentences:
    st = Statement()
    sts = []

    for w in s.words:
        #print(w)
        if w.feats is not None:
            if "Case=Nom" in w.feats:
                if w.upos == "PRON" or w.upos == "NOUN":
                    st.subject = st.subject + w.text + " "

            if "Case=Acc" in w.feats:
                if w.upos == "PRON" or w.upos == "NOUN":
                    st.object = st.object + w.text + " "

        if w.upos == "AUX" or w.upos == "VERB" or w.upos == "PART":
            st.verb = st.verb + w.text + " "

        if w.upos == "NOUN":
            st.noun = st.noun + w.text + " "

        if w.upos == "PUNCT":
            res.append(st) 
            st = Statement()      

for st in res:
    st.print()

#print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')
#print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')
