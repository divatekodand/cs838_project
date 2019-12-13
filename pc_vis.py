#Point cloud visualizer
# requirement - pip install open3d
import numpy as np
import open3d as o3d
import scipy.io as sio
import sys
import pdb


def read_pc(path):
    # exact path to the bin file
    pc = np.fromfile(path, dtype=np.float32).reshape((-1,4))
    return pc


def vis_pc(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])	


def main():
	args = sys.argv
	if(len(args) < 2):
		print("Path to bin file required")
	else:
		vis_pc(read_pc(args[1]))
	


if __name__ == '__main__':
    main()
