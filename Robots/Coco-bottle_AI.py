#to run paste python bottle_detect.py --network=coco-bottle into the terminal


import jetson.inference
import jetson.utils

import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

#parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="coco-bottle", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.1, help="minimum detection threshold to use")

try:
opt = parser.parse_known_args()[0]
except:
print("")
parser.print_help()
sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, threshold=0.2)

# create video sources & outputs
input = jetson.utils.videoSource("/dev/video0")
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)


def find_angle(x):
PPD = 0.0608
print(PPD)
A = 600-x
print(A)
output = A*PPD

return output

def Rotate(x):
if x == 1:
print("Turn LEFT")
else:
print("Turn RIGHT")

def Robot_Move():
print("move forward")


# process frames until the user exits
while True:
# capture the next image
img = input.Capture()

# detect objects in D ` ```` `` ` ` ` ` `` ` ` `` ` ` ` ` `` ` ` ` ` ` `` `q1w2 the image (with overlay)
detections = net.Detect(img, overlay=opt.overlay)

# print the detections
print("detected {:d} objects in image".format(len(detections)))

#for detection in detections:
#print(type(detection))

for i in range(len(detections)):
class_idx = detections[i].ClassID



if class_idx == 0:
center_cordinates = detections[i].Center
print("class index ", class_idx)
print("cords ", center_cordinates)
obj_angle = find_angle(center_cordinates[0])
print("the angle is ", obj_angle)

Angle_Buffer_Max = 5
Angle_Buffer_Min = -5

if obj_angle > Angle_Buffer_Max:
Rotate(1)

elif obj_angle < Angle_Buffer_Min:
Rotate(0)

else:
Robot_Move()

else:
print("class index ", class_idx)



# render the image
output.Render(img)

# update the title bar
output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

# print out performance info
net.PrintProfilerTimes()

# exit on input/output EOS
if not input.IsStreaming() or not output.IsStreaming():
#break

