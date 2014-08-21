#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import tvdb_api
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


parser=argparse.ArgumentParser(description="Busca un fichero en TVDB")
parser.add_argument('fichero',help="Fichero(s) a analizar",nargs="+")
parser.add_argument('-n','--nombreserie',help="Nombre de la serie",required=True)
parser.add_argument('-l','--lenguaje',help="Idioma a buscar",required=False)
args=parser.parse_args()

# Inicializar y buscar la serie
if args.lenguaje:
    t = tvdb_api.Tvdb(language=args.lenguaje)
else:
    t = tvdb_api.Tvdb()
serie=t[args.nombreserie]

print
print "Encontrada serie \"%s\"" % serie.data['seriesname']

# Generar un dict con todos los episodios, indexado por título
lista={}
for temporada in serie:
    for episodio in serie[temporada]:
        title=serie[temporada][episodio]['episodename']
        if title: lista[title]={"season":temporada,"episode":episodio}
#print lista
#print len(lista)

for fich in args.fichero:
    # Buscar capítulo más parecido
    nombrelimpio=os.path.splitext(os.path.basename(fich))[0].lower()
    results=process.extract(nombrelimpio,lista.keys(),limit=5)
    optselected=False
    while not optselected:
        print
        print "Analizando: %s" % fich
        print "Resultados:"
        num=1
        for r in results:
            titr=r[0]
            similarity=r[1]
            print "%2s %d) %02d%% S%02dE%02d - %s" % ("*" if num==1 else "",num,similarity,lista[titr]['season'],lista[titr]['episode'],titr)
            num+=1
        sel=raw_input("\nOpción (número, q para salir): ")
        if sel=="":
            sel="1"
        if sel.lower()=="q":
            sel="-1"
            optselected=True
        if int(sel) in range(len(results)+1):
            optselected=True
            break
        if not optselected: print "Opción incorrecta"

    if int(sel)>0:
        titsel=results[int(sel)-1][0]
        nomorig=os.path.basename(fich)
        nuevonom="%s - S%02dE%02d - %s%s" % (serie.data['seriesname'],lista[titsel]['season'],lista[titsel]['episode'],titsel,os.path.splitext(os.path.basename(fich))[1].lower())
       
        # No renombrar ficheros que ya estén bien
        if nuevonom!=nomorig:
            optselected=False
            while not optselected:
                print
                print "Nombre original: %s" % os.path.basename(fich)
                print "Nuevo nombre:    %s" % nuevonom
                print
                sel=raw_input("Renombrar? ([s]/n) ")
                if sel=="": sel="s"
                if sel.lower() in ['s','n']:
                    optselected=True
            if sel=="s":
                print "Renombrando..."
                pathorig=fich
                pathdest=os.path.join(os.path.dirname(fich),nuevonom)
                os.rename(pathorig,pathdest)
            else:
                print "No hacemos nada"

