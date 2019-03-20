#! /bin/bash

if [ $# -ne 3 ]; 
then
	echo "Use it as: ./start_tests test_type qos number_of_esp"
	echo "test_type = 0: no backgroud traffic --- 1: with backgroud traffic"
	echo "qos = 0 or 1"
	exit 1
fi


PWD=$(pwd)
if ! [ -d "$PWD/input" ]; then
	mkdir $PWD/input
fi
if ! [ -d "$PWD/output" ]; then
	mkdir $PWD/output
fi
if ! [ -d "$PWD/debug" ]; then
	mkdir $PWD/debug
fi


INPUT_FOLDER="$PWD/input"
CHECK_FOLDER="$PWD/debug"
OUTPUT_FOLDER="$PWD/output"
FORMAT="_.json"
PCAP_FORMAT="_.pcapng"

declare -a TIME=(1)
declare -a TIME_R=(1 2 3 4 5 6 7 8 9)
declare -a PAYLOAD=(10 100 500 1000 1500)
declare -a TESTE_1=(1 2 3)
declare -a PAYLOAD_TESTE_1=(10)



mosquitto_pub -h "127.0.0.1" -t "home/control" -m "off"
sleep 2



	for t in "${TIME[@]}"
	do
		for p in "${PAYLOAD_TESTE_1[@]}"
		do
			d=600
			mosquitto_pub -h "127.0.0.1" -t "home/control" -m "$t$p"
			sleep 1
			tshark -i "enp6s0" -a "duration:$d" -t "r" -w "$INPUT_FOLDER/temp.pcapng" > /dev/null 2>&1
			mosquitto_pub -h "127.0.0.1" -t "home/control" -m "off" 
			cp "$INPUT_FOLDER/temp.pcapng" "$CHECK_FOLDER/teste_$1_qos_$2_time_${TIME_R[$(($t-1))]}_nesp_$3_tmsg_$p$PCAP_FORMAT"
			sleep 1			
			tshark -2R "mqtt" -r "$INPUT_FOLDER/temp.pcapng" -T "json" > "$INPUT_FOLDER/test_$1_qos_$2_time_${TIME_R[$(($t-1))]}_nesp_$3_tmsg_$p$FORMAT"
		done
	done


rm $INPUT_FOLDER/temp.pcapng
