# Robust 3D Object Detection for Autonomous Vehicles using Sensor Fusion
cs838\_Project
TO train the depthmap prediction architecture, do the following:
cd monodepth2
python train.py --model\_name mono\_model

To evaluate the performance of depthmap prediction, do the following:
cd monodepth2

If you want to evaluate depthmap prediction using our approach, run the following:
python evaluate\_depth.py --png --load\_weights\_folder /home/divatekodand/tmp/depth\_supervision/models/weights\_19/ --eval\_mono --depth\_supervision

If you want to evaluate depthmap predcition using the existing approach, run the following:
python evaluate\_depth.py --png --load\_weights\_folder models/mono\_640x192/ --eval\_mono 

TO evaluate 3D object detection, do the following:
cd PointRCNN
python eval\_rcnn.py --cfg\_file cfgs/default.yaml --ckpt PointRCNN.pth --batch\_size 1 --eval\_mode rcnn --set RPN.LOC\_XZ\_FINE False


