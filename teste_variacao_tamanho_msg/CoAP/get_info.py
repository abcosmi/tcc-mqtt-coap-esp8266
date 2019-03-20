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
TIME_INTERVAL = -1		## Time interval between message sent by esp.
N_ESP = 1		## Number of ESPs on the network
PAYLOAD_LEN = -1		## Payload length
COAP_RESOURCE_CONTROL = "lamp" ## Mqtt default topic to control the ESP
BROKER_IP = "192.168.0.25"
OUTPUT_DELIMITER = " "
ESP = []
temp_output = ""
temp_list = []


############################ PROCESSING THE INPUTS AND GENERATE THE OUTPUTS:
def process(tshark_f):	
	esp_index = 0
	if len(ESP) == 0:
		ESP.append(esp_info.Esp("ESP0","192.168.0.23",TIME_INTERVAL,COAP_RESOURCE_CONTROL))	

	tshark = json.load(tshark_f)
	process_json(tshark)
	
	g = 0
	t = 0
	d = 0
	m = 0
	dp = 0
	
	if N_ESP > 1:
		for e in ESP:
			g = g + e.getNumMsg()
			t = t + e.totNumMsg()
			d = d + e.dupNumMsg()
			m = m + e.deltaTime(BROKER_IP)
			dp = dp + e.stdDev(BROKER_IP)
			
			g = int(g/N_ESP)
			t = int(t/N_ESP)
			d = int(d/N_ESP)
			m = m/N_ESP
			dp = dp/N_ESP
	else:
		g = ESP[0].getNumMsg()
		t = ESP[0].totNumMsg()
		d = ESP[0].dupNumMsg()
		m = ESP[0].deltaTime(BROKER_IP)
		dp = ESP[0].stdDev(BROKER_IP)
	

	
	temp = []
	temp.append(TIME_INTERVAL)
	temp.append(PAYLOAD_LEN)
	temp.append(g)
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
			msg_t = get_data(packet["_source"]["layers"]["coap"]["coap.type"],"i") 			
		except KeyError:
			msg_t = -1
		try:
			msg_code = get_data(packet["_source"]["layers"]["coap"]["coap.code"],"i") 			
		except KeyError:
			msg_code = -1
		try:
			msg_number = get_data(packet["_source"]["layers"]["coap"]["coap.mid"],"i")
		except KeyError:
			msg_number = -1
		try:
			msg_len = get_data(packet["_source"]["layers"]["coap"]["coap.payload_length"],"i") 
		except KeyError:
			msg_len = -1
		try: 
			resource = packet["_source"]["layers"]["coap"]["coap.opt.name_tree"]["coap.opt.uri_path"]
		except KeyError:
			resource = "no_resource"
		try:
			msg_j = packet["_source"]["layers"]["data-text-lines"]			
			msg_ = list(msg_j.keys())[0]
		except KeyError:
			msg_ = "no_message"
		
		if msg_ != "no_message":		## Treating Publish messages			
			msg_a = msg_.split("#")
			esp_id = msg_a[0]			
		
		msg = msg_info.CoapMsg(msg_t,msg_code,msg_number,msg_len,time_rel,resource,src_ip,dst_ip)						
		for i in range(0,N_ESP):			## Appending messages on the right ESP								
			if msg.getIP() == ESP[i].getIP() or msg.getDestIP() == ESP[i].getIP():				
				ESP[i].setMsgs(msg)
				
		
	
def process_output(output,l,t):	
	for i in l:				
		if i[0] == t:			
			output.write(str(i[1]) + OUTPUT_DELIMITER + str(i[2]) + OUTPUT_DELIMITER + str(i[3]) + OUTPUT_DELIMITER + str(i[4]) + OUTPUT_DELIMITER + str(i[5]) + OUTPUT_DELIMITER + str(i[6]) + "\n")
	


def main():	
	global filename
	global TEST_TYPE
	global TIME_INTERVAL
	global N_ESP
	global PAYLOAD_LEN
	file_list = os.listdir("./input")
	for f in file_list:
		filename = f		
		params = filename.split("_")
		TEST_TYPE = get_data(params[1],"i")		## Test 1 = with background traffic		
		TIME_INTERVAL = get_data(params[5],"i")		## Time interval between message sent by esp.
		N_ESP = get_data(params[7],"i")		## Number of ESPs on the network
		N_ESP = 1
		PAYLOAD_LEN = get_data(params[9],"i")		## Payload length		
		with open("input/"+f) as tshark_f:
			process(tshark_f)
	
	l = sorted(temp_list,key=itemgetter(0,1))
	
	for t in [1,5,10,30,60]:
		with open("output/"+filename[0:18] + str(t) + "_nesp_" + str(N_ESP) + ".dat","w") as output:
			process_output(output,l,t)
	
if __name__ == "__main__":
	main()
