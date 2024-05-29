import nltk
import deplacy
import pattern
from pattern.text.es import conjugate,PRESENT,SINGULAR,PLURAL,PAST,FUTURE
import spacy
import sys
from spellchecker import SpellChecker
import language_tool_python
import time
from flexionador import adaptarDeterminante, adaptarPalabraEnFrase,  flexionesGeneroyNumero, cambiarPalabraEnFrase,buscarDeterminantesRelacionados, masc_y_fem
sys.path.append(r'C:\Users\danie\OneDrive\Escritorio\TFG\spanish_inflections-main')
from busquedaRAE import is_noun, obtener_masculino_y_femenino

import spanish_inflections
from spanish_inflections import basic_noun_data, fix_word, search_adjetive, search_noun, search_word
from inflexionNumero import singularize, pluralize

#sys.stdout = open('C:/Users/danie/OneDrive/Escritorio/TFG/Pruebas/Prueba_1.txt', 'a+',encoding='utf-8')
#PRUEBA 1 : FLEXIONES GENERO Y NUMERO
nlp = spacy.load("es_core_news_sm")
"""
print("Prueba 1 : Flexiones genero y numero\n")
sustantivos_adjetivos = "niño perro gata hombre maestras rojo doctores bueno mala pequeñas amarillo rápidos lentas cerdo altos bajas blancos señor rey actor"

doc = nlp(sustantivos_adjetivos)
for token in doc:
     print("Palabra introducida: " +token.text)
     print(flexionesGeneroyNumero(token))
     

#sys.stdout.close()
time.sleep(20)

print("Prueba 1 : Flexiones genero y numero\n")
sustantivos_adjetivos2 = "estudiante cantante periodista artista atleta joven modelo policía turista dentista"
doc2 = nlp(sustantivos_adjetivos2)
for token in doc2:
     print("Palabra introducida: " +token.text)
     print(flexionesGeneroyNumero(token))
  
print("Prueba 1 : Flexiones genero y numero\n")
sustantivos_adjetivos2 = "zapato libro silla mesa ventana carro bicicleta casa sofá coche"
doc2 = nlp(sustantivos_adjetivos2)
for token in doc2:
     print("Palabra introducida: " +token.text)
     print(flexionesGeneroyNumero(token))
 
print("Prueba 1 : Flexiones genero y numero\n")
sustantivos_adjetivos2 = "sed tijeras gafas electricidad agua dolor hambre bragas vacaciones amor"
doc2 = nlp(sustantivos_adjetivos2)
for token in doc2:
     print("Palabra introducida: " +token.text)
     print(flexionesGeneroyNumero(token))

#PRUEBA 2 : Adaptar palabra en frase
#time.sleep(20)
print("PRUEBA 2 : Adaptar palabra en frase\n")
frase3 = "El perro de mi padre adoptivo es bonito"
doc3 = nlp(frase3)
token3 = doc3[1]
print("Frase: '%s' " %frase3+ "Palabra a sustituir: '%s'" %token3.text + " Palabra sustituta: " + "'gato'")
adaptarPalabraEnFrase(doc3,token3,"gato")

frase4 = "Mi primo pequeño tiene 9 años"
doc4 = nlp(frase4)
token4 = doc4[1]
print("Frase: '%s' " %frase4+ "Palabra a sustituir: '%s'" %token4.text + " Palabra sustituta: " + "'hermano'")
adaptarPalabraEnFrase(doc4,token4,"hermano")

frase5 = "A mi amigo le gusta el futbol"
doc5 = nlp(frase5)
token5 = doc5[2]
print("Frase: '%s' " %frase5+ "Palabra a sustituir: '%s'" %token5.text + " Palabra sustituta: " + "'padre'")
adaptarPalabraEnFrase(doc5,token5,"padre")

frase6 = "Las luces se apagaron"
doc6 = nlp(frase6)
token6 = doc6[1]
print("Frase: '%s' " %frase6+ "Palabra a sustituir: '%s'" %token6.text + " Palabra sustituta: " + "'bombillas'")
adaptarPalabraEnFrase(doc6,token6,"bombillas")

frase7 = "La fiesta se ha terminado"
doc7 = nlp(frase7)
token7 = doc7[1]
print("Frase: '%s' " %frase7+ "Palabra a sustituir: '%s'" %token7.text + " Palabra sustituta: " + "'reunión'")
adaptarPalabraEnFrase(doc7,token7,"reunión")

frase8 = "Los leopardos son preciosos"
doc8 = nlp(frase8)
token8 = doc8[1]
print("Frase: '%s' " %frase8+ "Palabra a sustituir: '%s'" %token8.text + " Palabra sustituta: " + "'leones'")
adaptarPalabraEnFrase(doc8,token8,"leones")

frase9 = "La mesa es roja"
doc9 = nlp(frase9)
token9 = doc9[1]
print("Frase: '%s' " %frase9+ "Palabra a sustituir: '%s'" %token9.text + " Palabra sustituta: " + "'silla'")
adaptarPalabraEnFrase(doc9,token9,"silla")

frase10 = "He merendado un bocadillo"
doc10 = nlp(frase10)
token10 = doc10[3]
print("Frase: '%s' " %frase10+ "Palabra a sustituir: '%s'" %token10.text + " Palabra sustituta: " + "'plátano'")
adaptarPalabraEnFrase(doc10,token10,"plátano")

frase11 = "Los caballos son gigantes"
doc11 = nlp(frase11)
token11 = doc11[1]
print("Frase: '%s' " %frase11+ "Palabra a sustituir: '%s'" %token11.text + " Palabra sustituta: " + "'elefantes'")
adaptarPalabraEnFrase(doc11,token11,"elefantes")

frase12 = "Las casas están vacías"
doc12 = nlp(frase12)
token12 = doc12[1]
print("Frase: '%s' " %frase12+ "Palabra a sustituir: '%s'" %token12.text + " Palabra sustituta: " + "'viviendas'")
adaptarPalabraEnFrase(doc12,token12,"viviendas")

frase3 = "El perro de mi padre adoptivo es bonito"
doc3 = nlp(frase3)
token3 = doc3[1]
print("Frase: '%s' " %frase3+ "Palabra a sustituir: '%s'" %token3.text + " Palabra sustituta: " + "'tortugas'")
adaptarPalabraEnFrase(doc3,token3,"tortugas")

frase4 = "Mi primo pequeño tiene 9 años"
doc4 = nlp(frase4)
token4 = doc4[1]
print("Frase: '%s' " %frase4+ "Palabra a sustituir: '%s'" %token4.text + " Palabra sustituta: " + "'hermana'")
adaptarPalabraEnFrase(doc4,token4,"hermana")

frase5 = "A mi hermano pequeño le gusta el futbol"
doc5 = nlp(frase5)
token5 = doc5[2]
print("Frase: '%s' " %frase5+ "Palabra a sustituir: '%s'" %token5.text + " Palabra sustituta: " + "'hermana'")
adaptarPalabraEnFrase(doc5,token5,"hermana")

frase6 = "Las luces se apagaron"
doc6 = nlp(frase6)
token6 = doc6[1]
print("Frase: '%s' " %frase6+ "Palabra a sustituir: '%s'" %token6.text + " Palabra sustituta: " + "'focos'")
adaptarPalabraEnFrase(doc6,token6,"focos")

frase7 = "La fiesta se ha terminado"
doc7 = nlp(frase7)
token7 = doc7[1]
print("Frase: '%s' " %frase7+ "Palabra a sustituir: '%s'" %token7.text + " Palabra sustituta: " + "'evento'")
adaptarPalabraEnFrase(doc7,token7,"evento")

frase8 = "Los leopardos son preciosos"
doc8 = nlp(frase8)
token8 = doc8[1]
print("Frase: '%s' " %frase8+ "Palabra a sustituir: '%s'" %token8.text + " Palabra sustituta: " + "'gacelas'")
adaptarPalabraEnFrase(doc8,token8,"gacelas")

frase9 = "La mesa es roja"
doc9 = nlp(frase9)
token9 = doc9[1]
print("Frase: '%s' " %frase9+ "Palabra a sustituir: '%s'" %token9.text + " Palabra sustituta: " + "'escritorios'")
adaptarPalabraEnFrase(doc9,token9,"escritorio")

frase10 = "He merendado la tarta de la nevera"
doc10 = nlp(frase10)
token10 = doc10[3]
print("Frase: '%s' " %frase10+ "Palabra a sustituir: '%s'" %token10.text + " Palabra sustituta: " + "'plátanos'")
adaptarPalabraEnFrase(doc10,token10,"plátano")

frase11 = "Los caballos son gigantes"
doc11 = nlp(frase11)
token11 = doc11[1]
print("Frase: '%s' " %frase11+ "Palabra a sustituir: '%s'" %token11.text + " Palabra sustituta: " + "'jirafas'")
adaptarPalabraEnFrase(doc11,token11,"jirafas")

frase12 = "Las casas están vacías"
doc12 = nlp(frase12)
token12 = doc12[1]
print("Frase: '%s' " %frase12+ "Palabra a sustituir: '%s'" %token12.text + " Palabra sustituta: " + "'apartamento'")
adaptarPalabraEnFrase(doc12,token12,"apartamento")
"""
frase3 = "El avituallamiento del barco fue saboteado"
doc3 = nlp(frase3)
token3 = doc3[1]
print("Frase: '%s' " %frase3+ "Palabra a sustituir: '%s'" %token3.text + " Palabra sustituta: " + "'víveres'")
adaptarPalabraEnFrase(doc3,token3,"víveres")

frase4 = "Sus ansias de poder terminaron llevándole a su propia perdición"
doc4 = nlp(frase4)
token4 = doc4[1]
print("Frase: '%s' " %frase4+ "Palabra a sustituir: '%s'" %token4.text + " Palabra sustituta: " + "'sed'")
adaptarPalabraEnFrase(doc4,token4,"sed")

frase5 = "Los quevedos son algo que se puso de moda a finales del siglo XIX"
doc5 = nlp(frase5)
token5 = doc5[3]
print("Frase: '%s' " %frase5+ "Palabra a sustituir: '%s'" %token5.text + " Palabra sustituta: " + "'gafas'")
adaptarPalabraEnFrase(doc5,token5,"gafas")

frase6 = "Las personas se fueron"
doc6 = nlp(frase6)
token6 = doc6[1]
print("Frase: '%s' " %frase6+ "Palabra a sustituir: '%s'" %token6.text + " Palabra sustituta: " + "'gente'")
adaptarPalabraEnFrase(doc6,token6,"gente")

frase7 = "Los miedos se apoderaron de él"
doc7 = nlp(frase7)
token7 = doc7[1]
print("Frase: '%s' " %frase7+ "Palabra a sustituir: '%s'" %token7.text + " Palabra sustituta: " + "'pánico'")
adaptarPalabraEnFrase(doc7,token7,"pánico")

frase8 = "La dentadura del tigre da miedo"
doc8 = nlp(frase8)
token8 = doc8[1]
print("Frase: '%s' " %frase8+ "Palabra a sustituir: '%s'" %token8.text + " Palabra sustituta: " + "'fauces'")
adaptarPalabraEnFrase(doc8,token8,"fauces")

frase9 = "Las precipitaciones mueven el barco"
doc9 = nlp(frase9)
token9 = doc9[1]
print("Frase: '%s' " %frase9+ "Palabra a sustituir: '%s'" %token9.text + " Palabra sustituta: " + "'aire'")
adaptarPalabraEnFrase(doc9,token9,"aire")

frase10 = "Las ganas mueven montañas"
doc10 = nlp(frase10)
token10 = doc10[1]
print("Frase: '%s' " %frase10+ "Palabra a sustituir: '%s'" %token10.text + " Palabra sustituta: " + "'fe'")
adaptarPalabraEnFrase(doc10,token10,"fe")

frase11 = "Los cables dan calambre"
doc11 = nlp(frase11)
token11 = doc11[1]
print("Frase: '%s' " %frase11+ "Palabra a sustituir: '%s'" %token11.text + " Palabra sustituta: " + "'electricidad'")
adaptarPalabraEnFrase(doc11,token11,"electricidad")

frase12 = "La fiesta fue muy larga"
doc12 = nlp(frase12)
token12 = doc12[1]
print("Frase: '%s' " %frase12+ "Palabra a sustituir: '%s'" %token12.text + " Palabra sustituta: " + "'vacaciones'")
adaptarPalabraEnFrase(doc12,token12,"vacaciones")
""" 
frase4 = "El otro día me caí por la escalera"
doc4 = nlp(frase4)
token4 = doc4[7]
cambios4 = ["balcón","precipicio"]
x=0
print("Frase original : " + frase4)
while(x<len(cambios4)):
    print("Palabra a quitar : " + token4.text + " Palabra a introducir :" +cambios4[x])
    adaptarPalabraEnFrase(doc4,token4,cambios4[x])
    x = x+1
    print("\n")


frase5 = "Me encantan las lentejas"
doc5 = nlp(frase5)
token5 = doc5[3]
cambios5 = ["macarrón","guisante","melocotón"]
y=0
print("Frase original : " + frase5)
while(y<len(cambios5)):
    print("Palabra a quitar : " + token5.text + " Palabra a introducir :" +cambios5[y])
    adaptarPalabraEnFrase(doc5,token5,cambios5[y])
    y = y+1
    print("\n")


frase6 = "El avituallamiento del barco fue saboteado"
doc6 = nlp(frase6)
token6 = doc6[1]
cambios6 = "víveres"
print("Frase original : " + frase6)
print("Palabra a quitar : " + token6.text + " Palabra a introducir :" +cambios6)
adaptarPalabraEnFrase(doc6,token6,cambios6)

frase7 = "Sus ansias de poder terminaron llevándole a su propia perdición"
doc7 = nlp(frase7)
token7 = doc7[1]
cambios7 = "sed"
print("Frase original : " + frase7)
print("Palabra a quitar : " + token7.text + " Palabra a introducir :" +cambios7)
adaptarPalabraEnFrase(doc7,token7,cambios7)

frase8 = "Los quevedos son algo que se puso de moda a finales del siglo XIX"
doc8 = nlp(frase8)
token8 = doc8[3]
cambios8 = "gafas"
print("Frase original : " + frase8)
print("Palabra a quitar : " + token8.text + " Palabra a introducir :" +cambios8)
adaptarPalabraEnFrase(doc8,token8,cambios8)
"""