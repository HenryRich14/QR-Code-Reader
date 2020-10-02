import tkinter as tk
from PIL import Image, ImageTk
import threading
import imutils
from imutils.video import VideoStream
import cv2


class QRReaderApp(object):
    def __init__(self, vs):
        self.vs = vs
        self.outputPath = "QR Codes\\current_frame.png"
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tk.Tk()
        self.panel = None

        #btn = tk.Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        #btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("test video")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()


vs = VideoStream().start()
pba = QRReaderApp(vs)
pba.root.mainloop()