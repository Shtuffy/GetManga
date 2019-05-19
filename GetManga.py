import praw
import time
from tkinter import *
import webbrowser
import os

reddit = praw.Reddit(client_id='v2-FmpdKuC_Lfw', client_secret='VROuxQeBU70Y5iVkXyN3aiskJ90', user_agent='my user agent')

filepath = 'C:/GetManga/'

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


create_folder(filepath)

#Manga posts
mlfilename = "mangaList"
mlfullpath = os.path.join(filepath, mlfilename+".txt")
if not os.path.exists(mlfullpath):
    mangaList = open(mlfullpath, "w+").read().splitlines()
else:
    mangaList = open(mlfullpath, "r").read().splitlines()

cfilename = "chapters"
cfullpath = os.path.join(filepath, cfilename+".txt")
chapters = open(cfullpath, "w+").read().splitlines()

clfilename = "chapterlinks"
clfullpath = os.path.join(filepath, clfilename+".txt")
chapterlinks = open(clfullpath, "w+").read().splitlines()

allchapters = [""]
allchapterlinks = [""]

#subreddit info
subreddit = reddit.subreddit('manga')
limit = 200
new_submissions = subreddit.new(limit=limit)

#GUI info
read = []
labels = [""]
root = Tk()

#Time info
currentTime = int(time.time())
howLongAgo = 24


class GetManga:
    mangaList = open(mlfullpath, "r").read().splitlines()
    chapters = open(cfullpath, "r").read().splitlines()
    chapterlinks = open(clfullpath, "r").read().splitlines()

    @staticmethod
    def get_manga():
        for submission in new_submissions:
            subAge = ((currentTime - submission.created_utc) / 60 / 60 / howLongAgo)
            if subAge < 1:
                allchapters.append(submission.title)
                allchapterlinks.append(submission.url)

        for x, name in enumerate(mangaList):
            for y in range(len(allchapters)):
                if (name.lower() in allchapters[y].lower()) and ("[disc]" in allchapters[y].lower()):
                    if allchapters[y].lower() not in chapters:
                        chapters.append(allchapters[y])

                    if allchapterlinks[y].lower() not in chapterlinks:
                        chapterlinks.append(allchapterlinks[y])

        if '' in chapterlinks and len(chapterlinks) > 0:
            chapterlinks.remove('')
        if '' in chapters and len(chapters) > 0:
            chapters.remove('')

        tempchapters = []
        for i in chapters:
            if i not in tempchapters:
                tempchapters.append(i)

        tempchapterlinks = []
        for i in chapterlinks:
            if i not in tempchapterlinks:
                tempchapterlinks.append(i)

        with open(cfullpath, "w") as f:
            for chapter in tempchapters:
                f.write("%s\n" % chapter)

        with open(clfullpath, "w") as f:
            for link in tempchapterlinks:
                f.write("%s\n" % link)


class CreateGUI:
    def open_url(url):
        webbrowser.open_new(url)

    @staticmethod
    def clear_display():
        windowstufflist = root.grid_slaves()
        for i, label in enumerate(windowstufflist):
            if str(label) in str(labels):
                labels.remove(str(label))
                label.destroy()

    @staticmethod
    def display_manga():
        CreateGUI.clear_display()
        GetManga.get_manga()

        mangalinksfile = open(clfullpath).read().splitlines()
        mangalistfile = open(mlfullpath).read().splitlines()
        mangachapters = open(cfullpath).read().splitlines()

        for i, url in enumerate(mangalinksfile):
            for x, name in enumerate(mangalistfile):
                if name not in mangalistfile:
                    chapters.append(mangalistfile[x])
            label = Label(root, text=str(mangachapters[i]), fg="blue", cursor="hand2")
            label.grid(row=i)
            label.bind("<Button-1>", lambda e, url=url: CreateGUI.open_url(url))
            labels.append(str(label))

        if '' in labels and len(labels) > 0:
            labels.remove('')

    @staticmethod
    def clear_actualmanga_file():
        open(cfullpath, "w").close()

    @staticmethod
    def clear_actualmangalinks_file():
        open(clfullpath, "w").close()

    @staticmethod
    def clear_mangalist_file():
        open(mlfullpath, "w").close()

    Label(root, text="Manga").grid(row=len(chapters) + 1)
    global mangaentry
    mangaentry = Entry(root)
    mangaentry.grid(row=len(chapters) + 1, column=1)

    @staticmethod
    def add_to_manga():
        mangalistfromfile = open(mlfullpath, "r").read()
        if mangaentry.get() not in mangalistfromfile:
            open(mlfullpath, "a").write(mangaentry.get() + '\n')
        else:
            print(mangaentry.get() + " already in mangaList.")


running = False


def live_updating():
    if running:
        CreateGUI.display_manga()

    root.after(1000, live_updating)


def start():
    global running
    running = True


def stop():
    global running
    running = False


Button(root, text="add", command=CreateGUI.add_to_manga).grid(row=len(chapters) + 1, column=2, sticky=W, pady=4)
Button(root, text="display", command=CreateGUI.display_manga).grid(row=len(chapters) + 2, column=1, sticky=W, pady=4)
Button(root, text="clear lookups", command=CreateGUI.clear_actualmanga_file).grid(row=len(chapters) + 2, column=2, sticky=W, pady=4)
Button(root, text="clear links", command=CreateGUI.clear_actualmangalinks_file).grid(row=len(chapters) + 3, column=2, sticky=W, pady=4)
Button(root, text="clear names", command=CreateGUI.clear_mangalist_file).grid(row=len(chapters) + 2, column=4, sticky=W, pady=4)
Button(root, text="delete display", command=CreateGUI.clear_display).grid(row=len(chapters) + 3, column=4, sticky=W, pady=4)
Button(root, text="live updater", command=start).grid(row=len(chapters) + 2, column=6, sticky=W, pady=4)
Button(root, text="stop live updater", command=stop).grid(row=len(chapters) + 3, column=6, sticky=W, pady=4)

CreateGUI.clear_actualmangalinks_file()
CreateGUI.clear_actualmanga_file()
CreateGUI()

root.after(1000, live_updating)

root.mainloop()
