from enum import Enum


class Speech(Enum):
    WELCOME = 1
    NO_OBSTACLES = 2
    OBSTACLE_DETECT = 3
    START_BYPASS_LEFT = 4
    START_BYPASS_RIGHT = 5
    COLLISION_WARNING = 6
    COLLISION_WARNING_RIGHT = 7
    COLLISION_WARNING_LEFT = 8
    WARNING_IN_FRONT_LEFT = 9
    WARNING_IN_FRONT_RIGHT = 10
    WARNING_IN_FRONT_BACK = 11
    BYPASS_RIGHT = 12
    BYPASS_LEFT = 13
