import customtkinter
import os
import subprocess
import re
from PIL import Image


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list=[], command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="WE")
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [
            checkbox.cget("text")
            for checkbox in self.checkbox_list
            if checkbox.get() == 1
        ]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.icon = customtkinter.CTkImage(
            dark_image=Image.open("ref.png"), size=(20, 20)
        )

        self.grid_rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.title("ADS Detector")
        self.geometry("650x380")
        self.iconbitmap("icon1.ico")

        # create scrollable checkbox frame
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(
            master=self, width=400, label_text="List of ADS"
        )
        self.scrollable_checkbox_frame.grid(
            row=1, column=1, padx=15, pady=(15, 5), sticky="ns"
        )

        # frame 1
        self.frame_1 = customtkinter.CTkFrame(self)
        self.frame_1.grid(row=1, column=0, padx=15, pady=(15, 5), sticky="ns")
        self.frame_1.grid_rowconfigure(0, weight=1)
        self.frame_1.grid_rowconfigure(1, weight=1)

        self.button_1 = customtkinter.CTkButton(
            master=self.frame_1, text="Open", command=self.Open
        )
        self.button_1.grid(row=0, column=0, padx=15, pady=10, sticky="ns")
        self.button_2 = customtkinter.CTkButton(
            master=self.frame_1, text="Delete", command=self.DEl
        )
        self.button_2.grid(row=1, column=0, padx=15, pady=10, sticky="ns")

        # frame 2
        self.frame_2 = customtkinter.CTkFrame(self)
        self.frame_2.grid(
            row=0, column=0, padx=15, pady=(15, 5), sticky="WE", columnspan=2
        )
        self.frame_2.grid_columnconfigure(0, weight=1)

        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_2, placeholder_text="Path location"
        )
        self.entry_1.grid(row=0, column=0, padx=(15, 5), pady=8, sticky="NWSE")
        self.button_3 = customtkinter.CTkButton(
            master=self.frame_2, text="SCAN", command=self.scan
        )
        self.button_3.grid(row=0, column=1, padx=(15, 5), pady=8, sticky="NWSE")
        self.button_4 = customtkinter.CTkButton(
            master=self.frame_2,
            text="",
            width=20,
            image=self.icon,
            command=self.refresh,
        )
        self.button_4.grid(row=0, column=2, padx=(0, 15), pady=8, sticky="NWSE")

        # frame 3
        self.frame_3 = customtkinter.CTkFrame(self)
        self.frame_3.grid(
            row=2, column=0, padx=15, pady=(10, 5), sticky="WE", columnspan=2
        )
        self.label_1 = customtkinter.CTkLabel(
            master=self.frame_3,
            text="- by Nikhil(cys58) and Angela(cys88)",
            fg_color="transparent",
            anchor="e",
            font=("roboto", 11),
        )
        self.label_2 = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Amrita Vishwa Vidyapeetham",
            fg_color="transparent",
            anchor="w",
            font=("roboto", 11),
        )
        self.frame_3.grid_rowconfigure(0, weight=1)
        self.frame_3.columnconfigure(0, weight=1)
        self.label_1.grid(row=0, column=1, padx=20, sticky="WE")
        self.label_2.grid(row=0, column=0, padx=20, sticky="WE")

    # def checkbox_frame_event(self):
    #    print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    def scan(self):
        # print(f"string: {self.entry_1.get()}")
        output = subprocess.check_output(
            "dir" + " " + self.entry_1.get() + " " + "/r", shell=True
        )
        a = output.decode().split("\r\n")
        pattern = re.compile(r".+(?=:\$DATA$)")
        a = [re.search(pattern, i).group().lstrip() for i in a if re.search(pattern, i)]
        for i in a:
            self.scrollable_checkbox_frame.add_item(i)

    def refresh(self):
        output = subprocess.check_output(
            "dir" + " " + self.entry_1.get() + " " + "/r", shell=True
        )
        a = output.decode().split("\r\n")
        pattern = re.compile(r".+(?=:\$DATA$)")
        a = [re.search(pattern, i).group().lstrip() for i in a if re.search(pattern, i)]
        for i in a:
            self.scrollable_checkbox_frame.remove_item(i)

    def Open(self):
        for k in self.scrollable_checkbox_frame.get_checked_items():
            exe = subprocess.check_output(
                "notepad " + self.entry_1.get() + "\\" + k.split(" ")[1], shell=False
            )

    def DEl(self):
        for k in self.scrollable_checkbox_frame.get_checked_items():
            result = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Remove-Item -Path "
                    + '"'
                    + self.entry_1.get()
                    + "\\"
                    + k.split(" ")[1]
                    + '"',
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            self.scrollable_checkbox_frame.remove_item(k)


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    app = App()
    app.mainloop()
