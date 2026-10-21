class PID:
    def __init__(self, kp, ki, kd, low=-1e9, high=1e9):
        self.kp,self.ki,self.kd=kp,ki,kd; self.low,self.high=low,high; self.i=0.0; self.prev=0.0
    def update(self,error,dt):
        self.i += error*dt
        d=(error-self.prev)/dt if dt else 0.0
        self.prev=error
        return max(self.low,min(self.high,self.kp*error+self.ki*self.i+self.kd*d))

def simulate_pid(target=1.0,steps=300,dt=0.02,kp=2.2,ki=0.4,kd=0.12):
    pid=PID(kp,ki,kd,-10,10); y=0.0; data=[]
    for k in range(steps):
        e=target-y; u=pid.update(e,dt); y += u*dt; data.append((k*dt,y,u,e))
    return data
