#!/usr/bin/python3.4
# coding=utf-8
'''
Created on 03 juillet. 2014

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

loops=1


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
CompByTools = []
tools=0
toolsimport=''
speedimport=''
DataToolsTake =[0,12,0,0]
DataToolsDrop =[0,12,0,1]
dico={}
nom=""
toolsMemory=0
speedMemory=0
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
 
LabInfo={}

LabInfo= {
         '3,17/1,2':{'Lab':'0','submission':0,'tool':0,'speed':[0,4,0,0]},
         'SO08':{'Lab':'1','submission':148,'tool':3,'speed':[0,5,0,0]},
         'SO12':{'Lab':'2','submission':148,'tool':3,'speed':[0,5,0,0]},
         'SO14':{'Lab':'3','submission':148,'tool':4,'speed':[0,5,0,0]},
         'SO16':{'Lab':'4','submission':148,'tool':4,'speed':[0,5,0,0]},
         'SO20':{'Lab':'5','submission':148,'tool':4,'speed':[0,5,0,0]},
         'SO24':{'Lab':'6','submission':148,'tool':4,'speed':[0,5,0,0]},
         'SO28':{'Lab':'7','submission':148,'tool':4,'speed':[0,5,0,0]},
         'SOT23':{'Lab':'8','submission':223,'tool':2,'speed':[0,4,0,0]},
         'SOT89':{'Lab':'9','submission':223,'tool':2,'speed':[0,4,0,0]},
         'SOT143':{'Lab':'10','submission':148,'tool':3,'speed':[0,4,0,0]},
         'SOT194':{'Lab':'11','submission':148,'tool':3,'speed':[0,4,0,0]},
         'SOT223':{'Lab':'12','submission':148,'tool':3,'speed':[0,4,0,0]},
         'SOD80':{'Lab':'13','submission':148,'tool':3,'speed':[0,4,0,0]},
         'SOD87':{'Lab':'14','submission':148,'tool':3,'speed':[0,4,0,0]},
         '0402':{'Lab':'15','submission':400,'tool':2,'speed':[0,4,0,0]},
         '0603':{'Lab':'16','submission':400,'tool':2,'speed':[0,4,0,0]},
         '0805':{'Lab':'17','submission':400,'tool':2,'speed':[0,4,0,0]},
         '1206':{'Lab':'18','submission':400,'tool':2,'speed':[0,4,0,0]},
         '1210':{'Lab':'19','submission':400,'tool':2,'speed':[0,4,0,0]},
         '1812':{'Lab':'20','submission':400,'tool':2,'speed':[0,4,0,0]},
         '2220':{'Lab':'21','submission':400,'tool':2,'speed':[0,4,0,0]},
         'R3216':{'Lab':'22','submission':400,'tool':2,'speed':[0,4,0,0]}
        }


# ~ We defined the dictionary Lab with keys and 4 Values
# ~ the value is the MT
# ~ the second value is the LAB
# ~ the third value is Center Dx of component
# ~ the fourth value is Center Dy of component

# ~ Unite Machine =0.0508mm
# 3 and 4 row are :
# Coordinate centrer of component Machine : ((longueur /0,0508)/2)


   
#Buffer is fixed all magasin with there Mag address
Buffer = {}



Buffer ={
         
        '0': [0,0,0,0],
        '1': [0, 0, 153 , 1725],
        '2': [0, 0, 153 , 2034],
        '3': [0, 0, 153 , 2357],
        '4': [0, 0, 153 , 2671],
        '5': [0, 0, 153 , 2986],
        '6': [0, 0, 153 , 3299],
        '7': [0, 0, 153 , 3614],
        '8': [0, 0, 153 , 3929],
        '9': [0, 0, 153 , 4242],
        '10': [0, 0, 153 , 4557],
        '11': [0, 0, 153 , 4969],
        '12': [0, 0, 153 , 5362],
        '13': [0, 0, 153 , 5804],
        '14': [0, 0, 153 , 6278], #14
        '15': [0, 0, 153 , 6278],
        '16': [0, 0, 153 , 6278],
        '17': [0, 0, 153 , 6278],
        '18': [0, 0, 153 , 6278],
        '19': [0, 0, 153 , 6278],
        '20': [0, 0, 7619, 5572],
        '21': [0, 0, 7619, 5572], #21
        '22': [0, 0, 7619 , 5253],
        '23': [0, 0, 7619 , 4940],
        '24': [0, 0, 7619 , 4625],
        '25': [0, 0, 7619 , 4311],
        '26': [0, 0, 7619 , 4005],
        '27': [0, 0, 7619 , 3686],
        '28': [0, 0, 7619 , 3369],
        '29': [0, 0, 7698 , 3055],
        '30': [0, 0, 7619 , 2737],
        '31': [0, 0, 7690 , 2480],
        '32': [0, 0, 7690 , 2087],
        '33': [0, 0, 7690 , 1652],
        '34': [0, 0, 7690 , 1190], #34
        '35': [0, 0, 7690 , 1190],
        '36': [0, 0, 7690 , 1190],
        '37': [0, 0, 7690 , 1190],
        '38': [0, 0, 7690 , 1190],
        '39': [0, 0, 7690 , 1190],
        '40': [0, 0, 7690 , 1190],
        '41': [0, 0, 366 , 6855] #41
      }
 
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
        decode_hex = codecs.decode(h[0], "hex")
        f.write(decode_hex)
        decode_hex1 = codecs.decode(h[1], "hex")
        f.write(decode_hex1)

#~ =================================================================================
#~ =================== DOT and Rotation===========================================
#~ the function dot() give the value of DOT for each componant
#~the user must enter the rotation for each component
#~ the rotation write in composants [1]
def Dot(submission,box):
    if box in LabInfo:
        submission=LabInfo[box]['submission']
        return submission
    else:
        print('Unknown package')
        return int(input('Enter the Dot for '+ box) or '400')
        #return int(raw_input('Enter the Dot for '+ box) or '400')

def Rotation(comp,composants,Rot):
    #Rot = int(raw_input('Enter a Rotation for component '+comp) or 0)
    Rot = int(input('Enter a Rotation for component '+comp+ ' : ') or 0)
    composants[1]= Rot
    return Rot

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
def pushDots(data,loops):
    bank = 'bank1'
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x208 , RELATIVE)
    for i in range(0 , 1):
    #for i in range(0 , loops):
        writeToFloppy([0, 0, 0, 0])
        writeToFloppy([0, 10, 0, 0])
        writeToFloppy([0, 1, loops, 0])
        print([0, 1, loops, 0])
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
            searchLab(NewMag, LabInfo, composants,Buffer)
        elif NewMag in range(15,20) or NewMag in range(35,40):
            print("impossible de rentrer ce magasin")
            warehouse (composants,comp)
    return NewMag

#~ ==============================================================================
#~ ==========================LAB===============================================


def searchLab(NewMag, LabInfo, comp,Buffer):
   
   keys = tuple(Buffer.keys())
   LabInfoK = tuple(LabInfo.keys())
   LabInfoI = tuple(LabInfo.items())
   for o in keys:
       if int(o) == NewMag:
          for i in LabInfoK:
              if comp[0] == i:
                val = LabInfo[i]['Lab']
                Buffer[o][1] = int(val)
                pushLab(Buffer,composants)
   return NewMag, LabInfo, comp ,Buffer
#~ ===================================================================================
#~ ==================================== pushLab ======================================
#~ pushLab is the function who can take all position of the section and give the Lab of component
#~ this is an option
#~f.seek() go in hexAddr['bank4P] = 39000
#~secondly f.seek() go in hexAddress = 3960C
#~finally f.seek() go in hexAddress = 3977F
#~ ===================================================================================

def pushLab(Buffer,composants):
    #print ("start pushLab()")
    bank = 'bank4P'
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x60C, RELATIVE)
    for k,v in Buffer.items():
        writeToFloppy(v)
    # ~ Nb lignes
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x77F, RELATIVE)
    writeToFloppy([len(Buffer) + addLines, len(Buffer) + addLines])
    #print ("finish of writting warehouse")
    

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


def pushComp(data, NewMag,Buffer,LabInfo,tools,composants,loops,CompByTools):
    print(loops)
    start=loops
    print(start)
    boucle=0
    print ("start pushComp()")
    bank = 'bank4'
   
    
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x208, RELATIVE)
    
    for i in range(0,1):
    #for i in range(0, loops):
        for n in range(0, start):
            writeToFloppy([0, 0, 0, 0])
            print([0, 0, 0, 0])
        
        writeToFloppy([0, 10, 0, 0])
        print([0, 10, 0, 0])
        
       
        print ("start to write component")
        
        #writeToFloppy([0, 10, 0, 0])
        
        chang=input("is change tool during this program ? [y/N] : ") or 'N'
        if chang =='y':
            

          
          for k,v in data.items():
              
                                   
              for r in Buffer.keys():
                    if str(v[0])!=r: pass
                    if str(v[0])==r: #find coordinate
                        for l,m in LabInfo.items():
                            if str(Buffer[r][1]) in m['Lab']:
                               Lab = m['Lab']
                               if str(Buffer[r][1])== Lab:
                                    tools=m['tool']
                                    speed=m['speed']
                                    
#===================================================================
              if tools==0:
                        
                        Read_Creating(k,dico)
                        for key,n in dico.items():
                                                
                                                if k==key:
                                                    print("trouvé")
                                                    toolsMemory=n[0]
                                                    print(toolsMemory)
                                                    speedMemory=n[1]
                                                    print(speedMemory)
                                                    n=toolsMemory
                                                    tools=toolsMemory
                                                    speed=[0,speedMemory,0,0]
                                                    print(n)
                                                    print(tools)
                                                    print(speed)
                                                    print(toolsMemory)
 
#=======================================================================
              if boucle==0:
                    n=tools
                    boucle=boucle+1
                    print("strat loop")
                    if n == tools:
                        
                        DataToolsDrop[2]=n
                        DataToolsTake[2]=n
                        writeToFloppy(DataToolsTake)
                        print(DataToolsTake)
                        writeToFloppy(speed)
                        print(speed)
                        writeToFloppy([0, 1, loops, 0])
                        print([0, 1, loops, 0])
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        ValAncien=tools
                        print(v)
                        
                        
                        
                        
                    else:
                                               
                        DataToolsDrop[2]=ValAncien
                        DataToolsTake[2]=tools
                        writeToFloppy(DataToolsTake)
                        print(DataToolsTake)
                        writeToFloppy([0, 1, loops, 0])
                        print([0, 1, loops, 0])
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        print(v)
                        n=tools
                        
              else:
                    
                    
                    if ValAncien == tools:
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        print(v)
                        
                    else:
                        
                        writeToFloppy([0, 2, 0, 0])
                        print('[0, 2, 0, 0]')
                        DataToolsDrop[2]=ValAncien
                        writeToFloppy(DataToolsDrop)
                        print(DataToolsDrop)
                        DataToolsDrop[2]=tools
                        DataToolsTake[2]=tools
                        n=tools
                        writeToFloppy(DataToolsTake)
                        print(DataToolsTake)
                        if DataToolsTake[2] != ValAncien:
                           writeToFloppy(speed)
                           print(speed)
                        writeToFloppy([0, 1, loops, 0])
                        print([0, 1, loops, 0])
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        print(v)
                        ValAncien=tools
                                
        else:
                        
                                #tools=raw_input("Enter tools for this programme")
                                tools=input("Enter tools for this programme")
                                DataToolsDrop[2]=tools
                                DataToolsTake[2]=tools
                                writeToFloppy(DataToolsTake)
                                writeToFloppy([0, 1, loops, 0])
                                for k,v in data.items():
                                    v[3] = yaxisdir + v[3]
                                    writeToFloppy(v)
                                writeToFloppy(DataToolsDrop)
                                
        # ~ Nb lignes
    writeToFloppy([0, 2, 0, 0])
    print('[0, 2, 0, 0]')
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x32, RELATIVE)
    writeToFloppy([len(data) + addLines, len(data) + addLines])
    print ("finish of writting components")
    return nbrLines(len(data)+addLines)

#~ =========================================================================
#~ Use this function when the value tool and speed aren't found
#~ the user enter himself these datas
def Read_Creating(k,dico):
    
    while 1 :
        nom=k
        #nom=input("Entrer the name box for"+k)
        if nom in dico:
            print("find")
            item=dico[nom]
            tools,speed=item[0],item[1]
            return k,dico,tools,speed
        else:
            print('Unknown package')
            toolsimport=int(input("Enter Tools for "+k+" :"))
            speedimport=int(input("Enter speed for "+k+" :"))
            boximport=input("Enter box for "+k+" :")
            dico[nom]=(toolsimport,speedimport,boximport)
                
        return dico[nom],k

def nbrLines(nbrLine):
       print(nbrLine) 
       bank='bank4'
       f.seek(hexAddr[bank], ABSOLUTE)
       f.seek(0x032, RELATIVE)
       print(nbrLine)
       nbrLines=nbrLine*2
       writeToFloppy(str(nbrLines))
       print(nbrLines)
       f.seek(hexAddr[bank], ABSOLUTE)
       f.seek(0x035, RELATIVE)








#~====================================================================



# ~ Pretty Print Construct PrettyPrinter objects explicitly
# ~ if you need to adjust the width constraint.
pp = pprint.PrettyPrinter(indent=4)

# ~ Constants
ABSOLUTE = 0
RELATIVE = 1
 

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
#~ ==================== FORMAT FOR EAGLE ===================================

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
 
#~ ===========================================================================
# ~ Write to Floppy : for Precidot, data will be recorded on bank1 and the coordinates
# ~ of points will be defined with
# ~ call to function pushDots(pins)
# ~For Novar we will used bank4 and
# ~ for allocation of components call to function pushComp(data.item()))
# we wil keep bank 2 and 3 for back-up

#~ ==============================================================================
#~ ============================= WRITTING ON FLOPPY DISK ========================
def ecriture_disquette():
       
    bank = 'bank1'
    print("before pushDots(pins)")
    Mod=input("is change loop during this program ? [y/N] : ") or 'N'
    if Mod =='y':
            loops= int(input("Enter the new loop : "))
    else:
            loops=1
    pushDots(pins,loops)
    print("after pushDots(pins)")
    bank = 'bank4P'
    #pushLab(Buffer,composants)
    print("after pushLab(Buffer)")
    print(Buffer)
    bank = 'bank4'
    print("change of bank")
    pp.pprint(composants) # defined indentation of components
    print("after pp.pprint(components)")
    pushComp(composants,NewMag,Buffer,LabInfo,tools,composants,loops,CompByTools)
    
    return bank
    
#~ =========================================================================
#~ ============================ INTRODUCTION ===============================
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

#~ ============================== Close to Floppy Disk ======================

f.close()

#~ ===========================================================================

