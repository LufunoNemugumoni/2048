from controller import Robot
import math, csv, json, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'algorithms')); sys.path.insert(0,str(ROOT/'ml'))
from pso import pso_step
from neural_network import TinyNetwork
TIME_STEP=64; MAX_SPEED=6.28
robot=Robot(); rid=int(robot.getControllerArgs() or '1')
left=robot.getDevice('left wheel motor'); right=robot.getDevice('right wheel motor')
left.setPosition(float('inf')); right.setPosition(float('inf')); left.setVelocity(0); right.setVelocity(0)
ps=[robot.getDevice(f'ps{i}') for i in range(8)]
for s in ps: s.enable(TIME_STEP)
gps=robot.getDevice('gps'); gps.enable(TIME_STEP)
compass=robot.getDevice('compass'); compass.enable(TIME_STEP)
em=robot.getDevice('emitter'); rx=robot.getDevice('receiver'); rx.enable(TIME_STEP)
net=TinyNetwork(6,5,2,seed=rid)
# common swarm target; PSO perturbs each agent target locally
base_goal=(3.0,-2.2)
log=[]; step=0

def heading(v): return math.atan2(v[0],v[2])
def wrap(a):
 while a>math.pi:a-=2*math.pi
 while a<-math.pi:a+=2*math.pi
 return a

while robot.step(TIME_STEP)!=-1:
 x,_,z=gps.getValues(); h=heading(compass.getValues())
 peers=[]
 while rx.getQueueLength()>0:
  try: peers.append(json.loads(rx.getString()))
  except: pass
  rx.nextPacket()
 msg=json.dumps({'id':rid,'x':x,'z':z}); em.send(msg.encode('utf-8'))
 # Consensus: average the goal estimate with peer positions, then move toward shared objective.
 gx,gz=base_goal
 if peers:
  meanx=sum(p['x'] for p in peers)/len(peers); meanz=sum(p['z'] for p in peers)/len(peers)
  gx=0.75*base_goal[0]+0.25*meanx; gz=0.75*base_goal[1]+0.25*meanz
 # PSO-inspired perturbation encourages role separation.
 pgx,pgz=pso_step((gx,gz),rid,step)
 err=math.atan2(pgz-z,pgx-x)-h; err=wrap(err)
 # Tiny neural policy: inputs are normalized front/side sensor evidence + goal direction.
 vals=[s.getValue()/4096.0 for s in ps]
 features=[min(vals[2],1),min(vals[3],1),min(vals[4],1),min(vals[5],1),math.cos(err),math.sin(err)]
 turn_bias=net.forward(features)[0]
 front=max(vals[2],vals[3],vals[4],vals[5])
 avoid=(vals[7]+vals[6])-(vals[0]+vals[1])
 turn=2.0*err+1.2*turn_bias+0.9*avoid
 if front>0.5: turn += 2.5 if vals[0]+vals[1] < vals[6]+vals[7] else -2.5
 base=3.2 if math.hypot(gx-x,gz-z)>0.5 else 1.5
 l=max(-MAX_SPEED,min(MAX_SPEED,base-turn)); r=max(-MAX_SPEED,min(MAX_SPEED,base+turn))
 left.setVelocity(l); right.setVelocity(r)
 log.append((step,rid,x,z,len(peers),gx,gz))
 if step%25==0:
  out=ROOT/'data'/f'robot_{rid}_log.csv'
  with open(out,'w',newline='') as f:
   w=csv.writer(f); w.writerow(['step','robot','x','z','peer_count','consensus_x','consensus_z']); w.writerows(log)
 step+=1
