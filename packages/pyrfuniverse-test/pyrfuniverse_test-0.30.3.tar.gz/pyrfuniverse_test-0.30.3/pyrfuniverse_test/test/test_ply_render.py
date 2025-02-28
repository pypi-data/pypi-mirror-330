import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pyrfuniverse.attributes as attr
from pyrfuniverse.envs.base_env import RFUniverseBaseEnv
from pyrfuniverse_test import mesh_path

env = RFUniverseBaseEnv()
env.SetViewBackGround([0.0, 0.0, 0.0])
point_cloud = env.InstanceObject(
    name="PointCloud", id=123456, attr_type=attr.PointCloudAttr
)
point_cloud.ShowPointCloud(ply_path=os.path.join(mesh_path, "000000_000673513312.ply"))
point_cloud.SetTransform(rotation=[-90, 0, 0])
point_cloud.SetRadius(radius=0.001)

env.Pend()
env.close()
