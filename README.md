# Robust 3D Object Detection for Autonomous Vehicles using Sensor Fusion

# To train the proposed depthmap prediction architecture:

1. To reproduce the baseline results from the original paper follow the README instructions in monodepth2 directory

2. To train the network proposed by us (use --depth_supervision)
```
cd monodepth2
python train.py --depth_supervision --model_name mono_model
```

3. To evaluated our proposed architecture for depth prediction (on kitti eigen split)
```
python evaluate_depth.py --load_weights_folder ~/path_to_trained_weights --eval_mono --depth_supervision
```

# Generate Pseudo Point Cloud for the KITTI 3D Object detection Benchmark dataset

1. Download KITTI 3D Object detection Benchmark dataset
```
cd kitti_3d_obj_det
python ./download_kitti.py
```

2. Make sure that the the KITTI 3D Object detection Benchmark dataset has the following directory structure - 
```
kitti_3d_obj_det
  ├── ImageSets
  ├── object
  │   ├──training
  │      ├──calib & velodyne & label_2 & image_2 & (optional: planes)
  │   ├──testing
  │      ├──calib & velodyne & image_2
```

3. Add `test_files.txt` to the object folder
```
cp ~/kitti_3d_obj_det/test_files.txt ~/kitti_3d_obj_det/object
```

4. Create a destination directory for Pseudo Point Cloud
```
mkdir ~/kitti_3d_obj_det/data/object/testing/velodyne_pseudo/
```

5. Generate Pseudo Point-Cloud
```
python generate_pc.py ~/tmp/depth_supervision/models/weights_19/depth_eigen_split.npy ~/kitti_3d_obj_det/data/object/test_files.txt ~/kitti_3d_obj_det/data/object/testing/velodyne ~/kitti_3d_obj_det/data/object/testing/velodyne_pseudo/ True
```

# Evaluate 3D Object detection results

1. Copy  KITTI 3D Object detection Benchmark dataset to PointRCNN folder and rename velodyne_pseudo to velodyne
```
mv ~/kitti_3d_obj_det/data/object/testing/velodyne ~/kitti_3d_obj_det/data/object/testing/velodyne_orig
mv ~/kitti_3d_obj_det/data/object/testing/velodyne_pseudo ~/kitti_3d_obj_det/data/object/testing/velodyne
mv ~/kitti_3d_obj_det/data ./PointRCNN/
```

2. Evaluate results with augmented point-cloud
```
cd PointRCNN
python eval\_rcnn.py --cfg\_file cfgs/default.yaml --ckpt PointRCNN.pth --batch\_size 1 --eval\_mode rcnn --set RPN.LOC\_XZ\_FINE False
```
