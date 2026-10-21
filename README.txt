INTELLIGENT AUTONOMOUS ROBOTIC SYSTEMS PROJECT
AUTONOMOUS SYSTEMS AND ROBOTICS 700
Webots R2023b + Python

IMPORTANT
This project is designed for Webots R2023b and does NOT use ROS or Gazebo.
Open the .wbt files in Webots and press the Run/Play button.

1. INSTALLATION
- Install Webots R2023b.
- Open Webots once and confirm it remains open.
- Optional for offline plots/perception: open Command Prompt in this folder and run:
    py -m pip install -r requirements.txt

2. COMPONENT A
Open:
    component_A/worlds/autonomous_navigation.wbt

The world contains one e-puck, boundary walls, obstacles and a red goal marker.
The controller uses:
- 8 proximity sensors ps0..ps7 for reactive obstacle avoidance.
- Camera for simulated visual sampling.
- GPS and Compass added through the e-puck turret slot.
- A* path planning on a coarse occupancy grid.
- PID heading control.
- A reactive safety layer to reduce collision risk.
- CSV logging to component_A/data/navigation_log.csv.

Controller directory:
    component_A/controllers/autonomous_controller/

3. COMPONENT B
Open:
    component_B/worlds/multi_robot.wbt

The world contains three e-pucks. Each robot has GPS, Compass, Emitter and Receiver in its turret slot.
The controller demonstrates:
- Robot-to-robot position messages.
- Distributed consensus-style goal estimation.
- PSO-inspired target perturbation.
- A small deterministic neural network policy.
- Collision avoidance using proximity sensors.
- Per-robot CSV logs.

4. OFFLINE EXPERIMENTS
Run:
    py component_B/experiments/centralised_vs_distributed.py

This creates:
    component_B/results/centralised_vs_distributed.csv

For navigation plots, first run Component A, then:
    py component_A/visualisation/plot_pid.py

5. OPEN-CV PERCEPTION
If you capture a Webots camera image and save it as:
    component_A/data/camera_frame.png
run:
    py component_A/visualisation/perception.py

6. PROJECT STRUCTURE
component_A/      single robot navigation, mapping, planning and control
component_B/      multi-robot swarm, communication and ML
screenshots/      place screenshots here
report/           report template and methodology

7. CONTROLLER REQUIREMENT
Webots Python controllers use the standard Webots controller API. The R2023b documentation
shows Python controllers obtaining devices with robot.getDevice(...) and running the simulation
inside robot.step(...). The e-puck uses the motor names 'left wheel motor' and 'right wheel motor'
and proximity sensors ps0..ps7.

8. TROUBLESHOOTING
If a controller does not start, check Webots Console for the exact Python error. Make sure the
controller folder name and Python file name match. For example:
controllers/autonomous_controller/autonomous_controller.py
controllers/swarm_robot_controller/swarm_robot_controller.py

9. ETHICS
The report includes privacy, safety, accountability, human oversight and South African context.
Do not use the simulation to make claims about real-world people or surveillance subjects.
