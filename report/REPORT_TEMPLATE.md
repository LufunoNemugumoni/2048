# Intelligent Autonomous Robotic Systems Project
## Autonomous Systems and Robotics 700

**Student:** ____________________  
**Student number:** ____________________  
**Date:** ____________________

## 1. Introduction
This project implements two integrated intelligent robotic systems in Webots using Python. Component A demonstrates autonomous navigation for a single mobile robot. Component B demonstrates multi-agent coordination using three robots. ROS and Gazebo are not used.

## 2. Component A: Single-Robot Navigation
### 2.1 Environment and sensors
The robot is an e-puck in a bounded Webots arena containing static obstacles and a goal marker. The simulated perception pipeline uses eight proximity sensors, a camera, GPS and Compass. The proximity sensors provide local obstacle evidence while GPS/Compass provide simulated pose/orientation information.

### 2.2 Sensor fusion and occupancy representation
Local proximity readings are normalised and combined with pose information. A coarse occupancy grid is used for planning. The grid is inflated around known obstacles to account for the robot footprint.

### 2.3 Path planning
Both Dijkstra and A* are implemented in `component_A/algorithms/path_planning.py`. A* is used by the Webots controller because its heuristic reduces unnecessary exploration for the known grid.

### 2.4 PID control
A PID controller regulates heading error. The proportional term responds to current error, the integral term reduces persistent bias and the derivative term damps rapid changes. The controller output is bounded before being converted into differential wheel speeds.

### 2.5 Safety layer
A reactive obstacle-avoidance layer overrides or modifies the planned motion when front proximity readings become high. This provides a second layer of protection against modelling/planning mismatch.

## 3. Component B: Multi-Agent Swarm System
Three e-puck robots run the same Python controller with different controller arguments. Each robot broadcasts its current position through an Emitter and reads peer messages through a Receiver. The robots form a shared goal estimate and use local sensor observations to avoid obstacles.

### 3.1 Consensus
The controller combines the common mission goal with peer information to form a distributed estimate. This illustrates consensus-style information sharing rather than relying on one central robot.

### 3.2 PSO-inspired coordination
`component_B/algorithms/pso.py` adds deterministic small perturbations to the shared target to create diversity between agents. This is an educational PSO-inspired component, not a claim of a complete industrial PSO implementation.

### 3.3 Neural network
`component_B/ml/neural_network.py` implements a small feed-forward network with a hidden layer. It consumes normalised sensor and goal-direction features and contributes a turn-bias signal to the controller.

### 3.4 Centralised vs distributed comparison
`component_B/experiments/centralised_vs_distributed.py` compares a centralised shared estimate with a distributed peer-informed estimate. Report the generated CSV values after running the experiment. Do not invent results before execution.

## 4. Results
Insert screenshots of Component A and Component B here. Include:
- Webots single-robot world.
- Robot reaching/approaching the goal.
- Three-robot swarm.
- Webots Console showing controller messages.
- Navigation path plot.
- Centralised vs distributed CSV/plot.

### Suggested metrics
| Metric | Component A | Component B |
|---|---:|---:|
| Goal distance at end | ______ | ______ |
| Simulation time | ______ | ______ |
| Collision count | ______ | ______ |
| Path length | ______ | ______ |
| Mean coordination error | N/A | ______ |

## 5. Ethical and Safety Considerations
Autonomous systems should minimise foreseeable physical risk, provide human oversight for safety-critical actions, and make logs available for accountability. Sensor data should be collected only for the stated purpose and retained appropriately. For South African deployments, privacy and data-protection considerations include POPIA when personal information is processed. The simulation itself does not identify real people.

## 6. Reproducibility
The project contains the Webots worlds, Python controllers, planning/control algorithms, experiment scripts, requirements file and result folders. Experiments should be rerun from a clean simulation and results should be stored with the project.

## 7. Conclusion
Component A integrates perception, planning and control in a single autonomous robot. Component B extends the system to distributed multi-agent coordination. The final conclusions should be based on the measured simulation results collected from the provided logs rather than assumed performance.
