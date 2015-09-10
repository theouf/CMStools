#!/usr/bin/python
# coding=utf-8
'''


@authors: David,Erwan, Theo
version Python 2.7 and 3.4

This prog permits configure  Precidot and Novar according to 2 input files.
first one is created from eagle by a module "testeur_UM.pnp" and contains components and pins x & y coordonates
second one is not yet defined and will contains component location in the novar componentroom


'''

import datetime, time
import pprint
import re
import sys
import struct
import codecs

from CMS_Conf import *

#

#~ ==============================GRAPHIC====================================
#~ Imports interface with date and hours on function Welcome()
#~ When the Writting on Floppy disk is finish the function Finish() is called
def welcome():
    print ('****************************************************')
    print ('************* Precidot30 & Novar33 *****************')
    print ('****************************************************')
    now = time.strftime("%A %d %B %Y %H:%M:%S")
    print ('**********' + now + '        ***')
    print ('****************************************************')

def Finish():
    print('****************************************************')
    print('************* Precidot30 & Novar33 *****************')
    print('****************************************************')
    print("*****  Thank you for using this program     ********")
    print("*****   You can remove the Floppy Disk      ********")
    print("*****                                       ********")
    print("*****            FABLAB LANNION             ********")
    print("*****                                       ********")
    print('****************************************************')
    print('****************************************************')
    
    
#~ ================================================================
#~ ==================== CONVERSION TO HEXADECIMAL =================
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

def Dot(submission,box, dicoComp,comp,Buffer,NewMag):
   
    if box in LabInfo:
        submission=LabInfo[box]['submission']
        return submission
    
    elif box in dicoDot:
        
        submission= dicoDot[box]
        precision(dicoComp,comp,box)
        print(submission)
        return submission
    else:
                print('Unknown package')
                #submission=int(raw_input('Enter the Dot for '+ box+" : ") or '400')
                submission=int(input('Enter the Dot for '+ box+" : ") or '400')
                dicoDot[box]=(submission)
                precision(dicoComp,comp,box)
                return submission

def precision(dicoComp,comp,box):

         if comp in dicoComp:pass 
         else:
                print("*******************************************")
                print("*********************** HELP TOOLS ********")
                print("*** TOOL 2 for box||Diameter :1.03 mm   ***")
                print("*** TOOL 3 for box||Diameter :2.83 mm   ***")
                print("*** TOOL 4 for box||Diameter :5.34 mm   ***")
                print("*******************************************")
                print("*******************************************")
                #toolsimport=int(raw_input("Enter Tools for "+box+" :"))
                toolsimport=int(input("Enter Tools for "+box+" : "))
                if toolsimport not in  range(0,5):
                    print("the manipulation is False")
                    toolsimport=int(input("Enter Tools for "+box+" :"))
                
                
                print("*************************")
                print("***** HELP SPEED ********")
                print("*** FAST   ||    F    ***")
                print("*** SLOW   ||    S    ***")
                print("*************************")
                print("*************************")
                #choise=raw_input("CHOISE THE SPEED MOVING ? [S/F] : ") or 'S'
                choise=input("CHOISE THE SPEED MOVING ? [S/F] : ") or 'S'
                if choise =='S' :
                       speedimport = 5
                elif choise =='s' :
                       speedimport = 5       
                elif choise =='F' :
                        speedimport = 4
                elif choise =='f':
                        speedimport = 4
                    
                print([0,speedimport,0,0])                
                
                
                dicoComp[comp]=(toolsimport,speedimport,box)
                
                return dicoComp









        
def Rotation(comp,composants,Rot):
            
            RotCarte=int(composants[1])
            print("*****************************************************")
            print("***********      HELP ROTATION    *******************")
            print("*** ROT 0        ||Rotation :0°         ||   ^|   ***")
            print("*** ROT 90       ||Rotation :90°        ||   <=   ***")
            print("*** ROT 180      ||Rotation :180°       ||   =>   ***")
            print("*** ROT 270      ||Rotation :270°       ||   |    ***")
            print("*****************************************************")
            print("*****************************************************")
            print("Rotation "+comp+" on the card :"+str(RotCarte))
            #RotMag = int(raw_input('Enter a Rotation for component '+comp+" : ") or 0)
            RotMag = int(input('Enter a Rotation in Mag '+comp+ ' : ') or 0)
            if RotMag<RotCarte : 
                Rot=RotCarte-RotMag
            else:
                Rot=360-RotMag+RotCarte
            
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
    print(data)
    bank = 'bank1'
    start=loops
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x208 , RELATIVE)
    for i in range(0 , 1):
    #for i in range(0 , loops):
        for n in range(0, start):
            writeToFloppy([0, 0, 0, 0])
            print([0, 0, 0, 0])
        writeToFloppy([0, 10, 0, 0])
        print([0, 10, 0, 0])
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
        # secondly searchLab() detects the Buffer key which equals NewMag and inserts the dictMag value in the
        # dictionary (Buffer)
        # Lab is indentical to the position of the section
#~ ===================================================================================
          
def warehouse (comp,composants):
    print("Choose an address for : " + comp)
    #NewMag = int(raw_input('Entrer an adress Mag : ') or 0)
    NewMag = int(input('Entrer an adress of Mag : ') or 0)
    for k in composants:
        if NewMag in range(1,14) or NewMag in range(21,34) or NewMag in range(41,46):
            pack2Mag[k] = NewMag
            
            searchLab(NewMag, LabInfo, composants,Buffer,dicoComp)
        elif NewMag in range(15,20) or NewMag in range(35,40):
            print("impossible de rentrer ce magasin")
            warehouse (composants,comp)
    return NewMag

#~ ==============================================================================
#~ ==========================LAB===============================================


def searchLab(NewMag, LabInfo, comp,Buffer,dicoComp):
   
   
   
   keys = tuple(Buffer.keys())
   LabInfoK = tuple(LabInfo.keys())
   LabInfoI = tuple(LabInfo.items())
   for o in keys:
       if int(o) == NewMag:
          
          
          for i in LabInfoK:
              
              if comp[0] == i:
                print(comp[0])
                val = LabInfo[i]['Lab']
                Buffer[o][1] = int(val)
                if int(Buffer[o][3])==int(ListBuffer[int(o)][3]):
                    ListBuffer[int(o)][1]=int(val)
              
               
       
                     
   return NewMag, LabInfo, comp ,Buffer
#~ ===================================================================================
#~ ==================================== pushLab ======================================
#~ pushLab is the function who can take all position of the section and give the Lab of component
#~ this is an option
#~f.seek() go in hexAddr['bank4P] = 39000
#~secondly f.seek() go in hexAddress = 39608
#~finally f.seek() go in hexAddress = 3977F
#~ ===================================================================================

def pushLab(ListBuffer):
    #print ("start pushLab()")
    bank = 'bank4P'
    level=0
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x608, RELATIVE)
    for n in range(1,len(ListBuffer)):
         writeToFloppy(ListBuffer[n])
         print(ListBuffer[n])
         level=level+1
    #~ Nb of Mag
    bank ='bank4'
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x036, RELATIVE)
    writeToFloppy([level])
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x038, RELATIVE)
    writeToFloppy([level])
   
    print ("finish of writting warehouse")
    

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


def pushComp(data, NewMag,Buffer,LabInfo,tools,composants,loops,dicoComp):
    
    start=loops
    boucle=0
    print ("start pushComp()")
    bank = 'bank4'
    lineCounter=0
    
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x208, RELATIVE)
    for i in range(0,1):
    #for i in range(0, loops):
        for n in range(0, start):
            writeToFloppy([0, 0, 0, 0])
            print([0, 0, 0, 0])
            lineCounter=lineCounter+1
        writeToFloppy([0, 10, 0, 0])
        print([0, 10, 0, 0])
        lineCounter=lineCounter+1
        print ("start to write component")
        
        if True:             
            for k,v in data.items():
              
              
              
              if v[1]=='0':
                  v[1]='360'
                                   
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
                             
                        
                        for key,n in dicoComp.items():
                                                
                                                if key==k :
                                                       
                                                       toolsMemory= n[0]
                                                       speedMemory= n[1]
                                                       tools=toolsMemory
                                                       speed=[0,speedMemory,0,0]
                                                else:pass
 
#=======================================================================
              if boucle==0:
                    n=tools
                    
                    boucle=boucle+1
                    print("strat loop")
                    if n == tools:
                        
                        DataToolsDrop[2]=n
                        DataToolsTake[2]=n
                        writeToFloppy(DataToolsTake)
                        lineCounter=lineCounter+1
                        print(DataToolsTake)
                        writeToFloppy(speed)
                        lineCounter=lineCounter+1
                        print(speed)
                        writeToFloppy([0, 1, loops, 0])
                        lineCounter=lineCounter+1
                        print([0, 1, loops, 0])
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        lineCounter=lineCounter+1
                        ValAncien=tools
                        print(v)
                        
                        
                        
                        
                    else:
                                               
                        DataToolsDrop[2]=ValAncien
                        DataToolsTake[2]=tools
                        writeToFloppy(DataToolsTake)
                        lineCounter=lineCounter+1
                        print(DataToolsTake)
                        writeToFloppy([0, 1, loops, 0])
                        lineCounter=lineCounter+1
                        print([0, 1, loops, 0])
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        lineCounter=lineCounter+1
                        print(v)
                        n=tools
                        
              else:
                    
                    
                    if ValAncien == tools:
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        lineCounter=lineCounter+1
                        print(v)
                        
                    else:
                        
                        writeToFloppy([0, 2, 0, 0])
                        lineCounter=lineCounter+1
                        print('[0, 2, 0, 0]')
                        DataToolsDrop[2]=ValAncien
                        writeToFloppy(DataToolsDrop)
                        lineCounter=lineCounter+1
                        print(DataToolsDrop)
                        DataToolsDrop[2]=tools
                        DataToolsTake[2]=tools
                        n=tools
                        writeToFloppy(DataToolsTake)
                        lineCounter=lineCounter+1
                        print(DataToolsTake)
                        if DataToolsTake[2] != ValAncien:
                           writeToFloppy(speed)
                           lineCounter=lineCounter+1
                           print(speed)
                        writeToFloppy([0, 1, loops, 0])
                        lineCounter=lineCounter+1
                        print([0, 1, loops, 0])
                        v[3] = yaxisdir + v[3]
                        writeToFloppy(v)
                        lineCounter=lineCounter+1
                        print(v)
                        ValAncien=tools
                                
        else:
                        
                                #tools=raw_input("Enter tools for this programme")
                                tools=input("Enter tools for this programme")
                                DataToolsDrop[2]=tools
                                DataToolsTake[2]=tools
                                writeToFloppy(DataToolsTake)
                                lineCounter=lineCounter+1
                                writeToFloppy([0, 1, loops, 0])
                                lineCounter=lineCounter+1
                                for k,v in data.items():
                                    v[3] = yaxisdir + v[3]
                                    writeToFloppy(v)
                                    lineCounter=lineCounter+1
        # ~ Nb lignes
    
    writeToFloppy(DataToolsDrop)
    lineCounter=lineCounter+1
    writeToFloppy([0, 2, 0, 0])
    lineCounter=lineCounter+1
    print('[0, 2, 0, 0]')
    f.seek(hexAddr[bank], ABSOLUTE)
    f.seek(0x032, RELATIVE)
    print(lineCounter)
    print ("finish of writting components")
    nbrLines(lineCounter)
   

#~ =========================================================================

def nbrLines(nbrLine):
       
       bank='bank4'
       f.seek(hexAddr[bank], ABSOLUTE)
       f.seek(0x032, RELATIVE)
       writeToFloppy([nbrLine])
       f.seek(hexAddr[bank], ABSOLUTE)
       f.seek(0x034, RELATIVE)
       writeToFloppy([nbrLine+1])


#~====================================================================




def eagleParser() :

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

	try:
		#SourceFile=raw_input("Enter your File Name : ")
		SourceFile=input("Enter your File Name : ")
		try:
			File=open(SourceFile,"r")
		except FileNotFoundError:
			print ('impossible to search the source File')
		
		source = AddressFile + SourceFile
	except :
		print ('impossible to search the source File')




	lines = [line.strip() for line in open(source)]
	components = []
	pins = []

	# ~ Read Lines
	for line in lines:
		line = line.rstrip()
		if "-composant-" in line:
			m = p.match(line)
			if m:
				#comp = m.group(1)
				#composants[comp] = list(m.group(2, 5, 3, 4))
				components.appends({'name':m.group(1),'package':m.group(2),'x':m.group(5),'y':m.group(3),'rot':m.group(4)})
				
				Rotation(components[-1],Rot)
				box=m.group(2)
				warehouse (components[-1])
				if components[-1]["package"] in pack2Mag.keys()):
					components[-1]["package"] = pack2Mag[components[-1]["package"]]
				else:
					print ("no pack " + components[-1]["package"] + " in bank, remove item " +components[-1][0])
					del(components[-1])
			else:
				print ("Ignored line: " + line)
		if "-Pin-" in line:
			m = p2.match(line)
			if m:
				pins.append(list((1,Dot(int(submission),box,dicoComp,comp,Buffer,NewMag)) + m.group(1, 2)))
			else:
				print ("Ignored line: " + line)
	return [components,pins]


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
    welcome()
    print()
    
    f = open(disk, 'rb+')
except IOError:
    print ('impossible to writting data')
print ('it\'s possible to writting data on a floppy disk')

#~======================================================================
#~================================ VARIABLES =========================

# ~ Source file for testing
#source = 'E:\Iut\Rapport de Stage/testeur_UM.pnp' # Windows
#~source = '../../../testeur_UM.pnp' # Linux
AddressFile= 'E:\Iut\Rapport de Stage/'
SourceFile=''

#~ ================================================================
# ~ Biscotte is the virtual support for the test
# ~ disk ='/dev/fd0' is the way of floppy disk
disk = 'biscotte'
# disk ='/dev/fd0'
#~====================================================================


# ~ time of point to drop
submission = 0
dicoDot={}
dicoComp={}
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
Labimport=''
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

#~ ===========================================================================
# ~ Write to Floppy : for Precidot, data will be recorded on bank1 and the coordinates
# ~ of points will be defined with
# ~ call to function pushDots(pins)
# ~For Novar we will used bank4 and
# ~ for allocation of components call to function pushComp(data.item()))
# we wil keep bank 2 and 3 for back-up

#~ ==============================================================================
#~ ============================= WRITTING ON FLOPPY DISK ========================

  
    
print("before pushDots(pins)")
print("**** for example 2 Electronic cards = 2 loops ******")
#loops= int(raw_input("How many Electronic card are you need to create ?  "))
loops= int(input("How many Electronic card are you need to create ?  ")or 1)
pushDots(pins,loops)
print("after pushDots(pins)")

print("change of bank")
pp.pprint(composants) # defined indentation of components
print("after pp.pprint(components)")
pushComp(composants,NewMag,Buffer,LabInfo,tools,composants,loops,dicoComp)
bank = 'bank4P'
pushLab(ListBuffer)
print(ListBuffer)
Finish()

    


#~ ============================== Close to Floppy Disk ======================

f.close()

#~ ===========================================================================

