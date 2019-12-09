from __future__ import absolute_import, division, print_function

import os
import numpy as np
from collections import Counter
from kitti_utils import *


def main():
    depth_calib_path = {}
    depth_calib_path['cam_to_cam'] = './calibration_data/calib_cam_to_cam.txt'
    depth_calib_path['imu_to_velo'] = './calibration_data/calib_imu_to_velo.txt'
    depth_calib_path['velo_to_cam'] = './calibration_data/calib_velo_to_cam.txt'

    lines = {}
    for dkey in depth_calib_path.keys():
        f = open(depth_calib_path[dkey], 'r')
        lines[dkey] = f.readlines()
        f.close()

    kitti3d_path = './calibration_data/data_object_calib/training/calib/'
    kitti3d_files = os.listdir(kitti3d_path)

    for file in kitti3d_files:
        data = read_calib_file(os.path.join(kitti3d_path, file))
        tmp_lines = lines

        # get velo to camera r and t
        RandT = data['Tr_velo_to_cam']
        # RandT = np.array[double(ele) for ele in RandT]
        RandT = RandT.reshape(3,4)
        R_mat = RandT[:, 0:3]
        R_mat = np.ravel(R_mat)

        R = 'R:'
        for val in R_mat:
            R += str(val) + ' '
        R = R[0:-1] + '\n'

        T_mat = RandT[2, :]
        T = 'T:'
        for val in T_mat:
            T += str(val) + ' '
        T = T[0:-1] + '\n'

        # get RO
        R0 = data['R0_rect']
        R0_str = 'R_rect_00:'
        for val in R0:
            R0_str += str(val) + ' '
        R0_str = R0_str[0:-1] + '\n'

        # get P2
        P2 = data['P2']
        P2_str = 'P_rect_02:'
        for val in P2:
            P2_str += str(val) + ' '
        P2_str = P2_str[0:-1] + '\n'

        tmp_lines['cam_to_cam'][25] = P2_str
        tmp_lines['cam_to_cam'][8] = R0_str

        tmp_lines['velo_to_cam'][1] = R
        tmp_lines['velo_to_cam'][2] = T

        out_cam_2_cam = ''.join(tmp_lines['cam_to_cam'])
        out_velo_2_cam = ''.join(tmp_lines['velo_to_cam'])

        out_cam_2_cam_file = file.split('.')[0] + 'cam_to_cam' + '.' + file.split('.')[1]
        out_velo_2_cam_file = file.split('.')[0] + 'velo_to_cam' + '.' + file.split('.')[1]

        fc = open(out_cam_2_cam_file, 'w')
        fc.write(out_cam_2_cam)
        fc.close()

        fv = open(out_velo_2_cam_file, 'w')
        fv.write(out_velo_2_cam)
        fv.close()


if __name__ == "__main__":
    main()