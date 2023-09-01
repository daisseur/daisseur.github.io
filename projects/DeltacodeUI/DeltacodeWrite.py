from DeltacodeProject.Deltacode import Deltacode, DayEncoding
import tkinter as tk
from tkinter import StringVar, Entry, Label, Button, Tk, Frame, Listbox
from clipboard import copy


class main:
    def __init__(self):
        self.main = Tk()
        self.main.geometry("750x750")

        self.grid_number = 0
        self.var_password = StringVar()
        self.var_txt = StringVar()
        self.var_shift = StringVar()
        self.var_result = StringVar()
        self.var_password.trace('w', self.change_label)
        self.var_txt.trace('w', self.change_label)
        self.var_shift.trace('w', self.change_label)

        """self.len_var_txt = self.return_len(self.var_password)
        self.len_var_password = self.return_len(self.var_txt)
        self.len_var_shift = self.return_len(self.var_shift)
        self.len_var_result = self.return_len(self.var_result)"""

        for l_n in range(len(self.var_result.get())):
            if l_n in range(0, 10000, +21) != "\n" and l_n != 0:
                self.var_result.set(self.var_result.get()[:l_n] + "\n")

    def return_len(self, var):
        if isinstance(var, StringVar):
            temp_var = StringVar()
            temp_var.set(str(len(var.get())))
            return temp_var
        else:
            return str(len(var))

    def create_label_entry(self, text, example="example", trace=None):
        frame = Frame()
        if trace is None:
            entry = Entry(frame, width=40)
        else:
            entry = Entry(frame, width=40, textvariable=trace)
        label = Label(frame, text=text, font=('Arial 13 bold'))
        """if temp_var is not None:
            label_info = Label(frame, textvariable=temp_var)
            label_info.grid(column=2, row=0, padx=30, pady=10)"""
        entry.insert(0, example)
        label.grid(column=0, row=0, pady=10)
        entry.grid(column=1, row=0, pady=10)
        frame.pack()

    def create_label(self, text="optionnel", trace=None, effect="italic"):
        frame_label = Frame()
        if trace is None:
            label = Label(frame_label, text=text, font=(f'Arial 11 {effect}'))
        else:
            label = Label(frame_label, text=text, font=(f'Arial 11 {effect}'), textvariable=trace)
        label.grid()
        frame_label.pack()

    def create_button(self, text, command=None):
        if command is None:
            button = Button(text=text)
        else:
            button = Button(text=text, command=command)
        button.pack()

    def create_option(self, lst: list, side="top"):
        nbr = 1
        listbox = Listbox(height=0, width=20)
        for e in lst:
            listbox.insert(nbr, e)
        listbox.pack(side=side)

    def change_label(self, *args):
        """self.len_var_txt = self.return_len(self.var_password)
        self.len_var_password = self.return_len(self.var_txt)
        self.len_var_shift = self.return_len(self.var_shift)
        self.len_var_result = self.return_len(self.var_result)"""

        password = self.var_password.get()
        string = self.var_txt.get()
        shift = self.var_shift.get()
        print(password, string, shift)
        result = ""
        if password != '' and string != '' and shift != '':
            result = DayEncoding(password=password, string=string, shift=int(shift)).encode()
            print(result)
        self.var_result.set(result)

    def copy(self):
        copy(self.var_result.get())
        self.var_result.set("Copié !")

    def menu(self):
        self.create_option(["Encoder", "Décoder"])
        self.create_option(["Avec hexa", "Sans hexa"])
        self.create_label_entry("Mot de passe", trace=self.var_password)
        self.create_label_entry("Texte à encoder", trace=self.var_txt)
        self.create_label_entry("Shift", example="32764", trace=self.var_shift)
        self.create_button("Encoder", command=self.change_label)
        self.create_label(trace=self.var_result)
        self.create_button("Copier", command=self.copy)

    def run(self):
        self.menu()
        self.main.mainloop()





class main_manual:

    def __init__(self):
        self.main = Tk()
        self.main.geometry("750x750")

        self.var_password = StringVar()
        self.var_txt = StringVar()
        self.var_shift = StringVar()
        self.var_result = StringVar()
        self.var_password.trace('w', self.change_label)
        self.var_txt.trace('w', self.change_label)
        self.var_shift.trace('w', self.change_label)

        self.entry_password = Entry(textvariable=self.var_password, width=40)
        self.entry_password.insert(0, "__password__")
        self.entry_txt = Entry(textvariable=self.var_txt, width=40)
        self.entry_txt.insert(0, "Petit test de démo")
        self.entry_shift = Entry(textvariable=self.var_shift, width=40)
        self.entry_shift.insert(0, "32764")

        self.label_password = Label(text="Mot de passe", font=('Arial 10 bold'))
        self.label_txt = Label(text="Texte à encoder", font=('Arial 10 bold'))
        self.label_shift = Label(text="Shift", font=('Arial 10 bold'))
        self.label_result = Label(textvariable=self.var_result, font=('Arial 10 italic'))

        self.button_result = Button(text="Encoder", command=self.change_label)
        self.button_copy = Button(text="Copier", command=self.copy)

        self.add_packs(self.label_password, self.entry_password)
        self.add_packs(self.label_txt, self.entry_txt)
        self.add_packs(self.label_shift, self.entry_shift)
        self.button_result.pack()
        self.label_result.pack(padx=10, pady=10)
        self.button_copy.pack()

    def copy(self):
        copy(self.var_result.get())
        self.var_result.set("Copié !")

    def add_packs(self, to_pack_1y, to_pack_2y, *args,):
        to_pack_1y.pack(*args)
        to_pack_2y.pack(*args)

    def change_label(self, *args):
        password = self.var_password.get()
        string = self.var_txt.get()
        shift = self.var_shift.get()
        print(password, string, shift)
        if password != '' and string != '' and shift != '':
            result = DayEncoding(password=password, string=string, shift=int(shift)).encode()
            print(result)
            self.var_result.set(result)

    def run(self):
        self.main.mainloop()

if __name__ == '__main__':
    main().run()