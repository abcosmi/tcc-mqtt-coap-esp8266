import esp_info
import msg_info
import json
import os
from operator import itemgetter


############################ GETTING DATA FROM LINE:
def get_data(line,op):
	result = -1
	if op == "f":	## Converting to float
		try:
			result = float(line)		## Removing the quotes.	
		except ValueError:
			result = -1
	elif op == "i":	## Converting to integer
		try:								
			result = int(float(line))
		except ValueError:
			result = -1

	return result

############################ CONSTANTS AND PARAMETERS BY FILE:
filename = ""
TEST_TYPE = -1		## Test 1 = with background traffic
QOS_LEVEL = -1		## Only QoS 0 and 1
TIME_INTERVAL = -1		## Time interval between message sent by esp.
N_ESP = -1		## Number of ESPs on the network
PAYLOAD_LEN = -1		## Payload length
MQTT_TOPIC_CONTROL = "home/control" ## Mqtt default topic to control the ESP
BROKER_IP = "192.168.0.25"
OUTPUT_DELIMITER = " "
ESP = []
temp_output = ""
temp_list = []


############################ PROCESS THE INPUTS AND GENERATE THE OUTPUTS:
def process(tshark_f):	
	ESP.append(esp_info.Esp("ESP0","192.168.0.23",QOS_LEVEL,TIME_INTERVAL,MQTT_TOPIC_CONTROL))	
	tshark = json.load(tshark_f)
	process_json(tshark)
	
	p = 0
	t = 0
	d = 0
	m = 0
	dp = 0
	
	if N_ESP > 1:
		for e in ESP:
			p = p + e.pubNumMsg()
			t = t + e.totNumMsg()
			d = d + e.dupNumMsg()
			m = m + e.deltaTime(BROKER_IP)
			dp = dp + e.stdDev(BROKER_IP)
			
			p = int(p/N_ESP)
			t = int(t/N_ESP)
			d = int(d/N_ESP)
			m = m/N_ESP
			dp = dp/N_ESP
	else:
		p = ESP[0].pubNumMsg()
		t = ESP[0].totNumMsg()
		d = ESP[0].dupNumMsg()
		m = ESP[0].deltaTime(BROKER_IP)
		dp = ESP[0].stdDev(BROKER_IP)
	

	
	temp = []
	temp.append(TIME_INTERVAL)
	temp.append(PAYLOAD_LEN)
	temp.append(p)
	temp.append(t)
	temp.append(d)
	temp.append(m)
	temp.append(dp)
	temp_list.append(temp)
	del ESP[0]

############################ CREATING A MESSAGE AND REDIRECT IT TO THE RIGHT ESP:
def process_json(tshark):
	buf = []
	for packet in tshark:
		try:
			src_ip = packet["_source"]["layers"]["ip"]["ip.src"] 
		except KeyError:
			src_ip = "no_ip"
		try:
			dst_ip = packet["_source"]["layers"]["ip"]["ip.dst"] 
		except KeyError:
			dst_ip = "no_ip"			
		try:			
			time_rel = get_data(packet["_source"]["layers"]["frame"]["frame.time_relative"],"f")
		except KeyError:
			time_rel = -1
		try:			
			msg_t = get_data(packet["_source"]["layers"]["mqtt"]["mqtt.hdrflags_tree"]["mqtt.msgtype"],"i") 			
		except KeyError:
			msg_t = -1
		try:
			msg_qos = get_data(packet["_source"]["layers"]["mqtt"]["mqtt.hdrflags_tree"]["mqtt.qos"],"i") 
		except KeyError:
			msg_qos = -1
		try:
			msg_len = get_data(packet["_source"]["layers"]["mqtt"]["mqtt.len"],"i") 
		except KeyError:
			msg_len = -1
		try:
			msg_top_len = get_data(packet["_source"]["layers"]["mqtt"]["mqtt.topic_len"],"i") 
		except KeyError:
			msg_top_len = -1
		try: 
			msg_top = packet["_source"]["layers"]["mqtt"]["mqtt.topic"] 
		except KeyError:
			msg_top = "no_topic"
		try:
			msg_qos1_id = get_data(packet["_source"]["layers"]["mqtt"]["mqtt.msgid"],"i") 
		except KeyError:
			msg_qos1_id = -1
		try:
			msg_dup = get_data(packet["_source"]["layers"]["mqtt"]["mqtt.hdrflags_tree"]["mqtt.dupflag"],"i") 
		except KeyError:
			msg_dup = 0
		try:
			
			msg_ = packet["_source"]["layers"]["mqtt"]["mqtt.msg"] 
		except KeyError:
			msg_ = "no_message"
		
		if msg_ != "no_message" and msg_top != MQTT_TOPIC_CONTROL:		## Treating Publish messages			
			msg_a = msg_.split("#")
			esp_id = msg_a[0]			
			if msg_qos1_id == -1:
				msg_number = get_data(msg_a[1],"i")	
			else:
				msg_number = msg_qos1_id
		else:														## Treating non-Publish messages			
			if msg_t == 4:
				msg_qos = 1
				msg_number = msg_qos1_id
			else:
				msg_number = -1
			esp_id = "get_ip"
		
		msg = msg_info.MqttMsg(msg_t,msg_number,msg_len,time_rel,msg_qos,msg_top,msg_top_len,src_ip,dst_ip)		## Create a new message		
		for i in range(0,N_ESP):			## Appending messages on the right ESP								
			if msg.getIP() == ESP[i].getIP() or msg.getDestIP() == ESP[i].getIP():				
				ESP[i].setMsgs(msg)
		

## Save the output file on the right way	
def process_output(output,l,t):	
	for i in l:				
		if i[0] == t:			
			output.write(str(i[1]) + OUTPUT_DELIMITER + str(i[2]) + OUTPUT_DELIMITER + str(i[3]) + OUTPUT_DELIMITER + str(i[4]) + OUTPUT_DELIMITER + str(i[5]) + OUTPUT_DELIMITER + str(i[6]) + "\n")
	


def main():	
	global filename
	global TEST_TYPE
	global QOS_LEVEL
	global TIME_INTERVAL
	global N_ESP
	global PAYLOAD_LEN
	file_list = os.listdir("./input")
	for f in file_list:
		filename = f	
		print(filename)
		params = filename.split("_")
		TEST_TYPE = get_data(params[1],"i")		## Test 1 = with background traffic
		QOS_LEVEL = get_data(params[3],"i")		## Only QoS 0 and 1
		TIME_INTERVAL = get_data(params[5],"i")		## Time interval between message sent by esp.
		N_ESP = get_data(params[7],"i")		## Number of ESPs on the network
		PAYLOAD_LEN = get_data(params[9],"i")		## Payload length		
		with open("input/"+f) as tshark_f:
			process(tshark_f)
	
    ## Keep the output sorted by payload lenght
	l = sorted(temp_list,key=itemgetter(0,1))
	
	for t in [1,5,10,30,60]:
		with open("output/"+filename[0:18] + str(t) + "_nesp_" + str(N_ESP) + ".dat","w") as output:
			process_output(output,l,t)
	
if __name__ == "__main__":
	main()
