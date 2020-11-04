from utils import *


class PopupWindow(object):
    def __init__(self, master, name, force_focus=True, create_root=True):
        self.master = master
        if create_root:
            self.root = tk.Tk()
        self.root.wm_title(name)
        self.root.wm_protocol("WM_DELETE_WINDOW", self.close)
        if force_focus:
            self.root.bind("<FocusOut>", self.refocus)
        self.root.resizable(False, False)

        # Other variables
        self.closed = False
        self.refocus_paused = False
        self.popup_window = None
        if hasattr(self.master, "popup_window"):
            if self.master.popup_window is not None:
                self.master.popup_window.close()
            self.master.popup_window = self
        if hasattr(self.master, "pause_cam"):
            self.master.pause_cam = True
        self.root.focus_force()

    def run(self):
        self.root.mainloop()

    def refocus(self, *args):
        if len(args) > 1:
            raise AttributeError("refocus takes 1 positional argument, found {}".format(1 + len(args)))
        if self.popup_window is None and not self.closed and not self.refocus_paused:
            self.root.focus_force()

    def close(self):
        self.closed = True
        self.master.popup_window = None
        self.master.root.focus_force()
        if hasattr(self.master, "pause_cam"):
            self.master.pause_cam = False
        self.root.destroy()


class PresetPopup(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Presets")

        # Widgets
        # Frames
        self.frm_buttons = None
        self.frm_ids = None
        self.frm_scouters = None
        # List boxes
        self.lst_presets = None
        # Buttons
        self.btn_save_preset = None
        self.btn_delete_preset = None
        self.btn_load_preset = None
        self.btn_use_preset = None
        # Entry boxes
        self.ent_preset_name = None
        self.ent_scouter_1 = None
        self.ent_scouter_2 = None
        self.ent_scouter_3 = None
        self.ent_scouter_4 = None
        self.ent_scouter_5 = None
        self.ent_scouter_6 = None
        # labels
        self.lbl_preset_name_id = None
        self.lbl_scouter_separator = None
        self.lbl_scouter_1_id = None
        self.lbl_scouter_2_id = None
        self.lbl_scouter_3_id = None
        self.lbl_scouter_4_id = None
        self.lbl_scouter_5_id = None
        self.lbl_scouter_6_id = None

        # Build Widgets
        self.build_widgets()
        center(self.root)

    def build_widgets(self):
        # Frames
        self.frm_buttons = tk.Frame(master=self.root, padx=10)
        self.frm_ids = tk.Frame(master=self.root, padx=5)
        self.frm_scouters = tk.Frame(master=self.root)

        # Listbox
        self.lst_presets = tk.Listbox(master=self.root)
        self.refill_list()
        self.lst_presets.select_set(tk.END)
        self.lst_presets.activate(tk.END)

        # Buttons
        self.btn_save_preset = tk.Button(master=self.frm_buttons, text="Save Preset", command=self.save_preset)
        self.btn_delete_preset = tk.Button(master=self.frm_buttons, text="Delete Preset", command=self.delete_preset)
        self.btn_load_preset = tk.Button(master=self.frm_buttons, text="Load Preset", command=self.load_preset)
        self.btn_use_preset = tk.Button(master=self.frm_buttons, text="Use Preset", command=self.use_preset)

        # Entry boxes
        self.ent_preset_name = tk.Entry(master=self.frm_scouters)
        self.ent_scouter_1 = tk.Entry(master=self.frm_scouters)
        self.ent_scouter_2 = tk.Entry(master=self.frm_scouters)
        self.ent_scouter_3 = tk.Entry(master=self.frm_scouters)
        self.ent_scouter_4 = tk.Entry(master=self.frm_scouters)
        self.ent_scouter_5 = tk.Entry(master=self.frm_scouters)
        self.ent_scouter_6 = tk.Entry(master=self.frm_scouters)

        # Labels
        self.lbl_preset_name_id = tk.Label(master=self.frm_scouters, text="Preset Name:")
        self.lbl_scouter_separator = tk.Label(master=self.frm_scouters, text=" ")
        self.lbl_scouter_1_id = tk.Label(master=self.frm_scouters, text="Scouter 1:")
        self.lbl_scouter_2_id = tk.Label(master=self.frm_scouters, text="Scouter 2:")
        self.lbl_scouter_3_id = tk.Label(master=self.frm_scouters, text="Scouter 3:")
        self.lbl_scouter_4_id = tk.Label(master=self.frm_scouters, text="Scouter 4:")
        self.lbl_scouter_5_id = tk.Label(master=self.frm_scouters, text="Scouter 5:")
        self.lbl_scouter_6_id = tk.Label(master=self.frm_scouters, text="Scouter 6:")

        # Add widgets to window
        self.lst_presets.grid(row=0, column=0)

        self.frm_buttons.grid(row=0, column=1)
        self.btn_save_preset.grid(row=0, column=0)
        self.btn_delete_preset.grid(row=1, column=0)
        self.btn_load_preset.grid(row=2, column=0)
        self.btn_use_preset.grid(row=3, column=0)

        self.frm_scouters.grid(row=0, column=2)
        self.lbl_preset_name_id.grid(row=0, column=0)
        self.lbl_scouter_separator.grid(row=1, column=0)
        self.lbl_scouter_1_id.grid(row=2, column=0)
        self.lbl_scouter_2_id.grid(row=3, column=0)
        self.lbl_scouter_3_id.grid(row=4, column=0)
        self.lbl_scouter_4_id.grid(row=5, column=0)
        self.lbl_scouter_5_id.grid(row=6, column=0)
        self.lbl_scouter_6_id.grid(row=7, column=0)

        self.ent_preset_name.grid(row=0, column=1)
        self.ent_scouter_1.grid(row=2, column=1)
        self.ent_scouter_2.grid(row=3, column=1)
        self.ent_scouter_3.grid(row=4, column=1)
        self.ent_scouter_4.grid(row=5, column=1)
        self.ent_scouter_5.grid(row=6, column=1)
        self.ent_scouter_6.grid(row=7, column=1)

    def refill_list(self):
        self.lst_presets.delete(0, tk.END)
        for preset in self.master.presets.keys():
            self.lst_presets.insert(tk.END, preset)
        self.lst_presets.insert(tk.END, "<new>")

    def save_preset(self, force_save=False):
        new_name = self.ent_preset_name.get()
        old_name = self.lst_presets.get(tk.ACTIVE)
        index = self.lst_presets.curselection()[0] if old_name != "<new>" else \
            self.lst_presets.get(0, tk.END).index("<new>")
        if not force_save:
            if new_name in self.lst_presets.get(0, tk.END) and new_name != old_name:
                PreExistingPresetPopup(self)
                return

            if new_name != old_name and old_name != "<new>":
                del (self.master.presets[old_name])

            self.master.presets[new_name] = [self.ent_scouter_1.get(),
                                             self.ent_scouter_2.get(),
                                             self.ent_scouter_3.get(),
                                             self.ent_scouter_4.get(),
                                             self.ent_scouter_5.get(),
                                             self.ent_scouter_6.get()]
            self.refill_list()
            self.lst_presets.select_set(index)
            self.lst_presets.activate(index)

    def delete_preset(self):
        name = self.lst_presets.get(tk.ACTIVE)
        if name != "<new>":
            del self.master.presets[name]
        self.refill_list()

    def load_preset(self):
        name = self.lst_presets.get(tk.ACTIVE)

        # Clear entry boxes
        self.ent_preset_name.delete(0, tk.END)
        self.ent_scouter_1.delete(0, tk.END)
        self.ent_scouter_2.delete(0, tk.END)
        self.ent_scouter_3.delete(0, tk.END)
        self.ent_scouter_4.delete(0, tk.END)
        self.ent_scouter_5.delete(0, tk.END)
        self.ent_scouter_6.delete(0, tk.END)

        if name == "<new>":
            return

        # Set text to preset data
        self.ent_preset_name.insert(0, name)
        self.ent_scouter_1.insert(0, self.master.presets[name][0])
        self.ent_scouter_2.insert(0, self.master.presets[name][1])
        self.ent_scouter_3.insert(0, self.master.presets[name][2])
        self.ent_scouter_4.insert(0, self.master.presets[name][3])
        self.ent_scouter_5.insert(0, self.master.presets[name][4])
        self.ent_scouter_6.insert(0, self.master.presets[name][5])

    def use_preset(self):
        name = self.lst_presets.get(tk.ACTIVE)
        if name == "<new>":
            return
        preset = self.master.presets[name]

        # Clear entry boxes
        self.master.ent_scouter_preset.delete(0, tk.END)
        self.master.ent_scouter_1.delete(0, tk.END)
        self.master.ent_scouter_2.delete(0, tk.END)
        self.master.ent_scouter_3.delete(0, tk.END)
        self.master.ent_scouter_4.delete(0, tk.END)
        self.master.ent_scouter_5.delete(0, tk.END)
        self.master.ent_scouter_6.delete(0, tk.END)

        # Fill entry boxes
        self.master.ent_scouter_preset.insert(0, name)
        self.master.ent_scouter_1.insert(0, preset[0])
        self.master.ent_scouter_2.insert(0, preset[1])
        self.master.ent_scouter_3.insert(0, preset[2])
        self.master.ent_scouter_4.insert(0, preset[3])
        self.master.ent_scouter_5.insert(0, preset[4])
        self.master.ent_scouter_6.insert(0, preset[5])

        self.close()


class NameNotFoundPopup(PopupWindow):
    def __init__(self, master, scouter_name):
        PopupWindow.__init__(self, master, "Name not found")
        # Other variables
        self.scouter_name = scouter_name

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_change_tablet = None
        self.btn_add_to_list = None
        self.btn_ignore = None
        # Build widgets
        self.build_widgets()

    def build_widgets(self):
        # Labels
        self.lbl_info = tk.Label(master=self.root,
                                 text="The name '" + self.scouter_name +
                                      "' is not in the list of expected scouters.\nWould you like to:",
                                 font=("Helvetica", 16))

        # Buttons
        self.btn_change_tablet = tk.Button(master=self.root,
                                           text="Change the name from the tablet to one from the list",
                                           font=("Helvetica", 12), command=self.change_tablet_name)
        self.btn_add_to_list = tk.Button(master=self.root, text="Add '" + self.scouter_name +
                                                                "' to the list of expected scouters",
                                         font=("Helvetica", 12), command=self.add_name_to_list)
        self.btn_ignore = tk.Button(master=self.root, text="Ignore this message", font=("Helvetica", 12),
                                    command=self.close)

        # Add widgets to window
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.btn_change_tablet.grid(row=1, column=0)
        self.btn_add_to_list.grid(row=1, column=1)
        self.btn_ignore.grid(row=2, column=0, columnspan=2)

    def run(self):
        PopupWindow.run(self)
        return self.scouter_name

    def change_tablet_name(self):
        ChangeTabletNamePopup(self)

    def add_name_to_list(self):
        AddScouterToListPopup(self)


class ChangeTabletNamePopup(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Change Tablet Name")

        # Widgets
        # Listboxes
        self.lst_expected_names = None
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_back = None
        self.btn_confirm = None
        # Entry boxes
        self.ent_name = None

        # Build Widgets
        self.build_widgets()
        center(self.root)

        # Mainloop
        self.run()

    def build_widgets(self):
        # Listboxes
        self.lst_expected_names = tk.Listbox(master=self.root)
        for ent in self.master.master.scout_entries:
            self.lst_expected_names.insert(tk.END, ent.get())
        self.lst_expected_names.bind("<<ListboxSelect>>", self.lst_select)

        # Labels
        self.lbl_info = tk.Label(master=self.root, text="Select a name from the list to change the\n" +
                                                        "tablet name to. If needed, edit the name\n" +
                                                        "in the box and then select 'Confirm'",
                                 font=("Helvetica", 12))

        # Buttons
        self.btn_back = tk.Button(master=self.root, text="Back", command=self.close)
        self.btn_confirm = tk.Button(master=self.root, text="Confirm", command=self.confirm)

        # Entry boxes
        self.ent_name = tk.Entry(master=self.root)

        # Add widgets to window
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.lst_expected_names.grid(row=1, column=0, columnspan=2)
        self.ent_name.grid(row=2, column=0, columnspan=2)
        self.btn_confirm.grid(row=3, column=0)
        self.btn_back.grid(row=3, column=1)

    def lst_select(self, event):
        if event is None:
            raise AttributeError("Expected event, found None")
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, self.lst_expected_names.get(self.lst_expected_names.curselection()))

    def confirm(self):
        self.master.scouter_name = self.ent_name.get()
        self.close()
        self.master.close()


class AddScouterToListPopup(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Add Name to List")

        # Widgets
        # Listboxes
        self.lst_expected_names = None
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_back = None
        self.btn_confirm = None
        # Entry boxes
        self.ent_name = None

        # Build Widgets
        self.build_widgets()
        center(self.root)

        # Mainloop
        self.run()

    def build_widgets(self):
        # Listboxes
        self.lst_expected_names = tk.Listbox(master=self.root)
        for ent in self.master.master.scout_entries:
            self.lst_expected_names.insert(tk.END, ent.get())

        # Labels
        self.lbl_info = tk.Label(master=self.root, text="Select a name from the list to change to\n" +
                                                        "the name from the tablet. If needed, edit\n" +
                                                        "the name in the box and then select 'Confirm'",
                                 font=("Helvetica", 12))

        # Buttons
        self.btn_back = tk.Button(master=self.root, text="Back", command=self.close)
        self.btn_confirm = tk.Button(master=self.root, text="Confirm", command=self.confirm)

        # Entry boxes
        self.ent_name = tk.Entry(master=self.root)
        self.ent_name.insert(0, self.master.scouter_name)

        # Add widgets to window
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.lst_expected_names.grid(row=1, column=0, columnspan=2)
        self.ent_name.grid(row=2, column=0, columnspan=2)
        self.btn_confirm.grid(row=3, column=0)
        self.btn_back.grid(row=3, column=1)

    def confirm(self):
        index = self.lst_expected_names.curselection()[0]
        self.master.master.scout_entries[index].delete(0, tk.END)
        self.master.master.scout_entries[index].insert(0, self.ent_name.get())
        self.close()
        self.master.close()


class UnreceivedScouterPopup(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Unfinished Scouting")

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_yes = None
        self.btn_cancel = None

        # Build widgets
        self.build_widgets()
        center(self.root)

        # Run
        self.run()

    def build_widgets(self):
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="Some of the expected scouters haven't\n" +
                                                        "turned in their qr codes yet. Do you\n" +
                                                        "want to go to the next match anyway?",
                                 font=("Helvetica", 12))

        # Buttons
        self.btn_yes = tk.Button(master=self.root, text="Yes", command=self.yes_click)
        self.btn_cancel = tk.Button(master=self.root, text="Cancel", command=self.close)

        # Add widgets to window
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.btn_yes.grid(row=1, column=0)
        self.btn_cancel.grid(row=1, column=1)

    def yes_click(self):
        self.close()
        self.master.setup_next_match(force=True)


class PreExistingPresetPopup(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Pre-existing Preset")

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_yes = None
        self.btn_no = None

        # Build widgets
        self.build_widgets()
        center(self.root)

        # Mainloop
        self.run()

    def build_widgets(self):
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="A preset with that name already\n" +
                                                        "exists. Do you want to update\n" +
                                                        "that preset with the new data?",
                                 font=("Helvetica", 12))

        # Buttons
        self.btn_yes = tk.Button(master=self.root, text="Yes", command=self.yes_click)
        self.btn_no = tk.Button(master=self.root, text="No", command=self.close)

        # Add widgets to window
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.btn_yes.grid(row=1, column=0)
        self.btn_no.grid(row=1, column=1)

    def yes_click(self):
        self.master.save_preset(force_save=True)
        self.close()


class WrongMatchNumberPopup(PopupWindow):
    def __init__(self, master, match_num):
        PopupWindow.__init__(self, master, "Incorrect match number")

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_yes = None
        self.btn_no = None

        # Other variables
        self.match_number = match_num

        # Build widgets
        self.build_widgets()
        center(self.root)

    def build_widgets(self):
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="The match number from the tablet doesn't\n"
                                                        "match the expected match number.\n"
                                                        "Do you want to change the match number\n"
                                                        "from the tablet to match the expected one?",
                                 font=("Helvetica", 12))

        # Buttons
        self.btn_yes = tk.Button(master=self.root, text="Yes", command=self.yes_click)
        self.btn_no = tk.Button(master=self.root, text="No", command=self.close)

        # Add widgets to window
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.btn_yes.grid(row=1, column=0)
        self.btn_no.grid(row=1, column=1)

    def yes_click(self):
        self.match_number = self.master.ent_match_num.get()
        self.close()

    def run(self):
        PopupWindow.run(self)
        return self.match_number


class RepeatedTeamNumberPopup(PopupWindow):
    def __init__(self, master, scouter, team_num):
        PopupWindow.__init__(self, master, "Repeated team number")

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_yes = None
        # Entry boxes
        self.ent_team_num = None

        # Other variables
        self.scouter = scouter
        self.team_number = team_num

        # Build widgets
        self.build_widgets()
        center(self.root)

    def build_widgets(self):
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="The team number from the tablet matches\n" +
                                                        "the team number submitted by {}.\n".format(self.scouter) +
                                                        "If this is a mistake, edit the team\n" +
                                                        "number in the box and click confirm.",
                                 font=("Helvetica", 12))

        # Buttons
        self.btn_yes = tk.Button(master=self.root, text="Yes", command=self.confirm_click)

        # Entry boxes
        self.ent_team_num = tk.Entry(master=self.root, font=("Helvetica", 12))
        self.ent_team_num.insert(0, str(self.team_number))

        # Pack widgets
        self.lbl_info.grid(row=0, column=0)
        self.ent_team_num.grid(row=1, column=0)
        self.btn_yes.grid(row=2, column=0)

    def confirm_click(self):
        self.team_number = self.ent_team_num.get()
        self.close()

    def run(self):
        PopupWindow.run(self)
        return self.team_number


class SettingsPopup(PopupWindow):
    def __init__(self, master):
        self.root = tk.Toplevel()
        PopupWindow.__init__(self, master, "Settings", create_root=False)

        # Widgets
        # Frames
        self.frm_variables = None
        self.frm_file_paths = None
        self.frm_buttons = None
        # Labels
        self.lbl_num_setup_id = None
        self.lbl_num_values_id = None
        self.lbl_space_1 = None
        self.lbl_qr_name_id = None
        self.lbl_space_2 = None
        self.lbl_setup_csv_id = None
        self.lbl_event_csv_id = None
        self.lbl_qr_strings_file_id = None
        self.lbl_space_3 = None
        # Buttons
        self.btn_setup_csv = None
        self.btn_event_csv = None
        self.btn_qr_strings_file = None
        self.btn_save = None
        self.btn_cancel = None
        # Entry boxes
        self.ent_qr_name = None
        self.ent_num_setup = None
        self.ent_num_values = None
        self.ent_setup_csv = None
        self.ent_event_csv = None
        self.ent_qr_strings_file = None

        # Other variables
        self.photo = None

        # Build widgets
        self.build_widgets()
        center(self.root)

    def build_widgets(self):
        font = ("Helvetica", 16)
        # Frames
        self.frm_variables = tk.Frame(master=self.root)
        self.frm_file_paths = tk.Frame(master=self.root, padx=10)
        self.frm_buttons = tk.Frame(master=self.root)

        # Labels
        self.lbl_num_setup_id = tk.Label(master=self.frm_variables, text="# of setup values:", font=font)
        self.lbl_num_values_id = tk.Label(master=self.frm_variables, text="# of game phases values:", font=font)
        self.lbl_space_1 = tk.Label(master=self.frm_variables, text="", font=("Helvetica", 2))
        self.lbl_qr_name_id = tk.Label(master=self.frm_variables, text="QR Code Name:", font=font)
        self.lbl_space_2 = tk.Label(master=self.frm_variables, text="", font=("Helvetica", 4))
        self.lbl_setup_csv_id = tk.Label(master=self.frm_file_paths, text="Setup data CSV file:", font=font)
        self.lbl_event_csv_id = tk.Label(master=self.frm_file_paths, text="Event data CSV file:", font=font)
        self.lbl_qr_strings_file_id = tk.Label(master=self.frm_file_paths, text="QR strings file:", font=font)
        self.lbl_space_3 = tk.Label(master=self.frm_file_paths, text="", font=("Helvetica", 4))

        # Buttons
        image = Image.open("Resources/folder.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.btn_setup_csv = tk.Button(master=self.frm_file_paths, image=self.photo, command=self.btn_setup_csv_click)
        self.btn_event_csv = tk.Button(master=self.frm_file_paths, image=self.photo, command=self.btn_event_csv_click)
        self.btn_qr_strings_file = tk.Button(master=self.frm_file_paths, image=self.photo,
                                             command=self.btn_qr_strings_file_click)
        self.btn_save = tk.Button(master=self.frm_buttons, text="Save", font=font, command=self.save_click)
        self.btn_cancel = tk.Button(master=self.frm_buttons, text="Cancel", font=font, command=self.close)

        # Entry boxes
        self.ent_num_setup = tk.Entry(master=self.frm_variables, width=3, font=font)
        self.ent_num_setup.insert(0, str(self.master.settings["num_setup"]))
        self.ent_num_values = tk.Entry(master=self.frm_variables, width=3, font=font)
        self.ent_num_values.insert(0, str(self.master.settings["num_values"]))
        self.ent_qr_name = tk.Entry(master=self.frm_variables, width=30, font=font)
        self.ent_qr_name.insert(0, str(self.master.settings["qr_name"]))
        self.ent_setup_csv = tk.Entry(master=self.frm_file_paths, width=65, font=("Helvetica", 12))
        self.ent_setup_csv.insert(0, str(self.master.settings["setup_csv_file"]))
        self.ent_event_csv = tk.Entry(master=self.frm_file_paths, font=("Helvetica", 12))
        self.ent_event_csv.insert(0, str(self.master.settings["event_csv_file"]))
        self.ent_qr_strings_file = tk.Entry(master=self.frm_file_paths, font=("Helvetica", 12))
        self.ent_qr_strings_file.insert(0, str(self.master.settings["qr_strings_file"]))

        # Pack widgets
        self.frm_variables.grid(row=0, column=0, pady=5)
        self.lbl_num_setup_id.grid(row=0, column=0)
        self.lbl_num_values_id.grid(row=0, column=2)
        self.lbl_space_1.grid(row=1, column=0, columnspan=4)
        self.lbl_qr_name_id.grid(row=2, column=0)
        self.lbl_space_2.grid(row=3, column=0, columnspan=4)
        self.ent_num_setup.grid(row=0, column=1, sticky="w")
        self.ent_num_values.grid(row=0, column=3, sticky="w")
        self.ent_qr_name.grid(row=2, column=1, columnspan=3, sticky="w")
        self.frm_file_paths.grid(row=1, column=0)
        self.lbl_setup_csv_id.grid(row=0, column=0)
        self.lbl_event_csv_id.grid(row=2, column=0)
        self.lbl_qr_strings_file_id.grid(row=4, column=0)
        self.ent_setup_csv.grid(row=1, column=0, sticky="we", ipady=4)
        self.ent_event_csv.grid(row=3, column=0, sticky="we", ipady=4)
        self.ent_qr_strings_file.grid(row=5, column=0, sticky="we", ipady=4)
        self.btn_setup_csv.grid(row=1, column=1)
        self.btn_event_csv.grid(row=3, column=1)
        self.btn_qr_strings_file.grid(row=5, column=1)
        self.lbl_space_3.grid(row=6, column=0, columnspan=2)
        self.frm_buttons.grid(row=2, column=0, pady=5)
        self.btn_save.grid(row=0, column=0)
        self.btn_cancel.grid(row=0, column=1)

    def btn_setup_csv_click(self):
        self.refocus_paused = True
        folder = self.ent_setup_csv.get()[:self.ent_setup_csv.get().rfind("/")]
        file = self.ent_setup_csv.get()[len(folder) + 1:]
        try:
            open(os.path.join(folder, file))
        except FileNotFoundError:
            folder = os.getcwd()
            file = ""
        filename = filedialog.askopenfilename(parent=self.root, title="Setup CSV file",
                                              initialdir=folder, initialfile=file,
                                              filetypes=[("Comma Separated Values", ".csv"), ("All Files", "*")])
        self.refocus_paused = False
        self.refocus()
        if len(filename) > 0:
            self.ent_setup_csv.delete(0, tk.END)
            self.ent_setup_csv.insert(tk.END, filename)

    def btn_event_csv_click(self):
        self.refocus_paused = True
        folder = self.ent_event_csv.get()[:self.ent_event_csv.get().rfind("/")]
        file = self.ent_event_csv.get()[len(folder) + 1:]
        try:
            open(os.path.join(folder, file))
        except FileNotFoundError:
            folder = os.getcwd()
            file = ""
        filename = filedialog.askopenfilename(parent=self.root, title="Event CSV file",
                                              initialdir=folder, initialfile=file,
                                              filetypes=[("Comma Separated Values", ".csv"),
                                                         ("All Files", "*")])
        self.refocus_paused = False
        self.refocus()
        if len(filename) > 0:
            self.ent_event_csv.delete(0, tk.END)
            self.ent_event_csv.insert(tk.END, filename)

    def btn_qr_strings_file_click(self):
        self.refocus_paused = True
        folder = self.ent_qr_strings_file.get()[:self.ent_qr_strings_file.get().rfind("/")]
        file = self.ent_qr_strings_file.get()[len(folder) + 1:]
        try:
            open(os.path.join(folder, file))
        except FileNotFoundError:
            folder = os.getcwd()
            file = ""
        filename = filedialog.askopenfilename(parent=self.root, title="QR strings file",
                                              initialdir=folder, initialfile=file,
                                              filetypes=[("Text file", ".txt")])
        self.refocus_paused = False
        self.refocus()
        if len(filename) > 0:
            self.ent_qr_strings_file.delete(0, tk.END)
            self.ent_qr_strings_file.insert(tk.END, filename)

    def save_click(self):
        self.master.settings["qr_name"] = self.ent_qr_name.get()
        self.master.settings["num_setup"] = self.ent_num_setup.get()
        self.master.settings["num_values"] = self.ent_num_values.get()
        self.master.settings["setup_csv_file"] = self.ent_setup_csv.get()
        self.master.settings["event_csv_file"] = self.ent_event_csv.get()
        self.master.settings["qr_strings_file"] = self.ent_qr_strings_file.get()
        self.close()


class ConfigFromCodePopup(PopupWindow):
    def __init__(self, master, qr_data):
        PopupWindow.__init__(self, master, "Config Reader")

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_config = None
        self.btn_cancel = None

        # Other variables
        self.qr_data = qr_data

        # Build widgets
        self.build_widgets()
        center(self.root)

        # Mainloop
        self.run()

    def build_widgets(self):
        font = ("Helvetica", 16)
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="Do you want to configure the settings\n"
                                                        "values using the scanned qr code?", font=font)
        # Buttons
        self.btn_config = tk.Button(master=self.root, text="Configure", font=font, command=self.btn_config_click)
        self.btn_cancel = tk.Button(master=self.root, text="Cancel", font=font, command=self.close)

        # Pack widgets
        self.lbl_info.grid(row=0, column=0, columnspan=2)
        self.btn_config.grid(row=1, column=0)
        self.btn_cancel.grid(row=1, column=1)

    def btn_config_click(self):
        old_settings = self.master.settings.copy()
        try:
            self.master.settings["qr_name"] = self.qr_data[0]
            self.master.settings["num_setup"] = self.qr_data[1]
            self.master.settings["num_values"] = self.qr_data[2]
            self.close()
        except IndexError:
            self.master.settings = old_settings
            ConfigErrorPopup(self)


class ConfigErrorPopup(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Configuration Error")

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_ok = None

        # Build widgets
        self.build_widgets()
        center(self.root)

        # Mainloop
        self.run()

    def build_widgets(self):
        font = ("Helvetica", 16)
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="There was an error configuring from the\n"
                                                        "qr code.  Please scan again, or enter the\n"
                                                        "data manually using the settings button", font=font)
        # Buttons
        self.btn_ok = tk.Button(master=self.root, text="OK", font=font, command=self.close)

        # Pack widgets
        self.lbl_info.grid(row=0, column=0)
        self.btn_ok.grid(row=1, column=0)

    def close(self):
        PopupWindow.close(self)
        self.master.close()


class FileNotFoundPopup(PopupWindow):
    def __init__(self, master, file_designation, key):
        self.root = tk.Toplevel()
        PopupWindow.__init__(self, master, "File Not Found", create_root=False)

        # Widgets
        # Labels
        self.lbl_info = None
        # Buttons
        self.btn_filename = None
        self.btn_ok = None
        # Entries
        self.ent_filename = None

        # Other variables
        self.file_designation = file_designation
        self.key = key
        self.photo = None

        # Build widgets
        self.build_widgets()
        center(self.root)

    def build_widgets(self):
        font = ("Helvetica", 16)
        # Labels
        self.lbl_info = tk.Label(master=self.root, text="Something went wrong outputting data\n"
                                                        "to the {} file.  "
                                                        "Please enter a\n".format(self.file_designation) +
                                                        "new file path into the field, or click the\n"
                                                        "button to choose a file from the directory.", font=font)

        # Buttons
        image = Image.open("Resources/folder.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.btn_filename = tk.Button(master=self.root, image=self.photo, font=font, command=self.btn_filename_click)
        self.btn_ok = tk.Button(master=self.root, text="OK", font=font, command=self.close)

        # Entries
        self.ent_filename = tk.Entry(master=self.root, font=font)
        self.ent_filename.insert(tk.END, self.master.settings[self.key])

        # Pack widgets
        self.lbl_info.grid(row=0, column=0, ipadx=10, columnspan=2)
        self.ent_filename.grid(row=1, column=0, sticky="we", padx=5, pady=5)
        self.btn_filename.grid(row=1, column=1, padx=5, pady=5)
        self.btn_ok.grid(row=2, column=0, columnspan=2, pady=5)

        self.root.grid_columnconfigure(0, weight=1)

    def btn_filename_click(self):
        filename = filedialog.askopenfilename(parent=self.root, title="{} file".format(self.file_designation))
        self.refocus()
        if len(filename) > 0:
            self.ent_filename.delete(0, tk.END)
            self.ent_filename.insert(tk.END, filename)

    def close(self):
        self.master.settings[self.key] = self.ent_filename.get()
        PopupWindow.close(self)
