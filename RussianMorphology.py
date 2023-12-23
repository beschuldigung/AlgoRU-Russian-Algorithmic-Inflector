import spacy, sqlite3

nlp = spacy.load("ru_core_news_sm")

cases = ["И", "Р", "Д", "В", "Т", "П"]

wordtypes = { #this is for matching spacy POS tags with their russian counterparts
    "существительное": "NOUN",
    "прилагательное": "ADJ",
    "глагол": "VERB",
    "наречие": "ADV",
    "местоимение": "PRON",
    "предлог": "PREP",
    "союз": "CONJ",
    "числительное": "NUM",
    "частица": "PART",
}

numbers = ["ед", "мн"]
verbgenders = ["м", "ж", "с", "мн"]

class morph(str):

    def which_aspect(word):
        doc = nlp(word)
        for token in doc:
            morph = str(token.morph)
            morph = morph.split("|")
            aspect = morph[0]
            new = aspect.split("=")
            new = new[1]
        if new == "Imp":
            return "imp"
        else:
            return "perf"

    def get_aspectpair(word):

        firstletter = word[0]

        conn = sqlite3.connect('verbdb.sqlite')
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM '{firstletter}' WHERE impf = '{word}'")
        rows = cur.fetchall()

        if len(rows) == 0:
            cur.execute(f"SELECT * FROM '{firstletter}' WHERE perf = '{word}'")
            rows = cur.fetchall()
            rows = list(rows)
            row = rows[0]
            row = str(row)
            print(row)
            row = row.split()
            print(row)
            return row
        else:
            rows = list(rows)
            row = rows[0]
            row = list(row)
            return row

    def inflector(word, case, number):

        newword = ""

        #LISTS OF VARIABLES THAT GOVERN EXCEPTIONS TO MORPHOLOGICAL PATTERNS
        reg_vowel_endings = "аеояьъ"
        short_e_endings = "яей"
        silibants = ["Ш", "Ж", "Ч", "Щ", "г", "к"]

        # checks for consonant clusters at the end of the word
        def consonantcluster(word):
            check = word[:-1]
            finalsounds = check[-2:]
            if finalsounds[0] not in reg_vowel_endings and finalsounds[1] not in reg_vowel_endings:
                return True
            
        # checks to see if the word ends with a consonant
        def ends_with_consonant(word):
            if word.lower():  # check if the word is not empty
                last_char = word[-1].lower()  # get the last character and convert it to lowercase
                return last_char not in reg_vowel_endings and last_char.isalpha()
            return False

        # checks to see if the word ends with a dipthong vowel
        def ends_with_dipthong(word):
            if word.lower():  # check if the word is not empty
                last_char = word[-1].lower()  # get the last character and convert it to lowercase
                return last_char in short_e_endings
            return False

        # checks to see if a Zischlaut would affect the morphology of the ending
        def zischending(word):
            if ends_with_consonant(word) == True: #if ends with consonant
                if any(word.lower().endswith(zisch) for zisch in silibants):
                    return True #sends True if ends with Zischlaut directly
                else:    
                    return False #sends false if any other consonant
            if ends_with_consonant(word) == False: #checks if there is a Zischlaut preceeding the vowel
                checkword = word[:-1]
                if any(checkword.lower().endswith(zisch) for zisch in silibants):
                    return True
                else:
                    return False

        # uses SpacY to classify animacy
        def is_alive(word):
            doc = nlp(word)
            for token in doc:
                morph = str(token.morph)
                morph = morph.split("|")
                anim = morph[0]
                anim = anim.split("=")
                anim = anim[1]
                if anim == "Anim": return True
                else: return False

        # uses spacy to check what the gender of the word is if it ends with (-ь), returning TRUE if masculine and FALSE if feminine
        def soft_sign_is_masc(word):
            doc = nlp(word)
            for token in doc:
                morph = str(token.morph).split("|")
                morph = morph[2]
                morph = morph.split("=")
                morph = morph[1]
                if morph == "Masc": 
                    return True
                if morph == "Fem":
                    return False
            
        if number == "ед":
            if case == "И":
                newword = word
            #Т
            if case == "Т":
                #FEMININE
                if word.endswith("а"):
                    newword = word[:-1]
                    newword = newword + "ой"
                #MASCULINE
                elif ends_with_consonant(word):
                    newword = word + "ом"
                #NEUTRAL
                elif word.endswith("о"):
                    newword = word[:-1]
                    newword = newword + "ом"
                #words ending с мягким знаком
                elif word.endswith("ь"):
                    #MASC
                    if soft_sign_is_masc(word) == True:
                        newword = word[:-1]
                        newword = newword + "ем"
                    #FEM
                    elif soft_sign_is_masc(word) == False:
                        newword = word + "ю"

            #Р
            elif case == "Р":
                # FEMININE
                if word.endswith("а"):
                    newword = word[:-1] + "у"
                # MASCULINE ANIMATE
                elif is_alive(word):
                    if ends_with_consonant(word):
                        newword = word + "а"
                    elif soft_sign_is_masc(word) == True:
                        newword = word[:-1] + "я"
                # MASCULINE INANIMATE (not living and ends with a consonant)
                elif ends_with_consonant(word) and not is_alive(word):
                    newword = word
                # NEUTRAL
                elif word.endswith("о"):
                    newword = word
                # SOFT SIGN, animacy is already checked so not necessary to check again
                elif word.endswith("ь"):
                    newword = word

            #Д
            elif case == "Д":
                #FEMININE
                if word.endswith("а"):
                    newword = word[:-1]
                    newword = newword + "е"
                #MASCULINE
                elif ends_with_consonant(word):
                    newword = word + "у"
                elif soft_sign_is_masc(word) == True:
                        newword = word[:-1] + "ю"
                #NEUTRAL
                elif word.endswith("о"):
                    newword = word[:-1]
                    newword = newword + "у"
                #words ending с мягким знаком
                elif word.endswith("ь"):
                    #MASC
                    if soft_sign_is_masc(word) == True:
                        newword = word[:-1]
                        newword = newword + "ю"
                    #FEM
                    elif soft_sign_is_masc(word) == False:
                        newword = word[:-1]
                        newword = newword + "и"

            #П
            elif case == "П":
                #FEMININE
                if word.endswith("а"):
                    newword = word[:-1]
                    newword = newword + "е"
                #MASCULINE
                elif ends_with_consonant(word):
                    newword = word + "е"
                #NEUTRAL
                elif word.endswith("о"):
                    newword = word[:-1]
                    newword = newword + "е"
                elif word.endswith("ь"):
                    #MASC
                    if soft_sign_is_masc(word) == True:
                        newword = word[:-1]
                        newword = newword + "e"
                    #FEM
                    if soft_sign_is_masc(word) == False:
                        newword = word[:-1]
                        newword = newword + "и"

            #В
            elif case == "В":
                #FEMININE
                if word.endswith("а"):
                    newword = word[:-1]
                    newword = newword + "ы"
                # MASCULINE ANIMATE
                elif is_alive(word):
                    if ends_with_consonant(word):
                        newword = word + "а"
                    elif soft_sign_is_masc(word) == True:
                        newword = word[:-1] + "я"
                # MASCULINE INANIMATE (not living and ends with a consonant)
                elif ends_with_consonant(word) and not is_alive(word):
                    newword = word + "a"
                #NEUTRAL
                elif word.endswith("о"):
                    newword = word[:-1]
                    newword = newword + "а"
                #SOFT SIGN, animacy is already checked so not necessary to check again
                elif word.endswith("ь"):
                    #MASC
                    if soft_sign_is_masc(word) == True:
                        newword = word[:-1]
                        newword = newword + "я"
                    #FEM
                    if soft_sign_is_masc(word) == False:
                        newword = word[:-1]
                        newword = newword + "и"
        
        elif number == "мн":
            #И
            if case == "И":
                if zischending(word) == True:
                    if ends_with_consonant(word) == True:
                        newword = word + "и"
                    elif ends_with_consonant(word) == False:
                        newword = word[:-1]
                        newword = newword + "и"
                else:
                    if ends_with_consonant(word) == True:
                        newword = word + "ы"
                    elif ends_with_consonant(word) == False:
                        newword = word[:-1]
                        newword = newword + "ы"
            #Т
            if case == "Т":
                if word.endswith("ь"):
                    newword = word[:-1]
                    newword = newword + "ями"
                elif ends_with_dipthong(word):    
                    newword = word[:-1]
                    newword = newword + "ями"    
                elif ends_with_consonant(word) == True:
                    newword = word + "ами"
                else:
                    newword = word[:-1]
                    newword = newword + "ами"      
            #Д
            if case == "Д":
                if word.endswith("ь"):
                    newword = word[:-1]
                    newword = newword + "ям"
                elif ends_with_dipthong(word):    
                    newword = word[:-1]
                    newword = newword + "ям" 
                elif ends_with_consonant(word) == True:
                    newword = word + "ам"
                else:
                    newword = word[:-1]
                    newword = newword + "ам"  
            #Р
            if case == "Р":
                if ends_with_consonant(word) == True: #MASCULINE CONSONANT ENDING
                    if is_alive(word): #CHECKS FOR ANIMACY
                        if word.endswith("а"):
                            if consonantcluster(word):
                                newword = word[:-1]
                                newword = newword[:-1] + "е" + newword[-1]
                            else:
                                newword = word[:-1]
                                if word.endswith("о"):
                                    if consonantcluster(word):
                                        newword = word[:-1]
                                        newword = newword[:-1] + "о" + newword[-1]
                                else:
                                    newword = word[:-1]
                        elif ends_with_consonant(word) == True:
                            newword = word + "ов"
                        elif word.endswith("й"):
                            newword = word[:-1]
                            newword = newword + "ев"
                        elif word.endswith("ь"):
                            newword = word[:-1]
                            newword = newword + "ей"
                    elif soft_sign_is_masc(word) == True:
                        newword = word[:-1] + "я"
                elif word.endswith("ь"):
                    if soft_sign_is_masc(word) == True: #MASCULINE SOFT SIGN ENDING
                        if is_alive(word): #CHECKS FOR ANIMACY
                            newword = word[:-1] + "ей"
                        else:
                            newword = word[:-1] + "и"
                    else:
                        newword = word[:-1] + "и"
                else: #FEMININE AND NEUTRAL
                    if zischending(word) == True:
                        if ends_with_consonant(word) == True:
                            newword = word + "и"
                        elif ends_with_consonant(word) == False:
                            newword = word[:-1]
                            newword = newword + "и"
                    else:
                        if ends_with_consonant(word) == True:
                            newword = word + "ы"
                        elif ends_with_consonant(word) == False:
                            newword = word[:-1]
                            newword = newword + "ы"

            #П
            if case == "П":
                if word.endswith("ь"):
                    newword = word[:-1]
                    newword = newword + "ях"
                elif ends_with_dipthong(word):    
                    newword = word[:-1]
                    newword = newword + "ях" 
                elif ends_with_consonant(word) == True:
                    newword = word + "ах"
                else:
                    newword = word[:-1]
                    newword = newword + "ах"
                
            #В
            if case == "В":
                if word.endswith("а"):
                    if consonantcluster(word):
                        newword = word[:-1]
                        newword = newword[:-1] + "е" + newword[-1]
                    else:
                        newword = word[:-1]
                if word.endswith("о"):
                    if consonantcluster(word):
                        newword = word[:-1]
                        newword = newword[:-1] + "о" + newword[-1]
                    else:
                        newword = word[:-1]
                elif word.endswith("о"):
                    newword = word[:-1]
                    newword = newword + "ок"
                elif ends_with_consonant(word) == True:
                    newword = word + "ов"
                elif word.endswith("й"):
                    newword = word[:-1]
                    newword = newword + "ев"
                elif word.endswith("ь"):
                    newword = word[:-1]
                    newword = newword + "ей"
                elif word.endswith(("ие", "ия")):
                    newword = word[:-1]
                    newword = newword + "й"
                elif word.endswith("я"):
                    newword = word[:-1]
                    newword = newword + "ь"
                elif word.endswith("е"):
                    newword = word + "й"
        
        return newword 

    def pronoun_inflector(word, case):
        
        newword = ""

        firstsing = ("я", "меня", "мне", "мной", "мне")
        firstplural = ("мы", "нас", "нам", "нами", "нас")
        secsing = ("ты", "тебя", "тебе", "тобой", "тебе")
        secplural = ("вы", "вас", "вам", "вами", "вас")
        thirdsingmasc = ("он", "его", "ему", "им", "нём")
        thirdsingfem = ("она", "её", "ей", "ей", "ней")
        thirdsingneut = ("оно", "его", "ему", "им", "нём")
        thirdмн = ("они", "их", "им", "ими", "них")

        if word in firstsing :
            if case == "И":
                newword = "я"
                return newword
            elif case == "В":
                newword = "меня"
                return newword
            elif case == "Р":
                newword = "меня"
                return newword
            elif case == "Д":
                newword = "мне"
                return newword
            elif case == "Т":
                newword = "мной"
                return newword
            elif case == "П":
                newword = "мне"
                return newword

        elif word in secsing :
            if case == "И":
                newword = "тебя"
                return newword
            elif case == "Р":
                newword = "тебя"
                return newword
            elif case == "В":
                newword = "тебя"
                return newword
            elif case == "Д":
                newword = "тебе"
                return newword
            elif case == "Т":
                newword = "тобой"
                return newword
            elif case == "П":
                newword = "тебе"
                return newword
            
        elif word in thirdsingmasc:
            if case == "И":
                newword = "он"
                return newword
            elif case == "Р":
                newword = "его"
                return newword
            elif case == "В":
                newword = "его"
                return newword
            elif case == "Д":
                newword = "ему"
                return newword
            elif case == "Т":
                newword = "им"
                return newword
            elif case == "П":
                newword = "нём"
                return newword
            
        elif word in thirdsingfem :
            if case == "И":
                newword = "она"
                return newword
            elif case == "Р":
                newword = "eë"
                return newword
            elif case == "В":
                newword = "её"
                return newword
            elif case == "Д":
                newword = "ей"
                return newword
            elif case == "Т":
                newword = "ей"
                return newword
            elif case == "П":
                newword = "ней"
                return newword
            
        elif word in thirdsingneut :
            if case == "И":
                newword = "оно"
                return newword
            elif case == "Р":
                newword = "его"
                return newword
            elif case == "В":
                newword = "оно"
                return newword
            elif case == "Д":
                newword = "ему"
                return newword
            elif case == "Т":
                newword = "им"
                return newword
            elif case == "П":
                newword = "нём"
                return newword

        elif word in firstplural :
            if case == "И":
                newword = "мы"
                return newword
            elif case == "Р":
                newword = "нас"
                return newword
            elif case == "В":
                newword = "нас"
                return newword
            elif case == "Д":
                newword = "нам"
                return newword
            elif case == "Т":
                newword = "нами"
                return newword
            elif case == "П":
                newword = "нас"
                return newword
            
        elif word in secplural :
            if case == "И":
                newword = "вы"
                return newword
            elif case == "Р":
                newword = "вас"
                return newword
            elif case == "В":
                newword = "вас"
                return newword
            elif case == "Д":
                newword = "вам"
                return newword
            elif case == "Т":
                newword = "вами"
                return newword
            elif case == "П":
                newword = "вас"
                return newword
            
        elif word in thirdмн :
            if case == "И":
                newword = "они"
                return newword
            elif case == "Р":
                newword = "их"
                return newword
            elif case == "В":
                newword = "их"
                return newword
            elif case == "Д":
                newword = "им"
                return newword
            elif case == "Т":
                newword = "ими"
                return newword
            elif case == "П":    
                newword = "их"
                return newword  

    def past_tense_conjugator(word, gender):

        doc = nlp(word)
        for token in doc:
            morph = str(token.lemma_)
            word = morph
        
        if word.endswith("ься"):
            if gender == "м":
                newword = word[:-4]
                newword = newword + ("лься")
                return newword
            if gender == "ж":
                newword = word[:-4]
                newword = newword + ("лась")
                return newword
            if gender == "с":
                newword = word[:-4]
                newword = newword + ("лось")
                return newword
            if gender == "мн":
                newword = word[:-4]
                newword = newword + ("лись")
                return newword
        else:    
            if gender == "м":
                newword = word[:-2]
                newword = newword + ("л")
                return newword
            if gender == "ж":
                newword = word[:-2]
                newword = newword + ("ла")
                return newword
            if gender == "с":
                newword = word[:-2]
                newword = newword + ("ло")
                return newword
            if gender == "мн":
                newword = word[:-2]
                newword = newword + ("ли")
                return newword

word = input("вводите пожалуюйста слово")
doc = nlp(word)

for token in doc:

    for wordtype_russian, wordtype_english in wordtypes.items():
        pos = token.pos_
        if pos == wordtype_english:
            wordtype = wordtype_russian
            continue

    print(f"часть речи: {wordtype}")
    print(f"со слова «{word}» получившиеся склонения:\n")

    if token.pos_ == 'NOUN':
        word = token.text
        for numberopt in numbers:
            number = numberopt
            print(number)
            for caseopt in cases:
                case = caseopt
                newword = morph.inflector(word, case, number)
                print(f"{caseopt}: {newword}")
            print("")
    
    if token.pos_ == "PRON":
        word = token.text
        for caseopt in cases:
            case = caseopt
            number = numberopt
            newword = morph.pronoun_inflector(word, case)
            print(f"{caseopt}: {newword}")

    elif token.pos_ == "VERB":
        word = token.text
        aspectpair = morph.get_aspectpair(word)
        for form in aspectpair:
            if form is None:
                aspectpair.remove(form)
        if len(aspectpair) == 2:
            print(f"несовершенный вид: {aspectpair[0]}")
            print(f"совершенный вид: {aspectpair[1]}")
            print()
        if len(aspectpair) == 3:
            print(f"несовершенный вид: {aspectpair[0]}")
            print(f"совершенный вид: {aspectpair[1]} (или) {aspectpair[2]}")
            print()
        for form in aspectpair:
            word = form
            for gender in verbgenders:
                newword = morph.past_tense_conjugator(word, gender)
                print(f"{gender}: {newword}")
            print()