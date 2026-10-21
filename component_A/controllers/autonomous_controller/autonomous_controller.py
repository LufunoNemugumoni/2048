from controller import Robot
import math, csv, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
ALG = PROJECT / 'algorithms'
sys.path.insert(0, str(ALG))
from path_planning import astar_grid, build_demo_grid
from pid_controller import PID

TIME_STEP = 64
MAX_SPEED = 6.28
GOAL = (3.1, -2.25)

robot = Robot()
left = robot.getDevice('left wheel motor')
right = robot.getDevice('right wheel motor')
left.setPosition(float('inf')); right.setPosition(float('inf'))
left.setVelocity(0); right.setVelocity(0)

ps = []
for i in range(8):
    s = robot.getDevice(f'ps{i}')
    s.enable(TIME_STEP); ps.append(s)

gps = robot.getDevice('gps'); gps.enable(TIME_STEP)
compass = robot.getDevice('compass'); compass.enable(TIME_STEP)
camera = robot.getDevice('camera'); camera.enable(TIME_STEP)

# Planned path over a coarse occupancy grid. Grid coordinates cover x/z in [-4,4]x[-3,3].
grid = build_demo_grid(40, 30)
start_cell = (4, 26)
goal_cell = (35, 4)
path_cells = astar_grid(grid, start_cell, goal_cell)
path = []
for gx, gz in path_cells:
    path.append((-4 + gx * 8/39, -3 + gz * 6/29))

heading_pid = PID(2.2, 0.01, 0.35, -2.5, 2.5)
log = []
step_count = 0

def heading_from_compass(v):
    # Webots compass vector points toward north. Convert to yaw in x-z plane.
    return math.atan2(v[0], v[2])

def wrap(a):
    while a > math.pi: a -= 2*math.pi
    while a < -math.pi: a += 2*math.pi
    return a

def camera_perception():
    # Lightweight perception; OpenCV is used offline in visualisation/perception.py.
    w, h = camera.getWidth(), camera.getHeight()
    img = camera.getImage()
    if not img or w*h == 0:
        return 0.0
    stride = max(1, (w*h)//200)
    total = 0
    count = 0
    for p in range(0, w*h, stride):
        r = camera.imageGetRed(img, w, h, p % w, p // w)
        g = camera.imageGetGreen(img, w, h, p % w, p // w)
        b = camera.imageGetBlue(img, w, h, p % w, p // w)
        total += (r+g+b)/3
        count += 1
    return total/max(1,count)

while robot.step(TIME_STEP) != -1:
    x, _, z = gps.getValues()
    dist_goal = math.hypot(GOAL[0]-x, GOAL[1]-z)
    if dist_goal < 0.25:
        left.setVelocity(0); right.setVelocity(0)
        print('GOAL REACHED. Distance:', round(dist_goal, 3))
        break

    # Select nearest future waypoint.
    idx = min(range(len(path)), key=lambda i: math.hypot(path[i][0]-x, path[i][1]-z))
    target = path[min(idx+2, len(path)-1)] if path else GOAL
    desired = math.atan2(target[1]-z, target[0]-x)
    yaw = heading_from_compass(compass.getValues())
    err = wrap(desired - yaw)
    turn = heading_pid.update(err, TIME_STEP/1000.0)

    vals = [s.getValue() for s in ps]
    front = max(vals[2], vals[3], vals[4], vals[5]) / 4096.0
    left_obs = max(vals[5], vals[6], vals[7]) / 4096.0
    right_obs = max(vals[0], vals[1], vals[2]) / 4096.0
    # Reactive safety layer over the planned path.
    avoid = max(-1.5, min(1.5, (right_obs-left_obs)*2.0))
    if front > 0.42:
        turn += 2.0 if right_obs < left_obs else -2.0
    base = max(1.2, min(MAX_SPEED, 3.8 * min(1.0, dist_goal)))
    l = max(-MAX_SPEED, min(MAX_SPEED, base - turn - avoid))
    r = max(-MAX_SPEED, min(MAX_SPEED, base + turn + avoid))
    left.setVelocity(l); right.setVelocity(r)

    cam_mean = camera_perception()
    log.append((step_count, x, z, dist_goal, err, front, cam_mean))
    step_count += 1
    if step_count % 25 == 0:
        out = PROJECT / 'data' / 'navigation_log.csv'
        with open(out, 'w', newline='') as f:
            w = csv.writer(f); w.writerow(['step','x','z','goal_distance','heading_error','front_obstacle','camera_mean'])
            w.writerows(log)

out = PROJECT / 'data' / 'navigation_log.csv'
with open(out, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['step','x','z','goal_distance','heading_error','front_obstacle','camera_mean']); w.writerows(log)
print('Navigation log saved to', out)
