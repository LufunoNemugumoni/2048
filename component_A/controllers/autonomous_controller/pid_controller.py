class PID:
    def __init__(self, kp, ki, kd, low=-1e9, high=1e9):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.low, self.high = low, high
        self.i = 0.0; self.prev = 0.0
    def update(self, error, dt):
        self.i += error * dt
        d = (error - self.prev) / dt if dt > 0 else 0.0
        self.prev = error
        u = self.kp*error + self.ki*self.i + self.kd*d
        return max(self.low, min(self.high, u))
