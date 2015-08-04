__author__ = 'Mehdi'

from Tkinter import *

TEXT_WIDTH = 100
TEXT_HEIGHT = 50

class Application(Frame):
    """
    """

    def __init__(self, master):
        """
            initiator
        """
        Frame.__init__(self, master)
        self.grid()
        self.create_compare_button()
        self.create_file_loaders()
        self.create_label()

    def create_compare_button(self):
        """
            create the compare settings button
        """
        self.compareButton = Button(self, text="Compare")
        self.compareButton["command"] = self.compare_settings
        self.compareButton.grid(row=5, column=0, sticky=W)

        self.textResult = Text(self, width=TEXT_WIDTH, height=TEXT_HEIGHT, wrap=NONE)
        self.textResult.insert(0.0, 'no files to compare ....')
        self.textResult.grid(row=6, column=0, sticky=W)

    def create_file_loaders(self):
        """
            create the file loaders
        """

        self.settingsFileLabel1 = Label(self, text="Choose you setting file ...")
        self.settingsFileLabel1.grid(row=2, column=0, sticky=W)

        self.loadFileButton1 = Button(self, text="Load Settings File")
        self.loadFileButton1["command"] = lambda: self.load_file(1)
        self.loadFileButton1.grid(row=1, column=0, sticky=W)

        self.settingsFileLabel2 = Label(self, text="Choose your setting file ...")
        self.settingsFileLabel2.grid(row=4, column=0, sticky=W)

        self.loadFileButton2 = Button(self, text="Load Settings File")
        self.loadFileButton2["command"] = lambda: self.load_file(2)
        self.loadFileButton2.grid(row=3, column=0, sticky=W)

    def create_label(self):
        """
            create label
        """
        self.label1 = Label(self, text="Hello, world!")
        self.label1.grid(row=0, column=0, columnspan=2, sticky=W)

    def compare_settings(self):
        from time import gmtime, strftime
        self.label1["text"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        with open('settings1.py', 'w') as outfile, open(self.settingsFileLabel1['text'], 'r') as infile:
            for line in infile:
                outfile.write(line)
        with open('settings2.py', 'w') as outfile, open(self.settingsFileLabel2['text'], 'r') as infile:
            for line in infile:
                outfile.write(line)

        from django.conf import Settings
        localSettings = Settings('settings1')
        tmpSettings = Settings('settings2')

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


        self.textResult.delete("1.0",END)
        self.textResult.insert(0.0, message + '\n\n' + messageDifferences)

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
root.geometry("600x400")

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
