import nef
import math

from com.jmatio.io import MatFileReader

data_c=array(MatFileReader("/Users/siddharth/Code/nengo/file48d3.mat").getMLArray("data_file").array)
#data_c=array(MatFileReader("/Users/siddharth/Code/nengo/file12d2.mat").getMLArray("data_file").array)
#data_c=array(MatFileReader("/Users/siddharth/Code/nengo/file4d4.mat").getMLArray("multidim").array)
data_r=array(MatFileReader("/Users/siddharth/Code/nengo/file2d2.mat").getMLArray("data").array)
#data=MatFileReader("/Users/siddharth/Code/nengo/file4d.mat").getMLArray("data").array
#data=array(MatFileReader("/Users/siddharth/Code/nengo/file4d.mat").getMLArray("data")) #.array)

#print data
#print data.T
dt = .001
mdt = 5 #multiplier for time period
c_stride = 12

# Define input population ... 
class Input_1(nef.SimpleNode):
    def origin_matlab(self):
        t=self.t_start
#	index = 99;
	index=int(t/(mdt*dt))%23
#	print size(data)
	return data_c.T[index,0:(c_stride-1)]


class Input_2(nef.SimpleNode):
    def origin_matlab(self):
        t=self.t_start
#	index = 99;
	index=int(t/(mdt*dt))%23
#	print size(data)
	return data_c.T[index,c_stride:2*c_stride-1]

class Input_3(nef.SimpleNode):
    def origin_matlab(self):
        t=self.t_start
#	index = 99;
	index=int(t/(mdt*dt))%23
#	print size(data)
	return data_c.T[index,2*c_stride:3*c_stride-1]

class Input_4(nef.SimpleNode):
    def origin_matlab(self):
        t=self.t_start
#	index = 99;
	index=int(t/(mdt*dt))%23
#	print size(data)
	return data_c.T[index,3*c_stride:4*c_stride-1]


class Input_5(nef.SimpleNode):
    def origin_matlab(self):
        t=self.t_start
#	index = 99;
	index=int(t/(mdt*dt))%50
#	print size(data)
	return data_r.T[index,:]

# How do I create this multi-dimensional system? - make_array

def feedback(x):
	return -1*x[0]*x[1]

#eye_4 = [[.2,0,0,0],[0,.2,0,0],[0,0,.2,0],[0,0,0,.1]]
cs = .075#cochlea_scaling
input_scale1 = [cs, cs, cs, cs, cs, cs, cs, cs, cs, cs, cs, cs]
#input_scale1 = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .1]


# Createa network
net=nef.Network('Matlab Test')

# create input populations
Cochlea1=net.make_array("Cochlea1", neurons=128, radius=1, length=12, encoders=[[1]])
Cochlea2=net.make_array("Cochlea2", neurons=128, radius=1, length=12, encoders=[[1]])
Cochlea3=net.make_array("Cochlea3", neurons=128, radius=1, length=12, encoders=[[1]])
Cochlea4=net.make_array("Cochlea4", neurons=128, radius=1, length=12, encoders=[[1]])

# connect input to input populations
input1=Input_1('input1')
net.add(input1)
net.connect(input1.getOrigin('matlab'),Cochlea1,pstc=.001)
thresh1=net.make('thresh1',100,1,intercept=(0.8,0.99))
net.connect(Cochlea1,thresh1,transform=input_scale1,pstc=.001)


input2=Input_2('input2')
net.add(input2)
net.connect(input2.getOrigin('matlab'),Cochlea2,pstc=.001)
thresh2=net.make('thresh2',100,1,intercept=(0.8,0.99))
net.connect(Cochlea2,thresh2,transform=input_scale1,pstc=.001)


input3=Input_3('input3')
net.add(input3)
net.connect(input3.getOrigin('matlab'),Cochlea3,pstc=.001)
thresh3=net.make('thresh3',100,1,intercept=(0.8,0.99))
net.connect(Cochlea3,thresh3,transform=input_scale1,pstc=.001)


input4=Input_4('input4')
net.add(input4)
net.connect(input4.getOrigin('matlab'),Cochlea4,pstc=.001)
thresh4=net.make('thresh4',100,1,intercept=(0.8,0.99))
net.connect(Cochlea4,thresh4,transform=input_scale1,pstc=.001)


def thresholdfunc(x):
	if x[0]>0.85: return 1
	else: return 0

# connect the results population
result1=net.make('result1',100,1)
result2=net.make('result2',100,1)
result3=net.make('result3',100,1)
result4=net.make('result4',100,1)

#net.connect(thresh,result)
net.connect(thresh1,result1,func=thresholdfunc,pstc=.001)
net.connect(thresh2,result2,func=thresholdfunc,pstc=.001)
net.connect(thresh3,result3,func=thresholdfunc,pstc=.001)
net.connect(thresh4,result4,func=thresholdfunc,pstc=.001)

# cascade multipliers to "results" 
#A=net.make('A',100,1,radius=10,quick=True)
#B=net.make('B',100,1,radius=10,quick=True,storage_code='B')

def product(x):
    return x[0]*x[1]

def product2(x):
    return 2*x[0]*x[1]

Comb1=net.make('Combined1',256,2,radius=1.5,quick=True)
mult_result1=net.make('mult_result1',100,1,radius=1,quick=True,storage_code='mult_result1',intercept=(0.2,0.99),encoders=[[1]])
net.connect(result1,Comb1,transform=[1,0],pstc=.001)
net.connect(result2,Comb1,transform=[0,1],pstc=.001)
net.connect(Comb1,mult_result1,func=product2,pstc=.001)

Comb2=net.make('Combined2',256,2,radius=1.5,quick=True)
mult_result2=net.make('mult_result2',100,1,radius=1,quick=True,storage_code='mult_result2',intercept=(0.2,0.99),encoders=[[1]])
net.connect(result3,Comb2,transform=[1,0],pstc=.001)
net.connect(result4,Comb2,transform=[0,1],pstc=.001)
net.connect(Comb2,mult_result2,func=product2,pstc=.001)

# feed the outputs of the multiplier into the next multiplier layer
Comb3=net.make('Combined3',256,2,radius=1.5,quick=True)
mult_result3=net.make('mult_result3',100,1,radius=1,quick=True,storage_code='mult_result3',intercept=(0.2,0.99),encoders=[[1]])

net.connect(mult_result1,Comb3,transform=[1,0],pstc=.001)
net.connect(mult_result2,Comb3,transform=[0,1],pstc=.001)
net.connect(Comb3,mult_result3,func=product2,pstc=.001)



Comb4=net.make('Combined4',256,2,radius=1.5,quick=True)





net.add_to(world)


#net.connect(Cochlea,thresh,transform=[[.75,-omega*0.1],[omega*0.1,.75]],pstc=.1)
#net.add_to(world)
#B=net.make("B",neurons=450,radius=75,dimensions=2) # mode='direct')
#net.connect(A,B,transform=[.1,0])
#omega=20*math.pi
#net.connect(B,B,transform=[[.75,-omega*0.1],[omega*0.1,.75]],pstc=.1)

#sim=net.network.simulator
#t=0
#dt=0.001
#while t<2:
#	sim.run(t,t+dt)
#	x=B.getOrigin('X').getValues().getValues()
#	t+=dt




# transpose
#input.functions=[ca.nengo.math.impl.PiecewiseConstantFunction([0.2,0.3,0.44,0.54,0.8,0.9],[0,5,0,-10,0,5,0])]
# this kind of piece wise linear function has values on one side and time at the other side.

