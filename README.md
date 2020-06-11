# mini-kitti-publisher
A very simple KITTI odometry dataset's images and velodyne points publisher 

### How to use
```
$ python mini_kitti_publisher.py --dir "...your kitti dataset base directory../sequences/XX"
```

We note that the directory should form like 
```
| your kitti dataset base dir 
    |-- sequences 
        |-- 00
            |-- image_0
                |-- 000000.png
                |-- 000001.png
                |-- ...
            |-- image_1
                |-- 000000.png
                |-- 000001.png
                |-- ...
            |-- image_2
                |-- 000000.png
                |-- 000001.png
                |-- ...
            |-- image_3
                |-- 000000.png
                |-- 000001.png
                |-- ...
            |-- velodyne
                |-- 000000.bin
                |-- 000001.bin
                |-- ...
        |-- 01
        |-- ...
```

### Termination of the program
- Use ```ctrl + \``` at the terminal.  

### Tip 
If you use my pre-tuned-visualization config file, it is easy to show how the data flow.
For example,
```
$ rviz -d rviz_setting.rviz

and other terminal 
$ rqt --perspective-file rqt_setting.perspective
```
