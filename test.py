import pybullet as p

try:
    p.connect(p.DIRECT)
    print("PyBullet connected successfully!")
except Exception as e:
    print("Error:", e)