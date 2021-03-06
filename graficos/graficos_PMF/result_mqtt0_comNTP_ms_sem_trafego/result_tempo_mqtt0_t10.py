#import plotly.plotly as py
#import plotly.tools as tls
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.4f' % float(height),
                ha='center', va='bottom')

width=0.35

for t in [1,2,3,4,5,6,7,8,9]:
	x1 = []
	avg1 = []
	

	fig, ax = plt.subplots()

	with open("/home/arthurcosmi/PG_testes/teste_ms/MQTT/semTrafego/ArduinoMqtt-qos0-NTP/output/test_0_qos_0_time_"+str(t)+"_nesp_1_tmsg_10.dat","r") as f:
		for line in f:
			info = line.split(" ")
			x1.append(int(info[0]))
			avg1.append(int(info[1]))
			

	

	#x_pos = np.arange(len(x1))
	#p1 = ax.bar(x_pos,avg1,width,align="center",color="blue")
	#p1 = ax.plot(x_pos,avg1,alpha=0.6,linestyle=' ',color="blue",marker="o")
	#yerr=std,error_kw=dict(elinewidth=2,ecolor='black',alpha=0.65)


	# PMF:
	weights = np.ones_like(avg1)/len(avg1)
	plt.hist(avg1, bins=30, weights=weights, color="blue", normed=False)
	plt.xlabel('Pacotes recebidos por segundo')
	plt.ylabel('PMF')



	#x2 = []
	#avg2 = []
	#std2 = []

	#with open("/home/arthurcosmi/PG_testes/MQTT/comTrafego/qos0/teste2/output/test_1_qos_0_time_"+str(t)+"_nesp_1.dat","r") as f:
		#for line in f:
			#info = line.split(" ")
			#x2.append(int(info[0]))
			#avg2.append(float(info[4]))
			#std2.append(float(info[5]))

	#avg2.append(float(0.0))
			
	#p2 = ax.bar(x_pos + width,avg2,width,align="center",color="red",alpha=0.6)
	#p1 = ax.plot(x_pos,avg,alpha=0.6,color="blue",marker="o")
	#ax.set_title("Tempo Médio de Transmissão para MQTT QoS 0 com e sem Tráfego \n com intervalo de "+str(t)+" segundos")
	#ax.set_xticks(x_pos+width/2)
	#ax.set_xticklabels(x1)
	#ax.set_xlabel("Tempo do Experimento em Segundos")
	#ax.set_ylabel("Pacotes Recebidos por Segundo")
	#ax.legend((p1[0], p2[0]), ('sem Tráfego', 'com Tráfego'),shadow=True,fontsize='small')
	#ax.grid(True)
	#plt.xlim(x_pos[0]-1,x_pos[len(x1)-1] + 1)
	#plt.xlim(x_pos[0],551)
	#if t == 1:
		#plt.ylim(0,11)
	#elif t > 1 and t < 4:
		#plt.ylim(0,6)
	#elif t == 4:
		#plt.ylim(0,5)
	#else:
		#plt.ylim(0,3)
	#autolabel(p1)

	#plt.show()
	plt.savefig("tempo"+str(t)+"t10.eps",format='eps')
	#plt.savefig("tempo"+str(t)+"t10.png")
