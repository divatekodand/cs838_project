#Point cloud visualizer
# requirement - pip install open3d
import numpy
import open3d as o3d

def vis_pc(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])	
	