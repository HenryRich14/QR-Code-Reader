from typing import *
import tkinter as tk
from tkinter import filedialog, messagebox
from pyzbar import pyzbar
import cv2
import csv
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import threading
from shutil import copyfile
import os


def pad_left_zeros(num, pad_num=3):
    output = str(num)
    while len(output) < pad_num:
        output = "0" + output
    return output


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    title_bar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + title_bar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class ErrorHandler(object):
    def __init__(self, error_file: str):
        self.errors: List[Error] = []
        self.error_file = error_file

    def add(self, error):
        self.errors.append(error)

    def quit(self):
        error_num = len(self.errors)
        if error_num == 0:
            return
        elif error_num == 1:
            error = self.errors[0]
            messagebox.showerror("Error", 'File "{}", line {}\n'.format(error.file_name, error.line) + error.message)
        else:
            with open(self.error_file, "a") as fs:
                print(str(datetime.now()), ":\n", file=fs)
                for error in self.errors:
                    print('File "{}", line {}'.format(error.file_name, error.line), file=fs)
                    print(error.message, file=fs)
                    print(file=fs)
                print(file=fs)
            messagebox.showerror("Error", "{} unexpected errors were encountered\n".format(error_num) +
                                          "while the program was running. Check\n"
                                          '"{}"\n'.format(self.error_file) + "for more details.")
        quit(1)


class Error(object):
    def __init__(self, error_handler, file_name: str, line: Union[int, str], message: str, quit_now: bool = True):
        error_handler.add(self)
        self.file_name = file_name
        self.line = str(line)
        self.message = message
        if quit_now:
            error_handler.quit()
