#! /bin/bash

if [ $# -ne 2 ]; 
then
	echo "Use it as: ./start_tests test_type number_of_esp"
	echo "test_type = 0: no backgroud traffic --- 1: with backgroud traffic"
	echo "Number of esp"
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


declare -a TIME=(1 2 4 7)
declare -a TIME_R=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
declare -a PAYLOAD=(100)

for t in "${TIME[@]}"
do
	for p in "${PAYLOAD[@]}"
	do		
		tmp=0
		coap-client -m "GET" "coap://CLIENT_IP_HERE/time?ticks"
		d=600
		tshark -i "enp6s0" -a "duration:$d" -t "r" -w "$INPUT_FOLDER/temp.pcapng" -q &
				
		while (( $(echo "$tmp <= $d" | bc -l) ));
		do			
			echo "$tmp"
			coap-client -m "GET" "coap://CLIENT_IP_HERE/time?ticks"
			sleep ${TIME_R[$(($t-1))]}
			tmp=$(perl -e "print $tmp + ${TIME_R[$(($t-1))]}")						
		done
		cp "$INPUT_FOLDER/temp.pcapng" "$CHECK_FOLDER/test_$1_qos_1_time_${TIME_R[$(($t-1))]}_nesp_$2_tmsg_$p$PCAP_FORMAT"
		sleep 1		
		tshark -2R "coap" -r "$INPUT_FOLDER/temp.pcapng" -T "json" > "$INPUT_FOLDER/test_$1_qos_1_time_${TIME_R[$(($t-1))]}_nesp_$2_tmsg_$p$FORMAT"
	done
done

rm $INPUT_FOLDER/temp.pcapng
