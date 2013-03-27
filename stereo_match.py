'''
Simple example of stereo image matching and point cloud generation.

Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net/ )
'''

import numpy as np
import cv2
import sys
import cv

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')


if __name__ == '__main__':
    print 'loading images...'
    
   # mx1 = np.asarray(cv.Load("stereo_camera_calibrate/mx1.xml"))
   # my1 = np.asarray(cv.Load("stereo_camera_calibrate/my1.xml"))
   # mx2 = np.asarray(cv.Load("stereo_camera_calibrate/mx2.xml"))
   # my2 = np.asarray(cv.Load("stereo_camera_calibrate/my2.xml"))

   # imgL = cv2.imread(sys.argv[1])
   # imgR = cv2.imread(sys.argv[2])
    
   # imgL_r = cv2.remap(imgL, mx1, my1, cv2.INTER_LINEAR)
   # imgR_r = cv2.remap(imgR, mx2, my2, cv2.INTER_LINEAR)

   # cv2.imwrite("leftrect.png", imgL_r)
   # cv2.imwrite("rightrect.png", imgR_r)

    imgL = cv2.pyrDown( cv2.imread(sys.argv[1]) )  # downscale images for faster processing
    imgR = cv2.pyrDown( cv2.imread(sys.argv[2]) )

  #  imgL = cv2.imread(sys.argv[1])
  #  imgR = cv2.imread(sys.argv[2])

    # disparity range is tuned for 'aloe' image pair
    window_size = 6
    min_disp = 0
    num_disp = 112-min_disp
    stereo = cv2.StereoSGBM(minDisparity = min_disp,
        numDisparities = num_disp,
        SADWindowSize = window_size,
        uniquenessRatio = 16,
        speckleWindowSize = 100,
        speckleRange = 32,
        disp12MaxDiff = 1,
        P1 = 8*3*window_size**2,
        P2 = 32*3*window_size**2,
        fullDP = False
    )

    print 'computing disparity...'
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    cv.SaveImage("disp.png", disp)

    print 'generating 3d point cloud...',
    h, w = imgL.shape[:2]
    f = 0.8*w                          # guess for focal length
   # Q = np.float32([[1, 0, 0, -0.5*w],
    #                [0,-1, 0,  0.5*h], # turn points 180 deg around x-axis,
    #                [0, 0, 0,     -f], # so that y-axis looks up
    #                [0, 0, 1,      0]])
    Q = np.float32([[1, 0, 0, -405.29743194580078],
		    [0, 1, 0, -474.25981140136719],
                    [0, 0, 0, 942.75118959968620],
                    [0, 0, .41217153724593619, 12.861756971321164]])
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = sys.argv[3]
    write_ply(sys.argv[3], out_points, out_colors)
    print '%s saved' % sys.argv[3]

    #cv2.imshow('left', imgL)
    #cv2.imshow('disparity', (disp-min_disp)/num_disp)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
