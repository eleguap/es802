# import numpy as np
import cv2
import time
import csv

class detector(object):
    def __init__(self,input):
        self.input = input

    def get_input(self):
        return self.input

    def set_input(self,input):
        self.input = input

    def capture_and_save_image(self,ret,frame,voltage):
        # If frame is successfully captured, save the captured frame as an image
        if ret:
            cv2.imwrite(f'Images/{voltage}_{time.time()}.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 10])

    def run_detection(self,markers,voltage,filename,save_image=False):
        x = input("Press 'e' to start: ")

        while x != 'e':
            if x == 'q':
                print('Bet, ending.')
                return None
            x = input("Try again: ")

        cap = cv2.VideoCapture(self.get_input())

        while True:
            ret, frame = cap.read()
            cv2.imshow('Video Feed', frame)

            key = cv2.waitKey(1)

            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('e'):
                previous_time = time.time()
                break

        while True:
            ret, frame = cap.read()
            cv2.imshow('Video Feed', frame)

            # Check for keyboard input
            key = cv2.waitKey(1)

            # If 'q' is pressed, exit the loop
            if key & 0xFF == ord('q'):
                break
            # If 'e' is pressed, capture and save an image
            elif key & 0xFF == ord('e'):
                elapsed_time = time.time() - previous_time
                with open(filename, 'a', newline='') as csvfile:
                    # creating a csv writer object
                    csvwriter = csv.writer(csvfile)
                    # writing the data rows
                    csvwriter.writerow([voltage,60/(elapsed_time*markers)])
                previous_time = time.time()
                if save_image:
                    self.capture_and_save_image(ret,frame,voltage)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detect = detector(0)

    while True:
        voltage = input('Voltage: ')

        if voltage == 'q':
            break

        current = input('Current: ')

        if current == 'q':
            break

        with open('200gDownCurrent1.csv', 'a', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            # writing the data rows
            csvwriter.writerow([voltage,current])

    # while True:
    #     voltage = input('Voltage: ')

    #     if voltage == 'q':
    #         break

    #     speed = input('Time: ')

    #     if speed == 'q':
    #         break

    #     with open('50gDowncCurrent1.csv', 'a', newline='') as csvfile:
    #         # creating a csv writer object
    #         csvwriter = csv.writer(csvfile)
    #         # writing the data rows
    #         csvwriter.writerow([voltage,1/(10*float(speed))])

    # Blue
    # detect.run_detection(3,20,'BlueMotor3Marker.csv')

    # Switch
    # detect.run_detection(3,20,'SwitchMotor3Marker.csv',True)

    # Broken
    # detect.run_detection(3,20,'BrokenMotor3Marker.csv')

    # Blue1
    # detect.run_detection(1,20,'BlueMotor1Marker.csv',True)
