'''
Created on 03 juin. 2014

@author: L'Henoret Erwan

version Python 3.4

'''
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

# ~ Source file for testing
source = 'E:\Iut\Rapport de Stage/testeur_UM.pnp'  # Windows
# source = '/home/fabmanager/Desktop/testeur_UM.pnp'     # Linux

#~ ================================================================

# ~ Biscotte is the virtual support for the test
# ~ disk ='/dev/fd0' is the way of floppy disk

# ~ biscotte est le nom donne 
# ~ afin de permettre les essais ce support est virtuel
# ~ disk ='/dev/fd0' permet de cible la disquette

disk = 'biscotte'
# disk ='/dev/fd0'
#~====================================================================
bank = 'bank4'
# ~ Loops repeat X times in the same  loop
# ~ Loops premet quand a lui de repeter X fois la meme boucle 
loops = 1

# ~ time of point to drop 
Depot = ''

NewMag = ''


# ~ Y axis direction 
yaxisdir = '-'


# ~ Added lines
addLines = 3 + loops

# ~ target can be Precidot or Nova
target = "Novar"

# ~ Bank address defini l'offset sur laquel les differentes bank sont situe sur la disquette
hexAddr = {}
hexAddr['bank1'] = 0x04000
hexAddr['bank2'] = 0x16206
hexAddr['bank3'] = 0x28206
hexAddr['bank4'] = 0x3A000
hexAddr['bank4P'] = 0x39000
# ~ package to magasin en Stand By pour l'instant
pack2Mag = {}



# ~ We defined the dictionary pack2Mag with keys and the Value 
# ~ the value is the LAB
# ~ the second value is the DOT
# ~ the third value is Center Dx of component
# ~ the fourth value is Center Dy of component
# ~ the fifth value is Rang by Input
# ~ Unite Machine =0.0508mm


pack2Mag = {}
#pack2Mag['3,17/1,2'] = 0
pack2Mag['SO08'] = 1  # longueur 5,1     Largeur 2,5
pack2Mag['SO12'] = 2
pack2Mag['SO14'] = 3
pack2Mag['SO16'] = 4
pack2Mag['SO20'] = 5
pack2Mag['SO24'] = 6
pack2Mag['SO28'] = 7
pack2Mag['SOT23'] = 8
pack2Mag['SOT89'] = 9
pack2Mag['SOT143'] = 10
pack2Mag['SOT194'] = 11
pack2Mag['SOT223'] = 12
pack2Mag['SOD80'] = 13
pack2Mag['SOD87'] = 14
pack2Mag['0402'] = 15
pack2Mag['0603'] = 16
pack2Mag['0805'] = 17
pack2Mag['1206'] = 18
pack2Mag['1210'] = 19
pack2Mag['1812'] = 20
pack2Mag['2220'] = 21
pack2Mag['R3216'] = 22
    
            
           
dictMag = {}           
#dictMag['3,17/1,2'] = 0 
dictMag['SO08'] = 1  # longueur 5,1     Largeur 2,5
dictMag['SO12'] = 2
dictMag['SO14'] = 3
dictMag['SO16'] = 4
dictMag['SO20'] = 5
dictMag['SO24'] = 6
dictMag['SO28'] = 7
dictMag['SOT23'] = 8
dictMag['SOT89'] = 9
dictMag['SOT143'] = 10
dictMag['SOT194'] = 11
dictMag['SOT223'] = 12
dictMag['SOD80'] = 13
dictMag['SOD87'] = 14
dictMag['0402'] = 15
dictMag['0603'] = 16
dictMag['0805'] = 17
dictMag['1206'] = 18
dictMag['1210'] = 19
dictMag['1812'] = 20
dictMag['2220'] = 21
dictMag['R3216'] = 22
               
           
           
           
           
           

# 3eme et 4eme colonne sont :
# Coordonnee centre composant Machine : ((longueur /0,0508)/2)

# ~ We defined the dictionary Lab with keys and 4 Values 
# ~ the value is the MT
# ~ the second value is the LAB
# ~ the third value is Center Dx of component
# ~ the fourth value is Center Dy of component

# ~ Unite Machine =0.0508mm




Lab = {}

Lab = {
        '1':  [0, 2, 157  , 1793],
        '2':  [0, 2, 157   , 2105],
        '3':  [0, 2, 157  , 2418],
        '4':  [0, 2, 157   , 2733],
        '5':  [0, 2, 157  , 3048],
        '6':  [0, 2, 157  , 3362],
        '7':  [0, 2, 157  , 3676],
        '8':  [0, 2, 157  , 3992],
        '9':  [0, 2, 157  , 4305],
        '10': [0, 2, 157 , 4620],
        '11': [0, 2, 157 , 4969],
        '12': [0, 2, 157 , 5362],
        '13': [0, 2, 157 , 5804],
        '14': [0, 2, 157 , 6278],
        '21': [0, 2, 7700, 5569],
        '22': [0, 2, 7700 , 5253],
        '23': [0, 2, 7700  , 4940],
        '24': [0, 2, 7700 , 4625],
        '25': [0, 2, 7700 , 4311],
        '26': [0, 2, 7700 , 4005],
        '27': [0, 2, 7700  , 3686],
        '28': [0, 2, 7700 , 3369],
        '29': [0, 2, 7698 , 3055],
        '30': [0, 2, 7700 , 2737],
        '31': [0, 2, 7690 , 2480],
        '32': [0, 2, 7690 , 2087],
        '33': [0, 2, 7690 , 1652],
        '34': [0, 2, 7690 , 1190],
        '41': [0, 2, 366 , 6855]
      } 
       
#Tampon is fixed all magasin with there Mag address
Tampon =[[0, 0, 157  , 1793],[0, 0, 157   , 2105],[0, 0, 157  , 2418],
         [0, 0, 157   , 2733],[0, 0, 157  , 3048],[0, 0, 157  , 3362],
         [0, 0, 157  , 3676],[0, 0, 157  , 3992],[0, 0, 157  , 4305],
         [0, 0, 157 , 4620],[0, 0, 157 , 4969],[0, 0, 157 , 5362],
         [0, 0, 157 , 5804],[0, 0, 157 , 6278],[0, 0, 7700, 5569],
         [0, 0, 7700 , 5253],[0, 0, 7700  , 4940],[0, 0, 7700 , 4625],
         [0, 0, 7700 , 4311],[0, 0, 7700 , 4005],[0, 0, 7700  , 3686],
         [0, 0, 7700 , 3369],[0, 0, 7698 , 3055],[0, 0, 7700 , 2737],
         [0, 0, 7690 , 2480],[0, 0, 7690 , 2087],[0, 0, 7690 , 1652],
         [0, 0, 7690 , 1190],[0, 0, 366 , 6855]]    
       
 
#~ =====================================================================
#~ ====================CONVERSION TO HEXADECIMAL ==================
#~ ================= into Little Endian ===========================


def intToHex(i):
    ret = []
    ret.append(format("%02X" % (int(i) & 0x00ff)))
    ret.append(format("%02X" % (int((int(i) / 0xff)) & 0xff)))
    return ret

def hexToInt(lbx, hbx):
    lb = int(ord(lbx))
    hb = int(ord(hbx))
    return [lb + hb * 256, lb, hb]

#~ =====================================================================
import  codecs
def writeToFloppy(t):
    for i in range(0, len(t)):
        h = intToHex(t[i])
        #f.write( h[0].decode('hex'))            # the function don't work on Python 3.4
        #f.write( h[1].decode('hex'))
        decode_hex = codecs.decode(h[0], "hex")  # convert a string into hexa
        f.write(decode_hex)  # write to an floppy 
       
        decode_hex1 = codecs.decode(h[1], "hex")
        f.write(decode_hex1)
        
#~======================================================================
#~ ==================  ECRITURE PARTIE PRECIDOT  =======================

def pushDots(data):
    # ~ Write to floppy  
    # ~ La methode seek () definit la position actuelle du fichier a l'offset
    # ~ en ecriture sur la bank recuperer 
    bank = 'bank1'
    
    f.seek(hexAddr[bank], ABSOLUTE)  # fileObject.seek (offset ,[ou])
    
 # ~ ERREUR ============================================ open disk en binaire rb+ 
                                                        # pour rectifier l'erreur
    f.seek(0x208 , RELATIVE)  # 1ere Etape 
                                              # offset : par exemple hexAddr['bank1'] = 0x04000
    for i in range(0 , loops):  # ou : 0 c'est a dire en partant du debut 
        writeToFloppy([0, 0, 0, 0])  # 2eme Etape
        writeToFloppy([0, 10, 0, 0])  # offset : par exemple hexAddr['bank1'] = 0x208
                                              # ou : 1
        writeToFloppy([0, 1, loops, 0])  # initialisation [0,0,0,0]
    for n in range(0, len(data)):  # Controle des points de reference [0,10,0,0]
                                              # regarde si la boucle est repeter [0,1,loops,0]
                                              # on parcour de l'index 0 jusqu'a la fin 
                                              # Inverse l'axe Y 
        data[n][3] = yaxisdir + data[n][3]  # on rajout un "-" au string Dy qui se situ
                                              # a la 3eme colonne de data
        writeToFloppy(data[n])                
                                              # on ecrit les donnees
    writeToFloppy([0, 2, 0, 0])  # on fini la boucle par [0,2,0,0]
    
    # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x32, RELATIVE)
    writeToFloppy([len(data) + addLines, len(data) + addLines])
    print ("Finish Points !! ")
    return data
#~ =================================================================================
#~ =================== DOT ========================

def Dot(Depot):
    
    print("Start of depot")
    if m == pack2Mag['SO08']:
        Depot = 148
    elif m == pack2Mag['SO12']:
        Depot = 200
    elif m == pack2Mag['SO14']:
        Depot = 200    
    elif m == pack2Mag['SO16']:
        Depot = 200
    elif m == pack2Mag['SO20']:
        Depot = 200
    elif m == pack2Mag['SO24']:
        Depot = 200
        
    elif m == pack2Mag['SO28']:
        Depot = 200
    elif m == pack2Mag['SOT23']:
        Depot = 200
    elif m == pack2Mag['SOT89']:
        Depot = 200
    elif m == pack2Mag['SOT143']:
        Depot = 200
    elif m == pack2Mag['SOT194']:
        Depot = 200
    elif m == pack2Mag['SOT223']:
        Depot = 200
    elif m == pack2Mag['SOD80']:
        Depot = 200
    elif m == pack2Mag['SOD87']:
        Depot = 200
    elif m == pack2Mag['0402']:
        Depot = 200
    elif m == pack2Mag['0603']:
        Depot = 200
    elif m == pack2Mag['0805']:
        Depot = 200
    elif m == pack2Mag['1206']:
        Depot = 400
    elif m == pack2Mag['1210']:
        Depot = 400
    elif m == pack2Mag['1812']:
        Depot = 200
    elif m == pack2Mag['2220']:
        Depot = 200 
    elif m == pack2Mag['R3216']:
        Depot = 400
    else:
        Depot = 400
    return Depot


#~ ===============================================================
#~ ================= PARTIE NOVAR : Placement du Composant ========
def pushComp(data, NewMag):
    print ("start pushComp()")
                                       # fileObject.seek (offset ,[ou])
    bank = 'bank4'    
    # print(bank)                       # 1ere Etape
    f.seek(hexAddr[bank], ABSOLUTE)  # offset : example hexAddr['bank1'] = 0x04000
    f.seek(0x208, RELATIVE) 
                                        # where : 0 
    for i in range(0, loops):  # 2eme Etape
        writeToFloppy([0, 0, 0, 0])  # offset : hexAddr['bank1'] = 0x208
        print ("start to write component")  # where : 1  
        writeToFloppy([0, 10, 0, 0])  # writting  Control to references of point.
        writeToFloppy([0, 1, loops, 0])  # writting one loop 
      
    for k, v in data.items():  # k is key of componant 
                                    # v is dx et dy
            v[3] = yaxisdir + v[3]  # ~ Inverse Y axis if needed
                                        # look for data for saving 
            
            writeToFloppy(v)
            
    writeToFloppy([0, 2, 0, 0])  # Writting  End of Programme
        # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x32, RELATIVE)  # write to data
    writeToFloppy([len(data) + addLines, len(data) + addLines])  # format d'ecriture
    print ("finish of writting components")  # finish to write
    
#~ =========================================================================

# ~ Pretty Print Construct PrettyPrinter objects explicitly 
# ~ if you need to adjust the width constraint.
pp = pprint.PrettyPrinter(indent=4)

# ~ Constants
ABSOLUTE = 0  # ~le positionnement de fichier absolu prend la valeur 0
RELATIVE = 1  # le positionnement de fichier~par rapport a la situation actuelle 
                # ~ on prendra la valeur 1
 
#~=================================================================================== 
#~ ==========================warehouse===============================================        
        # first  NewMag  could enter a warehouse address  for each component :")
        # secondly searchLab() detects the Lab key  which equals NewMag and inserts the dictMag value in the
        # dictionary (Lab)
        # Lab is indentical to the position of the section 
#~ ===================================================================================        
          
def warehouse (comp,composants):
        
        
           print("Choose an address for : " + comp)
           NewMag = input('Entrer an adress of Section\'s Mag for:')
           for k in composants:
               if NewMag == '1' or NewMag == '2' or NewMag == '3' or NewMag == '4' or NewMag == '5' or NewMag == '6' or NewMag == '7'or NewMag == '8' or NewMag == '9' or NewMag == '10' or NewMag == '11' or NewMag == '12' or NewMag == '13' or NewMag == '14' or NewMag == '21' or NewMag == '22' or NewMag == '23' or NewMag == '24' or NewMag == '25' or NewMag == '26' or NewMag == '27'or NewMag == '28' or NewMag == '29' or NewMag == '30'or NewMag == '31' or NewMag == '32' or NewMag == '33' or NewMag == '34' or NewMag == '41' or NewMag == '42' or NewMag == '43' or NewMag == '44' or NewMag == '45' or NewMag == '46' :
                  pack2Mag[k] = NewMag
                  searchLab(Lab, NewMag, dictMag, composants,Tampon) 
               #print("Avant la fonction searchLab " + NewMag)
               elif NewMag == '15' or NewMag == '16' or NewMag == '17' or NewMag == '18' or NewMag == '19' or NewMag == '20' or NewMag == '35'or NewMag == '36' or NewMag == '37' or NewMag == '38'or NewMag == '39' or NewMag == '40': 
                    print("impossible de rentrer ce magasin")
                    warehouse (composants,comp)
           return NewMag
 #~============================================================================== 
#~ ==========================LAB===============================================        


def searchLab(Lab, NewMag, dictMag, comp,Tampon): 
  

   
   keys = tuple(Lab.keys())
   dictMagK = tuple(dictMag.keys())
   dictMagI = tuple(dictMag.items())
   
   for o in keys:
       if o == NewMag: 
               
               for i in dictMagK:
                   
                   if comp[0] == i:
                       
                       for g in dictMag.items():
                           if i == g[0]:
                               
                               #print("the Lab\'s selection is " + str(g[1]))
                               
                               val = str(g[1])
                               Lab[o][1] = int(val)
                               #print(str(val))
                               #print("you select :" + str(Lab[o]) + " for the section")
                               #print("et vous placer lab :" + str(val))
                               #print(Lab[o])
                               #print("before Lab")
                               
                               #Tampon.append(Lab[o])
                               #print(Tampon)
                               
                               print("after Lab")
                               
   return Lab, NewMag, dictMag, comp ,Tampon           
              
def pushLab(Tampon):
    print ("start pushLab()")
                                        # fileObject.seek (offset ,[ou])
    bank = 'bank4P'    
                         # 1ere Etape
    f.seek(hexAddr[bank], ABSOLUTE)  # offset : example hexAddr['bank1'] = 0x04000
    f.seek(0x608, RELATIVE) 
                                        # where : 0 
    for v in Tampon:  # k is key of componant 
                                           # v is dx et dy
            writeToFloppy(v)
            
            
            
            
        # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0xFFF, RELATIVE)  # write to Lab
    writeToFloppy([len(Tampon) + addLines, len(Tampon) + addLines])  # format d'ecriture
    print ("finish of writting warehouse")  # finish to write
#~ =========================================================================    
     
     
     
     
     
     
     
   
   
   
   
       
       
           
           
       
                
#~ ==========================================================================
#~ ============================ SUPPORT DISQUETTE ===========================
# ~ Floppy dev (la fonction open permetta l'ecriture ou la lecture de la disquette 
# ~ r+ autorise l'ecriture et la lecture
# ~ b est le mode binaire

# ~ We can try to open ant writting on a floppy disk
# ~ with r+     authorize to read and write on a floppy
# ~ with b      authorize to translate on binary
#~============================================================================
try: 
    print ('it\'s possible to writting data on a floppy disk')       
    f = open(disk, 'rb+')         
    
except IOError:

                print ('impossible to writting data')
#~ =========================================================================
#~ ==================== FORMAT pour EAGLE ==================================
#~ ==================== FORMAT FOR EAGLE ===================================

# ~ Eagle RegExp extraction des donnee suivant une structure 
# ~ pour les composant : ^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$
# ~ pour les point  : ^-Pin--X-(.+)-Y-(.*)$
# ~ LINES sont une copie de la chaine de caractere de line 
# ~ du fichier source extrai de Eagle sans les espaces blanc

# ~ whith the help of The software Eagle we could be extract the data 
# ~ with this stucture
# ~ for components : ^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$
# ~ for points : ^-Pin--X-(.+)-Y-(.*)$
# ~LINES are a copy of String line without space

#~==========================================================================

p = re.compile('^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$')
p2 = re.compile('^-Pin--X-(.+)-Y-(.*)$')



lines = [line.strip() for line in open(source)]

composants = {}
pins = []

# ~ Read Lines
for line in lines:
    line = line.rstrip()
    
    if "-composant-" in line:
        m = p.match(line)
       
        if m:
            comp = m.group(1)
           
            composants[comp] = list(m.group(2, 5, 3, 4))
            warehouse (comp,composants[comp])
            
            
            if (composants[comp][0] in pack2Mag.keys()):
                composants[comp][0] = pack2Mag[composants[comp][0]]
               
            else:
                print ("no pack " + composants[comp][0] + " in bank, remove item " + comp)
                
                
                del(composants[comp])
        else:
            print ("Ignored line: " + line)
             
# ~ On rajout la valeur du Depot de colle a la ligne de compilation
# ~ '^-Pin--X-(.+)-Y-(.*)$' sur la colonne 1 
# ~ ainsi le temps de depot sera en fonction du composant
            
    
   
            
    if "-Pin-" in line:
       
        m = p2.match(line)
             
        if m:
            pins.append(list((1, Dot(Depot)) + m.group(1, 2)))
        else:
            print ("Ignored line: " + line)
 
   
 
#~===========================================================================
# ~ Write to Floppy : for Precidot, data will be recorded on bank1 and the coordinates 
# ~ of  points will be defined with
# ~ call to function pushDots(pins)
# ~For Novar we will used bank4 and 
# ~ for allocation of components call to function pushComp(data.item()))
# we wil keep bank 2 and 3 for back-up 


# ~ Pour la precidot : l'enregistement se fera sur 
# ~ la banque 1 et l'on definira la position des coordonees des points 
# ~ (appel de fonction pushDots(pins))
# ~ Pour la Novar on utilisera donc la banque 4 et pour le placement des
# ~ composants (appel de la fonction pushComp(data.item()))
# ~ on gardera la banque 2 et 3 pour une fonction sauvegarde "Ulterieure"
#~ ==============================================================================
#~ ============================= ECRITURE SUR DISQUETTE =========================
#~ ============================= WRITTING ON FLOPPY DISK ========================
def ecriture_disquette(): 
       
    bank = 'bank1'
    print("before pushDots(pins)")
    pushDots(pins)
    print("after pushDots(pins)") 
      
    bank = 'bank4'
    print("change of bank")
    pp.pprint(composants)  # defined indentation of components
    print("after pp.pprint(components)")
    pushComp(composants,NewMag)
    print("before pushLab(Tampon)")
    bank = 'bank4P' 
    pushLab(Tampon)
    print("after pushLab(Tampon)") 
    return bank
    
#~ =========================================================================   
#~ ============================ INTRODUCTION ===============================    

# ~ definition de la fonction Introduction
# ~ Importer une petite interface avec la date et l'heure
# ~ Appel de la fonction ecriture_disquette()

# ~definition of function introduction
# ~ Imports interface with date and hours
# ~ call to the function ectiture_disquette()
def introduction():
    print ('***********************************')
    print ('***     Precidot30 & Novar33    ***')
    print ('***********************************')
    now = time.strftime("%A %d %B %Y %H:%M:%S")
    print ('**' + now + '*')
    print ('***********************************')
    ecriture_disquette()
    
introduction()  # Appel de la fonction

#~ ==========================================================================
          
# ~ Print Pins

# ~ Read the floppy to check the result
# ~ f.seek(hexAddr[bank],ABSOLUTE)
# ~ f.seek(0x208,RELATIVE)
# ~ for pinid in range(0,len(pins)+addLines):
    # ~ sys.stdout.write("0x%04X = " % (pinid*4))
    # ~ for i in range(0,4):
        # ~ val = hexToInt(f.read(1),f.read(1))
        # ~ sys.stdout.write(" - %6d [%02X,%02X]" % ( val[0], val[1], val[2]))
    # ~ print ""
#~ ============================== FERMETURE DISQUETTE =======================       
#~ ============================== Close to Floppy Disk ======================

f.close()


#~ ===========================================================================


