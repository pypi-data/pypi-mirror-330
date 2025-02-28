# A Robotics Toolbox from Maziar Palhang

This is a simple Robotics Toolbox package.

To install this package:
on windows:
py -m pip install AIUT_RoboticsToolbox

on Linux and Mac:
python3 -m pip install AIUT_RoboticsToolbox

To use this package in your program, add the following line:
from AIUT_RoboticsToolbox.Toolbox import *

Routines:
rotx(ang) #angle in degrees
roty(ang)
rotz(ang)
rpy2r(gamma,beta,alpha)
r2rpy(r)
euler2r(alpha,beta,gamma)
r2euler(r)
angvec2r(theta,v)
r2angvec(r)
skew(k)  #make a skew matrix from a 3 element vector
r2skew(r) #finds the corresponding skew matrix of a rotation matrix
plot(r)  #plot a rotation matrix

Classes:

SerialLink(name,links)
Puma560(name)
SCARA(name,l1,l2)
