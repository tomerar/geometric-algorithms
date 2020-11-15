import sys
import numpy as np
import matplotlib.pyplot as plt


class Graham(object):
    def __init__(self, number_of_points=10, speed=0.5, range_min=-300, range_max=300):
        self.number_of_points = int(number_of_points)
        self.speed = float(speed)
        self.range_min = range_min
        self.range_max = range_max

    def RightTurn(self, p1, p2, p3):
        if (p3[1] - p1[1]) * (p2[0] - p1[0]) >= (p2[1] - p1[1]) * (p3[0] - p1[0]):
            return False
        return True

    def start(self):
        plt.close('all')
        # By default we build a random set of N points with coordinates in [-300,300)x[-300,300):
        list_points = [(np.random.randint(self.range_min, 300), np.random.randint(self.range_min, self.range_max))
                       for i in range(self.number_of_points)]
        list_points.sort()  # Sort the set of points
        list_points = np.array(list_points)  # Convert the list to numpy array
        plt.figure()  # Create a new fig
        L_upper = [list_points[0], list_points[1]]  # Initialize the upper part
        # Compute the upper part of the hull
        for i in range(2, len(list_points)):
            L_upper.append(list_points[i])
            while len(L_upper) > 2 and not self.RightTurn(L_upper[-1], L_upper[-2], L_upper[-3]):
                del L_upper[-2]
            new_point_list = np.array(L_upper)
            plt.clf()  # Clear plt.fig
            plt.plot(new_point_list[:, 0], new_point_list[:, 1], 'b-', picker=5)  # Plot lines
            plt.plot(list_points[:, 0], list_points[:, 1], ".r")  # Plot points
            plt.axis('off')  # No axis
            plt.show(block=False)  # Close plot
            plt.pause(self.speed)  # Mini-pause before closing plot

        L_lower = [list_points[-1], list_points[-2]]  # Initialize the lower part
        # Compute the lower part of the hull
        for i in range(len(list_points) - 3, -1, -1):
            L_lower.append(list_points[i])
            while len(L_lower) > 2 and not self.RightTurn(L_lower[-1], L_lower[-2], L_lower[-3]):
                del L_lower[-2]
            new_point_list = np.array(L_upper + L_lower)
            plt.clf()  # Clear plt.fig
            plt.plot(new_point_list[:, 0], new_point_list[:, 1], 'b-', picker=5)  # Plot lines
            plt.plot(list_points[:, 0], list_points[:, 1], ".r")  # Plot points
            plt.axis('off')  # No axis
            plt.show(block=False)  # Close plot
            plt.pause(self.speed)  # Mini-pause befor closing plot
        del L_lower[0]
        del L_lower[-1]
        L = L_upper + L_lower  # Build the full hull
        return np.array(L)
