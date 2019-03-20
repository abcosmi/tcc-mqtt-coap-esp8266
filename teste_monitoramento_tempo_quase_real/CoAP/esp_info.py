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
		self.dups = 0
		
	def getID(self):
		return self.esp_id
	
	def getIP(self):		
		return self.esp_ip
	
	def setIP(self,ip):
		self.esp_ip = ip
	
	def getMsgs(self,index):
		return self.msgs[index]
	
	def setMsgs(self,msg):		
		if msg.getICMP() != -1:
			msg.incDup()
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
				cont = cont + m.getDup()
		return self.dups

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
		notDup = self.msgs
		delta = 0		
		if len(notDup) == 0:
			return 0
		else:			
			for m_idx,m in enumerate(notDup):
				#m.printMsg()
				if m.getIP() == broker_ip:
					for n in range(m_idx+1,len(notDup)):
						if m.getMsgID() == self.msgs[n].getMsgID() and self.msgs[n].getType() == 2:
							delta = delta + (self.msgs[n].getTime() - m.getTime())/2
							break			
			return abs(delta/self.ackNumMsg())				
		
	def stdDev(self,broker_ip):
		media = self.deltaTime(broker_ip)		
		notDup = self.getNotDupMsg()
		delta = 0		
		if len(notDup) == 0:
			return 0
		else:
			for m_idx,m in enumerate(notDup):
				if m.getIP() == broker_ip:
					for n in range(m_idx+1,len(notDup)):
						if m.getMsgID() == self.msgs[n].getMsgID() and self.msgs[n].getType() == 2:
							#print('msgID: %s ---- delta: %f ---- n.time: %f - m.time: %f = %f' %(m.getMsgID(),delta,n.getTime(),m.getTime(),n.getTime() - m.getTime()))
							delta = delta + pow(((self.msgs[n].getTime() - m.getTime())/2 - media),2)
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
				#print("id=%s %d-- ref=%s %d\n" %(m.getMsgID(),len(m.getMsgID()),ref,len(ref)))
				if m.getMsgID() == ref:
					ref = ref + 1
				else:
					if m.getDup() != 0:
						return [False,"Duplicate message found"]
					else:
						return [False,"Message not found"]
		
		return [True,"Correct sequence"]
	
	
	## Messages per second	
	def msgSec(self):
		buf = []
		notDup = self.getNotDupMsg()
		time = notDup[1].getYTime()
		count = 0
		for t in range(time,time+550):
			for m in notDup:				
				if m.getCode() == 69:					
					if m.getYTime() == t:						
						count = count + 1
					elif m.getYTime() > t:
						print("esp: " + str(m.getYTime()) + " ----- tmp: " + str(t) + " ---- count:  " + str(count))
						buf.append(t-time)
						buf.append(count)
						count = 0
						break
		return buf
					


	def printEsp(self):
		for m in self.msgs:
			print("\nESP Code: " + self.esp_id)
			m.printMsg()
			
		
	
