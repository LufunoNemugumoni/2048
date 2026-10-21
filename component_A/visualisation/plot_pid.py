from pathlib import Path
import csv
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
log=ROOT/'data'/'navigation_log.csv'
if not log.exists():
    print('Run the Webots world first to create navigation_log.csv')
    raise SystemExit
xs=[]; zs=[]; d=[]
with open(log) as f:
    r=csv.DictReader(f)
    for row in r:
        xs.append(float(row['x'])); zs.append(float(row['z'])); d.append(float(row['goal_distance']))
plt.figure(); plt.plot(xs,zs); plt.scatter([xs[0]],[zs[0]],label='start'); plt.scatter([3.1],[ -2.25],label='goal'); plt.xlabel('X (m)'); plt.ylabel('Z (m)'); plt.title('Autonomous Navigation Path'); plt.legend(); plt.grid(True); plt.tight_layout(); plt.savefig(ROOT/'results'/'navigation_path.png',dpi=160); plt.close()
plt.figure(); plt.plot(d); plt.xlabel('Sample'); plt.ylabel('Distance to goal (m)'); plt.title('Goal Distance'); plt.grid(True); plt.tight_layout(); plt.savefig(ROOT/'results'/'goal_distance.png',dpi=160); plt.close()
print('Plots written to component_A/results')
