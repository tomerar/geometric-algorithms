import time
import tkinter as tk
import tkinter.font as tkFont
import traceback

import numpy as np
import matplotlib.pyplot as plt

from Graham import Graham
from GrahamScan_StepPlot import GrahamScan
from Jarvis import Jarvis
from JarvisMarch_StepPlot import GiftWrapping


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


def main():

    @timing
    def get_Graham():

        try:
            number_of_points = int(e1.get())
            speed = float(e2.get())
            graham = Graham(number_of_points=number_of_points, speed=speed)
            graham.start()
        except Exception as e:
            tk.messagebox.showwarning(title="warning ", message=str(e))

    @timing
    def get_jarvis():
        try:
            number_of_points = int(e1.get())
            speed = float(e2.get())
            jarvis = Jarvis(number_of_points=number_of_points, speed=speed)
            jarvis.start()
        except Exception as e:
            traceback.print_exc()
            tk.messagebox.showwarning(title="warning ", message=str(e))

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

    e1 = tk.Entry(master, font=fontStyle)
    e1.insert(tk.END, '10')
    e2 = tk.Entry(master, font=fontStyle)
    e2.insert(tk.END, '0.2')

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    # number_of_points = e1.get()
    # P = [(np.random.randint(-300, 300), np.random.randint(-300, 300)) for i in range(N)]
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

    tk.mainloop()


if __name__ == '__main__':
    main()
