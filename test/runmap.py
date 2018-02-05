import os
import re
import utm
import matplotlib.pylab as plt
import numpy as np
from scipy import ndimage


def parse_gpx(gpx_path):
    trkpt = []
    for l in open(gpx_path, 'r').readlines():
        if 'trkpt' in l and ('lon' in l or 'lat' in l):
            lonlat_coord = re.findall('[-+]?\d*\.\d+|\d+', l, re.IGNORECASE)
            utm_coord = utm.from_latlon(float(lonlat_coord[1]), float(lonlat_coord[0]))
            trkpt.append((float(lonlat_coord[0]), float(lonlat_coord[1]), utm_coord[0], utm_coord[1]))
    return trkpt


if __name__ == '__main__':
    # Parameters
    gpx_dir = '/Users/giulio/Downloads/Runtastic 2017-12-04 03.00.00'
    gpx_paths = sorted([os.path.join(gpx_dir, f) for f in os.listdir(gpx_dir) if f.endswith('.gpx')])
    img_width = 3840
    point_radius = 0
    size_filter = 21
    img_max = 5
    cluster_max_dist = 100000

    # Get coordinates
    trkpts = []
    for gpx_path in gpx_paths:
        print 'Processing: %s' % gpx_path
        trkpt = parse_gpx(gpx_path)
        if len(trkpt) == 0:
            # print 'Skip empty map'
            continue

        # Compute scale
        s = 1. / np.cos(np.deg2rad(trkpt[0][1]))

        # Check if current map belongs with any existing group
        curr_map_id = -1
        min_dist = np.inf
        for map_id, map in enumerate(trkpts):
            # Distance between center of the map and center of the current track
            dist = np.linalg.norm(np.mean(np.asarray(trkpt)[:, 2:], 0) - np.mean(np.asarray(map)[:, 2:], 0)) * s
            # print int(dist)
            if dist < cluster_max_dist and dist < min_dist:
                curr_map_id = map_id
                min_dist = dist
        if curr_map_id < 0:
            print 'Creating new map'
            trkpts.append(trkpt)
        else:
            print 'Adding track to map %d' % curr_map_id
            trkpts[curr_map_id].extend(trkpt)
    print 'Found %d maps' % len(trkpts)

    for curr_map_id, trkpt in enumerate(trkpts):
        # Create image
        print 'Create image: %d/%d' % (curr_map_id + 1, len(trkpts))
        pts = np.asarray(trkpt)[:, 2:]
        trk_min = np.min(pts, 0)
        trk_max = np.max(pts, 0)
        trk_size = trk_max - trk_min
        img_size = [int(img_width), int(img_width * trk_size[1] / trk_size[0])]
        img = np.zeros((img_size[1], img_size[0]), dtype=np.float)
        for p in pts:
            uv = (p - trk_min) / trk_size * img_size
            for uu in range(-point_radius, point_radius + 1):
                for vv in range(-point_radius, point_radius + 1):
                    v_vv = int(uv[1] + vv)
                    u_uu = int(uv[0] + uu)
                    if (0 <= v_vv < img_size[1]) and (0 <= u_uu < img_size[0]):
                        img[v_vv, u_uu] += 1
        img = ndimage.uniform_filter(img, size=size_filter)
        img[img > img_max] = img_max
        img_scale = (img / np.max(img) * 255).astype(np.uint8)

        # Save map
        cmred = 255 * np.ones((256, 3), dtype=np.uint8)
        cmred[:, 1] = np.linspace(255, 0, 256)
        cmred[:, 2] = np.linspace(255, 0, 256)
        img_color = cmred[img_scale]
        img_color = np.flipud(img_color)
        plt.imsave('/Users/giulio/Desktop/gpx/map_%d.png' % curr_map_id, img_color)

        # Show map
        if False:
            plt.figure()
            plt.imshow(img_scale, cmap='Greys')
            plt.colorbar()
            plt.show()