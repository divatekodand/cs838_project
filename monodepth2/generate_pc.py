from __future__ import absolute_import, division, print_function

import os
import numpy as np
from collections import Counter
from kitti_utils import *
import sys
import scipy.spatial as scsp


'''Module to generate Pseudo point cloud from depth maps'''

def get_pseudo_points(depth_map, v_points, filter_points=False, threshold=0.1):
    MATRIX_P2 = np.array([[719.787081, 0., 608.463003, 44.9538775],
                          [0., 719.787081, 174.545111, 0.1066855],
                          [0., 0., 1., 3.0106472e-03],
                          [0., 0., 0., 0]])
    # print(MATRIX_P2.shape)
    int_mat = MATRIX_P2[0:3, 0:3]
    # print(int_mat)
    # print(depth_map.shape)
    inv_int_mat = np.linalg.inv(int_mat)

    points_arr = np.ones((depth_map.shape[0]*depth_map.shape[1], 4))
    for i in range(depth_map.shape[0]):
        for j in range(depth_map.shape[1]):
            points_arr[i*depth_map.shape[1] + j, 0:3] = depth_map[i, j] * np.dot(inv_int_mat, np.array([i, j, 1]))

    if filter_points:
        tree = scsp.KDTree(v_points[:, 0:3])
        for i in range(points_arr.shape[0]):
            n_neighbors = tree.query_ball_point(points_arr[i, 0:3], threshold)
            if len(n_neighbors) < 1:
                points_arr[i, 3] = 0

    return points_arr


def main():
    '''
    arg1 = path to depth file
    arg2 = test_files.txt
    arg3 = velodyne path
    arg4 = dest_path
    arg5 = True of False filtering
    '''
    args = sys.argv[1:]

    assert len(args) == 5 and 'incorrect arguments'

    depth_file = args[0]
    test_file_path = args[1]
    velodyne_path = args[2]
    dest_path = args[3]

    depth_maps = np.load(depth_file)
    f = open(test_file_path, 'r')
    test_file_lines = f.readlines()
    test_file_strs = [line.split(' ')[1] for line in test_file_lines]

    assert len(test_file_strs) == depth_maps.shape[0] and  'number of items dont match'

    filter_points = True if args[4] == 'True' else False

    for i in range(depth_maps.shape[0]):
        depth_map = depth_maps[i,0,:,:]
        v_points = np.fromfile(os.path.join(velodyne_path, test_file_strs[i]+'.bin')).reshape(-1, 4)
        pseudo_points = get_pseudo_points(depth_map, v_points, filter_points)
        print('File - ', test_file_strs[i], '  # original points - ', v_points.shape[0], '  # pseudo points - ', pseudo_points.shape[0])
        all_points = np.concatenate((v_points, pseudo_points), axis=0)
        f = open(os.path.join(dest_path, test_file_strs[i]+'.bin'), 'w')
        all_points.tofile(f)
        f.close()


if __name__ == "__main__":
    main()
