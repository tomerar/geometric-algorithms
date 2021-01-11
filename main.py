print("convex hull app is loading...")
print("please wait")
import tkinter as tk
import tkinter.font as tkFont
import traceback
import xlsxwriter
import xlrd
import pathlib
from ExcelRead import ExcelRead
# from Graham import Graham
# from Jarvis import Jarvis
import time

import numpy as np
import matplotlib.pyplot as plt

range_min = -300
range_max = 300

click_flag = True
wait_time = 5
tk_global = None
wait_sum = 0



def wait_by():
    global click_flag
    global wait_time
    global pause_var
    global master
    global wait_sum
    start_time = 0
    end_time = 0

    if not click_flag:
        start_time = time.time()
        master.wait_variable(pause_var)
        end_time = time.time()
        wait_sum += end_time - start_time


class Jarvis(object):
    def __init__(self, speed=0.5, list_points=[]):
        self.speed = float(speed)
        self.list_point = list_points

    def RightTurn(self, p1, p2, p3):
        if (p3[1] - p1[1]) * (p2[0] - p1[0]) >= (p2[1] - p1[1]) * (p3[0] - p1[0]):
            return True
        return False

    def start(self):
        global wait_sum
        wait_sum = 0
        plt.close('all')
        # By default we build a random set of N points with coordinates in [-300,300)x[-300,300):
        list_points = self.list_point
        plt.figure("Jarvis")  # Define figure
        index = 0
        n = len(list_points)
        none_list = [None] * n
        l = np.where(list_points[:, 0] == np.min(list_points[:, 0]))
        pointOnHull = list_points[l[0][0]]
        i = 0
        while True:
            wait_by()
            none_list[i] = pointOnHull
            endpoint = list_points[0]
            for j in range(1, n):
                if (endpoint[0] == pointOnHull[0] and endpoint[1] == pointOnHull[1]) or not self.RightTurn(
                        list_points[j], none_list[i], endpoint):
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


class Graham(object):
    def __init__(self, speed=0.5, list_points=[]):
        self.speed = float(speed)
        self.list_point = list_points

    def RightTurn(self, p1, p2, p3):
        if (p3[1] - p1[1]) * (p2[0] - p1[0]) >= (p2[1] - p1[1]) * (p3[0] - p1[0]):
            return False
        return True

    def start(self):
        global wait_sum
        wait_sum = 0
        plt.close('all')
        # By default we build a random set of N points with coordinates in [-300,300)x[-300,300):
        self.list_point.sort()
        list_points = self.list_point
        list_points.sort()  # Sort the set of points
        list_points = np.array(list_points)  # Convert the list to numpy array
        plt.figure("Graham")  # Create a new fig
        L_upper = [list_points[0], list_points[1]]  # Initialize the upper part
        # Compute the upper part of the hull
        for i in range(2, len(list_points)):
            wait_by()
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
            wait_by()
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


class JarvisP(object):
    def __init__(self, number_of_points, speed=0.5, range_min=-300, range_max=300):
        self.number_of_points_list = number_of_points
        self.speed = float(speed)
        self.range_min = range_min
        self.range_max = range_max

    def RightTurn(self, p1, p2, p3):
        if (p3[1] - p1[1]) * (p2[0] - p1[0]) >= (p2[1] - p1[1]) * (p3[0] - p1[0]):
            return True
        return False

    def start(self):
        start_time = time.time()
        list_points = np.array(self.number_of_points_list)
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
    def __init__(self, number_of_points, speed=0.5, range_min=-300, range_max=300):
        self.number_of_points = number_of_points
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
        # list_points = [(np.random.randint(self.range_min, 300), np.random.randint(self.range_min, self.range_max))
        #                for i in range(self.number_of_points)]
        list_points = self.number_of_points
        list_points.sort()
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
    def __init__(self, start_range=1, end_range=5, min_range=-300, max_range=300):
        self.min_range = min_range
        self.max_range = max_range
        self.start_range = start_range
        self.end_range = end_range
        self.list_range = [2 ** x for x in list(range(self.start_range, self.end_range))]
        self.matrix_list = self.create_all_matrix(self.list_range)

    def create_all_matrix(self, list_range):
        list_t = []
        for num_point in list_range:
            list_t.append(
                [
                    (np.random.randint(self.min_range, self.max_range),
                     np.random.randint(self.min_range, self.max_range))
                    for i in range(num_point)
                ]
            )
        return list_t

    def create_jarvis_list(self):
        list_jarvis = []
        list_range = self.matrix_list
        for range_X in list_range:
            number_of_points = range_X
            speed = float(0.00000001)
            jarvis = JarvisP(number_of_points=number_of_points, speed=speed)
            time_long = jarvis.start()
            list_jarvis.append(time_long)
        return list_jarvis

    def create_graham_list(self):
        list_graham = []
        list_range = self.matrix_list
        for range_X in list_range:
            number_of_points = range_X
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
        # plotting the line 1 points
        plt.plot(x1, y1, label="graham")
        # line 2 points
        x2 = self.create_jarvis_list()
        y2 = list_range
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
        hours, rem = divmod(end - start - wait_sum, 3600)
        minutes, seconds = divmod(rem, 60)
        tk.messagebox.showinfo(title="info", message="{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
        return ret

    return wrap


def get_color():
    global click_flag
    color = "green" if click_flag else "red"
    return color


def main():
    def builder_point():
        class PointBuilder:
            def __init__(self, point, excel_name, e4):
                self.point = point
                self.xs = list(point.get_xdata())
                self.ys = list(point.get_ydata())
                self.xp = []
                self.yp = []
                self.workbook = None  # xlsxwriter.Workbook(self.excel_name)
                self.worksheet = None  # self.workbook.add_worksheet()
                self.index_excel = 0
                self.excel_name = excel_name
                self.clear()
                self.absolute_path = fr"{pathlib.Path(__file__).parent.absolute()}\{self.excel_name}"
                e4.delete(0, 'end')
                e4.insert(tk.END, self.absolute_path)
                self.add_row('x', 'y')
                self.cid = point.figure.canvas.mpl_connect('button_press_event', self)

            def clear(self):
                self.workbook = xlsxwriter.Workbook(self.excel_name)
                self.worksheet = self.workbook.add_worksheet()
                self.worksheet.write(self.index_excel, 0, '')  # Writes a strin
                self.workbook.close()

            def add_row(self, x, y):
                wbRD = xlrd.open_workbook(self.excel_name)
                sheets = wbRD.sheets()

                # open the same file for writing (just don't write yet)
                wb = xlsxwriter.Workbook(self.excel_name)

                # run through the sheets and store sheets in workbook
                # this still doesn't write to the file yet
                for sheet in sheets:  # write data from old file
                    newSheet = wb.add_worksheet(sheet.name)
                    for row in range(sheet.nrows):
                        for col in range(sheet.ncols):
                            newSheet.write(row, col, sheet.cell(row, col).value)

                newSheet.write(self.index_excel, 0, x)  # Writes a string
                newSheet.write(self.index_excel, 1, y)  # Writes a string
                self.index_excel += 1
                wb.close()  # THIS writes

            def __call__(self, event):
                if event.inaxes != self.point.axes:
                    return
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)
                self.xp.append(event.xdata)
                self.yp.append(event.ydata)
                self.add_row(event.xdata, event.ydata)
                self.point.set_data(self.xs, self.ys)
                self.point.figure.canvas.draw()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('click to build points')
        axes = plt.gca()
        axes.set_xlim([-300, 300])
        axes.set_ylim([-300, 300])
        point, = ax.plot([], [], ".r")  # empty line
        PointBuilder = PointBuilder(point=point, excel_name="PointBuilder.xlsx", e4=e4)
        plt.show()

    def stop_start():
        global click_flag
        global pause_var

        click_flag = not click_flag
        if click_flag:
            pause_var.set(pause_var.get() + 1)

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
            graham = Graham(list_points=list_points, speed=speed)
            graham.start()
        except Exception as e:
            traceback.print_exc()
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

    global wait_time
    global master
    global pause_var
    master = tk.Tk(className="geometric-algorithms")
    pause_var = tk.IntVar()
    # Gets the requested values of the height and widht.
    windowWidth = master.winfo_reqwidth()
    windowHeight = master.winfo_reqheight()

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

    global pause_button
    pause_button = tk.Button(
        master,
        text=f'Stop / Start', command=stop_start,
        font=fontStyle,
        bg="grey"
    ).grid(row=3,
           column=3,
           sticky=tk.W,
           pady=4)

    tk.Button(
        master,
        text=f'Point builder', command=builder_point,
        font=fontStyle,
    ).grid(row=1,
           column=3,
           sticky=tk.W,
           pady=4)

    tk.mainloop()


if __name__ == '__main__':
    main()
