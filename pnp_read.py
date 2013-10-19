#!/usr/bin/python

#~ Floppy disk
#~ disk = '/dev/fd0'
disk = 'writedByPrecidotBank4.bin'

# Size to read
size = 1024

#~ Use Bank
bank = 'bank4'

#~ Bank address
hexAddr = {}
hexAddr['bank1'] = 0x04206
hexAddr['bank2'] = 0x16206
hexAddr['bank3'] = 0x28206
hexAddr['bank4'] = 0x39fff
#~ hexAddr['bank4'] = 0x3a206

#~ =====================================================================

#~ Constants
ABSOLUTE = 0
RELATIVE = 1

#~ Floppy dev
f = open(disk,'rw+')

prev_hb = 0
#~ Write to floppy
f.seek(hexAddr[bank],ABSOLUTE)
for i in range(0,size):
    lb = int(ord(f.read(1)))
    hb = int(ord(f.read(1)))
    prev_hb = hb
    print "0x%06X = %8d [%02X,%02X] - %8d [%02X,%02X]" % ( hexAddr[bank]+i*2 , lb+hb*256, lb, hb , prev_hb+lb*256, prev_hb, lb)



f.close()
