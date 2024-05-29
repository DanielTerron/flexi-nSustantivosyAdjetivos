import sys
import spacy
from array import array
import pattern
from pattern.text.es import conjugate,PRESENT,SINGULAR,PLURAL,PAST,FUTURE
sys.path.append(r'C:\Users\danie\OneDrive\Escritorio\TFG\spanish_inflections-main')
import spanish_inflections 
from spanish_inflections import fix_verb, fix_word, rules_adjetive,rules_noun, basic_adj_data, basic_noun_data, search_adjetive, search_noun, search_rule
from busquedaRAE import obtener_masculino_y_femenino
from inflexionNumero import is_singular, singularizeChecked, pluralizeChecked
nlp = spacy.load("es_core_news_sm")

singularia_tantum = [
    "sed", "salud", "gente", "dinero", "pánico", "agua",
    "aire", "caos", "fama", "amor", "paz", "felicidad", "sufrimiento",
    "odio", "esperanza", "libertad", "justicia", "sabiduría", "fe",
    "miedo", "electricidad", "hambre", "dolor"
]
pluralia_tantum = [
    "tijeras", "gafas", "pantalones", "víveres", "albricias", "enseres",
    "vacaciones", "cenizas", "esponsales", "aduanas", "anales", "exequias",
    "nupcias", "bragas", "catacumbas", "cosquillas",
    "fauces", "misericordias", "trizas", "vítores", "andas", "modales"
]

def flexionesGeneroyNumero(token):
    """
    Esta función devuelve todas las variaciones de género y número de la palabra token

    Parámetros:
        token (spaCyToken): Palabra a buscar sus variaciones
        
    Retorna:
        variaciones(str[]): Array con la palabra + sus variaciones, en el orden MS, MP, FS, FP
        
    """
    if(search_noun(token.text) == None and search_adjetive(token.text) == None and token.tag_!="DET"): #si no es sustantivo ni adjetivo ni determinante
        return ("La palabra: " +token.text +" no es un adjetivo ni un sustantivo ni un determinante")
    if(token.text.lower() in singularia_tantum):
        if basic_noun_data(token.text.lower()).get("gender" == ["Masc"]):
            return ["MS: "+token.text,"FS: " , "MP: ", "FP: "]
        else:
            return ["MS: ", "FS: " +token.text, "MP: ", "FP: "]
    if(token.text.lower() in pluralia_tantum):
        if basic_noun_data(token.text.lower()).get("gender" == ["Masc"]):
            return ["MS: ", "FS: ","MP: " +token.text, "FP: "]
        else:
            return ["MS: ", "FS: ", "MP: ", "FP: "+token.text]
    if(search_noun(token.text) == None and search_adjetive(token.text) == None):
        if token.morph.get("Gender") == ["Masc"]:
            if token.morph.get("Number") == ["Sing"]:
                femsing = adaptarDeterminante(token.text,["Sing"],["Fem"])
                femplur = adaptarDeterminante(token.text,["Plur"],["Fem"])
                mascplur = adaptarDeterminante(token.text,["Plur"],["Masc"])
                return ["MS: "+token.text,"FS: " +femsing, "MP: "+mascplur, "FP: "+femplur]
            else:
                femsing = adaptarDeterminante(token.text,["Sing"],["Fem"])
                femplur = adaptarDeterminante(token.text,["Plur"],["Fem"])
                mascsing = adaptarDeterminante(token.text,["Sing"],["Masc"])
                return ["MS: "+mascsing,"FS: " +femsing, "MP: "+token.text, "FP: "+femplur]
        else:
            if token.morph.get("Number") == ["Sing"]:
                mascsing = adaptarDeterminante(token.text,["Sing"],["Masc"])
                femplur = adaptarDeterminante(token.text,["Plur"],["Fem"])
                mascplur = adaptarDeterminante(token.text,["Plur"],["Masc"])
                return ["MS: "+mascsing,"FS: " +token.text, "MP: "+mascplur, "FP: "+femplur]
            else:
                femsing = adaptarDeterminante(token.text,["Sing"],["Fem"])
                mascplur = adaptarDeterminante(token.text,["Plur"],["Masc"])
                mascsing = adaptarDeterminante(token.text,["Sing"],["Masc"])
                return ["MS: "+mascsing,"FS: " +femsing, "MP: "+mascplur, "FP: "+token.text]
    fem = ""
    masc = ""
    codigo = 0
    singular = singularizeChecked(token.text)
    listaGenero = masc_y_fem(token)
    
    if(search_noun(token.text)!=None):
        
        if(listaGenero is not None and len(listaGenero)==1 ): #en caso de que la palabra exista y sea invariable en genero
            
            if(basic_noun_data(token.text).get("gender") ==  ['Masc']): 
                masc = listaGenero[0]
                codigo = 1
            else:
                fem = listaGenero[0]
                codigo = 2
        elif(listaGenero is not None and len(listaGenero)>1):
            masc = listaGenero[0]
            fem = listaGenero[1]
            codigo = 3
        else:  return ["MS: ","FS: ","MP: ","FP: "]
        if(codigo == 1): #caso en el que la palabra es masculina e invariable en genero
            plural = pluralizeChecked(masc)
            variaciones = ["MS: "+masc, "FS: ", "MP: "+plural, "FP: "]
            return(variaciones)
        elif(codigo == 2):  #caso en el que la palabra es femenina e invariable en genero
            plural = pluralizeChecked(fem)
            variaciones = ["MS: ", "FS: "+fem, "MP: ", "FP: " +plural]
            return(variaciones)
        elif(codigo == 3):
            pluralMasc = pluralizeChecked(masc)
            pluralFem = pluralizeChecked(fem) 
            variaciones = ["MS: "+masc,"FS: " +fem, "MP: "+pluralMasc, "FP: "+pluralFem]
            return(variaciones)
    else:
        if(listaGenero is not None and len(listaGenero)==1 ): #en caso de que la palabra exista y sea invariable en genero
            
            if(basic_adj_data(token.text).get("gender") ==  ['Masc']): 
                masc = listaGenero[0]
                codigo = 1
            else:
                fem = listaGenero[0]
                codigo = 2
        elif(listaGenero is not None and len(listaGenero)>1):
            masc = listaGenero[0]
            fem = listaGenero[1]
            codigo = 3
        else:  return ["MS: ","FS: ","MP: ","FP: "]
        if(codigo == 1): #caso en el que la palabra es masculina e invariable en genero
            plural = pluralizeChecked(masc)
            variaciones = ["MS: "+masc, "FS: ", "MP: "+plural, "FP: "]
            return(variaciones)
        elif(codigo == 2):  #caso en el que la palabra es femenina e invariable en genero
            plural = pluralizeChecked(fem)
            variaciones = ["MS: ", "FS: "+fem, "MP: ", "FP: " +plural]
            return(variaciones)
        elif(codigo == 3):
            pluralMasc = pluralizeChecked(masc)
            pluralFem = pluralizeChecked(fem) 
            variaciones = ["MS: "+masc,"FS: " +fem, "MP: "+pluralMasc, "FP: "+pluralFem]
            return(variaciones)
   

def adaptarDeterminante(determinante, numero, genero): #Se le pasa un determinante y el genero y numero al que adaptar ese determinante
    determinante = determinante.lower()
    lemma = search_rule(spanish_inflections.rules_tanc,determinante).get("lemma")
    if (genero == ["Masc"] and numero == ['Sing']) :
        respuesta = spanish_inflections.fix_word(spanish_inflections.rules_tanc,lemma,"M","S")
    elif(genero == ["Masc"] and numero == ['Plur']) :
        respuesta = spanish_inflections.fix_word(spanish_inflections.rules_tanc,lemma,"M","P")
    elif(genero == ["Fem"] and numero == ['Sing']) :
        respuesta = spanish_inflections.fix_word(spanish_inflections.rules_tanc,lemma,"F","S")
    else:
        respuesta = spanish_inflections.fix_word(spanish_inflections.rules_tanc,lemma,"F","P")
    return respuesta


def buscarDeterminantesRelacionados(frase, Adjetivo):#devuelve el indice del determinante relacionado a un adjetivo
    mi_array = array('i')
    for token in frase:
        if token.tag_=="DET" and token in Adjetivo.children:#si es un determinante y esta relacionado con el adjetivo
            if (token.i not in mi_array):
                mi_array.append(token.i)
    for token in frase:
        if token.tag_=="DET" and Adjetivo in token.ancestors:#si es un determinante y esta relacionado con el adjetivo
            if (token.i not in mi_array):
                mi_array.append(token.i)
    if(len(mi_array)!=0):
        mi_array_sorted = array('i',sorted(mi_array))
        return mi_array_sorted
    return mi_array

def masc_y_fem(palabra):
    genero = []
    singular = singularizeChecked(palabra.text)
    doc = nlp(singular)
    if search_adjetive(doc[0].text) == None:
        if(basic_noun_data(doc[0].text).get("gender")==["Fem"] and basic_noun_data(doc[0].text).get("number") == ["Sing"]):
            masc = fix_word(spanish_inflections.rules_noun,doc[0].text,"M","S")
            if(masc == ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(masc)
                genero.append(doc[0].text)
        if(basic_noun_data(doc[0].text).get("gender")==["Fem"] and basic_noun_data(doc[0].text).get("number") == ["Plur"]):
            masc = fix_word(spanish_inflections.rules_noun,doc[0].text,"M","P")
            if(masc == ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(masc)
                genero.append(doc[0].text)
        elif(basic_noun_data(doc[0].text).get("gender")==["Masc"] and basic_noun_data(doc[0].text).get("number") == ["Sing"]):
            fem = fix_word(spanish_inflections.rules_noun,doc[0].text,"F","S")
            if(fem ==  ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(doc[0].text)
                genero.append(fem)
        elif(basic_noun_data(doc[0].text).get("gender")==["Masc"] and basic_noun_data(doc[0].text).get("number") == ["Plur"]):
            fem = fix_word(spanish_inflections.rules_noun,doc[0].text,"F","P")
            if(fem ==  ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(doc[0].text)
                genero.append(fem)
    else:
        if(basic_adj_data(doc[0].text).get("gender")==["Fem"] and basic_adj_data(doc[0].text).get("number") == ["Sing"]):
            masc = fix_word(spanish_inflections.rules_adjetive,doc[0].text,"M","S")
            if(masc == ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(masc)
                genero.append(doc[0].text)
        elif(basic_adj_data(doc[0].text).get("gender")==["Fem"] and basic_adj_data(doc[0].text).get("number") == ["Plur"]):
            masc = fix_word(spanish_inflections.rules_adjetive,doc[0].text,"M","P")
            if(masc == ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(masc)
                genero.append(doc[0].text)
        elif(basic_adj_data(doc[0].text).get("gender")==["Masc"] and basic_adj_data(doc[0].text).get("number") == ["Sing"]):
            fem = fix_word(spanish_inflections.rules_adjetive,doc[0].text,"F","S")
            if(fem == ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(doc[0].text)
                genero.append(fem)
        elif(basic_adj_data(doc[0].text).get("gender")==["Masc"] and basic_adj_data(doc[0].text).get("number") == ["Plur"]):
            fem = fix_word(spanish_inflections.rules_adjetive,doc[0].text,"F","P")
            if(fem ==  ""):#es invariable en genero
                genero.append(doc[0].text)
            else: 
                genero.append(doc[0].text)
                genero.append(fem)    
    return genero

def cambiarPalabraEnFrase(frase,numeroPalabra,palabraSustituta):
    palabras = frase.split()  # Divide la frase en una lista de palabras
    if numeroPalabra <= len(palabras):
        palabras[numeroPalabra] = palabraSustituta  # Reemplaza la palabra en la posición indicada
        return ' '.join(palabras)  # Une las palabras de nuevo en una frase

def adaptarPalabraYVerboEnFrase(frase,palabraSustituir,palabraSustituta):
    generoFinal = basic_noun_data(palabraSustituta).get("gender")
    numeroFinal = basic_noun_data(palabraSustituta).get("number")
    indice=None
    existePalabra = False
    fraseFinal = ""
    det = []
    
    determinanteCambiado = []
    adjetivoRoot = None
    i=0
    for token in frase:
        textoToken = token.text
        if(token.tag_ == "DET" ): #comprobamos si hay que cambiar algun determinante que se refiera al sustantivo a introducir o a adjetivos de los que dependa el sustantivo
            if(token in palabraSustituir.children):
               
                textoToken = adaptarDeterminante(token.text,numeroFinal,generoFinal)
                
                    
                
        elif(token.i == palabraSustituir.i):#comprobamos si la palabra es la palabra a sustituir de la frase comparar indices no .text
            textoToken = palabraSustituta
            existePalabra = True
        elif(token.tag_=="VERB" or token.tag_ == "AUX"):
            if(numeroFinal == ["Sing"]):
                textoToken = fix_verb(spanish_inflections.rules_verb,token.text,"M","S") 
            else:
                textoToken = fix_verb(spanish_inflections.rules_verb,token.text,"M","P") 
               
        elif(token.tag_ == "ADJ"):#comprobamos si hay que cambiar algun adjetivo que se refiera al sustantivo a introducir
                
            if(adjetivoRoot!=None):
                if(token in adjetivoRoot.children):
                    if(generoFinal == ['Masc']):
                        #busqueda = singularizeChecked(token.text)
                        flexiones = masc_y_fem(token)
                        textoToken = flexiones[0]
                        indice = buscarDeterminantesRelacionados(frase,token)
                        if(indice is not None):
                            if len(indice) != 0:
                                        
                                for token in frase:
                                    if token.i in indice:
                                         det.append(token.text)
                                y=0
                                while(len(det)>y):
                                    determinanteCambiado.append(adaptarDeterminante(det[y], numeroFinal,generoFinal))
                                    y = y+1
                        
                    else:
                        #busqueda = singularizeChecked(token.text)
                        flexiones = masc_y_fem(token)
                        if(len(flexiones)==1): #caso en el que el adjetivo sea invariable en genero
                            textoToken = flexiones [0]
                            indice = buscarDeterminantesRelacionados(frase,token)
                            if(indice is not None):
                                 if len(indice) != 0:
                                            
                                    for token in frase:
                                        if token.i in indice:
                                            det.append(token.text)
                                    y=0
                                    while(len(det)>y):
                                        determinanteCambiado.append(adaptarDeterminante(det[y], numeroFinal,generoFinal))
                                        y = y+1  
                    
                        else: #caso en el que el adjetivo sea variable en genero
                            textoToken = flexiones[1]
                            indice = buscarDeterminantesRelacionados(frase,token)
                            if(indice is not None):
                                if len(indice) != 0:
                                            
                                    for token in frase:
                                        if token.i in indice:
                                             det.append(token.text)
                                    y=0
                                    while(len(det)>y):
                                        determinanteCambiado.append(adaptarDeterminante(det[y], numeroFinal,generoFinal))
                                        y = y+1  
                        
        elif(palabraSustituir in token.children and token.tag_ != "VERB" and token.tag_ != "DET" and token.tag_ != "NOUN" or token in palabraSustituir.children and token.tag_ != "VERB" and token.tag_ != "DET" and token.tag_ != "NOUN"):
                        
            if(palabraSustituir in token.children):
                adjetivoRoot = token
            if(generoFinal == ['Masc']):
                #busqueda = singularizeChecked(token.text)
                flexiones = masc_y_fem(token)
                textoToken = flexiones[0]
                indice = buscarDeterminantesRelacionados(frase,token)
                if(indice is not None):
                    if len(indice) != 0:
                                        
                        for token in frase:
                            if token.i in indice:
                                det.append(token.text)
                                            
                        y=0
                        while(len(det)>y):
                            determinanteCambiado.append(adaptarDeterminante(det[y], numeroFinal,generoFinal)) 
                            y = y+1 
                    
            else:
                #busqueda = singularizeChecked(token.text)
                
                flexiones = masc_y_fem(token)
                if(len(flexiones)==1): #caso en el que el adjetivo sea invariable en genero
                    textoToken = flexiones [0]
                    indice = buscarDeterminantesRelacionados(frase,token)
                    if(indice is not None):
                        if len(indice) != 0:
                                            
                            for token in frase:
                                if token.i in indice:
                                    det.append(token.text)
                                                
                            y=0
                            while(len(det)>y):
                                determinanteCambiado.append(adaptarDeterminante(det[y], numeroFinal,generoFinal)) 
                                y = y+1 
                else: #caso en el que el adjetivo sea variable en genero
                    textoToken = flexiones[1]
                    indice = buscarDeterminantesRelacionados(frase,token)
                    if(indice is not None):
                        if len(indice) != 0:
                                            
                            for token in frase:
                                if token.i in indice:
                                    det.append(token.text)
                                                
                            y=0
                            while(len(det)>y):
                                determinanteCambiado.append(adaptarDeterminante(det[y], numeroFinal,generoFinal)) 
                                y = y+1 
            if(indice is not None):
                if len(indice)!=0:
                    x=0
                    while(len(indice)>x):
                        fraseFinal2 = cambiarPalabraEnFrase(fraseFinal,indice[x],determinanteCambiado[x])
                        fraseFinal = fraseFinal2 + " "
                        x = x+1
        if(i==0): textoToken = textoToken[0].upper() + textoToken[1:]
        fraseFinal += textoToken + " "
        textoToken=""
        i += 1
        indice=None
        det = []
        determinanteCambiado = []
        
    if(not existePalabra) : return print(f"La palabra {palabraSustituir.text} no se encuentra en la frase {frase.text}")
    return fraseFinal
                        
def adaptarPalabraEnFrase(frase, palabraSustituir, palabraSustituta):
    """
    Esta función sustituye en frase la palabraSustituir por la palabraSustituta adaptada en genero y número para concordar con el contexto de la frase

    Parámetros:
        frase (span): Frase en la que sustituir la palabraSustituir por la palabraSustituta
        palabraSustituir(spaCytoken): palabra a sustituir
        palabraSustituta (String): palabra sustituta
        
    Retorna:
        fraseFinal (String) : frase en concordancia con la palabraSustituta
        
    """
    if(palabraSustituta in singularia_tantum or palabraSustituta in pluralia_tantum):
        #print("Caso pluraria/singularia tantum")
        frase = adaptarPalabraYVerboEnFrase(frase,palabraSustituir,palabraSustituta)
        return print(frase)
    existePalabra = False
    fraseFinal = ""
    tokenNormal = nlp(palabraSustituta)
    singularPalabraSustituta = singularizeChecked(palabraSustituta)
    tokenSing =  nlp(singularPalabraSustituta)
    indice=None
    det = []
    determinanteCambiado = []
    adjetivoRoot = None
    pluralPalabraSustituta = pluralizeChecked(palabraSustituta)
    tokenPlural = nlp(pluralPalabraSustituta)

    generoFinal = basic_noun_data(palabraSustituta).get("gender")
    i=0
    if(is_singular(palabraSustituir.text)):
         palabraSustituta = singularizeChecked(palabraSustituta)
         for token in frase:
            
            textoToken = token.text
            
            if(token.tag_ == "DET"): #comprobamos si hay que cambiar algun determinante que se refiera al sustantivo a introducir o a adjetivos de los que dependa el sustantivo
                if(token in palabraSustituir.children):

                    textoToken = adaptarDeterminante(token.text,['Sing'],generoFinal)
                    
                    
                    
                
            elif(token.i == palabraSustituir.i):#comprobamos si la palabra es la palabra a sustituir de la frase comparar indices no .text
                textoToken = palabraSustituta
                existePalabra = True
                
            elif(token.tag_ == "ADJ"):#comprobamos si hay que cambiar algun adjetivo que se refiera al sustantivo a introducir
                
                if(adjetivoRoot!=None):
                    if(token in adjetivoRoot.children):
                        if(generoFinal == ['Masc']):
                            busqueda = singularizeChecked(token.text)
                            flexiones = masc_y_fem(token)
                            textoToken = flexiones[0]
                            indice = buscarDeterminantesRelacionados(frase,token)
                            if(indice is not None):
                                if len(indice) != 0:
                                    
                                    for token in frase:
                                        if token.i in indice:
                                            det.append(token.text)
                                    y=0
                                    while(len(det)>y):
                                        determinanteCambiado.append(adaptarDeterminante(det[y], ["Sing"],generoFinal))
                                        y = y+1
                    
                        else:
                            busqueda = singularizeChecked(token.text)
                            flexiones = masc_y_fem(token)
                            if(len(flexiones)==1): #caso en el que el adjetivo sea invariable en genero
                                textoToken = flexiones [0]
                                indice = buscarDeterminantesRelacionados(frase,token)
                                if(indice is not None):
                                    if len(indice) != 0:
                                        
                                        for token in frase:
                                            if token.i in indice:
                                                det.append(token.text)
                                        y=0
                                        while(len(det)>y):
                                            determinanteCambiado.append(adaptarDeterminante(det[y], ["Sing"],generoFinal))
                                            y = y+1  
                
                            else: #caso en el que el adjetivo sea variable en genero
                                textoToken = flexiones[1]
                                indice = buscarDeterminantesRelacionados(frase,token)
                                if(indice is not None):
                                    if len(indice) != 0:
                                        
                                        for token in frase:
                                            if token.i in indice:
                                                det.append(token.text)
                                        y=0
                                        while(len(det)>y):
                                            determinanteCambiado.append(adaptarDeterminante(det[y], ["Sing"],generoFinal))
                                            y = y+1  
                    
                if(palabraSustituir in token.children and token.tag_ != "DET" and token.tag_ != "VERB" and token.tag_ != "NOUN" or token in palabraSustituir.children and token.tag_ != "DET" and token.tag_ != "VERB" and token.tag_ != "NOUN"):
                    
                    if(palabraSustituir in token.children):
                        adjetivoRoot = token
                    if(generoFinal == ['Masc']):
                        busqueda = singularizeChecked(token.text)
                        flexiones = masc_y_fem(token)
                        textoToken = flexiones[0]
                        indice = buscarDeterminantesRelacionados(frase,token)
                        if(indice is not None):
                            if len(indice) != 0:
                                    
                                for token in frase:
                                    if token.i in indice:
                                        det.append(token.text)
                                        
                                y=0
                                while(len(det)>y):
                                    determinanteCambiado.append(adaptarDeterminante(det[y], ["Sing"],generoFinal)) 
                                    
                                    y = y+1 
                
                    else:
                        busqueda = singularizeChecked(token.text)
                        flexiones = masc_y_fem(token)
                        if(len(flexiones)==1): #caso en el que el adjetivo sea invariable en genero
                            textoToken = flexiones [0]
                            indice = buscarDeterminantesRelacionados(frase,token)
                            if(indice is not None):
                                if len(indice) != 0:
                                        
                                    for token in frase:
                                        if token.i in indice:
                                            det.append(token.text)
                                            
                                    y=0
                                    while(len(det)>y):
                                        determinanteCambiado.append(adaptarDeterminante(det[y], ["Sing"],generoFinal))
                                        
                                        y = y+1 
                        else: #caso en el que el adjetivo sea variable en genero
                            textoToken = flexiones[1]
                            indice = buscarDeterminantesRelacionados(frase,token)#buscamos si algun determinante acompaña al adejtivo
                            if(indice is not None):
                                if len(indice) != 0:
                                        
                                    for token in frase:
                                        if token.i in indice:
                                            det.append(token.text)
                                            
                                    y=0
                                    while(len(det)>y):
                                        
                                        determinanteCambiado.append(adaptarDeterminante(det[y], ["Sing"],generoFinal)) 
                                        
                                        y = y+1 
                if(indice is not None):
                    if len(indice)!=0:
                        x=0
                        while(len(indice)>x):
                            fraseFinal2 = cambiarPalabraEnFrase(fraseFinal,indice[x],determinanteCambiado[x])
                            fraseFinal = fraseFinal2 + " "
                            x = x+1
            if(i==0): textoToken = textoToken[0].upper() + textoToken[1:]
            fraseFinal += textoToken + " "
            textoToken=""
            i += 1
            indice=None
            det = []
            determinanteCambiado = []

    else :
         palabraSustituta = pluralizeChecked(palabraSustituta)
         for token in frase:
            
            textoToken = token.text

            if(token.tag_ == "DET" and token in palabraSustituir.children):#comprobamos si hay que cambiar algun determinante que se refiera al sustantivo a introducir
                textoToken = adaptarDeterminante(token.text,["Plur"],generoFinal)

            elif(token.i == palabraSustituir.i):#comprobamos si la palabra es la palabra a sustituir de la frase
                textoToken = palabraSustituta
                existePalabra = True

            elif(token.tag_ == "ADJ"):#comprobamos si hay que cambiar algun adjetivo que se refiera al sustantivo a introducir
                new_token = singularizeChecked(token.text)
                doc2 = nlp(new_token)
                if(doc2[0].tag_ == "ADJ"):
                    if(adjetivoRoot!=None):
                        if(token in adjetivoRoot.children):
                            if(generoFinal == ['Masc']):
                                busqueda = singularizeChecked(token.text)
                                flexiones = masc_y_fem(token)
                                textoToken = pluralizeChecked(flexiones[0])
                                indice = buscarDeterminantesRelacionados(frase,token)
                                if(indice is not None):
                                    if len(indice) != 0:
                                            
                                        for token in frase:
                                            if token.i in indice:
                                                det.append(token.text)
                                                
                                        y=0
                                        while(len(det)>y):
                                            determinanteCambiado.append(adaptarDeterminante(det[y], ["Plur"], generoFinal)) 
                                            y = y+1 
                
                            else:
                                busqueda = singularizeChecked(token.text)
                                flexiones = masc_y_fem(token)
                                if(len(flexiones)==1): #caso en el que el adjetivo sea invariable en genero
                                    textoToken = pluralizeChecked(flexiones[0])
                                    indice = buscarDeterminantesRelacionados(frase,token)
                                    if(indice is not None):
                                        if len(indice) != 0:
                                            
                                            for token in frase:
                                                if token.i in indice:
                                                    det.append(token.text)
                                                
                                            y=0
                                            while(len(det)>y):
                                                determinanteCambiado.append(adaptarDeterminante(det[y], ["Plur"], generoFinal)) 
                                                y = y+1 
                
                                else: #caso en el que el adjetivo sea variable en genero
                                    textoToken = pluralizeChecked(flexiones[1])
                                    indice = buscarDeterminantesRelacionados(frase,token)
                                    if(indice is not None):
                                        if len(indice) != 0:
                                            
                                            for token in frase:
                                                if token.i in indice:
                                                    det.append(token.text)
                                                    print(det)
                                            y=0
                                            while(len(det)>y):
                                                determinanteCambiado.append(adaptarDeterminante(det[y], ["Plur"], generoFinal)) 
                                                y = y+1 
                    if(palabraSustituir in token.children or token in palabraSustituir.children):
                        if(palabraSustituir in token.children):
                            adjetivoRoot = token
                        if(generoFinal == ['Masc']):
                            busqueda = singularizeChecked(token.text)
                            
                            flexiones = masc_y_fem(token)
                            textoToken = pluralizeChecked(flexiones[0])
                            indice = buscarDeterminantesRelacionados(frase,token)
                            if(indice is not None):
                                if len(indice) != 0:
                                            
                                    for token in frase:
                                        if token.i in indice:
                                            det.append(token.text)
                                                
                                        y=0
                                        while(len(det)>y):
                                            determinanteCambiado.append(adaptarDeterminante(det[y], ["Plur"], generoFinal)) 
                                            y = y+1 
                    
                        else:
                            busqueda = singularizeChecked(token.text)
                            flexiones = masc_y_fem(token)
                            if(len(flexiones)==1): #caso en el que el adjetivo sea invariable en genero
                                textoToken = pluralizeChecked(flexiones[0])
                                indice = buscarDeterminantesRelacionados(frase,token)
                                if(indice is not None):
                                    if len(indice) != 0:
                                            
                                        for token in frase:
                                            if token.i in indice:
                                                det.append(token.text)
                                                
                                        y=0
                                        while(len(det)>y):
                                            determinanteCambiado.append(adaptarDeterminante(det[y], ["Plur"], generoFinal)) 
                                            y = y+1 
                            else:
                                textoToken = pluralizeChecked(flexiones[1])
                                indice = buscarDeterminantesRelacionados(frase,token)
                                if(indice is not None):
                                    if len(indice) != 0:
                                            
                                        for token in frase:
                                            if token.i in indice:
                                                det.append(token.text)
                                                
                                        y=0
                                        while(len(det)>y):
                                            determinanteCambiado.append(adaptarDeterminante(det[y], ["Plur"], generoFinal)) 
                                            
                                            y = y+1 
                        
                    if(indice is not None):
                        if len(indice)!=0:
                            x=0
                            while(len(indice)>x):
                                fraseFinal2 = cambiarPalabraEnFrase(fraseFinal,indice[x],determinanteCambiado[x])
                                fraseFinal = fraseFinal2 + " "
                                x = x+1
            if(i==0): textoToken = textoToken[0].upper() + textoToken[1:]
            fraseFinal += textoToken + " "
            textoToken=""
            i += 1
            indice=None
            det = []
            determinanteCambiado = []

    if(not existePalabra) : return print(f"La palabra {palabraSustituir.text} no se encuentra en la frase {frase.text}")
    if fraseFinal and not fraseFinal[0].isupper():
        fraseFinal= fraseFinal[0].upper() + fraseFinal[1:]
    return print (fraseFinal)


    
