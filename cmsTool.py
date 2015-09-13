#!usr/bin/python


import datetime, time
import pprint
import re
import sys
import struct
import codecs
from operator import itemgetter

def askDefault(Question,default) :
	"""
	description :
		automation of user question, with default value
	Input :
		(question, default value)
	Output :
		value answered or default value
	Improvements :
		add a time-out 
	"""
		
	var = raw_input("Please enter "+Question+" (default : "+default+") :")
	if not var:
		var = default
	return var


class Pin() :
	""" the pin of a component is defined by its position : x, y and its size (small/medium/large)
		function "calcTps" calculates the time to push the soldering paste"""
		
		
	def __init__(self,x,y) :
		self.x=int(x)
		self.y=-1*int(y)
		self.size=self.getSize()
		self.depTime=self.calcTps()
		
	def getSize(self):
		""" ask to user wich is the size of the footprint
		toDo : automated"""
		size=askDefault(" the footprint's size (small,medium,large ","small")
		return size
		
	def calcTps(self):
		tps={"small":100,"medium":200,"large":300}
		return tps[self.size]
		
			
class Comp() :
	""" a component is defined by its name ; package, center position : x, y ; rotation on card """
	def __init__(self,name,pkg,x,y,rot) :
		self.name=name
		self.x=int(x)
		self.y=-1*int(y)
		self.rot=int(rot)
		print "component : "+self.name
		self.pkg=Package(pkg)
		self.calcRot()
		
	def calcRot(self):
		"""calculate the global rotation : card + mag"""
		if self.pkg.rot < self.rot : 
			self.rot-=self.pkg.rot
		else :
			self.rot+=360-self.pkg.rot
		
class Package():
	""" package is defined by its name, mag(nb & rot), the tool (nb,speed) to use """
	def __init__(self,name):
		self.name=name
		self.mag,self.rot=self.getMag()
		self.tool,self.toolSpeed=self.getTool()
		
	def getMag(self):
		""" ask to user wich mag then create a mag object
		toDo : get info from a file gerated by hand or via a vew app"""
		mag=askDefault(" the mag where is this component (help for help)","0")
		while mag=="help" :
			print("****************************************************")
			print("**********			HELP			***************")
			print("**********	Component  Mag in Novar	 **************")
			print("**********	0 if not a physical Comp **************")
			print("********		(vrac mag to add in this help)		***")
			print("***		1								34		***")
			print("***		\ /								/\		***")
			print("***		little							big		***")
			print("***		\ /								/\		***")
			print("***		10								31		***")
			print("***		11								30		***")
			print("***		\ /								/\		***")
			print("***		big								little	***")
			print("***		\ /								/\		***")
			print("***		14 								21		***")
			print("****************************************************")
			print("****************************************************")
			print "\n\n\n"
			mag=askDefault(" the mag where is this component ","help")
			
		rot=askDefault(" the rotation of  this component in the mag ","help")
		while rot=="help" :
			print("*****************************************************")
			print("**********            HELP          *****************")
			print("********** Component rotaion in Mag *****************")
			print("***  0    for     Rotation of  0 degree  |  ^|   ****")
			print("*** 90    for     Rotation of 90 degree  |  <=   ****")
			print("*** 180   for     Rotation of 180 degree |  =>   ****")
			print("*** 270   for     Rotation of 270 degree |  |    ****")
			print("*****************************************************")
			print("*****************************************************")
			rot=askDefault(" the rotation of  this component in the mag (help for help)","0")
		return int(mag),int(rot)
		
	def getTool(self):
		""" ask to user wich tool to use and at wich speed
		toDo : get info from a file gerated by hand or via a vew app"""
		tool=askDefault(" the tool used to pick this component (help for help)","0")
		while tool=="help" :
			print("*******************************************")
			print("********HELP TOOLS (0 if not a comp) ********")
			print("*** 2 for tool with diameter :1.03 mm   ***")
			print("*** 3 for tool with diameter :2.83 mm   ***")
			print("*** 4 for tool with diameter :5.34 mm   ***")
			print("*******************************************")
			print("*******************************************")
			tool=askDefault(" the tool used to pick this component (help for help)","0")
			
		speed=askDefault(" speed used to pick this component (s for slox, f for fast)","s")
		return int(tool),speed

class Datas():
	"""data to wrinte on Floppy"""
	offsets={	"machineParam":0x1042,
				"progLines":0x1208 ,
				"progLen":0x1032,
				"mag":0x608,
				"magLen":0x1036
			}
	
	def __init__(self) :
		self.datas=[]
		
		
	def addRefLine(self,x=0,y=0) :
		self.datas.append([0,0,x,y])
		
		
	def addCheckRef(self) :
		self.datas.append([0,10,0,0])
		
		
	def startLoop(self,loop=1) :
		self.datas.append([0,1,loop,0])
		
	
	def stopLoop(self,loop=1) :
		self.datas.append([0,2,0,0])
		

		
class Precidot(Datas) :
	"""novar data template for novar"""

	def __init__(self):
		Datas.__init__(self)
		self.offset=[Datas.offsets["progLines"],Datas.offsets["progLen"]]
		
	def addPin(self,pin) :
		self.datas.append([1,pin.depTime,pin.x,pin.y])
		
	def dataFormat(self,pins,loops):
		for loops in range (0,loops) :
			self.addRefLine()
		self.addCheckRef()
		self.startLoop(loops)
		for pin in sorted(pins, key=lambda tri: tri.x) :
			self.addPin(pin)
		self.stopLoop()
			
		
		
class Novar(Datas) :
	"""novar data template for novar"""
	def __init__(self):
		Datas.__init__(self)
		self.curTool=0
		self.curSpeed="s"
		self.offset=[Datas.offsets["progLines"],Datas.offsets["progLen"]]
		
	def addComp(self,comp) :
		self.datas.append([comp.mag,comp.rot,comp.x,comp.y])
		
	def changeTool(self,comp) :
		self.datas.append([0,12,self.curTool,1])
		self.curTool=comp.pkg.tool
		self.datas.append([0,12,comp.pkg.tool,0])
		
	def rangeTool(self,comp) :
		self.datas.append([0,12,self.curTool,1])
		self.curTool=0
		
	def changeSpeed(self,comp) :
		if comp.pkg.toolSpeed=="f":
			speed=5
		else :
			speed=4
		self.datas.append([0,speed,0,0])
		self.curSpeed=comp.pkg.toolSpeed

	def dataFormat(self,comps,loops):
		compTool=[[],[],[],[],[]]
		
		for loops in range (0,loops) :
			self.addRefLine()
		self.addCheckRef()
		
		"""order component fonction of tool (maybe later then speed), for each tool a loop"""
		for c in comps :
			compTool[c.pkg.tool].append(c)
		for tool in compTool :
			self.changeTool(c)
			self.startLoop(loops)
			for comp in sorted(tool, key=lambda x: x.pkg.toolSpeed) :
				if not comp.pkg.toolSpeed==self.curSpeed :
					self.changeSpeed(comp)
			self.stopLoop()
		self.rangeTool(comp)
			
		
class Mag(Datas):
	"""defined the Addr of all mag in novar"""
	def __init__(self):
		Datas.__init__(self)
		self.offset=[Datas.offsets["mag"],Datas.offsets["magLen"]]
		self.datas=[
					[0, 0, 153 , 1725],#1
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
					[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],
					[0, 0, 7619, 5572], #21
					[0, 0, 7619 , 5253],
					[0, 0, 7619 , 4940],
					[0, 0, 7619 , 4625],
					[0, 0, 7619 , 4311],
					[0, 0, 7619 , 4005],
					[0, 0, 7619 , 3686],
					[0, 0, 7619 , 3369],
					[0, 0, 7619 , 2737],
					[0, 0, 7690 , 2480],
					[0, 0, 7690 , 2087],
					[0, 0, 7690 , 1652],
					[0, 0, 7690 , 1190], #34
					[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],[0, 0, 0 , 0],
					[0, 0, 366 , 6855] #41          
				 ]
		
		
class InPut() :
	""" ask file name and parse it"""
	def __init__(self):
		self.inPutFile=self.getInPutFile()
		self.comps,self.pins=self.eagleParser()
		
	def getInPutFile(self) :
		"""**************"""
		"""get input file"""
		"""**************"""
		if len(sys.argv)>1 :
			inPutFile=sys.argv[1]
		else :
			inPutFile=askDefault("Input File Name : ","testeur_UM.pnp")
		try:
			fd=open(inPutFile,"r")
		except FileNotFoundError:
			print ('impossible to find the source File')
			exit
		InPutFile=fd.readlines()
		fd.close()
		return InPutFile
	
	def eagleParser(self) :

		#~ =========================================================================
		#~ ==================== FORMAT FOR EAGLE ===================================

		# ~ whith the help of The software Eagle we could be extract the data
		# ~ with this stucture
		# ~ for components : ^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$
		# ~ for points : ^-Pin--X-(.+)-Y-(.*)$
		

		#~==========================================================================

		pComp = re.compile('^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$')
		pPin = re.compile('^-Pin--X-(.+)-Y-(.*)$')

		components = []
		pins = []


		for line in self.inPutFile:
			m = pComp.match(line)
			if m :
				"""Components({'name':m.group(1),'package':m.group(2),'x':m.group(3),'y':m.group(4),'rot':m.group(5)})"""
				components.append(Comp(m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)))
				
			else :
				n = pPin.match(line)
				if n :
					"""pins.append({"mod": 1,"dt":Dot(int(submission),box,dicoComp,comp,Buffer,NewMag),"x" :n.group(1),"y":n.group(2)})"""
					pins.append(Pin(n.group(1),n.group(2)))
				else :
					print ("Ignored line: " + line)
		return components,pins


class Floppy():
	
	hexAddr = 	{
				'bank1' 	: 0x03000,
				'bank2' 	: 0x15000,
				'bank3' 	: 0x27000,
				'bank4P' 	: 0x39000
			}
	def __init__(self,dev="/def/fd0"):
		self.dev=dev
		
	def intToHex(self,i):
		ret = []
		ret.append(format("%02X" % (i & 0x00ff)))
		ret.append(format("%02X" % (int((i / 0xff)) & 0xff)))
		return ret

	def hexToInt(self,lbx, hbx):
		lb = int(ord(lbx))
		hb = int(ord(hbx))
		return [lb + hb * 256, lb, hb]
	
	
	def wDatas(self,bank,data):
		
		with open(self.dev,'rb+') as floppyFd :
			floppyFd.seek(Floppy.hexAddr[bank]+data.offset[0],0)
			for line in range(0,len(data.datas)):
				for val in range(0, len(data.datas[line])):
					h = self.intToHex(data.datas[line][val])
					floppyFd.write(codecs.decode(h[0], "hex"))
					floppyFd.write(codecs.decode(h[1], "hex"))
			if len(data.offset) > 1 :
				"""if length of data must be write, 2 offsets are available.
					len have to be write 2 times"""
				floppyFd.seek(Floppy.hexAddr[bank]+data.offset[1],0)
				h = self.intToHex(len(data.datas))
				floppyFd.write(codecs.decode(h[0], "hex"))
				floppyFd.write(codecs.decode(h[1], "hex"))
				floppyFd.write(codecs.decode(h[0], "hex"))
				floppyFd.write(codecs.decode(h[1], "hex"))

		



if __name__ == '__main__':
	
	print('*************************************************')
	print('*************  Precidot30 & Novar33  ************')
	print('*************        retrofit        ************')
	print("*************************************************")
	print("*****                                        ****")
	print("*****             FABLAB LANNION             ****")
	print("*****                                        ****")
	print('*************************************************')
	print("\n\n\n")
	print('*************************************************')
	print("*****                                        ****")
	print("*****          Insert a Floppy Disk          ****")
	print("*****                                        ****")
	print('*************************************************')


	floppy=Floppy("test")
	inPut=InPut()
	
	loops= int(askDefault("the number of electronic card you want to create","1"))
	
	precidot=Precidot()
	precidot.dataFormat(inPut.pins,loops)
	
	novar=Novar()
	mag=Mag()
	novar.dataFormat(inPut.comps,loops)
	
	floppy.wDatas("bank1",precidot)
	floppy.wDatas("bank2",novar)
	floppy.wDatas("bank2",mag)
	
	
	print('*************************************************')
	print('*************  Precidot30 & Novar33  ************')
	print('*************        retrofit        ************')
	print("*************************************************")
	print("*****                                        ****")
	print("*****             FABLAB LANNION             ****")
	print('*************************************************')
    
