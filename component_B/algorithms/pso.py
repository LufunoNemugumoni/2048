import random,math
def pso(target=(0,0),n=8,it=20):
 p=[[random.uniform(-3,3),random.uniform(-3,3)] for _ in range(n)];best=min(p,key=lambda x:math.hypot(x[0]-target[0],x[1]-target[1]));return best
