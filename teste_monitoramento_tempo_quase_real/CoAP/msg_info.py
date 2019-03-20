class CoapMsg(object):	
#	msg_type
# msg_code
#	msg_ID
#	msg_len
#	arrived_time
#	resource
#	dup
#	esp_ip
# broker_ip
	
	def __init__(self,msg_t,msg_c,msg_i,msg_l,arr_t,yt,res,espIP,brk_ip,icmp):
		self.msg_type = msg_t
		self.msg_code = msg_c
		self.msg_ID = msg_i
		self.msg_len = msg_l
		self.arrived_time = arr_t
		self.yield_time = yt
		self.resource = res		
		self.dup = 0
		self.esp_ip = espIP
		self.broker_ip = brk_ip
		self.icmp = icmp
		
	def getTime(self):
		return self.arrived_time
	
	def getYTime(self):
		return self.yield_time
	
	def getType(self):
		return self.msg_type
	
	def getCode(self):
		return self.msg_code
	
	def getMsgID(self):
		return self.msg_ID
	
	def getResource(self):
		return self.resource
	
	def getIP(self):
		return self.esp_ip
	
	def getDestIP(self):
		return self.broker_ip
	
	def getDup(self):
		return self.dup
	
	def setDup(self,d):
		self.dup = d 
	
	def incDup(self):
		self.dup = self.dup + 1		
		
	def getICMP(self):
		return self.icmp
	
	def printMsg(self):
		print('Source IP: %s' %self.esp_ip)
		print('Dest IP: %s' %self.broker_ip)
		print('Type: %i' %self.msg_type)
		print('Code: %i' %self.msg_code)
		print('Message Sequence Number: %s' %self.msg_ID)		
		print('Message Relative Time: %f' %self.arrived_time)
		print('Resource: %s' %self.resource)
