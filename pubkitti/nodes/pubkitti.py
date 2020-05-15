#!/usr/bin/env python

import os

import rospy
import tf2_ros
import tf_conversions
import sensor_msgs.msg as sensor_msgs
import std_msgs.msg as std_msgs
import geometry_msgs.msg

import argparse

import cv2
from cv_bridge import CvBridge
import numpy as np

parser = argparse.ArgumentParser(description='A simple kitti publisher')
parser.add_argument('--dir', default='/media/user/GS1TB/KITTI/dataset/sequences/00/', metavar='DIR', help='path to dataset')
args = parser.parse_args()


def makePointCloud2Msg(points, parent_frame, pcd_format):

    ros_dtype = sensor_msgs.PointField.FLOAT32

    dtype = np.float32
    itemsize = np.dtype(dtype).itemsize

    data = points.astype(dtype).tobytes()

    fields = [sensor_msgs.PointField(
        name=n, offset=i*itemsize, datatype=ros_dtype, count=1)
        for i, n in enumerate(pcd_format)]

    header = std_msgs.Header(frame_id=parent_frame, stamp=rospy.Time.now())
    num_field = 3
    return sensor_msgs.PointCloud2(
        header=header,
        height=1,
        width=points.shape[0],
        is_dense=False,
        is_bigendian=False,
        fields=fields,
        point_step=(itemsize * num_field),
        row_step=(itemsize * num_field * points.shape[0]),
        data=data
    )


if __name__ == '__main__':

    rospy.init_node('KittiPublisher') # don't have blank (space) in the name
    r = rospy.Rate(10)

    bridge = CvBridge()
 
    # 
    grayleftimg_publisher = rospy.Publisher("image_0", sensor_msgs.Image, queue_size=10)
    grayrightimg_publisher = rospy.Publisher("image_1", sensor_msgs.Image, queue_size=10)
    colorleftimg_publisher = rospy.Publisher("image_2", sensor_msgs.Image, queue_size=10)
    colorrightimg_publisher = rospy.Publisher("image_3", sensor_msgs.Image, queue_size=10)

    scan_publisher = rospy.Publisher('velodyne_points', sensor_msgs.PointCloud2, queue_size=10)

    #
    seqence_dir = args.dir
    grayleftimg_dir = os.path.join(seqence_dir, 'image_0')
    grayrightimg_dir = os.path.join(seqence_dir, 'image_1')
    colorleftimg_dir = os.path.join(seqence_dir, 'image_2')
    colorrightimg_dir = os.path.join(seqence_dir, 'image_3')

    scan_dir = os.path.join(seqence_dir, 'velodyne')
    scan_names = os.listdir(scan_dir)
    scan_names.sort()
    
    #
    num_frames = scan_names.__len__()
    for frame_idx in range(num_frames):
        frame_num_str = scan_names[frame_idx][:-4]
        img_name = frame_num_str + '.png'
        
        # pub images
        grayleftimg_path = os.path.join(grayleftimg_dir, img_name)
        grayleftimg_publisher.publish( bridge.cv2_to_imgmsg(cv2.imread(grayleftimg_path), 'bgr8') )

        grayrightimg_path = os.path.join(grayrightimg_dir, img_name)
        grayrightimg_publisher.publish( bridge.cv2_to_imgmsg(cv2.imread(grayrightimg_path), 'bgr8') )

        colorleftimg_path = os.path.join(colorleftimg_dir, img_name)
        colorleftimg_publisher.publish( bridge.cv2_to_imgmsg(cv2.imread(colorleftimg_path), 'bgr8') )

        colorrightimg_path = os.path.join(colorrightimg_dir, img_name)
        colorrightimg_publisher.publish( bridge.cv2_to_imgmsg(cv2.imread(colorrightimg_path), 'bgr8') )

        # pub velodyne scan 
        scan_path = os.path.join(scan_dir, scan_names[frame_idx])
        xyzi = np.fromfile(scan_path, dtype=np.float32).reshape((-1, 4))
        scan_publisher.publish(makePointCloud2Msg(xyzi[:, :3], "KITTI", 'xyz'))

        #
        r.sleep()
