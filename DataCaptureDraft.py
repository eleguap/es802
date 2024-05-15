import cv2
import numpy as np

class detector(object):
    def __init__(self,input):
        self.input = input

    def get_input(self):
        return self.input

    def set_input(self,input):
        self.input = input

    # def detect_screen(self,frame,scale = 0):
    #     height, width = frame.shape[:2]


    #     if scale:
    #         dimensions = (int(scale * width), int(scale * height))
    #         frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    #     kernel = (7, 7)
    #     sigmaX = 0
    #     blurred = cv2.GaussianBlur(frame, kernel, sigmaX)
    #     hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #     lower_saturation = 0
    #     upper_saturation = 40

    #     # Create a mask based on the saturation channel
    #     mask = cv2.inRange(hsv[:,:,1], lower_saturation, upper_saturation)

    #     contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    #     if contours:
    #         largest_contour = max(contours, key=cv2.contourArea)
    #         x, y, w, h = cv2.boundingRect(largest_contour)
    #         origin = (x, y)
    #         endpoint = (x + w, y + h)
    #         cv2.rectangle(frame, origin, endpoint, (255, 0, 0), 2)

    #     return mask

    def run_detection(self,frame_processing = None):
        cap = cv2.VideoCapture(self.get_input())

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            if frame_processing:
                frame = frame_processing(self,frame)

            cv2.imshow('Frame',frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


detect = detector(0)

detect.run_detection(detector.detect_screen)

# def best_exponential_model(self,exponents):
    #     x = self.get_x()
    #     best_coefficient

    #     for e in exponents:
    #         a = self.exponential_model(e)
    #         plt.plot(x,a * x**e,label=f'Exp Coef: {a}')
