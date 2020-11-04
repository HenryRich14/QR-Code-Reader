from Popup_Windows import *
from utils import *


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
        self.photo = None
        self.error_handler = ErrorHandler("Outputs/Error outputs.txt")

        # Widgets
        # Frames
        self.frm_window: Union[tk.Frame, None] = None
        self.frm_received_inputs: Union[tk.Frame, None] = None
        self.frm_expected_inputs: Union[tk.Frame, None] = None
        self.frm_match_num: Union[tk.Frame, None] = None
        self.frm_scouter_widgets: Union[tk.Frame, None] = None
        self.frm_scouter_names: Union[tk.Frame, None] = None
        self.frm_scouter_buttons: Union[tk.Frame, None] = None
        # Labels
        self.lbl_camera_img: Union[tk.Label, None] = None
        self.lbl_previous_inputs: Union[tk.Label, None] = None
        self.lbl_match_number_id: Union[tk.Label, None] = None
        self.lbl_scouter_preset_id: Union[tk.Label, None] = None
        self.lbl_scouter_separator: Union[tk.Label, None] = None
        self.lbl_scouter_1_id: Union[tk.Label, None] = None
        self.lbl_scouter_2_id: Union[tk.Label, None] = None
        self.lbl_scouter_3_id: Union[tk.Label, None] = None
        self.lbl_scouter_4_id: Union[tk.Label, None] = None
        self.lbl_scouter_5_id: Union[tk.Label, None] = None
        self.lbl_scouter_6_id: Union[tk.Label, None] = None
        self.lbl_scouter_btns_separator: Union[tk.Label, None] = None
        # Buttons
        self.btn_settings: Union[tk.Button, None] = None
        self.btn_decrement_match_num: Union[tk.Button, None] = None
        self.btn_increment_match_num: Union[tk.Button, None] = None
        self.btn_get_preset: Union[tk.Button, None] = None
        self.btn_save_preset: Union[tk.Button, None] = None
        self.btn_setup_next_match: Union[tk.Button, None] = None
        # Entry Boxes
        self.ent_match_num: Union[tk.Entry, None] = None
        self.ent_scouter_preset: Union[tk.Entry, None] = None
        self.ent_scouter_1: Union[tk.Entry, None] = None
        self.ent_scouter_2: Union[tk.Entry, None] = None
        self.ent_scouter_3: Union[tk.Entry, None] = None
        self.ent_scouter_4: Union[tk.Entry, None] = None
        self.ent_scouter_5: Union[tk.Entry, None] = None
        self.ent_scouter_6: Union[tk.Entry, None] = None
        # Build Widgets
        self.build_widgets()

        # Other variables
        self.pause_cam = False
        self.cam = cv2.VideoCapture(0)
        self.settings_file = "Resources/settings.txt"
        self.settings = {}
        self.previous_inputs = {}
        self.presets = {}
        self.popup_window: Union[PopupWindow, None] = None
        self.scout_entries: List[Union[tk.Entry, None]] = [self.ent_scouter_1, self.ent_scouter_2, self.ent_scouter_3,
                                                           self.ent_scouter_4, self.ent_scouter_5, self.ent_scouter_6]
        self.received_teams = []
        self.pull_settings()
        self.pull_previous_data()

        # Setup video thread
        self.thread = threading.Thread(target=self.video_loop, args=(), daemon=True)
        self.thread.start()

        # Test
        Error(self.error_handler, "main.py", 78, "Test1", False)
        Error(self.error_handler, "main.py", 79, "Test2", False)
        Error(self.error_handler, "main.py", 80, "Test3", False)

        # Start the mainloop()
        self.root.mainloop()

    def build_widgets(self):
        # Frames
        self.frm_window = tk.Frame(master=self.root)
        self.frm_received_inputs = tk.Frame(master=self.frm_window)
        self.frm_expected_inputs = tk.Frame(master=self.frm_window, padx=20)
        self.frm_match_num = tk.Frame(master=self.frm_expected_inputs, pady=40)
        self.frm_scouter_names = tk.Frame(master=self.frm_expected_inputs)
        self.frm_scouter_buttons = tk.Frame(master=self.frm_expected_inputs)

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
        self.btn_get_preset = tk.Button(master=self.frm_scouter_buttons, text="Open Presets", font=("Helvetica", 20),
                                        command=self.btn_get_preset_click)
        self.btn_save_preset = tk.Button(master=self.frm_scouter_buttons, text="Save As Preset", font=("Helvetica", 20),
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

        self.frm_scouter_buttons.grid(row=3, column=0, columnspan=2)
        self.btn_get_preset.grid(row=0, column=0)
        self.btn_save_preset.grid(row=0, column=1)
        self.btn_setup_next_match.grid(row=4, column=0, columnspan=2)

    def pull_settings(self):
        try:
            with open(self.settings_file, "r") as fs:
                self.settings = eval(fs.read().strip())
        except (FileNotFoundError, ValueError):
            self.settings = {"qr_name": "",
                             "num_setup": "",
                             "num_values": "",
                             "setup_csv_file": "",
                             "event_csv_file": "",
                             "qr_strings_file": "",
                             "current_frame_file": ""}

    def put_settings(self):
        try:
            os.makedirs("Resources")
        except OSError:
            pass
        with open(self.settings_file, "w") as fs:
            print(str(self.settings), file=fs)

    def pull_previous_data(self):
        try:
            with open(self.settings["qr_strings_file"], "r") as fs:
                for line in fs.readlines():
                    t = line[:-1].split(",")[-1]
                    self.previous_inputs[t] = line[:line.index(t)]
            self.update_previous_inputs()
        except FileNotFoundError:
            pass

        try:
            with open("Resources\\presets.txt", "r") as fs:
                self.presets = eval(fs.read())
        except FileNotFoundError:
            self.presets = {}

    def put_data(self):
        with open("Resources\\presets.txt", "w") as fs:
            print(str(self.presets), file=fs)

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

    def check_scouter_name(self, name) -> Union[tk.Entry, None]:
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
        SettingsPopup(self)

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
            if self.pause_cam:
                continue
            _, img = self.cam.read()
            while True:
                try:
                    cv2.imwrite(self.settings["current_frame_file"], img)
                    break
                except cv2.error:
                    FileNotFoundPopup(self, "Current frame", "current_frame_file")
                    while self.popup_window is not None:
                        pass
            codes_on_screen = pyzbar.decode(img)
            image = Image.open(self.settings["current_frame_file"])
            if len(codes_on_screen) > 0 and len(codes_on_screen[0].data.decode("utf-8")) > 0:
                qr = codes_on_screen[0].data.decode("utf-8")
                x, y, w, h = codes_on_screen[0].rect
                new_img = ImageDraw.Draw(image)
                if qr not in self.previous_inputs.values():
                    qr_data = qr.split(",")
                    if len(qr_data) == 0 or qr_data[-1] != self.settings["qr_name"]:
                        if len(qr_data) > 1 and qr_data[-1] == "config" and \
                                (qr_data[0] != self.settings["qr_name"] or qr_data[1] != self.settings["num_setup"] or
                                 qr_data[2] != self.settings["num_values"]):
                            ConfigFromCodePopup(self, qr_data)
                        elif len(qr_data) > 0 and qr_data[-1] == "config":
                            new_img.rectangle((x, y, x+w, y+h), outline="gold", width=4)
                        else:
                            new_img.rectangle((x, y, x+w, y+h), outline="red", width=4)
                    else:
                        new_img.rectangle((x, y, x+w, y+h), outline="orange", width=4)
                        self.parse_qr_code(qr_data)
                elif qr != list(self.previous_inputs.values())[-1]:
                    new_img.rectangle((x, y, x + w, y + h), outline="blue", width=4)
                else:
                    new_img.rectangle((x, y, x + w, y + h), outline="green", width=4)
            try:
                image = ImageTk.PhotoImage(image)
                if self.lbl_camera_img is not None:
                    self.lbl_camera_img.config(image=image)
                    self.lbl_camera_img.image = image
            finally:
                pass

    def parse_qr_code(self, qr_data):
        try:
            scouter, team, match = qr_data[:3]
        except:
            Error(self.error_handler, "main.py", 373, "qr_data: {}".format(qr_data))
            return
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
        for value in qr_data:
            qr += value + ","
        dst_file = "QR Codes\\" + team + "_" + match + ".png"
        copyfile(self.settings["current_frame_file"], dst_file)
        time_stamp = str(datetime.now())

        def chunks(data, n=self.settings["num_values"]):
            return [data[i:i + n] for i in range(0, len(data), n)]

        while True:
            try:
                with open(self.settings["qr_strings_file"], "a") as fs:
                    print(qr + time_stamp, file=fs)
                break
            except FileNotFoundError:
                FileNotFoundPopup(self, "QR strings", "qr_strings_file")
                while self.popup_window is not None:
                    pass

        while True:
            try:
                with open(self.settings["setup_csv_file"], "a") as csv_file:
                    csv_write = csv.writer(csv_file, dialect="excel", delimiter=",")
                    csv_write.writerow(qr_data[:self.settings["num_setup"]])
                break
            except FileNotFoundError:
                FileNotFoundPopup(self, "Setup data CSV", "setup_csv_file")
                while self.popup_window is not None:
                    pass

        while True:
            try:
                with open(self.settings["event_csv_file"], "a") as csv_file:
                    csv_write = csv.writer(csv_file, dialect="excel", delimiter=",")
                    setup_arr = [team, match, "Game Phase"]
                    del qr_data[:self.settings["num_setup"]]
                    for chunk in chunks(qr_data):
                        if len(chunk) < self.settings["num_values"]:
                            break
                        setup_arr[2] = chunk[0]
                        csv_write.writerow(setup_arr + ["S", "I", chunk[1], scouter])
                        csv_write.writerow(setup_arr + ["S", "O", chunk[2], scouter])
                        csv_write.writerow(setup_arr + ["S", "L", chunk[3], scouter])
                        csv_write.writerow(setup_arr + ["M", "H", chunk[4], scouter])
                        csv_write.writerow(setup_arr + ["M", "L", chunk[5], scouter])
                        csv_write.writerow(setup_arr + ["D", "", chunk[6], scouter])
                break
            except FileNotFoundError:
                FileNotFoundPopup(self, "Event data CSV", "event_csv_file")
                while self.popup_window is not None:
                    pass
        self.previous_inputs[time_stamp] = qr
        self.received_teams.append([scouter, team])
        self.update_previous_inputs()

    def close(self):
        if self.popup_window is not None:
            self.popup_window.close()
        self.put_settings()
        self.put_data()
        self.error_handler.quit()
        self.root.destroy()


if __name__ == "__main__":
    app = Application()
