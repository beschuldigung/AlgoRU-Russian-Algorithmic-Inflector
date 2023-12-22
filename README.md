# Russian-Algorithmic-Inflector
This is an ongoing project for what will eventually become a python library for performing algorithmic morphological changes in Russian nouns and verbs

# Morph Class

All of the morphological manipulation methods are built into the morph class. This will essentially encompass the entire library when finished. Currently the inflector method (for noun inflection) of the morph class works for the vast majority of non-irregular nouns and has the most common exceptions built in. For a large number of nouns this is already useable. The pronoun_inflector method, as it is quite simple, works perfectly. The past tense conjugator works for all non-irregular verb forms. 

# Incorporation of Spacy for POS tagging

the way I have it set up for development purposes is that I use a creative commons licensed SpacY NLP model trained on russian news texts for pos tagging created by Alexander Kukushkin (https://spacy.io/models/ru). The one I have been working with is ru_core_news_sm, which is trained on the smallest dataset (there are three that are distinguishable incrementally by size). I chose this one for performance optimization, as performing POS tagging on a single token is in my experience always accurate with this model. The pos tagging allows me to input any word class and have the script automatically loop it through the appropriate methods in the morph class. This makes development much quicker, because I can test outputs instantly. 

# how it generally works

You input a word, spacy identifies the POS, and the appropriate action is selected. For loops will cycle through a lists of gender, case, tense, etc and call the correspnding method in the morph class to output either a declination table or a conjugation table. This allows for quick development because you can spot errors in the script in multiple genders/cases/tenses at the same time and debug them together. However, in the long term, it is more my goal to build a script that does one-off morphological changes, rather than outputting declination/conjugation tables. 

# what still needs to be done

I am currently working on a parser for Zalizniaks grammar dictionary, as well as his renowned inflection annotation system. This will allow me to account for almost all inflection types and the vast majority of irregular forms as well, so this library can be used for professional NLP tasks. 
