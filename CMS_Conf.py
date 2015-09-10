#!/usr/bin/python
# coding=utf-8
'''


@authors: David,Erwan, Theo
version Python 2.7 and 3.4

This prog permits configure  Precidot and Novar according to 2 input files.
first one is created from eagle by a module "testeur_UM.pnp" and contains components and pins x & y coordonates
second one is not yet defined and will contains component location in the novar componentroom

here is the configuration of machines


'''



floppyBanks={
				"precidot"	:	"bank4",
				"novar"		:	"bank1"
			}



# ~ Bank address on the floppy
hexAddr = 	{
				'bank1' 	: 0x04000,
				'bank2' 	: 0x16206,
				'bank3' 	: 0x28206,
				'bank4' 	: 0x3A000,
				'bank4P' 	: 0x39000 # to be check what is it
			}

# ~ We defined the dictionary pack2Mag with keys and the Value
# ~ the value is the LAB
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


# ~ We defined the dictionary storeAddr with keys and 4 Values
# ~ the value is the MT
# ~ the second value is the LAB
# ~ the third value is Center Dx of component
# ~ the fourth value is Center Dy of component

# ~ Unite Machine =0.0508mm
# 3 and 4 row are :
# Coordinate centrer of component Machine : ((longueur /0,0508)/2)


   
#Buffer is fixed all magasin with there Mag address


storeAddr ={
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
ListBuffer=[
             [0,0,0,0],
             [0, 0, 153 , 1725],
             [0, 0, 153 , 2034],
             [0, 0, 153 , 2357],
             [0, 0, 153 , 2671],
             [0, 0, 153 , 2986],
             [0, 0, 153 , 3299],
             [0, 0, 153 , 3614],
             [0, 0, 153 , 3929],
             [0, 0, 153 , 4242],
             [0, 0, 153 , 4557],
             [0, 0, 153 , 4969],
             [0, 0, 153 , 5362],
             [0, 0, 153 , 5804],
             [0, 0, 153 , 6278], #14
             [0, 0, 153 , 6278],
             [0, 0, 153 , 6278],
             [0, 0, 153 , 6278],
             [0, 0, 153 , 6278],
             [0, 0, 153 , 6278],
             [0, 0, 7619, 5572],
             [0, 0, 7619, 5572], #21
             [0, 0, 7619 , 5253],
             [0, 0, 7619 , 4940],
             [0, 0, 7619 , 4625],
             [0, 0, 7619 , 4311],
             [0, 0, 7619 , 4005],
             [0, 0, 7619 , 3686],
             [0, 0, 7619 , 3369],
             [0, 0, 7698 , 3055],
             [0, 0, 7619 , 2737],
             [0, 0, 7690 , 2480],
             [0, 0, 7690 , 2087],
             [0, 0, 7690 , 1652],
             [0, 0, 7690 , 1190], #34
             [0, 0, 7690 , 1190],
             [0, 0, 7690 , 1190],
             [0, 0, 7690 , 1190],
             [0, 0, 7690 , 1190],
             [0, 0, 7690 , 1190],
             [0, 0, 7690 , 1190],
             [0, 0, 366 , 6855] #41
                         
             ]
