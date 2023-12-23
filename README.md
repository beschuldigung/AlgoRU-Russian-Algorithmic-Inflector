# Russian-Algorithmic-Inflector
This is an ongoing project for what will eventually become a python library for performing algorithmic morphological changes in Russian nouns and verbs

# morph() Class

All of the morphological manipulation methods are built into the morph() class. This will essentially encompass the entire library when finished. Currently the inflector() method (for noun inflection) of the morph class works for the vast majority of non-irregular nouns and has the most common exceptions built in. For a large number of nouns this is already useable. The pronoun_inflector() method, as it is quite simple, works perfectly. The past_tense_conjugator() works for all of the most basic non-irregular verb forms. The morph() class also has the get_aspectpair() method which looks through a database of verbal aspect pairs that I created myself and am consistently updating and outputs a list, in which [0] is the imperfective form and [1] (and depending on the verb also [2]) is/are the perfective form(s). This allows the script to put all forms through the past_tense_conjugator() method and, in the future, the present and future tense conjugators as well for complete conjugation capabilities. 

# Incorporation of SpacY for POS tagging and classifying animacy

The way I have it set up for development purposes is that I use an MIT licensed SpacY NLP model trained on russian news texts for POS tagging and classifying animacy created by Alexander Kukushkin (https://spacy.io/models/ru). The one I have been working with is ru_core_news_sm, which is trained on the smallest dataset (there are three that are distinguishable incrementally by size). I chose this one for performance optimization, as performing POS tagging on a single token is in my experience always accurate with this model. The pos tagging allows me to input any word class and have the script automatically loop it through the appropriate methods in the morph class. This makes development much quicker, because I can test outputs instantly. 

# how it generally works

You input a word, spacy identifies the POS, and the appropriate action is selected. For loops will cycle through a lists of gender, case, tense, etc and call the correspnding method in the morph() class to output either a declination table or a conjugation table. The get_aspectpair() method in the morph class searches for the inputed verb in my database and returns the full aspectual pair so that conjugations for all forms of the verb can be run through the past_tense_conjugator() method. This allows for quick development because you can spot errors in the script in multiple genders/cases/tenses at the same time and debug them together. However, in the long term, it is more my goal to build a script that does one-off morphological changes, rather than outputting declination/conjugation tables. 

# what still needs to be done

I am currently working on a parser for Zalizniaks grammar dictionary, as well as his renowned inflection annotation system, which doesn't exist yet, so it would actually be quite a hefty contribution to the world of NLP for the Russian language. This will allow me to account for almost all inflection types and the vast majority of irregular forms as well, so this library can be used for professional NLP tasks. I also have yet to tackle verb conjugation other than regular past tense forms. I'm still actively scraping russian texts for verbs to add to the database, but once I achieve a reasonable size, this database also needs to be cleaned, because the Spacy model sometimes mistakenly returns ukrainian verbs or ones from other slavic languages when using the lemma method in larger texts in their embedded context (I assume its due to the datasets used to train the model), or mistakenly tags a verb as one aspect form when it is in fact the other (an issue I, as previously described, don't have when POS tagging single verbs out of context) and there are a small number of double inputs. Adding inflection algorithms for adjectives and participles would be the last to follow. Russian morphology is a very complex system with a very very high number of irregularities, so you can imagine this project will take quite a while to complete with a ton of different moving parts. Having a lot of fun with it though and would love any feedback you may have :)

# examplary outputs/visuals

noun inflection

<img width="329" alt="tas" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/47b0edc1-fc55-4974-8f42-71d04beba736">
<img width="329" alt="tas2" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/0f57fc8e-ca81-48d9-b0bb-d45956d4b187">


past tense verb conjugation

<img width="371" alt="Screenshot 2023-12-23 at 03 07 57" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/755efcb2-e67e-44ee-83bd-1f89a22a495f">


how the (in progress) aspect pair SQLite database is structured

<img width="408" alt="Screenshot 2023-12-23 at 03 37 08" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/e6059208-46db-4364-8e49-f29700eb5094">


