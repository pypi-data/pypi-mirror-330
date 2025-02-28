import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pyrfuniverse.envs.base_env import RFUniverseBaseEnv
from pyrfuniverse_test.extend.digit_attr import DigitAttr

env = RFUniverseBaseEnv(ext_attr=[DigitAttr])

digit = env.InstanceObject(name="Digit", attr_type=DigitAttr)
digit.SetTransform(position=[0, 0.015, 0])
target = env.InstanceObject(name="DigitTarget")
target.SetTransform(position=[0, 0.05, 0.015])
env.SetViewTransform(position=[-0.1, 0.033, 0.014], rotation=[0, 90, 0])
env.Pend()
env.close()
