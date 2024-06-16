# Russian-Algorithmic-Inflector
This is an ongoing project for what will eventually become a python library for performing algorithmic morphological changes on Russian nouns and verbs

# morph() Class

All of the morphological manipulation methods are built into the morph() class. This will essentially encompass the entire library when finished. Currently the inflector() method (for noun inflection) of the morph class works for the vast majority of non-irregular nouns and has the most common exceptions built in. For a large number of nouns this is already useable. The pronoun_inflector() method, as it is quite simple, works perfectly. The past_tense_conjugator() works for all of the most basic non-irregular verb forms. The morph() class also has the get_aspectpair() method which looks through a database of verbal aspect pairs that I created myself and am consistently updating and outputs a list, in which [0] is the imperfective form and [1] (and depending on the verb also [2]) is/are the perfective form(s). This all allows the script to put all forms through the past_tense_conjugator() method and, in the future, the present and future tense conjugators as well for complete conjugation capabilities. 

# Incorporation of SpacY for POS tagging and classifying animacy

The way I have it set up for development purposes is that I use an MIT licensed SpacY NLP model trained on russian news texts for POS tagging and classifying animacy created by Alexander Kukushkin (https://spacy.io/models/ru). The one I have been working with is ru_core_news_sm, which is trained on the smallest dataset (there are three that are distinguishable incrementally by size). I chose this one for performance optimization, as performing POS tagging on a single token is in my experience always accurate with this model. The pos tagging allows me to input any word class and have the script automatically loop it through the appropriate methods in the morph class. This makes development much quicker, because I can test outputs instantly. 

# how it generally works

You input a word, spacy identifies the POS, and the appropriate action is selected. For loops will cycle through a lists of gender, case, tense, etc and call the correspnding method in the morph() class to output either a declination table or a conjugation table. The get_aspectpair() method in the morph class searches for the inputed verb in my database and returns the full aspectual pair so that conjugations for all forms of the verb can be run through the past_tense_conjugator() method. This allows for quick development because you can spot errors in the script in multiple genders/cases/tenses at the same time and debug them together. However, in the long term, it is more my goal to build a script that does one-off morphological changes, rather than outputting declination/conjugation tables. 

# what still needs to be done

I am currently working on a parser for Zalizniaks grammar dictionary, as well as his renowned inflection annotation system, which doesn't exist yet, so it would actually be quite a hefty contribution to the world of NLP for the Russian language. This will allow me to account for all inflection types and irregular forms as well (as well as their stress markings and how these change), so this library can be used for professional NLP tasks. I also have yet to tackle verb conjugation other than regular past tense forms. I'm still actively scraping russian texts for perfective form verbs to add to the database, but once I achieve a reasonable size, this database also needs to be cleaned, because the Spacy model sometimes mistakenly returns ukrainian verbs or ones from other slavic languages when using the lemma method in larger texts in their embedded context (I assume its due to the datasets used to train the model), or mistakenly tags a verb as one aspect form when it is in fact the other (an issue I, as previously described, don't have when POS tagging single verbs out of context) and there are a small number of double inputs. Adding inflection algorithms for adjectives and participles would be the last to follow. The aspect pairs are extracted from wiktionary using their API. Russian morphology is a very complex system with a very very high number of irregularities, so you can imagine this project will take quite a while to complete with a ton of different moving parts. Having a lot of fun with it though and would love any feedback you may have :)

# examplary outputs/visuals

noun inflection for the inputs девушка and учитель

<img width="329" alt="Screenshot 2023-12-25 at 21 56 00" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/9a4c62b0-2d3e-44ed-83fa-9ee02a254187">
<img width="328" alt="Screenshot 2023-12-25 at 22 00 42" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/ff1cd5b2-1c48-4c53-961a-ce67c631639a">


past tense verb conjugation for the verb возвращаться (the stress markings are inaccurate because I haven't built these changes into the script yet, so it retains the stress marking from the infinitive forms scraped from wiktionary, whereas the imperfective forms don't have them at all)

<img width="358" alt="Screenshot 2023-12-25 at 21 56 41" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/49bce984-f2c0-41f9-bfa2-9422a80acea7">


how the (in progress) aspect pair SQLite database is structured. Currently the database has 19,192 entries in total, and I have successfully extracted aspect pairs for 6,436 of these. 

<img width="475" alt="Screenshot 2023-12-25 at 22 00 06" src="https://github.com/ciaranmays/Russian-Algorithmic-Inflector/assets/154232302/be6b5534-8364-4cd4-944f-c760376d40d9">


(the data pulled from wiktionary, unlike my source code itself, which is licensed under an MIT license, is licensed under a CC BY-SA 4.0 DEED license. For information about the authors who contributed to the pages that the aspect pairs were extracted from, please visit the wiktionary page for the respective *imperfective* verb form on english wiktionary. For more information about the terms and restrictions of the two licenses, please read the LICENSE.md and DATA_LICENSE.md files)
