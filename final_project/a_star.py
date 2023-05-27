import numpy as np
import torch
import cv2
import math
import pyttsx3
import threading
import time
from multiprocessing import Process
from queue import Queue
import matplotlib.pyplot as plt
from find_path import build_path, a_star
from video_loader import *
from gtts import gTTS
from playsound import playsound
import threading
import time
from speeches import Speech
from project_utils import speak



class Algo:
    TEST_MODE = False
    NO_OBS_ALERT = False
    GREETING_ALERT = False
    OBSTACLE_ALERT = False


    def __init__(self):
        path = 'C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5/yolov5s.pt'
        self.model = torch.hub.load('C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5', 'custom', path,
                                    source='local')
        self.size = 416
        self.save_text_to_speach()
        b = self.model.names[0] = 'person'

    def save_text_to_speach(self):
        texts = ["Hello , Welcome to, Eyes in the Dark.","No obstacle detected, please continue.",
                 "There is an obstacle in the room", "Stop , take a left turn to start bypass the obstacle",
                 "Stop , take a right turn to start bypass the obstacle"
                 ]
        # Iterate over each text
        for i, text in enumerate(texts):
            # Create a gTTS object
            tts = gTTS(text=text, lang='en', slow=False)
            # Save the speech audio into a file
            filename = f"speek_files/{texts[i].split()[0]}_{i+1}.mp3"
            tts.save(filename)

    # def speak(self, speech_to_speak):
    #     if speech_to_speak.value == 1:
    #         playsound("speek_files/Hello_1.mp3")
    #     elif speech_to_speak.value == 2:
    #         playsound("speek_files/No_2.mp3")
    #     elif speech_to_speak.value == 3:
    #         playsound("speek_files/There_3.mp3")



    def say_to_person(self, message):
        Process(target=say_instrutions,
                args=(message,)).start()

    def detect_person_in_img(self, img):
        print("---In Function: detect_person_in_img()---")
        results = self.model(img, self.size)

        a = results.pandas().xyxy[0]
        pepole_list = []
        for index, row, in results.pandas().xyxy[0].iterrows():
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])
            d = (row['class'])
            print(f"<----found somthing! Making sure its a person!---->{row['name']}")
            if (d == 0) or (d == 77) or (d == 16) or (d == 15) or (d == 36):
                recx1, recty1 = ((x1 + x2) / 2, (y1 + y2) / 2)
                rect_center = int(recx1), int(recty1)
                cx = rect_center[0]
                cy = rect_center[1]
                cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
                person_point = (cy, cx)
                pepole_list.append(person_point)
                if d==0:
                    print(f"Class name = {row['name']}")
                else:
                    print(f"Class name = {row['name']} But we say person")
                print(f"Person Found in frame: ({person_point[0]},{person_point[1]})", end=" - ")

        print(f"Number of persons in frame: {len(pepole_list)}")
        if len(pepole_list) > 0:

            return pepole_list[0]
        else:
            return None

    def detect_obstacles_in_img(self, img):
        print("---In Function: detect_obstacles_in_img---")
        results = self.model(img, self.size)
        a = results.pandas().xyxy[0]
        obstacle_box = tuple()
        obstacles_list = []
        obstacles_list_names = []
        for index, row, in results.pandas().xyxy[0].iterrows():
            res_tuple = ()
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])
            d = (row['class'])
            if d == 36:
                continue
            obstacle_box = obstacle_box + (int(x1), int(y1), abs(int(x1 - x2)), abs(int(y1 - y2)))

            if d != 0:
                res_tuple = ((x1, y1), (x2, y2))
                obstacles_list_names.append(row['name'])
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                recx1, recty1 = ((x1 + x2) / 2, (y1 + y2) / 2)
                rect_center = int(recx1), int(recty1)
                cx = rect_center[0]
                cy = rect_center[1]
                # cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
                cv2.putText(img, row['name'], (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (225, 255, 255), 2)
                obstacles_list.append(res_tuple)

        print(f"Number Of obstacles :{len(obstacles_list_names)} ---> {' '.join(obstacles_list_names)}")
        for obs in obstacles_list:
            print(f"Position Of obstacle ({obs[0]}, {obs[1]})")

        return obstacles_list

    def create_maze(self, obstacles_list, height, width):
        maze = np.zeros((height, width), dtype=int)  # 900x1600
        for upper_left, bottom_right in obstacles_list:
            maze[int(upper_left[1]):int(bottom_right[1]), int(upper_left[0]):int(bottom_right[0])] = 1

        return maze

    def scale_before_solve(self, start, end, maze, scale):
        h, w = maze.shape[:2]
        start = (int(start[0] * scale), int(start[1] * scale))
        end = (int(end[0] * scale), int(end[1] * scale))
        maze = cv2.resize(maze.astype("uint8"), (0, 0), fx=scale, fy=scale)

        return start, end, maze

    def scale_after_solve(self, start, end, maze, maze_solver_path, scale, step=5):
        scale = int(1 / scale)
        h, w = maze.shape[:2]

        start = (int(start[0] * scale), int(start[1] * scale))
        end = (int(end[0] * scale), int(end[1] * scale))
        maze_solver_path = [(int(x * scale), int(y * scale)) for (x, y) in maze_solver_path]
        maze = cv2.resize(maze.astype("uint8"), (0, 0), fx=scale, fy=scale)

        return start, end, maze, maze_solver_path



    def process_frame(self, currnet_frame):

        if type(currnet_frame) == str:
            obstacle_img = cv2.imread(currnet_frame)
            person_point = self.detect_person_in_img(obstacle_img)
            if person_point is None:
                raise Exception("No person Exception")
            else:
                if not self.GREETING_ALERT:
                    # self.say_to_person("Hello, Welcome to, Eyes in the Dark.")
                    threading.Thread(target=speak, args=(Speech.WELCOME,)).start()
                    self.GREETING_ALERT = True
                obstacles_list = self.detect_obstacles_in_img(obstacle_img)
                if len(obstacles_list) == 0:
                    if not self.NO_OBS_ALERT:
                        self.NO_OBS_ALERT = True
                  #      self.say_to_person("No obstacle detected, please continue.")
                    threading.Thread(target=speak, args=(Speech.NO_OBSTACLES,)).start()
                    raise Exception("No obstacle Exception")

        # camera input 0
        else:
            person_point = self.detect_person_in_img(currnet_frame)
            if person_point is None:
                raise Exception("No person Detected in camera")
            else:
                if not self.GREETING_ALERT:
                    #self.say_to_person("Hello, Welcome to, Eyes in the Dark.")
                    threading.Thread(target=speak, args=(Speech.WELCOME,)).start()
                    self.GREETING_ALERT = True
                obstacle_img = currnet_frame
                obstacles_list = self.detect_obstacles_in_img(obstacle_img)
                if len(obstacles_list) == 0:
                    if not self.NO_OBS_ALERT:
                        self.NO_OBS_ALERT = True
                        self.say_to_person("No obstacle detected, please continue.")
                        threading.Thread(target=speak, args=(Speech.NO_OBSTACLES,)).start()
                    raise Exception("No obstacle Exception")

        height, width = obstacle_img.shape[:2]
        maze = self.create_maze(obstacles_list, height, width)

        scale = 0.2
        end = (int(height / 2), width - 10)
        # start, end, maze = self.scale_before_solve(start, end, maze, scale=scale) # start = (45,5), end = (45,155), maze = [(45,5), (45 ,10), (44,15)]
        # self.vis_debug(obstacle_img, maze, [(1, 1)], start, end, scale)

        # maze_solver_path = a_star((int(height / 2), int(width / 2)), end, maze, step=5)
        # if maze_solver_path is None:
        #     print("Cant find path!")
        #     # TODO: Tell the person there is no path to go
        #     return
        maze_solver_path = [(0, 0)]
        # TODO: Add maze_solver_path re-scale
        # start, end, maze, maze_solver_path = self.scale_after_solve(start, end, maze, maze_solver_path, scale=scale, step=5)

        # vis_ui = self.create_maze(obstacles_list, height, width)
        # vis_ui = np.zeros_like(maze)

        if self.TEST_MODE:
            # TODO: Solve vis_ui scaling bug
            self.vis_debug(obstacle_img, vis_ui, maze_solver_path, person_point, end, scale)




        return person_point, end, maze_solver_path, obstacles_list

    def vis_debug(self, obstacle_img, maze, maze_solver_path, start, end, scale):
        maze_vis = cv2.cvtColor((maze * 255).astype("uint8"), cv2.COLOR_GRAY2BGR)

        cv2.circle(maze_vis, (start[1], start[0]), radius=int(30), color=(255, 255, 0), thickness=-1)
        cv2.circle(maze_vis, (end[1], end[0]), radius=int(30), color=(0, 255, 0), thickness=-1)

        maze_solver_path = [(y, x) for x, y in maze_solver_path]
        maze_solver_path = np.array(maze_solver_path)
        cv2.polylines(maze_vis, [maze_solver_path], isClosed=False, color=(0, 255, 0), thickness=1)
        cv2.polylines(obstacle_img, [maze_solver_path], isClosed=False, color=(0, 255, 0), thickness=1)

        vis_obstacle_img = cv2.resize(obstacle_img, (0, 0), fx=1, fy=1)
        # maze_vis = cv2.resize(maze_vis, (0, 0), fx=0.5, fy=0.5)

        # TODO: scaling bug
        # maze_vis = cv2.resize(maze_vis, (0, 0), fx=int(1 / scale), fy=int(1 / scale))
        cv2.imshow("obstacle_img", vis_obstacle_img)
        cv2.imshow("maze_vis", maze_vis)
        cv2.waitKey(0)


if __name__ == "__main__":
    algo = Algo()
    # vl = VideoLoader(0)
    # vl.run()
    # algo.process_frame(vl.set_current_frame())
    algo.process_frame(
        currnet_frame='C:/Users/User/PycharmProjects/eyes_in_the_dark/models/yolov5/data/images/chair1.jpg')
