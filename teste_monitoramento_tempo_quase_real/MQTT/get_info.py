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
BROKER_IP = "IP_BROKER_HERE"
OUTPUT_DELIMITER = " "
ESP = []
temp_output = ""
temp_list = []


############################ PROCESS THE INPUTS AND GENERATE THE OUTPUTS:
def process(tshark_f):	
	ESP.append(esp_info.Esp("ESP0","ESP_IP_HERE",QOS_LEVEL,TIME_INTERVAL,MQTT_TOPIC_CONTROL))	
	tshark = json.load(tshark_f)
	process_json(tshark)

	temp = ESP[0].msgSec()
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
			yield_time = get_data(msg_a[2],"i") 
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
		
		msg = msg_info.MqttMsg(msg_t,msg_number,msg_len,time_rel,yield_time,msg_qos,msg_top,msg_top_len,src_ip,dst_ip)	
		
		for i in range(0,N_ESP):			## Appending messages on the right ESP								
			if msg.getIP() == ESP[i].getIP() or msg.getDestIP() == ESP[i].getIP():				
				ESP[i].setMsgs(msg)
		
	
def process_output(output,l,t):	
	for i in l:						
		if i[0] == t/10:			
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
		print (filename)
		params = filename.split("_")
		TEST_TYPE = get_data(params[1],"i")		## Test 1 = with background traffic
		QOS_LEVEL = get_data(params[3],"i")		## Only QoS 0 and 1
		TIME_INTERVAL = get_data(params[5],"f")		## Time interval between message sent by esp.
		N_ESP = get_data(params[7],"i")		## Number of ESPs on the network
		PAYLOAD_LEN = get_data(params[9],"i")		## Payload length		
		with open("input/"+f) as tshark_f:
			process(tshark_f)
			
	ci = 1
	cp = 1
	for t in range(1,19):
		if (t-1) % 2 != 0:
			with open("output/"+filename[0:18] + str(ci) + "_nesp_" + str(N_ESP) + "_tmsg_10.dat","w") as output:
				for i in range(0,len(temp_list[t-1])-2,2):
					if temp_list[t-1][i] < temp_list[t-1][i+2]:
						output.write(str(temp_list[t-1][i]) + " " + str(temp_list[t-1][i+1]) + "\n")
					else:					
						output.write(str(temp_list[t-1][i]) + " " + str(temp_list[t-1][i+1]) + "\n")											
						break
			ci = ci + 1
		else:
			with open("output/"+filename[0:18] + str(cp) + "_nesp_" + str(N_ESP) + "_tmsg_100.dat","w") as output:
				for i in range(0,len(temp_list[t-1])-2,2):
					if temp_list[t-1][i] < temp_list[t-1][i+2]:
						output.write(str(temp_list[t-1][i]) + " " + str(temp_list[t-1][i+1]) + "\n")
					else:					
						output.write(str(temp_list[t-1][i]) + " " + str(temp_list[t-1][i+1]) + "\n")											
						break			
			cp = cp + 1

	
if __name__ == "__main__":
	main()
