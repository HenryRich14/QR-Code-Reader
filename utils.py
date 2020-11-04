from typing import *
import tkinter as tk
from tkinter import filedialog
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
