import tkinter as tk


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class PopupWindow(object):
    def __init__(self, master, name):
        self.master = master
        self.root = tk.Tk()
        self.root.wm_title(name)
        self.root.wm_protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<FocusOut>", self.refocus)
        self.root.resizable(False, False)
        self.root.focus_force()

        # Other variables
        self.popup_window = None
        if hasattr(self.master, "popup_window"):
            self.master.popup_window = self
    
    def run(self):
        self.root.mainloop()

    def refocus(self, *args):
        if self.popup_window is None:
            self.root.focus_force()

    def close(self):
        self.master.popup_window = None
        self.master.root.focus_force()
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


class SettingsWindow(PopupWindow):
    def __init__(self, master):
        PopupWindow.__init__(self, master, "Settings")

        # Widgets
        # Frames
        self.frm_buttons = None
        # Labels
        self.lbl_num_setup_id = None
        self.lbl_num_vals_id = None
        # Buttons
        self.btn_save = None
        self.btn_cancel = None
        # Entry boxes
        self.ent_num_setup = None
        self.ent_num_vals = None

        # Build widgets
        self.build_widgets()
        center(self.root)

    def build_widgets(self):
        font = ("Helvetica", 16)
        # Frames
        self.frm_buttons = tk.Frame(master=self.root)

        # Labels
        self.lbl_num_setup_id = tk.Label(master=self.root, text="Number of values in setup hashmap:",
                                         font=font)
        self.lbl_num_vals_id = tk.Label(master=self.root, text="Number of values in the game phases:",
                                        font=font)

        # Buttons
        self.btn_save = tk.Button(master=self.frm_buttons, text="Save", font=font, command=self.save_click)
        self.btn_cancel = tk.Button(master=self.frm_buttons, text="Cancel", font=font, command=self.close)

        # Entry boxes
        self.ent_num_setup = tk.Entry(master=self.root, font=font)
        self.ent_num_setup.insert(0, str(self.master.settings["num_setup"]))
        self.ent_num_vals = tk.Entry(master=self.root, font=font)
        self.ent_num_vals.insert(0, str(self.master.settings["num_vals"]))

        # Pack widgets
        self.lbl_num_setup_id.grid(row=0, column=0)
        self.lbl_num_vals_id.grid(row=1, column=0)
        self.ent_num_setup.grid(row=0, column=1)
        self.ent_num_vals.grid(row=1, column=1)
        self.frm_buttons.grid(row=2, column=0, columnspan=2)
        self.btn_save.grid(row=0, column=0)
        self.btn_cancel.grid(row=0, column=1)

    def save_click(self):
        self.master.settings["num_setup"] = self.ent_num_setup.get()
        self.master.settings["num_vals"] = self.ent_num_vals.get()
        self.close()
