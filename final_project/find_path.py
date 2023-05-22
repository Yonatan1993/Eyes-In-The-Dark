import numpy as np
import matplotlib

matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import math
from datetime import datetime
import cv2

class Node:
    def __init__(self, x, y, walkable, world):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.world = world

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def is_obstacle(self):
        return self.world[self.x, self.y] == 1


def plot_path(path, start, end):
    world = np.zeros((900, 1600))
    plt.imshow(world, cmap="gray")
    plt.plot(start[1], start[0], "ro")
    plt.plot(end[1], end[0], "bo")
    # for obstacle in obstacles:
    #     plt.plot(obstacle[1], obstacle[0], "ko")
    if path is not None:
        path_array = np.array(path)
        plt.plot(path_array[:, 1], path_array[:, 0], "g")
    plt.show()


def plot_maze(maze, start, end):
    plt.imshow(maze, cmap="gray")
    plt.plot(start[1], start[0], "ro")
    plt.plot(end[1], end[0], "bo")
    plt.show(block=True)


# Define the A* algorithm implementation here
def a_star(start, end, world, step=1):
    # Initialize start and end nodes
    start_node = Node(start[0], start[1], True, world)
    end_node = Node(end[0], end[1], True, world)

    # Create a 2D grid of nodes
    grid = []
    for x in range(world.shape[0]):
        row = []
        for y in range(world.shape[1]):
            node = Node(x, y, not world[x, y], world)
            row.append(node)
        grid.append(row)

    # Create open and closed lists
    open_list = []
    closed_list = []

    # Add the start node to the open list
    open_list.append(start_node)

    # While the open list is not empty
    while len(open_list) > 0:

        # Get the node with the lowest f cost from the open list
        current_node = open_list[0]
        for node in open_list:
            if node.f < current_node.f:
                current_node = node

        # Remove the current node from the open list and add it to the closed list
        open_list.remove(current_node)
        closed_list.append(current_node)

        # If the current node is the end node, return the path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append((current.x, current.y))
                current = current.parent

            return path[::-1]

        # Generate neighbors of the current node
        # neighbors = [(0, 5), (0, -5), (5, 0), (-5, 0), (5, 5), (5, -5), (-5, 5), (-5, -5)]
        # step = 1
        neighbors = [(0, step), (0, -step), (step, 0), (-step, 0), (step, step), (step, -step), (-step, step), (-step, -step)]
        for x, y in neighbors:
            neighbor_x = current_node.x + x
            neighbor_y = current_node.y + y
            # This if checks whether the potential neighbor is outside the bounds of the grid.
            if neighbor_x < 0 or neighbor_x >= len(grid) or neighbor_y < 0 or neighbor_y >= len(grid[0]):
                continue
            neighbor = grid[neighbor_x][neighbor_y]
            if neighbor.is_obstacle() or neighbor in closed_list:
                continue
            if x != 0 and y != 0:
                # diagonal movement
                g = current_node.g + math.sqrt(2)
            else:
                # horizontal or vertical movement
                g = current_node.g + 1

            # calculate the h value using Manhattan distance
            h = abs(current_node.x - end_node.x) + abs(
                current_node.y - end_node.y)

            # calculate the f value
            f = g + h
            # check if the neighbor has not been visited before or if it has a better path
            if neighbor in open_list and f >= neighbor.f:
                continue
            if neighbor in closed_list and f >= neighbor.f:
                continue

            # otherwise, update the neighbor's values and add it to the open list
            neighbor.g = g
            neighbor.h = h
            neighbor.f = f
            neighbor.parent = current_node

            if neighbor not in open_list:
                open_list.append(neighbor)

    # if no path is found
    return None


def build_path(start, end, height, width, obstacles_list):
    maze = np.zeros((height, width), dtype=int) # 900x1600
    for upper_left, bottom_right in obstacles_list:
        maze[int(upper_left[1]):int(bottom_right[1]), int(upper_left[0]):int(bottom_right[0])] = 1
    cv2.imshow("maze", (maze*255).astype("uint8"))
    cv2.waitKey(0)
    route = a_star(start, end, maze)
    plt.imshow(maze, cmap="gray")
    plt.plot(start[1], start[0], "ro")
    plt.plot(end[1], end[0], "bo")
    if route is not None:
        route_array = np.array(route)
        plt.plot(route_array[:, 1], route_array[:, 0], "g")
    plt.show(block=True)
    return route

if __name__ == "__main__":
    # Define the start and end points
    start = (450, 50)
    end = (450, 1550)
    obstacle_lis = [((660, 354), (962, 622))]
    path = build_path(start, end, 900, 1600, obstacle_lis)




