__author__ = 'Mehdi'

from Tkinter import *

BASE_X = 20
BASE_Y = 10
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 25
TEXT_WIDTH = 100
TEXT_HEIGHT = 50
COLOR_DARK_GREEN = "#0C4B33"
COLOR_LIGHT_GREEN = "#44B78B"

Version = 'prototype 0.2'

DEFAULT_FILE_TEXT = "Choose you setting file ..."


class ComparatorException(Exception):
    pass


class Application(Frame):
    """
    """

    def __init__(self, master):
        """
            initiator
        """
        Frame.__init__(self, master)
        #self.grid()
        self.pack(fill=BOTH, expand=1)
        self.create_compare_button()
        self.create_file_loaders()
        self.create_label()

    def calculate_y(self, row):
        """
        calculate the y position where to place the element
        :param row:
        :return:
        """
        return BASE_Y + (BUTTON_HEIGHT + 5) * row

    def create_compare_button(self):
        """
            create the compare settings button
        """
        self.compareButton = Button(self, text="Compare", bg=COLOR_DARK_GREEN, fg='White')
        self.compareButton["command"] = self.compare_settings
        #self.compareButton.grid(row=5, column=0, sticky=W)
        self.compareButton.place(x=BASE_X, y=self.calculate_y(3), width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.textResult = Text(self, width=TEXT_WIDTH, height=TEXT_HEIGHT, wrap=NONE)
        self.textResult.insert(0.0, 'no files to compare ....')
        #self.textResult.grid(row=6, column=0, sticky=W)
        self.textResult.place(x=BASE_X, y=self.calculate_y(4), width=BUTTON_WIDTH*5)

    def create_file_loaders(self):
        """
            create the file loaders
        """

        self.settingsFileLabel1 = Label(self, text=DEFAULT_FILE_TEXT, bg=COLOR_LIGHT_GREEN)
        #self.settingsFileLabel1.grid(row=2, column=0, sticky=W)
        self.settingsFileLabel1.place(x=BASE_X+BUTTON_WIDTH+5, y=self.calculate_y(1), width=BUTTON_WIDTH*4-5, height=BUTTON_HEIGHT)

        self.loadFileButton1 = Button(self, text="Load Settings File", bg=COLOR_DARK_GREEN, fg='White')
        self.loadFileButton1["command"] = lambda: self.load_file(1)
        #self.loadFileButton1.grid(row=1, column=0, sticky=W)
        self.loadFileButton1.place(x=BASE_X, y=self.calculate_y(1), width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

        self.settingsFileLabel2 = Label(self, text=DEFAULT_FILE_TEXT, bg=COLOR_LIGHT_GREEN)
        #self.settingsFileLabel2.grid(row=4, column=0, sticky=W)
        self.settingsFileLabel2.place(x=BASE_X+BUTTON_WIDTH+5, y=self.calculate_y(2), width=BUTTON_WIDTH*4-5, height=BUTTON_HEIGHT)

        self.loadFileButton2 = Button(self, text="Load Settings File", bg=COLOR_DARK_GREEN, fg='White')
        self.loadFileButton2["command"] = lambda: self.load_file(2)
        #self.loadFileButton2.grid(row=3, column=0, sticky=W)
        self.loadFileButton2.place(x=BASE_X, y=self.calculate_y(2), width=BUTTON_WIDTH, height=BUTTON_HEIGHT)

    def create_label(self):
        """
            create label
        """
        self.label1 = Label(self, text="Welcome to django settings utils version: %s!" % Version, bg=COLOR_LIGHT_GREEN)
        #self.label1.grid(row=0, column=0, columnspan=2, sticky=W)
        self.label1.place(x=BASE_X, y=self.calculate_y(0), width=5*BUTTON_WIDTH, height=BUTTON_HEIGHT)

    def compare_settings(self):

        fileName1= self.settingsFileLabel1['text']
        fileName2= self.settingsFileLabel2['text']
        if fileName1 == DEFAULT_FILE_TEXT or fileName2 == DEFAULT_FILE_TEXT:
            message = 'You didnt choose the files yet!!!'
        else:
            try:
                with open('settings1.py', 'w') as outfile, open(fileName1, 'r') as infile:
                    for line in infile:
                        outfile.write(line)
                with open('settings2.py', 'w') as outfile, open(fileName2, 'r') as infile:
                    for line in infile:
                        outfile.write(line)
                try:
                    from django.conf import Settings
                except:
                    raise ComparatorException('You need to have django in your python path !!!')

                try:
                    localSettings = Settings('settings1')
                    tmpSettings = Settings('settings2')
                except:
                    raise ComparatorException('An error has occured while building settings. are these setting files?')

                localSettingsDictKeys = localSettings.__dict__.keys()
                tmpSettingsDictKeys = tmpSettings.__dict__.keys()

                message = ''
                messageDifferences = ''
                for key in localSettingsDictKeys:
                    if key not in tmpSettingsDictKeys:
                        message += "the setting: %s has been found in your local settings file but not in the example file\n" % key

                for key in tmpSettingsDictKeys:
                    if key not in localSettingsDictKeys:
                        message += "the setting: %s is missing from your local settings file\n" % key
                    elif localSettings.__dict__[key] != tmpSettings.__dict__[key]:
                        messageDifferences += '\n\ndifferent values for setting %s\n' % key
                        messageDifferences += 'value for settingsfile1:\n'
                        messageDifferences += localSettings.__dict__[key].__str__()
                        messageDifferences += '\nvalue for settingsfile2:\n'
                        messageDifferences += tmpSettings.__dict__[key].__str__()


                message += '\n\n' + messageDifferences
            except ComparatorException, ex:
                message = ex.message


        self.textResult.delete("1.0",END)
        self.textResult.insert(0.0, message)

    def load_file(self, labelNo):
        from tkFileDialog import askopenfilename
        filename = askopenfilename()
        if labelNo == 1:
            self.settingsFileLabel1["text"] = filename
        if labelNo == 2:
            self.settingsFileLabel2["text"] = filename


root = Tk()

#set the general app window
root.title('DjangoSettingsUtils')
root.geometry("%dx%d" % (BUTTON_WIDTH*5+2*BASE_X, 600))


app = Application(root)

menu1 = Menu(root)

root.mainloop()
"""
root = Tk()
#set the general app window
root.title('DjangoSettingsUtils')
root.geometry("600x400")
app = Frame(root)
app.grid()
#set the app window content
#add a label
w = Label(root, text="Hello, world!")
w.pack()
#add a compare button
compareButton = Button(app, text="Compare")
compareButton.grid()
root.mainloop()
"""
