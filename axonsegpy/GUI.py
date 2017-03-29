import tkinter as tk
import json
import sys
from tkinter import filedialog
from tkinter import Spinbox
from tkinter import Canvas
from tkinter import RIGHT
from PIL import Image, ImageTk

from core.ConfigParser import parse


class TkFileDialogExample(tk.Frame):

  def __init__(self, root):
    self.photo = None
    self.filename=None
    self.configFile=("./test.json")
    tk.Frame.__init__(self, root)

    # define canvas
    self.w = Canvas(root, width=200, height=200, borderwidth=3, background="black")
    self.w.pack(side=RIGHT)


    # algorithms choice dropdown
    lst1 = ['Extendedminima','Myelin','Algo 3']
    var1 = tk.StringVar()
    var1.set("Extendedminima")
    drop = tk.OptionMenu(root,var1, *lst1)
    drop.pack()

    # options for buttons
    button_opt = {'fill': 'both' , 'padx': 5, 'pady': 5}

    # define buttons
    self.selectbtn = tk.Button(self, text='Select Image', command=self.askopenfilename).pack(**button_opt)
    self.runalgobtn = tk.Button(self, text='Run algo', command=self.runalgorithm).pack(side=RIGHT, **button_opt)
    self.previewbtn = tk.Button(self, text='Preview', command=self.previewalgorithm).pack(**button_opt)


    # define spinbox
    s = Spinbox(root, from_=0, to=10)
    s.pack()


    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.PNG'
    options['filetypes'] = [('all files', '.*'), ('PNG file', '.png'), ('TIFF file', '.tiff')]
    options['initialdir'] = '.'
    options['initialfile'] = ''
    options['parent'] = root
    options['title'] = 'Please select an image'

    # This is only available on the Macintosh, and only when Navigation Services are installed.
    #options['message'] = 'message'

    # if you use the multiple file version of the module functions this option is set automatically.
    #options['multiple'] = 1

  def askopenfilename(self):
    """Returns an opened file in read mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """

    # get filename
    self.filename = filedialog.askopenfilename(**self.file_opt)

    # Code below should put the image in the canvas
    if self.filename:
      # TODO : get only the filename from the path
      image = Image.open(0, self.filename)
      photo = ImageTk.PhotoImage(image)
      #self.w.create_image(photo)

  def previewalgorithm(self):
    # Here, the algo should be run
    # in future releases, it should take the canvas image as input
    # and output it in the canvas
    pass

  def runalgorithm(self):
    # Here, the algo should be run
    # in future releases, it should take the canvas image as input
    # and output it in the canvas
    #TODO: Call modifyConfigFile
    parse(self.configFile)

if __name__=='__main__':
  root = tk.Tk()
  TkFileDialogExample(root).pack()
  root.mainloop()