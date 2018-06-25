import matplotlib.pyplot as plt
import numpy as np

"""Characteristics of a stereo system."""
__author__ = "Giulio Marin"
__email__ = "giulio.marin@me.com"
__date__ = "2016/04/30"

class Camera:
    def __init__(self, sensor_name, lens_name, sensor_size, fov, baseline, subpixel):
        # input
        self.sensor_size = np.asarray(sensor_size)
        self.fov = np.asarray(fov)
        self.fov_rad = np.deg2rad(np.asarray(fov))
        self.baseline = float(baseline)
        self.subpixel = float(subpixel)
        self.name = "%s_%s_b%.0f" % (sensor_name, lens_name, self.baseline)

        # Computed
        self.focal = self.sensor_size / 2.0 / np.tan(self.fov_rad / 2.0)

    def __repr__(self):
        str = "-------------------------------"
        str += "\nSensor: %s" % self.name
        str += "\nSize = [%d, %d] px" % (self.sensor_size[0], self.sensor_size[1])
        str += "\nFoV = [%.2f, %.2f] deg" % (self.fov[0], self.fov[1])
        str += "\nFocal = [%.2f, %.2f] px" % (self.focal[0], self.focal[1])
        str += "\n-------------------------------"
        return str

######################
# Parameters
######################

# Visualization
LINE_W = 2
Z_VEC = np.arange(300, 2001, 10)

# Stereo cameras
cameras = []
# cameras.append(Camera("test", "test", (480, 640), (37.0, 47.0), 50.0, 0.5))
cameras.append(Camera("sir21", "?", (480, 640), (36.7, 47.0), 50.0, 0.5))
cameras.append(Camera("sir30", "?", (480, 640), (54.6, 69.0), 50.0, 0.5))
aptina_f = (51.6, 76.1)
cameras.append(Camera("aptina_f", "DHB5025", (800, 1280), aptina_f, 60.0, 0.5))
cameras.append(Camera("aptina_h", "DHB5025", (400, 640), aptina_f, 60.0, 0.5))
# aptina_f = (54.0, 69.0)
# cameras.append(Camera("aptina_f", "DIF04043EH", (800, 1280), aptina_f, 50.0, 0.5))
# cameras.append(Camera("aptina_f", "DIF04043EH", (800, 1280), aptina_f, 65.0, 0.5))
# cameras.append(Camera("aptina_h", "DIF04043EH", (400, 640), aptina_f, 50.0, 0.5))
# cameras.append(Camera("aptina_h", "DIF04043EH", (400, 640), aptina_f, 65.0, 0.5))

print "Cameras"
for cam in cameras:
    print cam


######################
# Percentage overlapping FOV
######################

plt.figure()
for cam in cameras:
    percFov = 1 - cam.baseline * cam.focal[1] / (Z_VEC * cam.sensor_size[1])
    plt.plot(Z_VEC, percFov, label=cam.name)

plt.title('Percentage common FoV')
plt.xlabel('Distance [mm]')
plt.ylabel('Common FoV [%]')
plt.legend(loc='lower right')
plt.xlim((Z_VEC[0], Z_VEC[-1]))
plt.grid()
for l in plt.gca().lines:
    plt.setp(l, linewidth=LINE_W)
for l in plt.gca().get_legend().get_lines():
    plt.setp(l, linewidth=LINE_W)
# plt.savefig('commonfov.png', transparent = True)

######################
# Size of FOV
######################

plt.figure()
for cam in cameras:
    percFov = 1 - cam.baseline * cam.focal[1] / (Z_VEC * cam.sensor_size[1])
    sizeFov = percFov * 2 * np.tan(cam.fov_rad[1] / 2.) * Z_VEC
    plt.plot(Z_VEC, sizeFov, label=cam.name)

plt.title('Size of common H FoV')
plt.xlabel('Distance [mm]')
plt.ylabel('Size of FoV [mm]')
plt.legend(loc='upper left')
plt.xlim((Z_VEC[0], Z_VEC[-1]))
plt.grid()
for l in plt.gca().lines:
    plt.setp(l, linewidth=LINE_W)
for l in plt.gca().get_legend().get_lines():
    plt.setp(l, linewidth=LINE_W)
# plt.savefig('sizecommonfovh.png', transparent = True)

plt.figure()
for cam in cameras:
    percFov = 1 - cam.baseline * cam.focal[0] / (Z_VEC * cam.sensor_size[0])
    sizeFov = percFov * 2 * np.tan(cam.fov_rad[0] / 2.) * Z_VEC
    plt.plot(Z_VEC, sizeFov, label=cam.name)

plt.title('Size of common V FoV')
plt.xlabel('Distance [mm]')
plt.ylabel('Size of FoV [mm]')
plt.legend(loc='upper left')
plt.xlim((Z_VEC[0], Z_VEC[-1]))
plt.grid()
for l in plt.gca().lines:
    plt.setp(l, linewidth=LINE_W)
for l in plt.gca().get_legend().get_lines():
    plt.setp(l, linewidth=LINE_W)
# plt.savefig('sizecommonfovv.png', transparent = True)

######################
# Depth resolution
######################

plt.figure()
for cam in cameras:
    deltaZ = Z_VEC ** 2 / (cam.focal[1] * cam.baseline - Z_VEC * cam.subpixel) * cam.subpixel
    plt.plot(Z_VEC, deltaZ, label=cam.name)

plt.title('Depth resolution at different distance')
plt.xlabel('Distance [mm]')
plt.ylabel('Depth resolution [mm]')
plt.legend(loc='upper left')
plt.xlim((Z_VEC[0], Z_VEC[-1]))
plt.grid()
for l in plt.gca().lines:
    plt.setp(l, linewidth=LINE_W)
for l in plt.gca().get_legend().get_lines():
    plt.setp(l, linewidth=LINE_W)
for p in np.arange(1, 5, 1):
    plt.plot(Z_VEC, Z_VEC * p / 100.0, 'k--')
# plt.savefig('depthres.png', transparent = True)

######################
# Disparity vs Depth
######################

plt.figure()
for cam in cameras:
    disparity = cam.baseline * cam.focal[1] / Z_VEC
    plt.plot(Z_VEC, disparity, label=cam.name)

plt.title('Disparity at different distance')
plt.xlabel('Distance [mm]')
plt.ylabel('Disparity [pixel]')
plt.legend(loc='upper right')
plt.xlim((Z_VEC[0], Z_VEC[-1]))
plt.grid()
for l in plt.gca().lines:
    plt.setp(l, linewidth=LINE_W)
for l in plt.gca().get_legend().get_lines():
    plt.setp(l, linewidth=LINE_W)
# plt.savefig('disparitydepth.png', transparent = True)

plt.show()
