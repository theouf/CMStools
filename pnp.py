#!/usr/bin/python

#~ Source file
source = 'testeur_UM.pnp'

#~ Floppy disk
#~ disk = '/dev/fd0'
disk = 'biscotte'

#~ Use Bank
bank = 'bank4'

#~ Loops
loops = 1

#~ Added lines
addLines = 3+loops

#~ Precidot or Nova
target = "nova"

#~ Bank address
hexAddr = {}
hexAddr['bank1'] = 0x04000
hexAddr['bank2'] = 0x16206
hexAddr['bank3'] = 0x28206
hexAddr['bank4'] = 0x3A000

#~ package to magasin
pack2Mag = {}
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
pack2Mag['0805'] = 15
pack2Mag['1206'] = 16
pack2Mag['1210'] = 17
pack2Mag['1812'] = 18
pack2Mag['2220'] = 19

#~ =====================================================================
def intToHex(i):
    ret = []
    ret.append(format("%02X" % (int(i) & 0x00ff)))
    ret.append(format("%02X" % ((int(i)/0xff) & 0xff)))
    return ret

def hexToInt(lbx,hbx):
    lb = int(ord(lbx))
    hb = int(ord(hbx))
    return [lb+hb*256,lb,hb]

#~ =====================================================================
def writeToFloppy(t):
    for i in range(0,len(t)):
        h = intToHex(t[i])
        f.write(h[0].decode("hex"))
        f.write(h[1].decode("hex"))

def pushDots(data):
    #~ Write to floppy
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x208,RELATIVE)
    for i in range(0,loops):
        writeToFloppy([0,0,0,0])
    writeToFloppy([0,10,0,0])
    writeToFloppy([0,1,loops,0])
    for n in range(0,len(data)):
        writeToFloppy(data[n])
    writeToFloppy([0,2,0,0])
    
    #~ Nb lignes
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x32,RELATIVE)
    writeToFloppy([len(data)+addLines,len(data)+addLines])

def pushComp(data):
    #~ Write to floppy
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x208,RELATIVE)
    for i in range(0,loops):
        writeToFloppy([0,0,0,0])
    writeToFloppy([0,10,0,0])
    writeToFloppy([0,1,loops,0])
    for n in range(0,len(data)):
        writeToFloppy(data[n])
    writeToFloppy([0,2,0,0])
    
    #~ Nb lignes
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x32,RELATIVE)
    writeToFloppy([len(data)+addLines,len(data)+addLines])


#~ =====================================================================

#~ Imports
import sys
import re
import pprint

#~ Pretty Print
pp = pprint.PrettyPrinter(indent=4)

#~ Constants
ABSOLUTE = 0
RELATIVE = 1

#~ Floppy dev
f = open(disk,'rw+')

#~ Eagle RegExp
p = re.compile('^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$')
p2 = re.compile('^-Pin--X-(.+)-Y-(.*)$')

#~ Get Eagle file lines
lines = [line.strip() for line in open(source)]

composants = {}
pins = []

#~ Read Lines
for line in lines:
    line = line.rstrip()
    if "-composant-" in line:
        m = p.match(line)
        if m:
            comp = m.group(1)
            composants[comp]=list(m.group(2,5,3,4))
            if ( composants[comp][0] in pack2Mag.keys() ):
                composants[comp][0] = pack2Mag[composants[comp][0]]
            else: 
                print "no pack "+composants[comp][0]+" in bank, remove item "+comp
                del(composants[comp])
        else:
            print "Ignored line: "+line
    if "-Pin-" in line:
        m = p2.match(line)
        if m:
            pins.append(list((1,200)+m.group(1,2)))
        else:
            print "Ignored line: "+line
            
#~ Print Pins

#~ Write to Floppy
if ( target == "precidot" ):
    pushDots(pins)
else:
    pp.pprint(composants)
    pushComp(composants.values())


#~ Read the floppy to check the result
#~ f.seek(hexAddr[bank],ABSOLUTE)
#~ f.seek(0x208,RELATIVE)
#~ for pinid in range(0,len(pins)+addLines):
    #~ sys.stdout.write("0x%04X = " % (pinid*4))
    #~ for i in range(0,4):
        #~ val = hexToInt(f.read(1),f.read(1))
        #~ sys.stdout.write(" - %6d [%02X,%02X]" % ( val[0], val[1], val[2]))
    #~ print ""
        
f.close()

