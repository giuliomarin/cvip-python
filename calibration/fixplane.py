from cvip import xmlparser as xml
import numpy as np
import utils

planepath = '/Data/1_seat/calibration/cameras/ProcessedCalib/groundPlane2.xml'
calibpath = '/Data/1_seat/calibration/cameras/ProcessedCalib/groundPlane2.xml'

calib = xml.parse(calibpath)
plane = xml.parse(planepath)

Rp = xml.get(plane, ['R'])
Tp = xml.get(plane, ['T'])
print xml.get(plane, ['groundPlane'])
RTp = np.eye(4)
RTp[:3, :3] = Rp
RTp[:3, 3] = Tp.transpose()
print RTp[2, :]

R = xml.get(calib, ['camera_calibrations', 'camera_3', 'R'])
T = xml.get(calib, ['camera_calibrations', 'camera_3', 'T'])
RT = np.eye(4)
RT[:3, :3] = R
RT[:3, 3] = T.transpose()

RTf = RTp.dot(RT)

print RTf[0, 0], RTf[0, 1], RTf[0, 2], RTf[1, 0], RTf[1, 1], RTf[1, 2], RTf[2, 0], RTf[2, 1], RTf[2, 2]
print RTf[:3,3]
print RTf[2, :]