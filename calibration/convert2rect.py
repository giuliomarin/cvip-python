from cvip import ymlparser
import utils
import copy

if __name__ == '__main__':

    calib_in_path = '/Data/0_Dataset/multicam_out/calib_s1_small_s2_s3_s4.yml'
    calib_out_path = '/Data/0_Dataset/multicam_out/calib_s1_small_s2_s3_s4_rect.yml'
    ref_idx = 0

    # Read calibration
    calib = utils.SensorCalib(calib_in_path, 1)
    calib_new = copy.deepcopy(calib)

    # Ref cam
    calib_cam_ref = calib.camera_calib[ref_idx]
    RTref = utils.getExtrinsics(calib_cam_ref)

    for calib_idx in calib.camera_calib:
        calib_cam = calib.camera_calib[calib_idx]
        RT = utils.getExtrinsics(calib_cam).dot(utils.invRT(RTref))
        R = RT[:3, :3]
        T = RT[:3, 3].reshape(3, 1)
        K = utils.getIntrinsics(calib_cam)
        calib_new.camera_calib[calib_idx].R = R
        calib_new.camera_calib[calib_idx].T = T / 1000.
        calib_new.camera_calib[calib_idx].K = K
        if calib_new.camera_calib[calib_idx].Rrect is not None:
            calib_new.camera_calib[calib_idx].D = calib_cam.D * 0
            calib_new.camera_calib[calib_idx].P = None
            calib_new.camera_calib[calib_idx].Rrect = None

    calib_new.write(calib_out_path)
