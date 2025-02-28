import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import cv2
import numpy as np

from pyrfuniverse.envs.base_env import RFUniverseBaseEnv
import pyrfuniverse.attributes as attr
from pyrfuniverse_test.extend.gelslim_attr import GelSlimAttr

env = RFUniverseBaseEnv(ext_attr=[GelSlimAttr])

gelslim = env.InstanceObject(name="GelSlim", attr_type=GelSlimAttr)
gelslim.SetTransform(position=[0, 0, 0])
target = env.InstanceObject(name="GelSlimTarget", attr_type=attr.RigidbodyAttr)
target.SetTransform(position=[0, 0.03, 0],rotation=[90, 0, 0])
env.SetViewTransform(position=[-0.1, 0.03, 0.], rotation=[0, 90, 0])

for i in range(50):
    env.step()
    target.AddForce([0, -1, 0])

gelslim.GetData()
env.step()
image = np.frombuffer(gelslim.data["light"], dtype=np.uint8)
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
cv2.imshow("light", image)
cv2.waitKey(0)
image = np.frombuffer(gelslim.data["depth"], dtype=np.uint8)
image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
cv2.imshow("depth", image)
cv2.waitKey(0)

gelslim.BlurGel()
gelslim.GetData()
env.step()
image = np.frombuffer(gelslim.data["light"], dtype=np.uint8)
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
cv2.imshow("light", image)
cv2.waitKey(0)
image = np.frombuffer(gelslim.data["depth"], dtype=np.uint8)
image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
cv2.imshow("depth", image)
cv2.waitKey(0)
env.Pend()
env.close()
