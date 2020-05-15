cmake_minimum_required(VERSION 2.8.3)
project(pubkitti)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  tf2
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)


