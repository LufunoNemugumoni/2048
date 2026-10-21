from pathlib import Path
import csv, math, random
ROOT=Path(__file__).resolve().parents[2]
random.seed(7)
def run(n=3,steps=200,centralised=True):
    p=[[random.uniform(-3,3),random.uniform(-2,2)] for _ in range(n)]
    goal=[3,-2]
    total=0
    for _ in range(steps):
        if centralised:
            cx=sum(x for x,z in p)/n; cz=sum(z for x,z in p)/n
        for i,(x,z) in enumerate(p):
            tx,tz=goal
            if not centralised:
                others=p[:i]+p[i+1:]
                if others: tx=.8*tx+.2*sum(q[0] for q in others)/len(others); tz=.8*tz+.2*sum(q[1] for q in others)/len(others)
            dx, dz=tx-x,tz-z; d=math.hypot(dx,dz); total+=d
            if d>1e-6: p[i]=[x+0.03*dx/d,z+0.03*dz/d]
    return total/(n*steps)
out=ROOT/'results'/'centralised_vs_distributed.csv'
with open(out,'w',newline='') as f:
 w=csv.writer(f); w.writerow(['mode','mean_distance']); w.writerow(['centralised',run(centralised=True)]); w.writerow(['distributed',run(centralised=False)])
print('Experiment saved:',out)
