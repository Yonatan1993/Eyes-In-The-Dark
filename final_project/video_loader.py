import cv2
from a_star import *
from guide_person import track_and_guide
import traceback



class VideoLoader:
    count = 0
    def __init__(self, video_path, camera_connected=False):
        self.current_frame = None
        self.camera_connected = camera_connected
        self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)

    def is_camera_connected(self):
        return self.video.grab()

    def closeCamera(self):
        self.video.release()
        cv2.destroyAllWindows()

    def set_current_frame(self, frame):
        self.current_frame = frame

    def get_current_frame(self):
        return self.current_frame

    def get_frame_from_camera(self):
        # Check if camera opened successfully
        self.camera_connected = self.is_camera_connected()
        if not self.camera_connected:
            print("Error opening video stream.")
            self.closeCamera()
            return
        # Capture frame-by-frame
        ret, frame = self.video.read()
        return frame

    def show_frame(self, frame):
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.closeCamera()

    def starting_model(self, algo_frame, video_loader):
        # pass to model

        while self.video.isOpened():
            try:
                # self.count += 1
                # if self.count % 4 != 0:
                #     continue
                frame = self.get_frame_from_camera()
                if frame is not None:
                    self.show_frame(frame)
                    screen_height, screen_width = frame.shape[:2]
                    start, end, maze_solver_path, obstacle_list = algo_frame.process_frame(frame)
                    track_and_guide(start, end,  maze_solver_path, algo_frame, video_loader
                                    , screen_height, screen_width, obstacle_list)

            except Exception as e:

                if str(e) == 'No person Detected in camera':
                    print("No Person Detect in frame")
                elif str(e) == "No obstacle Exception":
                    print("No obstacle Detect in frame")
                else:
                    print("Error: ", str(e))
                    traceback.print_exc()


if __name__ == "__main__":
    #video_loader = VideoLoader('C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5/data/video'
                       #        '/live_bypass_right.mp4')

    video_loader = VideoLoader(0)
    algo = Algo()
    frame = video_loader.get_frame_from_camera()
    video_loader.starting_model(algo, video_loader)
    video_loader.video.release()
