#!/usr/bin/python
# coding=utf-8
#~ ========================== IMPORT  =================================
import datetime, time
import pprint
import re
import sys
import struct
#~======================================================================
#~================================ VARIABLES =========================

#~ Source file for testing
fichier_name = 'E:\Iut\Rapport de Stage/testeur_UM.pnp' 

#~ ================================================================


def composant_recherche():
    print("Début programme")
   
   # form=FORM('Your Choose:', SELECT(line,_name='fichier_name',requires=IS_IN_SET([value, 'no'])).xml()
    
    try:
      
        fichier = open(fichier_name, "r")
       
        for line in fichier:
           
            lines = line.strip() 
           
            p = re.compile('^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$')
                  
            if "-composant-" in line:
                    m = p.match(line)
                   
                    if m:
                        composant = m.group(1)
                        print(composant)
    except IOError:
            print ("Erreur lors de l'ouverture du fichier !")
    except ValueError:
           print ("Erreur lors de la conversion !")
    
    finally:
            fichier.close()
    return
composant_recherche()
