import sys
import importlib
import paho.mqtt.client as mqtt
import time
from tkinter import *

from app import AppFrame
from login import LoginFrame
from tkinter import font as tkfont


class App(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self._frame = None
        self.client_name = None
        self.username = None
        self.password = None
        self.switch_frame("login")

    def setframe(self, frame):
        self._frame = frame

    def switch_frame(self, frame_string, frame=None):
        if frame is not None:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.grid_forget()

        frame_dict = {"login": LoginFrame, "app": AppFrame}
        frame_class = frame_dict.get(frame_string)

        new_frame = frame_class(self) if frame_string == "login" else frame_class(self, )
        if self._frame is not None:
            self._frame.destroy()
            self._frame = new_frame
            self._frame.grid()
        else:
            self._frame = LoginFrame(self)
            self._frame.grid()
        # frame.winfo_toplevel().geometry("300x150")

    def get_center(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)
        return width, height, x_coordinate, y_coordinate


if __name__ == '__main__':
    app = App()
    app.title("Chat app")
    app.mainloop()  # Keeps the window open/running
