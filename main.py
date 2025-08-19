import threading
import time
from tkinter import *
from tkinter import ttk
from yt_dlp_wrapper import *
from dataclasses import dataclass


class App(Tk):

    PRIMARY_COLOR = '#222323',
    SECONDARY_COLOR = '#292A2A',
    TEXT_COLOR = '#DDDDDD',
    ACCENT_COLOR = '#EDC077',
    SECONDARY_ACCENT_COLOR = '#A24936'

    def __init__(self):
        super().__init__()
        self.geometry("600x300")

        wrapper = ttk.Frame(self)
        wrapper.pack(fill=BOTH, expand=True)

        title = ttk.Label(wrapper, text='YouTube DLP Wrapper')

        url_input = FormInput(wrapper, "URL")
        target_folder_input = FormInput(wrapper, "Target Folder")

        options_frame = ttk.Frame(wrapper)

        options: list[RadiobuttonSet.Option] = [
            RadiobuttonSet.Option(label='Best Audio', value=YtDlpWrapper.RequestType.best_audio),
            RadiobuttonSet.Option(label='DaVinci Compatible', value=YtDlpWrapper.RequestType.davinci_compatible),
            RadiobuttonSet.Option(label='Best Video + Audio', value=YtDlpWrapper.RequestType.best_video_and_audio),
        ]
        import_option = RadiobuttonSet(options_frame, options)

        confirm_button = ConfirmButton(wrapper, url_entry=url_input, import_option=import_option, target_folder_input=target_folder_input)

        title.pack()
        options_frame.pack()
        import_option.pack()

        url_input.pack(fill=X)
        target_folder_input.pack(fill=X)
        confirm_button.pack()

        self.style = ttk.Style(self)
        self.style.theme_use('alt')

        self.style.configure('TFrame', background=self.PRIMARY_COLOR)
        self.style.configure('TLabel', font=('Calibri', 14), foreground=self.TEXT_COLOR, background=self.PRIMARY_COLOR)

        self.style.configure('TButton', font=('Calibri Bold', 14), background=self.ACCENT_COLOR, foreground=self.PRIMARY_COLOR, padding=(5,2), borderwidth=2, borderradius=10)
        self.style.map('TButton', background=[('active', self.SECONDARY_ACCENT_COLOR)])
        self.style.configure('TRadiobutton', font=('Calibri', 12), foreground=self.TEXT_COLOR, background=self.PRIMARY_COLOR)
        self.style.map('TRadiobutton', background=[('active', self.SECONDARY_COLOR)])



class RadiobuttonSet(ttk.Frame):

    @dataclass
    class Option[T]:
        label: str
        value: T

    selected: StringVar


    def __init__(self, parent, options: list[Option]):
        ttk.Frame.__init__(self, parent)
        self.selected = StringVar()
        
        i = 0
        for option in options:
            ttk.Radiobutton(self, text=option.label, value=option.value, variable=self.selected).pack(fill=X, ipady=5)
            i += 1
    

    def get_value(self):
        return self.selected.get()



class FormInput(ttk.Frame):

    def __init__(self, parent: Widget, label: str):
        ttk.Frame.__init__(self, parent, padding=(15, 5))

        ttk.Label(self, text=label).pack(side=LEFT, padx=10, expand=False)
        self._entry = ttk.Entry(self)
        self._entry.pack(side=RIGHT, expand=True, fill=X)
    

    def get_value(self):
        return self._entry.get() 


class ConfirmButton(ttk.Button):
    
    def __init__(self, parent: Widget, import_option: Widget, url_entry: Widget, target_folder_input: Widget):
        ttk.Button.__init__(self, parent, text="Import", command=self.threaded_click)
        self.import_option = import_option
        self.url_entry = url_entry
        self.target_folder_input = target_folder_input

    def threaded_click(self):
        t1 = threading.Thread(target=self.on_click)
        t1.start()

    def on_click(self):
        request_type = self.import_option.get_value()
        url = self.url_entry.get_value()
        directory = self.target_folder_input.get_value().replace("\\", "/")

        if request_type == "":
            print("ERROR - Select a RequestType")
            return

        if request_type not in YtDlpWrapper.RequestType:
            print("ERROR - %s is not a valid RequestType" % request_type)
            return
        
        if url == "":
            print("ERROR: Provide a URL")

        # TODO - Find a lazy dumb way to do this
        if directory != "":
            t1 = threading.Thread(target=YtDlpWrapper.call, args=(request_type, url, directory))
        if directory == "":
            t1 = threading.Thread(target=YtDlpWrapper.call, args=(request_type, url))

        t1.start()
        t1.join()



app = App()
app.mainloop()