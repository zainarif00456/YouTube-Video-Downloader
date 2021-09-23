import os
from tkinter import *
from pytube import YouTube
from tkinter import ttk, filedialog, messagebox
import threading

"""
Written by: Zain-Ul-Abdeen
Email: zainarif00456@gmail.com
"""

class UserInterface(Tk):
    def __init__(self):
        """
        The constructor contains the code of user interface and default path for downloading file.
        """
        super().__init__()
        self.link = StringVar()
        self.path = "C:\\YouTube Video Downloader\\Downloads"
        self.initComponents()


    def initComponents(self):
        """
        All the components of User Interface are added in this Function.
        :return:
        """
        self.geometry("500x350")
        self.maxsize(500, 350)
        self.minsize(500, 350)
        self.title("YouTube Video Downloader")
        logo = PhotoImage(file="icon.png")
        self.iconphoto(False, logo)
        self.config(bg="grey")


        self.heading = Label(self, text="Welcome to YouTube Videos Downloader",bg="blue", fg="white", font="arial 19 bold")
        self.heading.pack(side=TOP, fill=X)

        self.linklabel = Label(self, text="Enter Video URL", bg="grey", font=("", 14, "bold"))
        self.linklabel.pack(pady=(10, 5))
        self.entrylink =  Entry(self, textvariable=self.link, width=40)
        self.entrylink.pack(pady=5)

        self.chooseres = Label(self, text="Get Video Resolution", bg="grey", font=("", 14, "bold"))
        self.chooseres.pack(pady=5)
        self.val = ["High Quality", "Low Quality", "Audio (MP3)"]
        self.result = ttk.Combobox(self, values=self.val)
        self.result.pack(pady=5)

        self.direct = Button(self, text="Select Location", bg="blue", fg="white",font=("", 11, "bold"), command=self.downloadlocation)
        self.direct.pack(pady=5)
        self.dir = Label(self, text=self.path, bg="grey", font=("", 11, "bold"))
        self.dir.pack(pady=5)


        self.download = Button(self, text="DOWNLOAD", bg="green", fg="white", command=self.passurl)
        self.download.pack(pady=5)

        self.progress = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.progress.pack(pady=5)

    def passurl(self):
        """
        Contain threading function. This function will start thread for downloading...
        :return:
        """
        try:
            downloadThread = threading.Thread(target=lambda: self.downloadvideo())
            downloadThread.start()
        except Exception as e:
            messagebox.showerror("Threading Error", f"ERROR OCCURED: {e}")

    def downloadvideo(self):
        """
        This function will get data from Labels and entries etc and perform different operations for downloading.
        :return:
        """
        videolink = ""
        videolink = str(self.link.get())
        if videolink == "":
            self.linklabel.config(text="Please Enter Video URL!!", font=("", 14, "bold"), fg="red")
            return
        elif "youtube" not in videolink:
            self.linklabel.config(text="Please Enter Correct Video URL!!", font=("", 14, "bold"), fg="red")
            messagebox.showerror("ERROR: ", "INVALID LINK")
            return
        #       A message box for notifying that downloading started. If you wanna keep it, your choice...
       # messagebox.showinfo("Status", "DOWNLOADING STARTED. Click OK TO CONTINUE"
        #                              "\nNOTE: Do not close the Downloader until the downloading is completed")
        self.progress.start()
        cursor = YouTube(videolink)
        select = cursor.streams.get_highest_resolution()
        self.choice = StringVar()
        c = self.result.get()
        try:
            if  c == self.val[0]:
                select = cursor.streams.get_highest_resolution()
            elif c == self.val[1]:
                select = cursor.streams.get_lowest_resolution()
            elif c == self.val[2]:
                select = cursor.streams.filter(only_audio=True).first()

            select.download(self.path)
        except Exception as e:
            messagebox.showinfo("Download Error", f"ERROR OCCURED: '{select.title}' has no audio file to download. Only video available...")
            return
        self.progress.stop()
        choice=messagebox.askyesno("Download Status", f"File Downloaded to {self.path}. Do You Want to Open Download Folder")

        if choice==1:
            os.startfile(self.path)
        elif choice==0:
            pass



    def downloadlocation(self):
        """
        This function will get the download location and configure the label text...
        :return:
        """
        self.path = filedialog.askdirectory()
        self.dir.config(text=self.path)



if __name__ == '__main__':
    ui = UserInterface()
    ui.mainloop()