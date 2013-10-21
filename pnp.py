#!/usr/bin/python

#~ Source file
source = 'testeur_UM.pnp'

#~ Floppy disk
disk = '/dev/fd0'
#~ disk = 'biscotte'

#~ Use Bank
bank = 'bank4'

#~ Added lines
addLines = 4

#~ Precidot or Nova
target = "precidot"

#~ Bank address
hexAddr = {}
hexAddr['bank1'] = 0x04000
hexAddr['bank2'] = 0x16206
hexAddr['bank3'] = 0x28206
hexAddr['bank4'] = 0x3A000

#~ =====================================================================
def intoToHex(i):
    ret = []
    ret.append(format("%02X" % (int(i) & 0x00ff)))
    ret.append(format("%02X" % ((int(i)/0xff) & 0xff)))
    return ret
#~ =====================================================================
def writeToFloppy(data):

    #~ Write to floppy
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x208,RELATIVE)
    f.write("\x00\x00\x00\x00\x00\x00\x00\x00")
    f.write("\x00\x00\x0A\x00\x00\x00\x00\x00")
    f.write("\x00\x00\x01\x00\x01\x00\x00\x00")
    for n in range(0,len(data)):
        f.write("\x01\x00")
        f.write("\xC8\x00")
        f.write(data[n][1][0].decode("hex"))
        f.write(data[n][1][1].decode("hex"))
        f.write(data[n][1][2].decode("hex"))
        f.write(data[n][1][3].decode("hex"))
    f.write("\x00\x00\x02\x00\x00\x00\x00\x00")
    
    #~ Nb lignes
    nb_lines = []
    nb_lines.append(intoToHex(len(data)+addLines)[0])
    nb_lines.append(intoToHex(len(data)+addLines)[1])
    
    f.seek(hexAddr[bank],ABSOLUTE)
    f.seek(0x32,RELATIVE)
    f.write(nb_lines[0].decode("hex"))
    f.write(nb_lines[1].decode("hex"))
    f.write(nb_lines[0].decode("hex"))
    f.write(nb_lines[1].decode("hex"))


#~ =====================================================================

#~ Imports
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
            composants[comp]=[list(m.group(2,3,4,5)),[]]
        else:
            print "Ignored line: "+line
    if "-Pin-" in line:
        m = p2.match(line)
        if m:
            pins.append([list(m.group(1,2)),[]])
        else:
            print "Ignored line: "+line
            
#~ Parse composants and create hex version
for composant in composants:
    composants[composant][1].append(composants[composant][0][0])
    for i in range(1,4):
        x = int(composants[composant][0][i])
        composants[composant][1].append("%02X %02X" % (x & 0x00ff, (x/0xff) & 0xff))
        
#~ Parse Pins and create hex version
for pinid in range(0,len(pins)):
    pins[pinid][1].append(intoToHex(pins[pinid][0][0])[0])
    pins[pinid][1].append(intoToHex(pins[pinid][0][0])[1])
    pins[pinid][1].append(intoToHex(pins[pinid][0][1])[0])
    pins[pinid][1].append(intoToHex(pins[pinid][0][1])[1])

#~ Print Pins
#~ pp.pprint(pins)

#~ Write to Floppy
if ( target == "precidot" ):
    writeToFloppy(pins)
else:
    writeToFloppy(composants)


#~ Read the floppy to check the result
f.seek(hexAddr[bank],ABSOLUTE)
f.seek(0x208,RELATIVE)
for pinid in range(0,len(pins)+addLines):
    print " - ".join("{0:02x}".format(ord(c)) for c in f.read(8))

f.close()

