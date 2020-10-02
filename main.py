import tkinter as tk
from pyzbar import pyzbar
import cv2
import csv
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import threading
from shutil import copyfile
from Popup_Windows import *


def pad_left_zeros(num, pad_num=3):
    output = str(num)
    while len(output) < pad_num:
        output = "0" + output
    return output


class Application(object):
    def __init__(self):
        # Setup root
        self.root = tk.Tk()
        self.root.state("zoomed")
        self.root.bind("<F11>",
                       lambda event: self.root.attributes("-fullscreen",
                                                          not self.root.attributes("-fullscreen")))
        self.root.wm_title("QR Code Reader")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.close)

        # Widgets
        # Frames
        self.frm_window = None
        self.frm_received_inputs = None
        self.frm_expected_inputs = None
        self.frm_match_num = None
        self.frm_scouter_widgets = None
        self.frm_scouter_names = None
        self.frm_scouter_btns = None
        # Labels
        self.lbl_camera_img = None
        self.lbl_previous_inputs = None
        self.lbl_match_number_id = None
        self.lbl_scouter_preset_id = None
        self.lbl_scouter_separator = None
        self.lbl_scouter_1_id = None
        self.lbl_scouter_2_id = None
        self.lbl_scouter_3_id = None
        self.lbl_scouter_4_id = None
        self.lbl_scouter_5_id = None
        self.lbl_scouter_6_id = None
        self.lbl_scouter_btns_separator = None
        # Buttons
        self.btn_settings = None
        self.btn_decrement_match_num = None
        self.btn_increment_match_num = None
        self.btn_get_preset = None
        self.btn_save_preset = None
        self.btn_setup_next_match = None
        # Entry Boxes
        self.ent_match_num = None
        self.ent_scouter_preset = None
        self.ent_scouter_1 = None
        self.ent_scouter_2 = None
        self.ent_scouter_3 = None
        self.ent_scouter_4 = None
        self.ent_scouter_5 = None
        self.ent_scouter_6 = None
        # Build Widgets
        self.build_widgets()

        # Other variables
        self.cam = cv2.VideoCapture(0)
        self.current_frame_file = "Outputs/current_frame.png"
        self.setup_list = "Outputs\\setup_list.csv"
        self.event_list = "Outputs\\event_list.csv"
        self.qr_strings_file = "Resources/qr_strings.txt"
        self.settings_file = "Resources/settings.txt"
        self.settings = {}
        self.previous_inputs = {}
        self.presets = {}
        self.popup_window = None
        self.scout_entries = [self.ent_scouter_1, self.ent_scouter_2, self.ent_scouter_3,
                              self.ent_scouter_4, self.ent_scouter_5, self.ent_scouter_6]
        self.received_teams = []
        self.pull_previous_data()
        self.pull_settings()

        # Setup video thread
        self.thread = threading.Thread(target=self.video_loop, args=(), daemon=True)
        self.thread.start()

        # Start the mainloop()
        self.root.mainloop()

    def build_widgets(self):
        # Frames
        self.frm_window = tk.Frame(master=self.root)
        self.frm_received_inputs = tk.Frame(master=self.frm_window)
        self.frm_expected_inputs = tk.Frame(master=self.frm_window, padx=20)
        self.frm_match_num = tk.Frame(master=self.frm_expected_inputs, pady=40)
        self.frm_scouter_names = tk.Frame(master=self.frm_expected_inputs)
        self.frm_scouter_btns = tk.Frame(master=self.frm_expected_inputs)

        # Labels
        self.lbl_camera_img = tk.Label(master=self.frm_received_inputs, text="Camera is warming up...",
                                       font=("Helvetica", 40))
        self.lbl_previous_inputs = tk.Label(master=self.frm_received_inputs, font=("Helvetica", 18))
        self.lbl_match_number_id = tk.Label(master=self.frm_match_num, text="Match Number:",
                                            font=("Helvetica", 26))
        self.lbl_scouter_preset_id = tk.Label(master=self.frm_scouter_names, text="Preset Name:",
                                              font=("Helvetica", 26))
        self.lbl_scouter_separator = tk.Label(master=self.frm_scouter_names, text=" ", font=("Helvetica", 18))
        self.lbl_scouter_1_id = tk.Label(master=self.frm_scouter_names, text="Scouter 1:", font=("Helvetica", 26))
        self.lbl_scouter_2_id = tk.Label(master=self.frm_scouter_names, text="Scouter 2:", font=("Helvetica", 26))
        self.lbl_scouter_3_id = tk.Label(master=self.frm_scouter_names, text="Scouter 3:", font=("Helvetica", 26))
        self.lbl_scouter_4_id = tk.Label(master=self.frm_scouter_names, text="Scouter 4:", font=("Helvetica", 26))
        self.lbl_scouter_5_id = tk.Label(master=self.frm_scouter_names, text="Scouter 5:", font=("Helvetica", 26))
        self.lbl_scouter_6_id = tk.Label(master=self.frm_scouter_names, text="Scouter 6:", font=("Helvetica", 26))
        self.lbl_scouter_btns_separator = tk.Label(master=self.frm_expected_inputs, text=" ", font=("Helvetica", 18))

        # Buttons
        image = Image.open("Resources/settings_gear.png")
        image = image.resize((50, 50), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.btn_settings = tk.Button(master=self.frm_expected_inputs, image=self.photo,
                                      command=self.btn_settings_click)
        self.btn_decrement_match_num = tk.Button(master=self.frm_match_num, text="-", font=("Helvetica", 18),
                                                 command=self.btn_decrement_click)
        self.btn_increment_match_num = tk.Button(master=self.frm_match_num, text="+", font=("Helvetica", 18),
                                                 command=self.btn_increment_click)
        self.btn_get_preset = tk.Button(master=self.frm_scouter_btns, text="Open Presets", font=("Helvetica", 20),
                                        command=self.btn_get_preset_click)
        self.btn_save_preset = tk.Button(master=self.frm_scouter_btns, text="Save As Preset", font=("Helvetica", 20),
                                         command=self.btn_save_preset_click)
        self.btn_setup_next_match = tk.Button(master=self.frm_expected_inputs, text="Setup Next Match",
                                              font=("Helvetica", 20), command=self.setup_next_match)

        # Entry Boxes
        self.ent_match_num = tk.Entry(master=self.frm_match_num, width=3, font=("Helvetica", 26))
        self.ent_match_num.insert(0, pad_left_zeros(0))
        self.ent_scouter_preset = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))
        self.ent_scouter_1 = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))
        self.ent_scouter_2 = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))
        self.ent_scouter_3 = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))
        self.ent_scouter_4 = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))
        self.ent_scouter_5 = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))
        self.ent_scouter_6 = tk.Entry(master=self.frm_scouter_names, font=("Helvetica", 26))

        # Add widgets to window
        self.frm_window.grid(row=0, column=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frm_received_inputs.grid(row=0, column=0)
        self.lbl_camera_img.grid(row=0, column=0)
        self.lbl_previous_inputs.grid(row=1, column=0)

        self.frm_expected_inputs.grid(row=0, column=1)

        self.frm_match_num.grid(row=0, column=0, sticky="e")
        self.lbl_match_number_id.grid(row=0, column=0)
        self.ent_match_num.grid(row=0, column=2)
        self.btn_decrement_match_num.grid(row=0, column=4)
        self.btn_increment_match_num.grid(row=0, column=5)

        self.btn_settings.grid(row=0, column=1, sticky="e")

        self.frm_scouter_names.grid(row=1, column=0, columnspan=2)
        self.lbl_scouter_preset_id.grid(row=0, column=0)
        self.lbl_scouter_separator.grid(row=1, column=0)
        self.lbl_scouter_1_id.grid(row=2, column=0)
        self.lbl_scouter_2_id.grid(row=3, column=0)
        self.lbl_scouter_3_id.grid(row=4, column=0)
        self.lbl_scouter_4_id.grid(row=5, column=0)
        self.lbl_scouter_5_id.grid(row=6, column=0)
        self.lbl_scouter_6_id.grid(row=7, column=0)

        self.ent_scouter_preset.grid(row=0, column=1)
        self.ent_scouter_1.grid(row=2, column=1)
        self.ent_scouter_2.grid(row=3, column=1)
        self.ent_scouter_3.grid(row=4, column=1)
        self.ent_scouter_4.grid(row=5, column=1)
        self.ent_scouter_5.grid(row=6, column=1)
        self.ent_scouter_6.grid(row=7, column=1)

        self.lbl_scouter_btns_separator.grid(row=2, column=0)

        self.frm_scouter_btns.grid(row=3, column=0, columnspan=2)
        self.btn_get_preset.grid(row=0, column=0)
        self.btn_save_preset.grid(row=0, column=1)
        self.btn_setup_next_match.grid(row=4, column=0, columnspan=2)

    def pull_settings(self):
        with open(self.settings_file, "r") as fs:
            self.settings = eval(fs.read().strip())

    def put_settings(self):
        with open(self.settings_file, "w") as fs:
            fs.write(str(self.settings))

    def pull_previous_data(self):
        with open(self.qr_strings_file, "r") as fs:
            for line in fs.readlines():
                t = line[:-1].split(",")[-1]
                self.previous_inputs[t] = line[:line.index(t)]
        self.update_previous_inputs()

        with open("Resources\\presets.txt", "r") as fs:
            self.presets = eval(fs.read())

    def put_data(self):
        with open("Resources\\presets.txt", "w") as fs:
            fs.write(str(self.presets))

    def update_previous_inputs(self):
        lbl_text = ""
        count = 5
        for qr_data in list(self.previous_inputs.values())[-5:]:
            name, team, match = qr_data.split(",")[:3]
            lbl_text += name + " : " + team + " : " + match + "\n"
            if count > 1:
                count -= 1
            else:
                break
        else:
            while count > 0:
                lbl_text = "\n" + lbl_text
                count -= 1
        lbl_text = lbl_text[:-1]
        self.lbl_previous_inputs.config(text=lbl_text)

    def check_scouter_name(self, name):
        for ent in self.scout_entries:
            if ent.cget("bg") == "green" or ent.get() == "":
                continue
            full_name = name.split(" ")
            full_expected = ent.get().split(" ")
            full_name_len = len(full_name)
            full_expected_len = len(full_expected)
            if full_name_len == 0 or full_expected_len == 0:
                continue
            if full_expected[0] in full_name[0] or full_name[0] in full_expected[0]:
                if full_name_len > 1 and full_expected_len > 1:
                    if full_name[-1][0] == full_expected[-1][0]:
                        return ent
                    return None
                return ent
        return None

    # Button Click Methods

    def btn_settings_click(self):
        SettingsWindow(self)

    def btn_decrement_click(self):
        match_str = self.ent_match_num.get()
        if match_str.isnumeric():
            match_num = int(match_str)
            if match_num > 0:
                self.ent_match_num.delete(0, tk.END)
                self.ent_match_num.insert(0, pad_left_zeros(match_num - 1))
            return
        self.ent_match_num.delete(0, tk.END)
        self.ent_match_num.insert(0, pad_left_zeros(0))

    def btn_increment_click(self):
        match_str = self.ent_match_num.get()
        if match_str.isnumeric():
            match_num = int(match_str)
            self.ent_match_num.delete(0, tk.END)
            self.ent_match_num.insert(0, pad_left_zeros(match_num + 1))
            return
        self.ent_match_num.delete(0, tk.END)
        self.ent_match_num.insert(0, pad_left_zeros(0))

    def btn_get_preset_click(self):
        if self.popup_window is None:
            PresetPopup(self).run()

    def btn_save_preset_click(self):
        if self.popup_window is None:
            self.popup_window = PresetPopup(self)

            # Clear entry boxes
            self.popup_window.ent_preset_name.delete(0, tk.END)
            self.popup_window.ent_scouter_1.delete(0, tk.END)
            self.popup_window.ent_scouter_2.delete(0, tk.END)
            self.popup_window.ent_scouter_3.delete(0, tk.END)
            self.popup_window.ent_scouter_4.delete(0, tk.END)
            self.popup_window.ent_scouter_5.delete(0, tk.END)
            self.popup_window.ent_scouter_6.delete(0, tk.END)

            # Fill entry boxes
            self.popup_window.ent_preset_name.insert(0, self.ent_scouter_preset.get())
            self.popup_window.ent_scouter_1.insert(0, self.ent_scouter_1.get())
            self.popup_window.ent_scouter_2.insert(0, self.ent_scouter_2.get())
            self.popup_window.ent_scouter_3.insert(0, self.ent_scouter_3.get())
            self.popup_window.ent_scouter_4.insert(0, self.ent_scouter_4.get())
            self.popup_window.ent_scouter_5.insert(0, self.ent_scouter_5.get())
            self.popup_window.ent_scouter_6.insert(0, self.ent_scouter_6.get())

            self.popup_window.run()

    def setup_next_match(self, force=False):
        if self.popup_window is None:
            if not force:
                missing_scouters = []
                for ent in self.scout_entries:
                    if ent.cget("bg") != "green" and len(ent.get()) > 0:
                        missing_scouters.append(ent.get())

                if len(missing_scouters) > 0:
                    UnreceivedScouterPopup(self)
                    return

            for ent in self.scout_entries:
                ent.config(bg="SystemWindow")

            self.btn_increment_click()
            self.received_teams.clear()

    def video_loop(self):
        while True:
            ret_val, img = self.cam.read()
            # get first qr code on screen if any, and convert to string
            codes_on_screen = pyzbar.decode(img)
            cv2.imwrite(self.current_frame_file, img)
            image = Image.open(self.current_frame_file)
            if len(codes_on_screen) > 0 and len(codes_on_screen[0].data.decode("utf-8")) > 0:
                qr = codes_on_screen[0].data.decode("utf-8")
                x, y, w, h = codes_on_screen[0].rect
                new_img = ImageDraw.Draw(image)
                if qr not in self.previous_inputs.values():
                    new_img.rectangle((x, y, x+w, y+h), outline="red", width=4)
                    self.parse_qr_code(qr)
                elif qr != list(self.previous_inputs.values())[-1]:
                    new_img.rectangle((x, y, x + w, y + h), outline="blue", width=4)
                else:
                    new_img.rectangle((x, y, x + w, y + h), outline="green", width=4)
            image = ImageTk.PhotoImage(image)
            if self.lbl_camera_img is not None:
                self.lbl_camera_img.config(image=image)
                self.lbl_camera_img.image = image

    def parse_qr_code(self, qr):
        qr_data = qr.strip().split(",")
        if len(qr_data) < 2 or qr_data[-2] != "InfiniteRechargeScouting":
            return
        try:
            if qr == '':
                return
            scouter, team, match = qr_data[:3]
        except ValueError:
            print(len(qr))
            print(qr)
            print(qr_data)
            raise ValueError("not enough values to unpack (expected 3, got {})".format(len(qr_data)))
        ent = self.check_scouter_name(scouter)
        if ent is not None:
            ent.config(bg="green")
        else:
            self.popup_window = NameNotFoundPopup(self, scouter)
            scouter = self.popup_window.run()
            ent = self.check_scouter_name(scouter)
            if ent is not None:
                ent.config(bg="green")
        if self.ent_match_num.get().isnumeric() and int(match) != int(self.ent_match_num.get()):
            print(match)
            print(self.ent_match_num.get())
            self.popup_window = WrongMatchNumberPopup(self, match)
            match = self.popup_window.run()
        for s, t in self.received_teams:
            if team == t:
                self.popup_window = RepeatedTeamNumberPopup(self, s, team)
                team = self.popup_window.run()
        qr_data[0] = scouter
        qr_data[1] = team
        qr_data[2] = match
        qr = ""
        for data in qr_data:
            qr += data + ","
        dst_file = "QR Codes\\" + team + "_" + match + ".png"
        copyfile(self.current_frame_file, dst_file)
        time_stamp = str(datetime.now())

        def chunks(data, n=self.settings["num_vals"]):
            return [data[i:i + n] for i in range(0, len(data), n)]

        with open(self.qr_strings_file, "a") as fs:
            fs.write(qr + time_stamp + "\n")

        with open(self.setup_list, "a") as csv_file:
            csv_write = csv.writer(csv_file, dialect="excel", delimiter=",")
            csv_write.writerow(qr_data[:self.settings["num_setup"]])

        with open(self.event_list, "a") as csv_file:
            csv_write = csv.writer(csv_file, dialect="excel", delimiter=",")
            setup_arr = [team, match, "Game Phase"]
            del qr_data[:self.settings["num_setup"]]
            for chunk in chunks(qr_data):
                if len(chunk) < self.settings["num_vals"]:
                    if len(chunk) != 2:  # Expected number of extraneous items
                        print(chunk)
                        print("len:", len(chunk))
                    break
                setup_arr[2] = chunk[0]
                csv_write.writerow(setup_arr + ["S", "I", chunk[1], scouter])
                csv_write.writerow(setup_arr + ["S", "O", chunk[2], scouter])
                csv_write.writerow(setup_arr + ["S", "L", chunk[3], scouter])
                csv_write.writerow(setup_arr + ["M", "H", chunk[4], scouter])
                csv_write.writerow(setup_arr + ["M", "L", chunk[5], scouter])
                csv_write.writerow(setup_arr + ["D", "", chunk[6], scouter])
        self.previous_inputs[time_stamp] = qr
        self.received_teams.append([scouter, team])
        self.update_previous_inputs()

    def close(self):
        if self.popup_window is not None:
            self.popup_window.close()
        self.put_settings()
        self.put_data()
        self.root.destroy()


if __name__ == "__main__":
    app = Application()
