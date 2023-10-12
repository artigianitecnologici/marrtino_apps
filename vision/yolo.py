import sys,os,time
import argparse
import cv2
import torch
from PIL import Image

from models.common import DetectMultiBackend



from imageserver import ImageServer





class Yolo:

    def __init__(self):
        print('Loading yolov5 model...')
        # Model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        print(self.model.names)
        print('Loading yolov5 model...Done')

    def evalImageFile(self, imfile):
        #img = Image.open(imfile)  # PIL image
        img = cv2.imread(imfile)[..., ::-1]  # OpenCV image (BGR to RGB)
        return self.evalImage(img)


    def evalImage(self, img):

        if img is None:  # not an image
            return None  

        print(type(img))
        print(img.shape)

        results = self.model([img], size=640)
        # results = self.model([img1,img2,...], size=640) # batch of images

        # Results
        results.print()
        results.show()
        #results.save() save results on files in 'runs/...' folders

        #results.xyxy[0]  # img predictions (tensor)
        #results.pandas().xyxy[0]  # img predictions (pandas)

        dat = results.pandas().xyxy[0]

        print(dat)

        #      xmin    ymin    xmax   ymax  confidence  class    name
        # 0  749.50   43.50  1148.0  704.5    0.874023      0  person
        # 1  433.50  433.50   517.5  714.5    0.687988     27     tie
        # 2  114.75  195.75  1095.0  708.0    0.624512      0  person
        # 3  986.00  304.00  1028.0  420.0    0.286865     27     tie
       
        res = ""
        for i in dat.index:
            n = dat.iloc[i]["name"]
            c = dat.iloc[i]["confidence"]
            res = res + "%s;%0.3f;" %(n,c)
            
        print(res)

        # person;0.874;tie;0.688;person;0.625;tie;0.289;

        

        return res


ynet = None

def yolo_predict(img):
    global ynet
    if ynet is None:
        ynet = Yolo()
    if isinstance(img,str):
        r = ynet.evalImageFile(img)
    else:
        r = ynet.evalImage(img)       
    print("Result: %r" %r)
    return r



# wait for Keyboard interrupt
def dospin():
    run = True
    while (run):
        try:
            time.sleep(120)
        except KeyboardInterrupt:
            print("Exit")
            run = False



# main function
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Yolov5')
    parser.add_argument('-image', type=str, default=None, help='image file')
    parser.add_argument('--server', help='start server', action='store_true')
    parser.add_argument('--init', help='init net', action='store_true')

    args = parser.parse_args()

    # yolo server port    
    yoloport=9300

    if args.image is not None:
        print('Predict image %s' %args.image)
        ynet = Yolo()
        r = ynet.evalImageFile(args.image)
        print(r)

    if args.server:
        imgserver = ImageServer(yoloport)
        imgserver.set_predict_cb_fn(yolo_predict)
        imgserver.start()
        dospin() 
        imgserver.stop()
    elif args.init:
        # init net
        ynet = Yolo()


    sys.exit(0)

