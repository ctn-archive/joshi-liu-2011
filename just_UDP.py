import nef
from numeric import *
import socket, sys, time
from struct import *

fmt_string = '!iI'
stride = 8
y_offset = 8
y_length = 8
x_offset = 1
x_length = 8

HOST = "127.0.0.1"
PORT = str(9000)
BUFFSIZE = 1024
ADDR = (HOST,PORT)


class event:
    def __init__(self,addr,time):
        self.time = time
        self.x = 127 - ((addr>>x_offset)&2**(x_length-1)-1)
        self.y = (addr>>y_offset)&2**(y_length-1)-1
        self.intensity = 1 - (addr & 1)
    def __repr__(self):
        return repr((self.intensity,self.x,self.y,self.time))

# Use the below for command line inputs
#host = sys.argv[1]
#textport = sys.argv[2]

host = HOST
textport = PORT



def sth(x):
	if x>0.1:
		return (x-.02)
	elif x<-0.1:
		return (x+.02)
	else:
		return 0

def sthn(x):
	return [sth(y) for y in x]

def zero(m,n):
    # Create zero matrix
    new_matrix = [[0 for row in range(n)] for col in range(m)]
    return new_matrix

def eye(n):
    new_matrix = [[(row == col) for row in range(n)] for col in range(n)]
    return new_matrix


def multmin(matrix1):
	# Matrix multiplication
	new_matrix = zero(len(matrix1),len(matrix1))
	for i in range(len(matrix1)):
		for j in range(len(matrix1)):
			if(i != j):
				for k in range(len(matrix1[0])):
					new_matrix[i][j] -= matrix1[i][k]*matrix1[j][k]

	return new_matrix


def transpose(matrix1):
	new_matrix = zero(len(matrix1[0]),len(matrix1))
	for i in range(len(matrix1)):
		for j in range(len(matrix1[0])):
			new_matrix[j][i] = matrix1[i][j]

	return new_matrix

f = open('clips.txt')

num_images = 200
clippre = []
for img in range(num_images):
        line = f.readline()
	imgpre=[]
	first = 0
	for char in range(len(line)):
		if (line[char] == ' '):
			last = char
			imgpre.append(round(float(line[first:last]),4))
			first = char+1
		
	clippre.append(imgpre)
		
f.close()


f = open('dictionary.txt')

num_dict = 128
PHI_pre = []
for img in range(num_dict):
        line = f.readline()
	dictpre=[]
	first = 0
	for char in range(len(line)):
		if (line[char] == ' '):
			last = char
			dictpre.append(round(float(line[first:last]),4))
			first = char+1
		
	PHI_pre.append(dictpre)	
f.close()


class MyInput(nef.SimpleNode):
	def origin_value(self):
		out_pre = zero(1,64)
		out = out_pre[0][:]
		t=int(self.t_start/.2)
		if(t > 0):
			data, addr = sock.recvfrom(BUFFSIZE)
    			#print addr
		        #print "sanity check:", addr[1]/4, (len(data)-4)/8, (len(data)-4)%8
    			if (((len(data)-4)%8 != 0)or ((len(data)-4)/8 ==0 )):
                               print "There is an error in the format of the packets sent"
                                #sys.exit(1)
    			tind = unpack("!i",data[0:4])
    			# print tind
    			event_list = []    
    			for iter in range(4,len(data)-4,stride):
        			message = unpack(fmt_string,data[iter:(iter+stride)]) 
        			#print message
        			event_list.append(event(message[0],message[1]))
    			# print event_list
    			# manipulate this incoming list of events however you want to.
			for events in event_list:
				if (events.x < 8 and events.y < 8):
					outind = int(events.x+8*(8-events.y-1))
					out[outind] = 2*int(events.intensity)-1
		return out



dict = array(PHI_pre)
numNodes = len(dict)
numInputs = len(dict[0])

recur =multmin(dict)
lif = array(eye(64))*0.9
dubeye = array(eye(64))*2

net=nef.Network('LCA',quick=True)
net.add_to(world)

#input=net.make_input('input',clippre[15])

#neuron=net.make_array('neurons',100,numNodes,intercept=(0,1))
outs=net.make('decoders',1,numInputs,mode='direct')
#neuron_value=net.make('neuron_value',1,numNodes,mode='direct')
myinput=MyInput('input')
net.add(myinput)

#net.connect(input,neuron,transform=dict)
#net.connect(myinput.getOrigin('value'),neuron,transform=dict)
#net.connect(neuron,neuron,transform=recur,func=sthn)
net.connect(myinput.getOrigin('value'),outs,transform=dubeye)
net.connect(outs,outs,transform=lif)
#net.connect(neuron,neuron_value,func=sthn)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST,int(PORT) ))

net.view(play=0.1)

#sim=net.network.simulator
#sim.run(0,1,0.001)

#print neuron_value.getOrigin('X').getValues().getValues()
#print outs.getOrigin('X').getValues().getValues()
