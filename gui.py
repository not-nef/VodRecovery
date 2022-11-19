import tkinter
import sv_ttk
import ntkutils
from tkinter import ttk
import pyperclip

import RecoverVodGUI as r

class Label(tkinter.Label):
    def __init__(self, text):
        super(Label, self).__init__(topframe, text=text, font=("Segoe UI", 11, ""), justify="left", background="#ffffff")


root = tkinter.Tk()
root.resizable(False, False)
root.title("VodRecovery")
root.geometry("430x200")
sv_ttk.set_theme("light")

topframe = tkinter.Frame(bg="#ffffff")
topframe.place(x=0, y=0, height=120, width=430)
btnframe = tkinter.Frame(bg="#f3f3f3")
btnframe.place(x=0, y=120, height=80, width=430)

def clear():
    ntkutils.clearwin(topframe)
    ntkutils.clearwin(btnframe)

def validatesegments(link):
    clear()
    segment_ratio = r.return_segment_ratio(link)
    lbl = Label(segment_ratio).pack(anchor="w", padx=20, pady=20)
    btnreturn = ttk.Button(btnframe, text="Return to main menu", command=mainpage).pack(side="left", padx=20)

def succesfullrecover(link):
    clear()
    lbl = Label(f"Successfully recovered Vod! (Copied link to clipboard)").pack(anchor="w", padx=20, pady=20)
    btnvalidate = ttk.Button(btnframe, text="Validate segments", command=lambda:validatesegments(link)).pack(side="left", padx=20)
    btnreturn = ttk.Button(btnframe, text="Return to main menu", command=mainpage).pack(side="left")
    pyperclip.copy(link)

def invalidlink():
    clear()
    lbl = Label("Invalid link. Make sure your link follow this scheme:\n\nhttps://twitchtracker.com/streamer_name/streams/vod_id").pack(anchor="w", padx=20, pady=20)
    btnretry = ttk.Button(btnframe, text="Retry", command=asklink).pack(side="left", padx=20)
    btncancel = ttk.Button(btnframe, text="Cancel", command=mainpage).pack(side="left")

def linkrecover(link):
    clear()

    lbl = Label("Recovering Vod, please wait...")
    lbl.pack(anchor="w", padx=20, pady=20)
    lbl.wait_visibility()
    lbl.update_idletasks()

    recovered_vod = r.website_vod_recover(link)
    if recovered_vod == "invalid": invalidlink()
    elif recovered_vod.endswith(".m3u8"): succesfullrecover(recovered_vod)

def asklink():
    clear()

    lbl = Label("Enter the link.").pack(anchor="w", padx=20, pady=20)
    link = ttk.Entry(topframe, width=100)
    link.pack(anchor="w", padx=20)
    btncontinue = ttk.Button(btnframe, text="Continue", command=lambda:linkrecover(link.get())).pack(side="left", padx=20)
    btnlinkhelp = ttk.Button(btnframe, text="What link?", state="disabled").pack(side="left")

def recover():
    clear()

    lbl = Label("Select your recovery method.").pack(anchor="w", padx=20, pady=20)
    btnlink = ttk.Button(btnframe, text="With Link", command=asklink).pack(side="left", padx=20)
    btnmanual = ttk.Button(btnframe, text="Manually", state="disabled").pack(side="left")
    btncsv = ttk.Button(btnframe, text="With SullyGnome CSV export", state="disabled").pack(side="left", padx=20)

def mainpage():
    clear()

    lbl = Label("Welcome to VodRecovery!\n\nI want to...").pack(side="left", padx=20)
    btnrecover = ttk.Button(btnframe, text="Recover a Vod", command=recover).pack(side="left", padx=20)
    btndownload = ttk.Button(btnframe, text="Download a Vod", state="disabled").pack(side="left")


mainpage()
root.mainloop()