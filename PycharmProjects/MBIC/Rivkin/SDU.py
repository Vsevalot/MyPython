import random
import matplotlib.pyplot as plt

epsiland=0.5
dt=0.0001
x1=[0]
y1=[1]
x2=[0]
y2=[1]
a1=0.5
a2=1.5
D=0
for i in range(700000):
    x1.append(x1[-1]+(x1[-1]-x1[-1]**3/3-y1[-1])*dt/epsiland)
    y1.append(y1[-1]+(x1[-2]+a1+D*random.random())*dt)
    x2.append(x2[-1]+(x2[-1]-x2[-1]**3/3-y1[-1])*dt/epsiland)
    y2.append(y2[-1]+(x2[-2]+a2+D*random.random())*dt)

t=list(range(len(x1)))
plt.figure(figsize=(20.0, 15.0))
plt.subplot(2,3,1)
plt.plot(t,x1)
plt.xlabel('time')
plt.title("x(t), a = "+str(a1)+", eps = "+str(epsiland)+"; D = (0,"+str(D)+')')
plt.subplot(2,3,2)
plt.plot(t,y1)
plt.xlabel('time')
plt.title("y(t), a = "+str(a1)+", eps = "+str(epsiland)+"; D = (0,"+str(D)+')')
plt.subplot(2,3,3)
plt.plot(x1,y1)
plt.xlabel('x')
plt.ylabel('y')
plt.subplot(2,3,4)
plt.plot(t,x2)
plt.xlabel('time')
plt.title("x(t), a = "+str(a2)+", eps = "+str(epsiland)+"; D = (0,"+str(D)+')')
plt.subplot(2,3,5)
plt.plot(t,y2)
plt.xlabel('time')
plt.title("y(t), a = "+str(a2)+", eps = "+str(epsiland)+"; D = (0,"+str(D)+')')
plt.subplot(2,3,6)
plt.plot(x2,y2)
plt.xlabel('x')
plt.ylabel('y')
figName="a1="+str(a1)+"_a2="+str(a2)+"_eps="+str(epsiland)+"_D="+str(D)
plt.savefig("C:\\Users\\УрФУ\\Desktop\\Rivkin\\lab1\\"+figName+".jpg")