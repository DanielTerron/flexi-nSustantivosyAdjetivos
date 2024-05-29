import spacy
from apiLanguageTool import check_spelling
from spanish_inflections import basic_adj_data, basic_noun_data, search_noun
nlp = spacy.load("es_core_news_sm")
consonante={"b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"}
vocal={"a","e","i","o","u","á","é","í","ó","ú"}
def is_singular(word):
    if(search_noun(word)!=None):
        if basic_noun_data(word).get("number")  == ['Plur']:
            return False
        else:
            return True
    else:
        if basic_adj_data(word).get("number")  == ['Plur']:
            return False
        else:
            return True
        
def is_plural(word):
    if(search_noun(word)!=None):
        if basic_noun_data(word).get("number")  == ['Plur']:
            return True
        else:
            return False
    else:
        if basic_adj_data(word).get("number")  == ['Plur']:
            return True
        else:
            return False

def pluralize(word):
    if(is_plural(word)):
        return word
    if word.endswith("ch"):
        return word + "es"
    elif not word.endswith(("l", "r", "n", "d", "z", "j", "y")) and not word.endswith in vocal:
        return word + "s"
    elif word[-1] == "z":
        return word[:-1] + "ces"
    elif  word.endswith(("l", "r", "n", "d", "j")):
        if len(word) > 1 and word[-2] not in consonante:
            return word + "es"
        else:
            return word + "s"
    elif word.endswith(("í", "ú")):
        return word + "es"
    elif word[-1] in "aeiouáéó":
        return word + "s"
    elif word[-1] in consonante and word[-2] in consonante:
        return word + "es"
    elif word.endswith("y") and word[-2] in "aeiouáéíóú":
        return word + "es"
    elif word.endswith(("s", "x")):
        return word + "es"
    else:
        return word + "s"
  
    
def singularize(word):
    if is_singular(word):
        return word
    if word.endswith("ches"):
        return word[:-2]
    elif word.endswith("es"):
            if word[-3] == "c":
                return word[:-3] + "z"
            else:
                return word[:-2]
    elif word.endswith("s"):
            return word[:-1]
    else:
        return word
    
def pluralizeChecked(word):
    wordPluralized = pluralize(word)
    wordPluralized = check_spelling(wordPluralized)
    return wordPluralized

def singularizeChecked(word):
    wordSingularized = singularize(word)
    wordSingularized = check_spelling(wordSingularized)
    return wordSingularized