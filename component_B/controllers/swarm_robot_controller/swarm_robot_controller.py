from controller import Robot
r=Robot();T=64
ps=[r.getDevice('ps%d'%i) for i in range(8)]
for s in ps:s.enable(T)
l=r.getDevice('left wheel motor');rr=r.getDevice('right wheel motor');l.setPosition(float('inf'));rr.setPosition(float('inf'))
em=r.getDevice('emitter');rx=r.getDevice('receiver');rx.enable(T)
while r.step(T)!=-1:
 v=[s.getValue() for s in ps];em.send(r.getName().encode());
 while rx.getQueueLength():rx.nextPacket()
 front=max(v[0],v[1],v[7]);vl=vr=2.8
 if front>80:vl,vr=-1.5,2.8
 elif max(v[5],v[6])>max(v[2],v[3])+8:vl,vr=2.2,3.2
 elif max(v[2],v[3])>max(v[5],v[6])+8:vl,vr=3.2,2.2
 l.setVelocity(vl);rr.setVelocity(vr)
