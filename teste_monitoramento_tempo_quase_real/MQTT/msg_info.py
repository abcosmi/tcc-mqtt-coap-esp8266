class MqttMsg(object):	
#	msg_type
#	msg_ID
#	msg_len
#	arrived_time
#	qos
#	topic
#	topic_len
#	dup
#	esp_ip
# broker_ip
	
	def __init__(self,msg_t,msg_i,msg_l,arr_t,yt,_qos,top,top_l,espIP,brk_ip):
		self.msg_type = msg_t
		self.msg_ID = msg_i
		self.msg_len = msg_l
		self.arrived_time = arr_t
		self.ytime = yt
		self.qos = _qos
		self.topic = top
		self.topic_len = top_l
		self.dup = 0
		self.esp_ip = espIP
		self.broker_ip = brk_ip
		
	def getTime(self):
		return self.arrived_time
	
	def getYTime(self):
		return self.ytime
	
	def getType(self):
		return self.msg_type
	
	def getMsgID(self):
		return self.msg_ID
	
	def getQoS(self):
		return self.qos
	
	def getTopic(self):
		return self.topic
	
	def getIP(self):
		return self.esp_ip
	
	def getDestIP(self):
		return self.broker_ip
	
	def getDup(self):
		return self.dup
	
	def incDup(self):
		self.dup = self.dup + 1		
	
	def printMsg(self):
		print('Source IP: %s' %self.esp_ip)
		print('Dest IP: %s' %self.broker_ip)
		print('Type: %i' %self.msg_type)
		print('Message Sequence Number: %s' %self.msg_ID)		
		print('Message Relative Time: %f' %self.arrived_time)
		print('Message Yield Time: %i' %self.ytime)
		print('Message QoS: %i' %self.qos)
		print('Topic: %s' %self.topic)
