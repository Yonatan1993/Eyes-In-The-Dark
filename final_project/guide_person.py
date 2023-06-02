import pygame
import pyttsx3
import time
import math
from multiprocessing import Process
from speeches import Speech
from gtts import gTTS
from playsound import playsound
import threading
from project_utils import speak



# Define the colors
white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
brown = (165, 42, 42)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)

# Define the text-to-speech message
message = "   ."

# Set the initial velocity of the dot
velocity = [0, 0]

# Define the size of the trail
trail_size = 500
PASSED_YELLOW_CORNER = False
PASSED_ORANGE_CORNER = False
PERSON_STARTED_BYPASS_ROUTE = False
PERSON_AT_THE_MIDDLE = False




# def speak( speech_to_speak):
#     if speech_to_speak.value == 1:
#         playsound("speak_files/Hello_1.mp3")
#     elif speech_to_speak.value == 2:
#         playsound("speak_files/No_2.mp3")
#     elif speech_to_speak.value == 3:
#         playsound("speak_files/There_3.mp3")
#     elif speech_to_speak.value == 4:
#         playsound("speak_files/Stop_4.mp3")
#     elif speech_to_speak.value == 5:
#         playsound("speak_files/Stop_5.mp3")


def init_engines(screen_height, screen_width):
    # Initialize Pygame
    pygame.init()
    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("2D Simulation")

    return  screen


def check_collision(dot_pos, dot_radius, last_color_touched,screen):
    # Check if the dot has touched a colored pixel
    screen_width = screen.get_width()
    for i in range(-dot_radius - 1, dot_radius + 1):
        for j in range(-dot_radius - 1, dot_radius + 1):
            x = int(dot_pos[0] + i)
            y = int(dot_pos[1] + j)
            color = screen.get_at((x, y))
            # print(f"Pixel color at ({x}, {y}): {color}")
            if color == yellow and last_color_touched != 'yellow':
                threading.Thread(target=speak,args=(Speech.COLLISION_WARNING,)).start()
                last_color_touched = 'yellow'
                return last_color_touched


            elif color == blue and last_color_touched != 'blue':
                if dot_pos[0] < screen_width / 2:  # If the dot is on the left half of the screen
                    threading.Thread(target=speak, args=(Speech.COLLISION_WARNING_LEFT,)).start()
                else:  # If the dot is on the right half of the screen
                    threading.Thread(target=speak, args=(Speech.COLLISION_WARNING_RIGHT,)).start()
                last_color_touched = 'blue'
                return last_color_touched

            elif color == gray and last_color_touched != 'gray':
                threading.Thread(target=speak, args=(Speech.WARNING_IN_FRONT_LEFT,)).start()
                last_color_touched = 'gray'
                return last_color_touched

            elif color == brown and last_color_touched != 'brown':
                threading.Thread(target=speak, args=(Speech.WARNING_IN_FRONT_RIGHT,)).start()
                last_color_touched = 'brown'
                return last_color_touched

            elif color == orange and last_color_touched != 'orange':
                threading.Thread(target=speak, args=(Speech.WARNING_IN_FRONT_BACK,)).start()
                last_color_touched = 'orange'
                return last_color_touched

    return last_color_touched


def track_and_guide(current_pos, end_position, path, ap, vl, screen_height, screen_width, obstacle_pos=None):
    print("******Simulation Started**********")
    # Define the main loop
    screen = init_engines(screen_height, screen_width)
    # Define the font for the text-to-speech output
    font = pygame.font.Font(None, 30)
    RUNNING = True
    frame_rate = 60
    # Define a list to keep track of previous dot positions
    dot_positions = []
    last_spoken_color = None
    # Define the radius of the dot and the obstacle

    dot_radius = 20
    # Define the speed of the dot in pixels
    dot_speed = 2.0
    # Define the start position
    start_position = (current_pos[1], current_pos[0])
    end_position = (end_position[1], end_position[0])
    clock = pygame.time.Clock()

    while RUNNING:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        # Define the obstacle parameters
        obstacle_color = (255, 0, 0)  # red
        # if obstacle_pos is None:
        #     obstacle_pos = [((0, 0), (1, 1))]
        obstacle_top_left, obstacle_bottom_right = obstacle_pos[0]
        ymin, xmin = obstacle_top_left
        ymax, xmax = obstacle_bottom_right
        obstacle_width = xmax - xmin
        obstacle_height = ymax - ymin

        frame = vl.get_frame_from_camera()
        vl.show_frame(frame)
        # Update the dot's position
        person_pos = ap.detect_person_in_img(frame)
        if person_pos is None:
            dot_pos = (current_pos[1], current_pos[0])
        else:
            current_pos = person_pos
            dot_pos = (current_pos[1], current_pos[0])

        # Append the current position to the list of dot positions
        # Keep only the last `trail_size` positions
        dot_positions.append(tuple(dot_pos))
        dot_positions = dot_positions[-trail_size:]

        # Check for collisions with the obstacle or a yellow pixel
        last_spoken_color = check_collision(dot_pos, dot_radius, last_spoken_color, screen)
        if not PERSON_STARTED_BYPASS_ROUTE:
            starting_bypass_route(dot_pos, last_spoken_color, obstacle_height, obstacle_pos)
        if not PASSED_YELLOW_CORNER and PERSON_STARTED_BYPASS_ROUTE:
            check_if_person_passed_blue_corner(dot_pos, obstacle_pos, obstacle_height, last_spoken_color)
        if not PASSED_ORANGE_CORNER and PERSON_STARTED_BYPASS_ROUTE:
            last_spoken_color = check_if_person_passed_orange_corner(dot_pos, obstacle_pos, obstacle_height,
                                                                     last_spoken_color)
        if not PERSON_AT_THE_MIDDLE and PASSED_ORANGE_CORNER:
            is_person_at_middle_line(dot_pos, obstacle_pos, obstacle_height, last_spoken_color,tolerance=10)

        # Draw the screen
        screen.fill(white)
        pygame.draw.circle(screen, black, start_position, 5)
        pygame.draw.circle(screen, black, end_position, 5)
        pygame.draw.circle(screen, green, dot_pos, dot_radius)

        # Draw the trail
        for i in range(1, len(dot_positions)):
            pygame.draw.line(screen, black, dot_positions[i - 1], dot_positions[i], int(dot_radius / dot_radius))


        # Define the colors for the coating
        coating_colors = {
            'up': (128, 128, 128),  # gray
            'down': (165, 42, 42),  # brown
            'left': (0, 0, 255),  # blue
            'right': (255, 165, 0),  # orange
            'center': (255, 255, 0)  # yellow
        }

        # Create the obstacle surface
        obstacle_surface = pygame.Surface((obstacle_width, obstacle_height))
        obstacle_surface.fill(obstacle_color)

        # Draw the coating on the surface
        coating_width = 5

        # Top coating
        top_coating_rect = pygame.Rect((0, 0), (obstacle_width, coating_width))
        pygame.draw.rect(obstacle_surface, coating_colors['up'], top_coating_rect)

        # Bottom coating
        bottom_coating_rect = pygame.Rect((0, obstacle_height - coating_width), (obstacle_width, coating_width))
        pygame.draw.rect(obstacle_surface, coating_colors['down'], bottom_coating_rect)

        # Left coating
        left_coating_rect = pygame.Rect((0, 0), (coating_width, obstacle_height))
        pygame.draw.rect(obstacle_surface, coating_colors['left'], left_coating_rect)

        # Right coating
        right_coating_rect = pygame.Rect((obstacle_width - coating_width, 0), (coating_width, obstacle_height))
        pygame.draw.rect(obstacle_surface, coating_colors['right'], right_coating_rect)

        # Center coating
        center_coating_rect = pygame.Rect((coating_width, coating_width),
                                          (obstacle_width - 2 * coating_width, obstacle_height - 2 * coating_width))
        pygame.draw.rect(obstacle_surface, coating_colors['center'], center_coating_rect)

        # Draw small red rectangle on top of the yellow coating
        # TODO : Bring this part Back
        # red_rect = pygame.Rect(int(xmin), int(ymin), (obstacle_width, obstacle_height))
        # pygame.draw.rect(obstacle_surface, obstacle_color, red_rect)

        # Draw the obstacle on the screen
        screen.blit(obstacle_surface, obstacle_top_left)

        text = font.render('Eyes In The Dark TM', True, black)
        screen.blit(text, (10, screen_height - 50))
        pygame.display.flip()

        # Delay for the specified frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()


def starting_bypass_route(dot_pos,last_spoken_color, obstacle_height, obstacle_pos):
    global PERSON_STARTED_BYPASS_ROUTE
    if not PERSON_STARTED_BYPASS_ROUTE:
        PERSON_STARTED_BYPASS_ROUTE = True
        print("---Inside starting_bypass_route() function ")
        # Define the upper left and lower left corners of the obstacle
        upper_left_corner, _ = obstacle_pos[0]
        yu_left, xu_left = upper_left_corner
        bottom_left_corner = (yu_left, xu_left + obstacle_height)
        yb_right, xb_right = bottom_left_corner

        # Calculate the distances between the person and the upper left and lower left corners
        upper_left_distance = math.sqrt((dot_pos[0] - yu_left) ** 2 + (dot_pos[1] - xu_left) ** 2)
        lower_left_distance = math.sqrt((dot_pos[0] - yb_right) ** 2 + (dot_pos[1] - xb_right) ** 2)

        # Check which corner the person is closer to
        if upper_left_distance < lower_left_distance:
            # The person is closer to the upper left corner, so they should turn right
            threading.Thread(target=speak, args=(Speech.START_BYPASS_LEFT,)).start()
            print("________Tell The person take left turn______")
        else:
            # The person is closer to the lower left corner, so they should turn left
            threading.Thread(target=speak, args=(Speech.START_BYPASS_RIGHT,)).start()
            print("______Tell The person take right turn_____")

        last_spoken_color = 'upper_left_start'

    return last_spoken_color


def check_if_person_passed_blue_corner(dot_pos, obstacle_pos, obstacle_height,last_spoken_color):
    # Define the upper left and lower left corners of the obstacle
    global PASSED_YELLOW_CORNER
    upper_left_corner, _ = obstacle_pos[0]
    yu_left, xu_left = upper_left_corner
    bottom_left_corner = (yu_left, xu_left + obstacle_height)
    yb_right, xb_right = bottom_left_corner

    # Check if the dot has passed the upper left corner
    if dot_pos[1] < xu_left and dot_pos[0] < yu_left:
        PASSED_YELLOW_CORNER = True
        print("------In Function check_if_person_passed_blue_corner() function, person taking right turn ------")
        if last_spoken_color != 'upper_yellow':
            threading.Thread(target=speak,args=(Speech.BYPASS_RIGHT,)).start()
            last_spoken_color = 'upper_yellow'

    # Check if the dot has passed the lower left corner
    elif dot_pos[1] > xb_right and dot_pos[0] < yb_right:
        PASSED_YELLOW_CORNER = True
        print("------In Function check_if_person_passed_blue_corner() function, person taking left turn---- ")
        if last_spoken_color != 'lower_yellow':
            threading.Thread(target=speak, args=(Speech.BYPASS_LEFT,)).start()
            last_spoken_color = 'lower_yellow'

    return last_spoken_color


def check_if_person_passed_orange_corner(dot_pos, obstacle_pos, obstacle_height, last_spoken_color):
    global PASSED_ORANGE_CORNER
    coating_width = 5
    # Define the upper right and lower right corners of the obstacle
    _, bottom_right_corner = obstacle_pos[0]
    yb_right, xb_right = bottom_right_corner
    upper_right_corner = (yb_right, xb_right - obstacle_height)
    yu_right, xu_right = upper_right_corner

    # Check if the dot has passed the upper right corner
    if dot_pos[1] < xu_right and dot_pos[0] > yu_right:
        PASSED_ORANGE_CORNER = True
        if last_spoken_color != 'upper_right_corner':
            print("----In Function check_if_person_passed_orange_corner() , person taking right turn---- ")
            threading.Thread(target=speak, args=(Speech.BYPASS_RIGHT,)).start()
            last_spoken_color = 'upper_right_corner'

    # Check if the dot has passed the bottom right corner
    elif dot_pos[1] > xb_right and dot_pos[0] > yb_right:
        PASSED_ORANGE_CORNER = True
        if last_spoken_color != 'bottom_right_corner':
            print("----In Function check_if_person_passed_orange_corner() , person taking left turn---- ")
            threading.Thread(target=speak, args=(Speech.BYPASS_LEFT,)).start()
            last_spoken_color = 'bottom_right_corner'

    return last_spoken_color


def is_person_at_middle_line(dot_pos, obstacle_pos, obstacle_height, last_spoken_color,tolerance=10):
    global PERSON_AT_THE_MIDDLE
    _, bottom_right_corner = obstacle_pos[0]
    xmin, ymin = bottom_right_corner

    center_line_y = ymin - (obstacle_height / 2)
    # if center_line_y - tolerance <= dot_pos[1] <= center_line_y + tolerance:
    if last_spoken_color == 'bottom_right_corner':
        if center_line_y > dot_pos[1] and not PERSON_AT_THE_MIDDLE:
            print("----In Function is_person_at_middle_line() , person taking left turn---- ")
            PERSON_AT_THE_MIDDLE = True
            threading.Thread(target=speak, args=(Speech.BYPASS_RIGHT,)).start()

    elif last_spoken_color == 'upper_right_corner':
        if center_line_y < dot_pos[1] and not PERSON_AT_THE_MIDDLE:
            print("----In Function is_person_at_middle_line() , person taking left right---- ")
            PERSON_AT_THE_MIDDLE = True
            threading.Thread(target=speak, args=(Speech.BYPASS_LEFT,)).start()

    return PERSON_AT_THE_MIDDLE
