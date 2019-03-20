#from msg_info import *
import msg_info


class Esp(object):	
#	esp_id
#	qos
#	esp_ip
#	msgs
	
	def __init__(self,_id,ip,time_interval,control_resource):
		self.esp_id = _id
		self.esp_ip = ip
		self.def_time_int = time_interval
		self.control_resource = control_resource
		self.msgs = []
		
	def getID(self):
		return self.esp_id
	
	def getIP(self):		
		return self.esp_ip
	
	def setIP(self,ip):
		self.esp_ip = ip
	
	def getMsgs(self,index):
		return self.msgs[index]
	
	def setMsgs(self,msg):		
		for m in self.msgs:		### Verify duplicate messages
			if m.getMsgID() == msg.getMsgID() and m.getType() == msg.getType():
				m.incDup()
		self.msgs.append(msg)
	
	def setTimeInterval(self,t):
		self.def_time_int = t
		
	def setQOS(self,QOS):
		self.qos = QOS
		
	def getNotDupMsg(self):
		buf = []		
		for m in self.msgs:						
			if m.getDup() == 0:				
				buf.append(m)				
					
		return buf ## Return a list of not duplicate messages
	
	def dupNumMsg(self):
		cont = 0
		for m in self.msgs:
			if m.getDup() != 0:
				cont = cont + 1
		return cont

	def getNumMsg(self):
		notDup = self.getNotDupMsg()
		cont = 0		
		for m in notDup:
			if m.getCode() == 1 and m.getDup() == 0:
				cont = cont + 1		
		return cont	
	
	def ackNumMsg(self):
		notDup = self.getNotDupMsg()
		cont = 0		
		for m in notDup:
			if m.getType() == 2 and m.getDup() == 0:
				cont = cont + 1		
		return cont	
	
	def totNumMsg(self):	
		return len(self.msgs)
		
	def deltaTime(self, broker_ip):
		notDup = self.getNotDupMsg()
		delta = 0		
		if len(notDup) == 0:
			return 0
		else:			
			for m in notDup:
				if m.getIP() == broker_ip:
					for n in notDup:
						if m.getMsgID() == n.getMsgID() and n.getType() == 2:
							delta = delta + (n.getTime() - m.getTime())/2
							break
			return abs(delta/self.ackNumMsg())				
		
	def stdDev(self,broker_ip):
		media = self.deltaTime(broker_ip)		
		notDup = self.getNotDupMsg()
		delta = 0		
		if len(notDup) == 0:
			return 0
		else:
			for m in notDup:
				if m.getIP() == broker_ip:
					for n in notDup:
						if m.getMsgID() == n.getMsgID() and n.getType() == 2:
							delta = delta + pow(((n.getTime() - m.getTime())/2 - media),2)
							break
			var = delta/(len(notDup)/2)
			return pow(var,0.5)

	def verifySeqNum(self,max_id):
		if len(self.msgs) == 0:
			return [False,"No messages can be found to this device"]
		for m in self.msgs:
			if m.getType() == 3:				
				ref = m.getMsgID()
				break

		for m in self.msgs:
			if m.getType() == 3:
				if m.getMsgID() == ref:
					ref = ref + 1
				else:
					if m.getDup() != 0:
						return [False,"Duplicate message found"]
					else:
						return [False,"Message not found"]
		
		return [True,"Correct sequence"]
		
		

	def printEsp(self):
		for m in self.msgs:
			print("\nESP Code: " + self.esp_id)
			m.printMsg()
			
		
	
