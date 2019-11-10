#Point cloud visualizer
# requirement - pip install open3d
import numpy as np
import open3d as o3d
import scipy.io as sio
import pdb

def camera_to_lidar(points):
    # cal mean from train set
    MATRIX_T_VELO_2_CAM = ([
        [7.49916597e-03, -9.99971248e-01, -8.65110297e-04, -6.71807577e-03],
        [1.18652889e-02, 9.54520517e-04, -9.99910318e-01, -7.33152811e-02],
        [9.99882833e-01, 7.49141178e-03, 1.18719929e-02, -2.78557062e-01],
        [0, 0, 0, 1]
    ])
    # cal mean from train set
    MATRIX_R_RECT_0 = ([
        [0.99992475, 0.00975976, -0.00734152, 0],
        [-0.0097913, 0.99994262, -0.00430371, 0],
        [0.00729911, 0.0043753, 0.99996319, 0],
        [0, 0, 0, 1]
    ])
    p = np.ones((points.shape[0], 4), dtype=points.dtype)
    p[:, 0:3] = points
    p = np.matmul(np.linalg.inv(np.array(MATRIX_R_RECT_0)), np.transpose(p))
    p = np.matmul(np.linalg.inv(np.array(MATRIX_T_VELO_2_CAM)), p)
    p = np.transpose(p)
    return p[:, 0:3]


def read_pc(path):
    # exact path to the bin file
    pc = np.fromfile(path, dtype=np.float32).reshape((-1,4))
    return pc


def vis_pc(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])	


def main():
    img_points = sio.loadmat('./data_sample/000039_depth.mat')
    pc = sio.loadmat('./data_sample/000039_pc_crop.mat')
    # pc = pc['val'][:, 0:3]
    # pc = read_pc('./006656.bin')
    # pc = pc[:, 0:3]
    pc = pc['val']
    img_points = img_points['points']
    vis_pc(pc)
    img_points = camera_to_lidar(img_points)  * np.array([50,50,50])
    vis_pc(img_points)
    all_points = np.concatenate((pc, img_points), axis=0)
    vis_pc(all_points)
    img_points_mean = np.mean(img_points, axis=0)
    pc_mean = np.mean(pc, axis=0)
    print('img mean - ', img_points_mean)
    print('pc mean - ', pc_mean)
    scale = img_points_mean / pc_mean
    print('scale - ', scale)


if __name__ == '__main__':
    main()