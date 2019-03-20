#from msg_info import *
import msg_info


class Esp(object):	
#	esp_id
#	qos
#	esp_ip
#	msgs
	
	def __init__(self,_id,ip,qos,time_interval,control_topic):
		self.esp_id = _id
		self.esp_ip = ip
		self.qos = qos
		self.def_time_int = time_interval
		self.control_topic = control_topic
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
				if (m.getType() == 3 or m.getType() == 4) and m.getTopic() != self.control_topic:					
					buf.append(m)				
					
		return buf ## Return a list of not duplicate messages
	
	def dupNumMsg(self):
		cont = 0
		for m in self.msgs:
			if m.getDup() != 0 and m.getType() == 3:
				cont = cont + 1
		return cont

	def pubNumMsg(self):
		notDup = self.getNotDupMsg()
		cont = 0		
		for m in notDup:
			if m.getType() == 3 and m.getDup() == 0:
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
			qos1 = 0
			qos0 = 0
			id_count = 0
			for m in notDup:								
				if m.getQoS() == 0:
					qos0 = qos0 + 1
				elif m.getQoS() == 1:					
					qos1 = qos1 + 1
					if m.getMsgID() == 0:
						id_count = id_count + 1
				
			if self.qos == 0 or id_count > 2:				
				for i in range(0,len(notDup) - 1):	
					#print("delta: %f ---- i+1: %f - i: %f = %f" %(delta,notDup[i+1].getTime(),notDup[i].getTime(),notDup[i+1].getTime() - notDup[i].getTime()))					
					delta = delta + abs((notDup[i+1].getTime() - notDup[i].getTime()) )								
				return abs(delta/(self.pubNumMsg() - 1))
			else:				
				for m in notDup:
					m.printMsg()
					if m.getIP() == broker_ip:
						for n in notDup:
							if m.getMsgID() == n.getMsgID() and n.getType() == 4:								
								delta = delta + (n.getTime() - m.getTime())/2
								break
				return abs(delta/self.pubNumMsg())				
		
	def stdDev(self,broker_ip):
		media = self.deltaTime(broker_ip)		
		notDup = self.getNotDupMsg()
		delta = 0		
		if len(notDup) == 0:
			return 0
		else:
			id_count = 0
			qos1 = 0
			qos0 = 0
			for m in notDup:				
				if m.getQoS() == 0:
					qos0 = qos0 + 1
				elif m.getQoS() == 1:
					qos1 = qos1 + 1
					if m.getMsgID() == 0:
						id_count = id_count + 1
				
			if self.qos == 0 or id_count > 2:				
				for i in range(0,len(notDup) - 1):	
					#print("delta: %f ---- i+1: %f - i: %f = %f" %(delta,notDup[i+1].getTime(),notDup[i].getTime(),notDup[i+1].getTime() - notDup[i].getTime()))		
					#print("i+1: %f - i: %f - 10 = %f ---- media: %f ---- delta: %f" %(notDup[i+1].getTime(),notDup[i].getTime(),abs(notDup[i+1].getTime() - notDup[i].getTime()-10) ,media,delta))
					delta = pow((abs(notDup[i+1].getTime() - notDup[i].getTime())  - media),2) + delta
				var = delta/(len(notDup)-1)
				return pow(var,0.5)
			else:
				for m in notDup:
					if m.getIP() == broker_ip:
						for n in notDup:
							if m.getMsgID() == n.getMsgID() and n.getType() == 4:
								#print('msgID: %s ---- delta: %f ---- n.time: %f - m.time: %f = %f' %(m.getMsgID(),delta,n.getTime(),m.getTime(),n.getTime() - m.getTime()))
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
				if m.getYTime() == t:						
					count = count + 1
				elif m.getYTime() > t:
					buf.append(t-time)
					buf.append(count)
					count = 0
					break
		return buf		

	def printEsp(self):
		for m in self.msgs:
			print("\nESP Code: " + self.esp_id)
			m.printMsg()
			
		
	
