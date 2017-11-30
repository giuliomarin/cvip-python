from cvip import ymlparser
import utils
import numpy as np
import copy

if __name__ == '__main__':

    calib_rt_path = '/Data/0_Dataset/multicam_out/calib_rt_4.yml'
    calib_paths = ['/Data/0_Dataset/multicam_out/calib_s1_small.yml',
                   '/Data/0_Dataset/multicam_out/calib_s2.yml',
                   '/Data/0_Dataset/multicam_out/calib_s3.yml',
                   '/Data/0_Dataset/multicam_out/calib_s4.yml']
    calib_out_path = '/Data/0_Dataset/multicam_out/calib_s1_small_s2_s3_s4.yml'

    # Read calibration
    calib_rt = utils.SensorCalib(calib_rt_path)
    calib_new = copy.deepcopy(calib_rt)
    if len(calib_rt.camera_calib) != len(calib_paths):
        print 'Num cameras rt: %d but provided %d calib' % (len(calib_rt.camera_calib), len(calib_paths))

    num_cam = 0
    calib_new.camera_calib = {}

    for calib_idx, calib_path in enumerate(calib_paths):
        camRT = calib_rt.camera_calib[calib_idx]
        RTs = np.eye(4)
        RTs[:3, :3] = camRT.R
        RTs[:3, 3] = camRT.T.transpose()

        calib = utils.SensorCalib(calib_path)
        for c in calib.camera_calib:
            cam = calib.camera_calib[c]
            RTc = np.eye(4)
            RTc[:3, :3] = cam.R
            RTc[:3, 3] = cam.T.transpose()
            RTtot = RTc.dot(RTs)
            cam.R = RTtot[:3, :3]
            cam.T = RTtot[:3, 3].reshape(3, 1)
            calib_new.camera_calib[num_cam] = cam
            num_cam += 1

    # Set number of cameras
    calib_new.write(calib_out_path)
