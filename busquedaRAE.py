import sys
import requests
import spacy
import spanish_inflections
from spanish_inflections import fix_word
sys.path.append(r'C:\Users\danie\OneDrive\Escritorio\TFG\spanish_inflections-main')
nlp = spacy.load("es_core_news_sm")
from bs4 import BeautifulSoup

def is_masc(palabra):
    if(palabra.morph.get("Gender")==["Masc"]):
        return True
    else:
        return False

def is_noun(palabra):
     if(palabra.pos_=="NOUN" or palabra.pos_ == "VERB"):
        return True
     else:
        return False
     
def obtener_masculino_y_femenino(palabra):
    """
    Esta función busca la palabra en la página de la RAE y extrae el masculino y el femenino.
    
    Parámetros:
        palabra (str): Palabra a buscar en la RAE
        
    Retorna:
        genero(str[]): Array con la palabra + su femenino/masculino si es que es variable en genero, si no devuelve unicamente la palabra
        
    """

    # Normalizamos la palabra para formar la URL
    palabra_normalizada = palabra.lower().strip().replace(" ", "-")

    # Construimos la URL de búsqueda en la RAE
    url = f"https://dle.rae.es/{palabra_normalizada}"

    try:
        # Establecemos un user-agent para simular un navegador web estándar
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Realizamos la solicitud HTTP
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verificamos si hay errores en la solicitud HTTP

        # Parseamos el contenido HTML de la página
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscamos el título de la página que contiene la información del masculino y femenino
        title_tag = soup.find("title")

        # Extraemos el texto del título
        title_text = title_tag.text.strip()

        # Dividimos el título en palabras
        palabras = title_text.split("|")

        # Devolvemos el array de masculinos y femeninos, ya que puede contener una sola entrada al haber palabras invariables en genero
        genero = palabras[0].strip().split(", ")
        if(genero is None or palabra_normalizada not in genero) : 
            print(f"La palabra {palabra} no está en el Diccionario") 
            return []
        if(len(genero)==2):
            return genero
        else : #comprobamos si la palabra es invariable en genero, o si es heteronimo que en ese caso agregariamos su masculino/femenino
            doc = nlp(palabra)
            token = doc[0]
            if(is_masc(token)):
                if(is_noun(token)):
                    word = fix_word(spanish_inflections.rules_noun,palabra,"F","S")
                else:
                    word = fix_word(spanish_inflections.rules_adjetive,palabra,"F","S")
                if(word == genero[0]):#caso en el que la palabra sea invariable en genero ya que el fix_word nos ha devuelto lo mismo
                    return genero
                else:
                    genero.append(word)
                    return genero
            else:
                if(is_noun(token)):
                    word = fix_word(spanish_inflections.rules_noun,palabra,"M","S")
                    
                else:
                    word = fix_word(spanish_inflections.rules_adjetive,palabra,"M","S")
                    
                if(word == genero[0]):#caso en el que la palabra sea invariable en genero ya que el fix_word nos ha devuelto lo mismo
                    return genero
                else:
                    word2 = genero[0]
                    genero[0] = word
                    genero.append(word2)
                    return genero
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud HTTP: {e}")
        