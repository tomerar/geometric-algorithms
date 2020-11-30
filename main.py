import tkinter as tk
import tkinter.font as tkFont
import traceback

from ExcelRead import ExcelRead
from Graham import Graham
from Jarvis import Jarvis
import time

import numpy as np
import matplotlib.pyplot as plt


class JarvisP(object):
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
        start_time = time.time()
        # By default we build a random set of N points with coordinates in [-300,300)x[-300,300):
        list_points = np.array(
            [(np.random.randint(0, 300), np.random.randint(0, 300)) for i in range(self.number_of_points)])
        # list_points.sort()  # Sort the set of points
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
                if (endpoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not self.RightTurn(
                        list_points[j], none_list[i], endpoint):
                    endpoint = list_points[j]
            i = i + 1
            pointOnHull = endpoint
            J = np.array([none_list[k] for k in range(n) if none_list[k] is not None])
            index += 1
            if endpoint[0] == none_list[0][0] and endpoint[1] == none_list[0][1]:
                break
        for i in range(n):
            if none_list[-1] is None:
                del none_list[-1]
        P = np.array(none_list)

        # Plot final hull
        end_time = time.time()
        return end_time - start_time


class GrahamP(object):
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
        start_time = time.time()
        # By default we build a random set of N points with coordinates in [-300,300)x[-300,300):
        list_points = [(np.random.randint(self.range_min, 300), np.random.randint(self.range_min, self.range_max))
                       for i in range(self.number_of_points)]
        # list_points.sort()  # Sort the set of points
        list_points = np.array(list_points)  # Convert the list to numpy array
        L_upper = [list_points[0], list_points[1]]  # Initialize the upper part
        # Compute the upper part of the hull
        for i in range(2, len(list_points)):
            L_upper.append(list_points[i])
            while len(L_upper) > 2 and not self.RightTurn(L_upper[-1], L_upper[-2], L_upper[-3]):
                del L_upper[-2]
            new_point_list = np.array(L_upper)

        L_lower = [list_points[-1], list_points[-2]]  # Initialize the lower part
        # Compute the lower part of the hull
        for i in range(len(list_points) - 3, -1, -1):
            L_lower.append(list_points[i])
            while len(L_lower) > 2 and not self.RightTurn(L_lower[-1], L_lower[-2], L_lower[-3]):
                del L_lower[-2]
            new_point_list = np.array(L_upper + L_lower)
        del L_lower[0]
        del L_lower[-1]
        L = L_upper + L_lower  # Build the full hull
        end_time = time.time()
        return end_time - start_time


class PlotStat(object):
    def __init__(self, start_range=1, end_range=5):
        self.start_range = start_range
        self.end_range = end_range
        self.list_range = [2 ** x for x in list(range(self.start_range, self.end_range))]
        # self.list_range = [x for x in list(range(self.start_range, self.end_range, 50)]
        print(self.list_range)

    def create_jarvis_list(self):
        list_jarvis = []
        list_range = self.list_range
        for range_X in list_range:
            number_of_points = int(range_X)
            speed = float(0.00000001)
            jarvis = JarvisP(number_of_points=number_of_points, speed=speed)
            time_long = jarvis.start()
            list_jarvis.append(time_long)
        return list_jarvis

    def create_graham_list(self):
        list_graham = []
        list_range = self.list_range
        for range_X in list_range:
            number_of_points = int(range_X)
            speed = float(0.00000001)
            graham = GrahamP(number_of_points=number_of_points, speed=speed)
            time_long = graham.start()
            list_graham.append(time_long)
        return list_graham

    def start(self):
        plt.close('all')
        # line 1 points
        plt.figure("Graham vs Jarvis")
        list_range = self.list_range
        x1 = self.create_graham_list()
        y1 = list_range
        print(f"x1 {x1}")
        print(f"y1 {y1}")
        print()
        # plotting the line 1 points
        plt.plot(x1, y1, label="graham")
        # line 2 points
        x2 = self.create_jarvis_list()
        y2 = list_range
        print(f"x2 {x2}")
        print(f"y2 {y2}")
        # plotting the line 2 points
        plt.plot(x2, y2, label="jarvis")

        # naming the x axis
        plt.xlabel('time sec')
        # naming the y axis
        plt.ylabel('points')
        # giving a title to my graph
        plt.title('graham vs jarvis ')

        # show a legend on the plot
        plt.legend()

        # function to show the plot
        plt.show()


def timing(f):
    def wrap(*args):
        start = time.time()
        ret = f(*args)
        end = time.time()
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
        tk.messagebox.showinfo(title="info", message="{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
        return ret

    return wrap


range_min = -300
range_max = 300


def main():
    def get_point_from_excel():
        path = number_of_points = e4.get()
        exc = ExcelRead(path)
        return exc.get_list_point()

    @timing
    def get_Graham():

        try:
            number_of_points = int(e1.get())
            speed = float(e2.get())
            if e4.get() == '':
                list_points = [(np.random.randint(range_min, range_max), np.random.randint(range_min, range_max))
                               for i in range(number_of_points)]
            else:
                list_points = get_point_from_excel()
            print(list_points)
            graham = Graham(list_points=list_points, speed=speed)
            graham.start()
        except Exception as e:
            tk.messagebox.showwarning(title="warning ", message=str(e))

    @timing
    def get_jarvis():
        try:
            number_of_points = int(e1.get())
            speed = float(e2.get())
            if e4.get() == '':
                list_points = np.array([(np.random.randint(range_min, range_max),
                                         np.random.randint(range_min, range_max))
                                        for i in range(number_of_points)])
            else:
                list_points = np.array(get_point_from_excel())

            print(list_points)
            jarvis = Jarvis(list_points=list_points, speed=speed)
            jarvis.start()
        except Exception as e:
            traceback.print_exc()
            tk.messagebox.showwarning(title="warning ", message=str(e))

    def get_jar_vs_gra():
        try:
            p = PlotStat(start_range=1, end_range=int(e3.get()) + 1)
            p.start()
        except Exception as e:
            traceback.print_exc()

    master = tk.Tk(className="geometric-algorithms")
    # Gets the requested values of the height and widht.
    windowWidth = master.winfo_reqwidth()
    windowHeight = master.winfo_reqheight()
    print("Width", windowWidth, "Height", windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(master.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    master.geometry("+{}+{}".format(positionRight, positionDown))
    # master.geometry("300x200")
    fontStyle = tkFont.Font(family="Lucida Grande", size=16)
    num_labal = tk.Label(
        master,
        text="number of points",
        font=fontStyle
    ).grid(row=0)
    speed_labal = tk.Label(
        master,
        text="delay iterations (sec)",
        font=fontStyle
    ).grid(row=1)
    speed_labal = tk.Label(
        master,
        text="convex Hull:",
        font=fontStyle
    ).grid(row=3)

    speed_labal = tk.Label(
        master,
        text="Graham vs Jarvis (points 2^X)",
        font=fontStyle
    ).grid(row=4, column=0)

    speed_labal = tk.Label(
        master,
        text="load excel points path",
        font=fontStyle
    ).grid(row=5, column=0)

    e1 = tk.Entry(master, font=fontStyle)
    e1.insert(tk.END, '10')
    e2 = tk.Entry(master, font=fontStyle)
    e2.insert(tk.END, '0.2')
    e3 = tk.Entry(master, font=fontStyle)
    e3.insert(tk.END, '10')
    e4 = tk.Entry(master, font=fontStyle)
    e4.insert(tk.END, '')

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=4, column=1)
    e4.grid(row=5, column=1)
    tk.Button(
        master,
        text='Graham',
        command=get_Graham,
        font=fontStyle
    ).grid(row=3,
           column=1,
           sticky=tk.W,
           pady=4)
    tk.Button(
        master,
        text='jarvis', command=get_jarvis,
        font=fontStyle
    ).grid(row=3,
           column=2,
           sticky=tk.W,
           pady=4)

    tk.Button(
        master,
        text='start plot', command=get_jar_vs_gra,
        font=fontStyle
    ).grid(row=4,
           column=2,
           sticky=tk.W,
           pady=4)

    tk.mainloop()


if __name__ == '__main__':
    main()
