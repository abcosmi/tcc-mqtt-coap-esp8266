#import plotly.plotly as py
#import plotly.tools as tls
import matplotlib.pyplot as plt
import numpy as np



plt.rcParams.update({'font.size': 13})




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

for t in [1,2,4,7]:
	x1 = []
	avg1 = []
	avg2 = []
	avg3 = []
	

	fig, ax = plt.subplots()

	with open("/home/arthurcosmi/DocWindows/PG/teste_ms/CoAP/semTrafego/semTrafego/comNTP/output/test_0_qos_1_time_"+str(t)+"_nesp_1_tmsg_10.dat","r") as f:
		for line in f:
			info = line.split(" ")
			x1.append(int(info[0]))
			avg1.append(int(info[1]))
			


	with open("/home/arthurcosmi/PG_testes/teste_ms/MQTT/semTrafego/ArduinoMqtt-qos0-NTP/output/test_0_qos_0_time_"+str(t)+"_nesp_1_tmsg_10.dat","r") as f1:
		for line in f1:
			info = line.split(" ")
			x1.append(int(info[0]))
			avg2.append(int(info[1]))
			
			

			

	
	

	x_pos = np.arange(len(x1))
	#p1 = ax.bar(x_pos,avg1,width,align="center",color="blue")
	# essa linha ----->  p1 = ax.plot(x_pos,avg1,alpha=0.6,linestyle=' ',color="blue",marker="o")
	
	
	# PMF deu certo:
	weights1 = np.ones_like(avg1)/len(avg1)
	weights2 = np.ones_like(avg2)/len(avg2)
	#weights3 = np.ones_like(avg3)/len(avg3)
	#plt.hist(avg1, bins=30, weights=weights1, color="blue", normed=False, alpha=0.5)
	#plt.hist(avg2, bins=30, weights=weights2, color="red", normed=False, alpha=0.5)
	#plt.hist(avg3, bins=30, weights=weights3, color="green", normed=False, alpha=0.5)
	plt.hist([avg1,avg2],weights=[weights1,weights2],bins=15, color=["blue","green"], normed=False, alpha=0.5)


	if t == 1:
		x = np.arange(0,11,step=1)
	elif t == 2:
		x = np.arange(0,6,step=1)
	elif t == 4:
		x = np.arange(0,4,step=1)
	else:
		x = np.arange(0,3,step=1)
	plt.xticks(x,x)

	


	plt.xlabel('Pacotes recebidos por segundo')
	plt.ylabel('PMF')
	plt.legend(["CoAP","MQTT"])
	#plt.title('CoAP com trafego ' + str(t*100) + ' ms')
	#plt.show()
	
	# tentativa2 CDF deu certo, mas nãp será utilizada.
	#num_bins = 50
	#counts, bin_edges = np.histogram (avg1, bins=num_bins, normed=True)
	#cdf = np.cumsum (counts)
	#plt.plot (bin_edges[1:], cdf/cdf[-1])
	#plt.xlabel('Pacotes capturados por segundo')
	#plt.ylabel('CDF')
	#plt.title('CoAP com trafego ' + str(t*100) + ' ms')
	#plt.show()
	
	# tentativa1:
	#x = np.sort(avg1)
	#y = np.arange(1,len(x)+1)/len(x)
	#plt.plot(x,y,linestyle='none',marker='.')
	#plt.xlabel('Porcentagem de pacotes')
	#plt.ylabel('CDF')
	#plt.margins(0.02)
	#plt.show()
	
	
	
	


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
	#ax.set_xticklabels([0,2,4,6,8,10])
	
	#ax.set_xlabel("Tempo do Experimento em Segundos")
	#ax.set_ylabel("Pacotes Recebidos por Segundo")
	
	#ax.legend((p1[0], p2[0]), ('sem Tráfego', 'com Tráfego'),shadow=True,fontsize='small')
	
	#ax.grid(True)
	#plt.xlim(x_pos[0],551)
	#if t == 1:
#		plt.ylim(0,11)
#	elif t > 1 and t < 4:
#		plt.ylim(0,6)
#	elif t == 4:
#		plt.ylim(0,5)
#	else:
#		plt.ylim(0,3)
	#autolabel(p1)

	#plt.show()
	plt.savefig("tempo"+str(t)+"t10.eps",format='eps')
	#plt.savefig("tempo"+str(t)+"t10.png")
