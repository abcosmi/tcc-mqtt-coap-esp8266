#import plotly.plotly as py
#import plotly.tools as tls
import matplotlib.pyplot as plt
import numpy as np


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

for t in [1,5,10,30,60]:
	x1 = []
	avg1 = []
	std1 = []

	fig, ax = plt.subplots()

	with open("/home/arthurcosmi/PG_testes/coap/testes/semTrafego/teste2-3/output/test_0_qos_1_time_"+str(t)+"_nesp_1.dat","r") as f:
		for line in f:
			info = line.split(" ")
			x1.append(int(info[0]))
			avg1.append(float(info[4]))
			std1.append(float(info[5]))

	

	x_pos = np.arange(len(x1))
	p1 = ax.bar(x_pos,avg1,width,align="center",color="blue")
	#yerr=std,error_kw=dict(elinewidth=2,ecolor='black',alpha=0.65)


	x2 = []
	avg2 = []
	std2 = []

	with open("/home/arthurcosmi/PG_testes/coap/testes/comTrafego/teste2-2/output/test_1_qos_1_time_"+str(t)+"_nesp_1.dat","r") as f:
		for line in f:
			info = line.split(" ")
			x2.append(int(info[0]))
			avg2.append(float(info[4]))
			std2.append(float(info[5]))

	#avg2.append(float(0.0))
			
	p2 = ax.bar(x_pos + width,avg2,width,align="center",color="red",alpha=0.6)
	#p1 = ax.plot(x_pos,avg,alpha=0.6,color="blue",marker="o")
	#ax.set_title("Tempo Médio de Transmissão para CoAP com e sem Tráfego \n com intervalo de "+str(t)+" segundos")
	ax.set_xticks(x_pos+width/2)
	ax.set_xticklabels(x1)
	ax.set_xlabel("Tamanho do Payload (bytes)")
	ax.set_ylabel("Tempo Médio (ms)")
	ax.legend((p1[0], p2[0]), ('sem Tráfego', 'com Tráfego'),shadow=True,fontsize='small')
	ax.grid(True)
	#plt.xlim(x_pos[0]-1,x_pos[4] + 1)
	plt.ylim(0,0.045)
	#autolabel(p1)

	#plt.show()
	plt.savefig("tempo"+str(t)+".eps",format='eps')
	#plt.savefig("tempo"+str(t)+".png")
