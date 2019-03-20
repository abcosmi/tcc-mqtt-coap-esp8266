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
	per1 = []
	#std1 = []

	fig, ax = plt.subplots()

	with open("/home/arthurcosmi/PG_testes/coap/testes/comTrafego/teste2-2/output/test_1_qos_1_time_"+str(t)+"_nesp_1.dat","r") as f:
		for line in f:
			info = line.split(" ")
			x1.append(int(info[0]))
			pub = int(info[1])
			tot = int(info[2])
			dup = int(info[3])
			per1.append((dup/tot)*100)
			#per1.append((pub/tot)*100*2)
			

	per1.pop()
	#std1.pop()
	print(len(per1))
	x_pos = np.arange(len(x1)-1)
	p1 = ax.bar(x_pos,per1,width,align="center",color="blue",alpha=0.6)
	#yerr=std,error_kw=dict(elinewidth=2,ecolor='black',alpha=0.65)


	x2 = []
	per2 = []
	std2 = []

	with open("/home/arthurcosmi/PG_testes/coap/testes/semTrafego/teste2-2/output/test_0_qos_1_time_"+str(t)+"_nesp_1.dat","r") as f:
		for line in f:
			info = line.split(" ")
			x2.append(int(info[0]))
			pub = int(info[1])
			tot = int(info[2])
			dup = int(info[3])
			per2.append((dup/tot)*100)			
			#per2.append((pub/tot)*100*2)

	#avg2.append(float(0.0))
	per2.pop()
	print(len(per2))		
	p2 = ax.bar(x_pos + width,per2,width,align="center",color="red",alpha=0.6)
	#p1 = ax.plot(x_pos,avg,alpha=0.6,color="blue",marker="o")
	#ax.set_title("Porcentagem de Mensagens Enviadas MQTT QoS 1 e CoAP \n com intervalo de "+str(t)+" segundos")
	ax.set_xticks(x_pos+width/2)
	ax.set_xticklabels(x1)
	ax.set_xlabel("Tamanho do Payload (em Bytes)")
	ax.set_ylabel("Porcentagem de Mensagens Enviadas")
	ax.legend((p1[0], p2[0]), ('com Tráfego', 'Sem Tráfego'),shadow=True,fontsize='small')
	ax.grid(True)

	#autolabel(p1)

	#plt.show()
	plt.savefig("msg"+str(t)+".png")
