import sys
import numpy as np
import matplotlib.pyplot as plt


class Jarvis(object):
    def __init__(self, number_of_points=10, speed=0.5, range_min=-300, range_max=300):
        self.number_of_points = int(number_of_points)
        self.speed = float(speed)
        self.range_min = range_min
        self.range_max = range_max

    def RightTurn(self, p1, p2, p3):
        if (p3[1] - p1[1]) * (p2[0] - p1[0]) >= (p2[1] - p1[1]) * (p3[0] - p1[0]):
            return True
        return False

    def start(self):
        plt.close('all')
        # By default we build a random set of N points with coordinates in [-300,300)x[-300,300):
        list_points = np.array([(np.random.randint(0, 300), np.random.randint(0, 300)) for i in range(self.number_of_points)])
        plt.figure()  # Define figure
        index = 0
        n = len(list_points)
        none_list = [None] * n
        l = np.where(list_points[:, 0] == np.min(list_points[:, 0]))
        pointOnHull = list_points[l[0][0]]
        i = 0
        while True:
            none_list[i] = pointOnHull
            endpoint = list_points[0]
            for j in range(1, n):
                if (endpoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not self.RightTurn(list_points[j], none_list[i], endpoint):
                    endpoint = list_points[j]
            i = i + 1
            pointOnHull = endpoint
            J = np.array([none_list[k] for k in range(n) if none_list[k] is not None])
            plt.clf()  # Clear plot
            plt.plot(J[:, 0], J[:, 1], 'b-', picker=5)  # Plot lines
            plt.plot(list_points[:, 0], list_points[:, 1], ".r")  # Plot points
            plt.axis('off')  # No axis
            plt.show(block=False)  # Close plot
            plt.pause(self.speed)  # Mini-pause before closing plot
            index += 1
            if endpoint[0] == none_list[0][0] and endpoint[1] == none_list[0][1]:
                break
        for i in range(n):
            if none_list[-1] is None:
                del none_list[-1]
        P = np.array(none_list)

        # Plot final hull
        plt.clf()
        plt.plot(P[:, 0], P[:, 1], 'b-', picker=5)
        plt.plot([P[-1, 0], P[0, 0]], [P[-1, 1], P[0, 1]], 'b-', picker=5)
        plt.plot(list_points[:, 0], list_points[:, 1], ".r")
        plt.axis('off')
        plt.show(block=False)
        plt.pause(self.speed)
        return P

