#open with meshlab
import freenect
import time
from PIL import Image
import numpy as np

#Kinect Parameters
minDistance = -10.0
scaleFactor = 0.0021
w=640.0
h=480.0

KinectAngle=0
#Tilt the Kinect
ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)
freenect.set_tilt_degs(dev, KinectAngle) #Min=-30, Max=30
dev=freenect.close_device(dev)
time.sleep(3)

def generate_pointcloud(pil_rgb_img, pil_depth_img, ply_file):
    points = []    
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            color = rgb.getpixel((u,v))
            Z=(depth[v][u])*0.1
            if Z==0:continue
            X=(u - (w / 2.0)) * (Z + minDistance) * scaleFactor
            Y=(v - (h / 2.0)) * (Z + minDistance) * scaleFactor
            points.append("%f %f %f %d %d %d 0\n"%(X,Y,Z,color[0],color[1],color[2]))

    with open(ply_file,"w") as ply:
        ply.write("ply\n" + \
                  "format ascii 1.0\n" + \
                  "element vertex {}\n".format(len(points)) + \
                  "property float x\n" + \
                  "property float y\n" + \
                  "property float z\n" + \
                  "property uchar red\n" + \
                  "property uchar green\n" + \
                  "property uchar blue\n" + \
                  "property uchar alpha\n" + \
                  "end_header\n" + \
                  "{}".format("".join(points)))


rgb = Image.fromarray(freenect.sync_get_video()[0])
KinectDepth,_=freenect.sync_get_depth(0, freenect.DEPTH_MM)
depth=np.array(KinectDepth)

generate_pointcloud(rgb, depth, "PointCloud.ply")

