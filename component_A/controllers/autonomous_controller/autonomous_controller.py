from controller import Robot
import os,csv
r=Robot(); T=64
ps=[r.getDevice('ps%d'%i) for i in range(8)]
for s in ps:s.enable(T)
l=r.getDevice('left wheel motor'); rr=r.getDevice('right wheel motor'); l.setPosition(float('inf'));rr.setPosition(float('inf'))
g=r.getDevice('gps');g.enable(T); c=r.getDevice('compass');c.enable(T); cam=r.getDevice('camera');cam.enable(T)
base=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'));os.makedirs(os.path.join(base,'data'),exist_ok=True)
f=open(os.path.join(base,'data','navigation.csv'),'w');w=csv.writer(f);w.writerow(['time','x','z','front'])
try:
 while r.step(T)!=-1:
  v=[s.getValue() for s in ps];p=g.getValues();front=max(v[0],v[1],v[7]); vl=vr=3.0
  if front>85:vl,vr=-1.5,3.0
  elif max(v[5],v[6])>max(v[2],v[3])+8:vl,vr=2.2,3.2
  elif max(v[2],v[3])>max(v[5],v[6])+8:vl,vr=3.2,2.2
  l.setVelocity(vl);rr.setVelocity(vr);w.writerow([r.getTime(),p[0],p[2],front]);f.flush()
finally:f.close()
