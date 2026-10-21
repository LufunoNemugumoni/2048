import math

def pso_step(goal, robot_id, iteration):
    # Deterministic lightweight PSO-inspired velocity update for reproducibility.
    phase=0.37*robot_id+0.11*iteration
    vx=0.18*math.sin(phase); vz=0.18*math.cos(phase*1.3)
    return goal[0]+vx, goal[1]+vz
