import nef
import math

from com.jmatio.io import MatFileReader

data=array(MatFileReader("/Users/siddharth/Code/nengo/file.mat").getMLArray("data").array)

#print data
#print data.T
dt = .001
mdt = 5 #multiplier for time period

class Input(nef.SimpleNode):
    def origin_matlab(self):
        t=self.t_start
#	index = 99;
	index=int(t/(mdt*dt))%100
        return data.T[index]

def feedback(x):
	return -1*x[0]*x[1]
        
net=nef.Network('Matlab Test')
A=net.make("A",neurons=150,radius=150,dimensions=1)
input=Input('input')
net.add(input)
net.connect(input.getOrigin('matlab'),A)
#net.add_to(world)
B=net.make("B",neurons=450,radius=75,dimensions=2) # mode='direct')
net.connect(A,B,transform=[.1,0])
omega=20*math.pi
net.connect(B,B,transform=[[.75,-omega*0.1],[omega*0.1,.75]],pstc=.1)




#sim=net.network.simulator
#t=0
#dt=0.001
#while t<2:
#	sim.run(t,t+dt)
#	x=B.getOrigin('X').getValues().getValues()
#	t+=dt


net.add_to(world)


# transpose
#input.functions=[ca.nengo.math.impl.PiecewiseConstantFunction([0.2,0.3,0.44,0.54,0.8,0.9],[0,5,0,-10,0,5,0])]
# this kind of piece wise linear function has values on one side and time at the other side.

