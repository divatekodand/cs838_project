import os
import re
import errno
import shutil
import argparse
 
def copy(src, dest):
  '''
  Copies src directory/file to dest directory/file
  :param src:
  :param dest:
  :return: None
  '''
  try:
    shutil.copytree(src, dest)
  except OSError as e:
    # If the error was caused because the source wasn't a directory
    if e.errno == errno.ENOTDIR:
      shutil.copy(src, dest)
    else:
      print('Directory not copied. Error: %s' % e)
      raise

def create_split(obj_dir, val_file):
  ''' 
  Creates a validation split using the provided text file containing labels for
  validation partition.
  '''
  print('Started creating validation split')
  val = open(val_file)
  labels = val.readlines()
  labels = [l.strip() for l in labels]
  src_dirs = {'img' : os.path.join(os.path.abspath(obj_dir),'training', 'image_2'), \
  'label' : os.path.join(os.path.abspath(obj_dir),'training', 'label_2'), \
  'lidar' : os.path.join(os.path.abspath(obj_dir),'training', 'velodyne')}
  dst_dirs = {'img' : os.path.join(os.path.abspath(obj_dir),'testing', 'image_2'), \
  'label' : os.path.join(os.path.abspath(obj_dir),'testing', 'label_2'), \
  'lidar' : os.path.join(os.path.abspath(obj_dir),'testing', 'velodyne')}
  for key in dst_dirs.keys():
    os.mkdir(dst_dirs[key])
  for label in labels:
    filenames = {'img' : label + '.png', 'label' : label + '.txt', 'lidar' : label + '.bin'}

    for t in ['img', 'label', 'lidar']:
      shutil.move(os.path.join(src_dirs[t], filenames[t]), \
      os.path.join(dst_dirs[t], filenames[t])) 
      print('src: ', os.path.join(src_dirs[t], filenames[t]), 'dst: ', os.path.join(dst_dirs[t], filenames[t]))
  val.close()


def mk_dirs_and_copy(dirs, datadir):
  '''
  Creates directory structure required by the training/validation pipeline and 
  copies the extracted data into training folder
  '''
  if not os.path.exists(datadir):
    os.mkdir(datadir)
    objdir = os.path.join(datadir, 'object')
    os.mkdir(objdir)
    traindir = os.path.join(objdir, 'training')
    testdir = os.path.join(objdir, 'testing')
    os.mkdir(traindir)
    os.mkdir(testdir)

    ## Copy labels, images and point-cloud to traindir
    src_dirs = { 'image_2' : os.path.join(os.path.join(dirs['images'], 'training'), 'image_2'),
    'label_2' : os.path.join(os.path.join(dirs['labels'], 'training'), 'label_2'), 
    'velodyne' : os.path.join(os.path.join(dirs['point_cloud'], 'training'), 'velodyne')}
    print('Copying data to training folder')  
    for key in src_dirs.keys():
      copy(src_dirs[key], os.path.join(traindir, key))

def unzip_files(dataset_files, dataset_dir):
  '''
  Unzips the dataset files downloaded and
  returns the destination directory paths in a dictionary.
  '''
  dirs = {}

  for zipfile in dataset_files:
    if zipfile[-3:] == 'zip':
      dst_dir = os.path.join(dataset_dir, zipfile.split('.')[0])
      if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
        os.system('unzip -K ' + os.path.join(dataset_dir, zipfile) + ' -d ' + dst_dir)
      else:
        print(dst_dir, ' already present.') 
      if re.search('label', dst_dir):
        dirs['labels'] = dst_dir
      elif re.search('velodyne', dst_dir):
        dirs['point_cloud'] = dst_dir
      else:
        dirs['images'] = dst_dir

  return dirs
      
def main():
  ''' 
  This script (download_kitty.py) downloads the dataset for KITTI 3D Object detection benchmark 
  and creates training and validation splits. 
  '''
  parser = argparse.ArgumentParser(description='download_kitti')
  parser.add_argument('-v', '--val', type=str, nargs='?', default='./ImageSets/val.txt',
                        help='set log tag')
  args = parser.parse_args()
  val_file = args.val
  print('valfile : ', val_file)        
  datasets_urls = {'left_color_images': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip', 
                   'right_color_images': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_3.zip',
                   'left_color_images_temporal': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_prev_2.zip', 
                   'right_color_images_temporal': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_prev_3.zip',
                   'point_cloud': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_velodyne.zip',
                   'camera_calibration_mat': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip',
                   'labels': 'https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip',
	     'obj_dev_kit':'https://s3.eu-central-1.amazonaws.com/avg-kitti/devkit_object.zip'}

  dataset_dir = './datasets'
  datadir = './data'
  dirs = {}

  if not os.path.exists(datadir):
    if not os.path.exists(dataset_dir):
      ##Download the zip files
      os.mkdir(dataset_dir)
      os.system('wget -P ' + dataset_dir + ' ' + datasets_urls['left_color_images'])
      os.system('wget -P ' + dataset_dir + ' ' + datasets_urls['point_cloud'])
      os.system('wget -P '+ dataset_dir + ' ' + datasets_urls['labels'])
    else:
      print('Dataset files already downloaded.')
    ##Extract the zip files  
    dataset_files = os.listdir('./datasets')
    dirs = unzip_files(dataset_files, dataset_dir)
    print('Dataset extracted to following directories: ', dirs)

    ##Create required directory structure and copy data
    mk_dirs_and_copy(dirs, datadir)
    
    ##Split the data
    create_split(os.path.join(datadir, 'object'), val_file) 

if __name__ == '__main__':
  main()
