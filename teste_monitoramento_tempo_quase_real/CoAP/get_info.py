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
OUTPUT_DELIMITER = " "
ESP = []
temp_output = ""
temp_list = []


############################ PROCESSING THE INPUTS AND GENERATE THE OUTPUTS:
def process(tshark_f):	
	esp_index = 0
	if len(ESP) == 0:
		ESP.append(esp_info.Esp("ESP0","ESP_IP",TIME_INTERVAL,COAP_RESOURCE_CONTROL))	

	tshark = json.load(tshark_f)
	process_json(tshark)
	
	temp = ESP[0].msgSec()
	temp_list.append(temp)
	#print(temp_list)
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
			icmp = packet["_source"]["layers"]["icmp"]["icmp.type"] 
		except KeyError:
			icmp = -1
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
			yield_time = get_data(msg_a[2],"i") 
		else:
			yield_time = -1
		
		msg = msg_info.CoapMsg(msg_t,msg_code,msg_number,msg_len,time_rel,yield_time,resource,src_ip,dst_ip,icmp)

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
	global TIME_INTERVAL
	global N_ESP
	global PAYLOAD_LEN
	file_list = os.listdir("./input")
	for f in file_list:
		filename = f		
		print(filename)
		params = filename.split("_")
		TEST_TYPE = get_data(params[1],"i")		## Test 1 = with background traffic		
		TIME_INTERVAL = get_data(params[5],"f")		## Time interval between message sent by esp.
		N_ESP = get_data(params[7],"i")		## Number of ESPs on the network
		N_ESP = 1
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
