"""Offline OpenCV perception demo. Run with a captured camera frame named camera_frame.png."""
from pathlib import Path
try:
 import cv2, numpy as np
except ImportError:
 print('Install requirements.txt to use OpenCV perception.'); raise SystemExit
ROOT=Path(__file__).resolve().parents[2]
img=cv2.imread(str(ROOT/'data'/'camera_frame.png'))
if img is None:
 print('Place a camera_frame.png in component_A/data/'); raise SystemExit
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
mask=cv2.inRange(hsv,(0,80,60),(12,255,255))
count=int(np.count_nonzero(mask)); ratio=count/(img.shape[0]*img.shape[1])
print(f'Red-object pixel ratio: {ratio:.4f}')
cv2.imwrite(str(ROOT/'results'/'perception_mask.png'),mask)
