import math, random
class TinyNetwork:
    def __init__(self,n_in,n_hidden,n_out,seed=1):
        r=random.Random(seed); self.w1=[[r.uniform(-0.6,0.6) for _ in range(n_in)] for _ in range(n_hidden)]; self.b1=[0]*n_hidden; self.w2=[[r.uniform(-0.5,0.5) for _ in range(n_hidden)] for _ in range(n_out)]; self.b2=[0]*n_out
    def forward(self,x):
        h=[math.tanh(sum(wi*xi for wi,xi in zip(w,row))+b) for row,b in zip(self.w1,self.b1)]
        return [math.tanh(sum(wi*hi for wi,hi in zip(row,h))+b) for row,b in zip(self.w2,self.b2)]
