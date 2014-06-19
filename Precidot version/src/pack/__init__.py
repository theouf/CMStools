#!/usr/bin/python3.4
# coding=utf-8
'''
Created on 19 juin. 2014

@author: L'Henoret Erwan
version Python 2.7 and 3.4

careful! some function must be modified which Python 2.7 or 3.4
for example : the input function


Attention certaine fonction doit être modifier suivant le Python
notament la fonction intput
j'ai prévu à cette effet la fonction pour les deux sorte de Python
enlever le # pour activer la fonction devant celui qui vous convient
et désactivé l'autre

'''
#~ ========================== IMPORT =================================
import datetime, time
import pprint
import re
import sys
import struct
#~======================================================================
#~================================ VARIABLES =========================

# ~ Source file for testing
source = 'E:\Iut\Rapport de Stage/testeur_UM.pnp' # Windows
#~source = '../../../testeur_UM.pnp' # Linux

#~ ================================================================

# ~ Biscotte is the virtual support for the test
# ~ disk ='/dev/fd0' is the way of floppy disk

# ~ biscotte est le nom donne
# ~ afin de permettre les essais ce support est virtuel
# ~ disk ='/dev/fd0' permet de cible la disquette

#~disk = '../../../biscotte'
disk = 'biscotte'
# disk ='/dev/fd0'
#~====================================================================
bank = 'bank4'
# ~ Loops repeat X times in the same loop
# ~ Loops premet quand a lui de repeter X fois la meme boucle
loops = 1

# ~ time of point to drop
submission = 0
box=[]
NewMag = ''

# include the rotation
Rot=[]



# ~ Y axis direction
yaxisdir = '-'

#~ DataTools is for change Tool during the program
#~ DataToolsTake is temporary variable for taking the tool selected
#~ DataToolsDrop is temporary variable for drop the tool
DataTools = []

DataToolsTake =[0,12,0,0]
DataToolsDrop =[0,12,0,1]

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


# ~ We defined the dictionary pack2Mag with keys and the Value
# ~ the value is the LAB
# ~ the second value is the DOT
# ~ the third value is Center Dx of component
# ~ the fourth value is Center Dy of component
# ~ the fifth value is Rang by Input
# ~ Unite Machine =0.0508mm

pack2Mag = {}
#pack2Mag['3,17/1,2'] = 0
pack2Mag['SO08'] = 1 
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
dictMag['SO08'] = 1 
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
               
           
           
pack2Depot = {}
pack2Depot['3,17/1,2'] = 0
pack2Depot['SO08'] = 148
pack2Depot['SO12'] = 200
pack2Depot['SO14'] = 200
pack2Depot['SO16'] = 200
pack2Depot['SO20'] = 200
pack2Depot['SO24'] = 200
pack2Depot['SO28'] = 200
pack2Depot['SOT23'] = 223
pack2Depot['SOT89'] = 200
pack2Depot['SOT143'] = 200
pack2Depot['SOT194'] = 200
pack2Depot['SOT223'] = 200
pack2Depot['SOD80'] = 200
pack2Depot['SOD87'] = 200
pack2Depot['0402'] = 200
pack2Depot['0603'] = 200
pack2Depot['0805'] = 200
pack2Depot['1206'] = 400
pack2Depot['1210'] = 200
pack2Depot['1812'] = 200
pack2Depot['2220'] = 200
pack2Depot['R3216'] = 400
           
           



# ~ We defined the dictionary Lab with keys and 4 Values
# ~ the value is the MT
# ~ the second value is the LAB
# ~ the third value is Center Dx of component
# ~ the fourth value is Center Dy of component

# ~ Unite Machine =0.0508mm
# 3 and  4 row are :
# Coordinate centrer of component Machine : ((longueur /0,0508)/2)



Lab = {}

Lab = {
        '1': [0, 2, 157 , 1793],
        '2': [0, 2, 157 , 2105],
        '3': [0, 2, 157 , 2418],
        '4': [0, 2, 157 , 2733],
        '5': [0, 2, 157 , 3048],
        '6': [0, 2, 157 , 3362],
        '7': [0, 2, 157 , 3676],
        '8': [0, 2, 157 , 3992],
        '9': [0, 2, 157 , 4305],
        '10': [0, 2, 157 , 4620],
        '11': [0, 2, 157 , 4969],
        '12': [0, 2, 157 , 5362],
        '13': [0, 2, 157 , 5804],
        '14': [0, 2, 157 , 6278],
        '21': [0, 2, 7700, 5569],
        '22': [0, 2, 7700 , 5253],
        '23': [0, 2, 7700 , 4940],
        '24': [0, 2, 7700 , 4625],
        '25': [0, 2, 7700 , 4311],
        '26': [0, 2, 7700 , 4005],
        '27': [0, 2, 7700 , 3686],
        '28': [0, 2, 7700 , 3369],
        '29': [0, 2, 7698 , 3055],
        '30': [0, 2, 7700 , 2737],
        '31': [0, 2, 7690 , 2480],
        '32': [0, 2, 7690 , 2087],
        '33': [0, 2, 7690 , 1652],
        '34': [0, 2, 7690 , 1190],
        '41': [0, 2, 366 , 6855]
      }
       
#Buffer is fixed all magasin with there Mag address
Buffer =[[0, 0, 153 , 1725],[0, 0, 153 , 2034],[0, 0, 153 , 2357],
         [0, 0, 153 , 2671],[0, 0, 153 , 2986],[0, 0, 153 , 3299],
         [0, 0, 153 , 3614],[0, 0, 153 , 3929],[0, 0, 153 , 4242],
         [0, 0, 153 , 4557],[0, 0, 153 , 4969],[0, 0, 153 , 5362],
         [0, 0, 153 , 5804],[0, 0, 153 , 6278],[0, 0, 7619, 5572],
         [0, 0, 7619 , 5253],[0, 0, 7619 , 4940],[0, 0, 7619 , 4625],
         [0, 0, 7619 , 4311],[0, 0, 7619 , 4005],[0, 0, 7619 , 3686],
         [0, 0, 7619 , 3369],[0, 0, 7698 , 3055],[0, 0, 7619 , 2737],
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
import codecs
def writeToFloppy(t):
    for i in range(0, len(t)):
        h = intToHex(t[i])
        #f.write( h[0].decode('hex')) # the function don't work on Python 3.4
        #f.write( h[1].decode('hex'))
        decode_hex = codecs.decode(h[0], "hex") 
        f.write(decode_hex) 
       
        decode_hex1 = codecs.decode(h[1], "hex")
        f.write(decode_hex1)
        
#~======================================================================
#~ ================== PART PRECIDOT =======================
# ~ Write to floppy
    # ~ the methode seek () defined the actual position of file (offset)
    # ~ f is the disk
    # ~ writting on bank selected

#~ [0, 0, 0, 0] for init
#~ [0, 10, 0, 0] for control the point of reference
#~ [0, 1, loops, 0] repeat by loop

#~ data[n][3] = yaxisdir + data[n][3] datas are reverse on Dy
#~================================================================
def pushDots(data):
    
    bank = 'bank1'
    
    f.seek(hexAddr[bank], ABSOLUTE) 
    f.seek(0x208 , RELATIVE)     
    for i in range(0 , loops): 
        writeToFloppy([0, 0, 0, 0]) 
        writeToFloppy([0, 10, 0, 0]) 
        writeToFloppy([0, 1, loops, 0]) 
    for n in range(0, len(data)): 
         data[n][3] = yaxisdir + data[n][3] 
         writeToFloppy(data[n])
                                              
    writeToFloppy([0, 2, 0, 0]) 
    
    # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x32, RELATIVE)
    writeToFloppy([len(data) + addLines, len(data) + addLines])
    print ("Finish Points !! ")
    return data
#~ =================================================================================
#~ =================== DOT ===========================================
#~ the function dot() give the value of DOT for each componant
def Dot(submission,box):
    
    if box in pack2Depot:
        submission=pack2Depot[box]
        return submission
    else:
        print('Unknown package')
        return int(input('Enter the Dot for '+ box) or '400')
        #return int(raw_input('Enter the Dot for '+ box) or '400')
#~==============================================================================
#~ ==========================Rotation===============================================
#~the user must enter the rotation for each component
#~ the rotation write in composants [1]

#~====================================================================

def Rotation(comp,composants,Rot):
    #Rot = int(raw_input('Enter a Rotation for component '+comp) or 0)
    Rot = int(input('Enter a Rotation for component '+comp+ ' : ') or 0)
    composants[1]= Rot
       
    return Rot

#~=====================================================================
#~ ===============================================================
#~ ================= PART NOVAR : Allocation of Components ========

# PushComp determines the change of Tools for each components if we need
#~ ============================Tools ===================================

# We chose the change of tools during the program
# first the user specifed DataToolsTake and modified the current Tool 
#for to take an other coponent also you drop off the tool(DataToolsDrop)
# secondly we chose the new tool (chose the number 1,2,3) and DataToolsTake
# modified for taken the new tool.
##~ [0, 1, loop, 0]) #start the loop with the new tool
#~ [0, 2, 0, 0]) #end loop
#~ ===================================================================
 
# and we execute the same thing from PushDot ( found the position of componant
# and convert the Datas to Hexa with the function writeToFloppy()
# f.seek() go to hexAddr['bank4'] = 0x3A000
# secondly go to 3A208
# finally go to 32000

#~ [0, 2, 0, 0]) #end loop
#v[3] = yaxisdir + v[3] # ~ Inverse Y axis if needed
#~ ===============================================================


def pushComp(data, NewMag,DataTools):
    print ("start pushComp()")
                                       
    bank = 'bank4'

    
    f.seek(hexAddr[bank], ABSOLUTE) 
    f.seek(0x208, RELATIVE)
                                       
    for i in range(0, loops): 
        writeToFloppy([0, 0, 0, 0]) 
        print ("start to write component") 
        writeToFloppy([0, 10, 0, 0]) 
        tools=int(input("enter your tool to start your program "))
        DataToolsTake[2]=tools
        DataToolsDrop[2]=tools
        print(DataToolsTake)
        writeToFloppy(DataToolsTake)
        writeToFloppy([0, 1, loops, 0]) 
        
        chang=input("is change tool during this program ? [y/N] : ") or 'N'
        if chang =='y':
            
            for k, v in data.items(): 
                print(v)                    
                #response= raw_input("Change tool for "+str(k)+" ? [y/N]: ") or 'N'
                response= input("Change tool for "+str(k)+" ? [y/N]: ") or 'N'
                if response == 'y':
                    
                    writeToFloppy([0, 2, 0, 0]) 
                    DataToolsDrop[2]=tools
                    writeToFloppy(DataToolsDrop)
                                      
                    print("the tool is : "+str(DataToolsTake[2]))
                    print("change tool for "+str(k)+": ")
                    #numero=raw_input("what is the number?")
                    tools=int(input("chose the number 2,3,4"))
                    DataToolsTake[2]=tools
                    writeToFloppy(DataToolsTake) 
                    writeToFloppy([0,1,loops,0]) 
                    v[3] = yaxisdir + v[3] 
                    writeToFloppy(v) 
                    print(v) 
                else:    
                    v[3] = yaxisdir + v[3] 
                    writeToFloppy(v) 
                    print(v)                                 
             
    writeToFloppy([0, 2, 0, 0]) 
        # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x32, RELATIVE) 
    writeToFloppy([len(data) + addLines, len(data) + addLines]) 
    print ("finish of writting components") 
    print (data)
#~ =========================================================================

# ~ Pretty Print Construct PrettyPrinter objects explicitly
# ~ if you need to adjust the width constraint.
pp = pprint.PrettyPrinter(indent=4)

# ~ Constants
ABSOLUTE = 0 
RELATIVE = 1 
 
    
#~===================================================================================
#~ ==========================warehouse===============================================
        # first NewMag could enter a warehouse address for each component :")
        # secondly searchLab() detects the Lab key which equals NewMag and inserts the dictMag value in the
        # dictionary (Lab)
        # Lab is indentical to the position of the section
#~ ===================================================================================
          
def warehouse (comp,composants):
    print("Choose an address for : " + comp)
    #NewMag = int(raw_input('Entrer an adress of Section\'s Mag for:') or 0)
    NewMag = int(input('Entrer an adress of Section\'s Mag for:') or 0)
    for k in composants:
        if NewMag in range(1,14) or NewMag in range(21,34) or NewMag in range(41,46):
            pack2Mag[k] = NewMag
            searchLab(Lab, NewMag, dictMag, composants,Buffer)
        elif NewMag in range(15,20) or NewMag in range(35,40):
            print("impossible de rentrer ce magasin")
            warehouse (composants,comp)
    return NewMag

#~ ==============================================================================
#~ ==========================LAB===============================================


def searchLab(Lab, NewMag, dictMag, comp,Buffer):
  
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
                               
                               #Buffer.append(Lab[o])
                               #print(Buffer)
    
                        
                               
   return Lab, NewMag, dictMag, comp ,Buffer
#~ ===================================================================================
#~ ==================================== pushLab ======================================
#~ pushLab is the function who can take all position of the section and give the Lab of component
#~ this is an option  
#~f.seek() go in hexAddr['bank4P] = 39000
#~secondly  f.seek() go in hexAddress = 3960C
#~finally f.seek() go in hexAddress = 3977F
#~ ===================================================================================

def pushLab(Buffer):
    print ("start pushLab()")
                                        
    bank = 'bank4P'
                                     
    f.seek(hexAddr[bank], ABSOLUTE) 
    f.seek(0x60C, RELATIVE)
                                     
    for n in range(0,len(Buffer)): 
            
            writeToFloppy(Buffer[n])
                
        # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x77F, RELATIVE) 
    writeToFloppy([len(Buffer) + addLines, len(Buffer) + addLines]) 
    print ("finish of writting warehouse") 
#~ =========================================================================
#~ ==========================================================================
#~ ============================ SUPPORT DISQUETTE ===========================
# ~ Floppy dev (la fonction open permetta l'ecriture ou la lecture de la disquette
# ~ r+ autorise l'ecriture et la lecture
# ~ b est le mode binaire

# ~ We can try to open ant writting on a floppy disk
# ~ with r+ authorize to read and write on a floppy
# ~ with b authorize to translate on binary
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
# ~ pour les point : ^-Pin--X-(.+)-Y-(.*)$
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
            Rotation(comp,composants[comp],Rot)
            box=m.group(2)
            warehouse (comp,composants[comp])
           
            
            if (composants[comp][0] in pack2Mag.keys()):
                composants[comp][0] = pack2Mag[composants[comp][0]]
               
            else:
                print ("no pack " + composants[comp][0] + " in bank, remove item " + comp)
                
                
                del(composants[comp])
        else:
            print ("Ignored line: " + line)
             

            
    if "-Pin-" in line:
       
        m = p2.match(line)
    
        if m:
            pins.append(list((1,Dot(submission,box)) + m.group(1, 2)))
        else:
            print ("Ignored line: " + line)
 
   
 
#~===========================================================================
# ~ Write to Floppy : for Precidot, data will be recorded on bank1 and the coordinates
# ~ of points will be defined with
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
    pp.pprint(composants) # defined indentation of components
    print("after pp.pprint(components)")
   
    pushComp(composants,NewMag,DataTools)
    print("before pushLab(Buffer)")
    bank = 'bank4P'
    pushLab(Buffer)
    print("after pushLab(Buffer)")
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
    print ('*** Precidot30 & Novar33 ***')
    print ('***********************************')
    now = time.strftime("%A %d %B %Y %H:%M:%S")
    print ('**' + now + '*')
    print ('***********************************')
    ecriture_disquette()
    
introduction() # Appel de la fonction

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



