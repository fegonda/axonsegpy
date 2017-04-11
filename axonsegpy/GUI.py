import tkinter as tk
import sys
import json
import sys
from tkinter import filedialog
from tkinter import Spinbox
from tkinter import Canvas
from tkinter import RIGHT
from tkinter import ttk
from PIL import Image, ImageTk
from core.readAlgoFile import readAlgo
from core.readAlgoFile import getAlgoList
from core.ConfigParser import parse
from core.modifyConfigFile import addAlgorithme


class GUI(tk.Frame):

  def __init__(self, root):
    self.photo = None
    self.filename=None
    self.configFile=("./test.json")
    tk.Frame.__init__(self, root)
    self.parametre = {}
    # define canvas
    self.w = Canvas(root, width=200, height=200, borderwidth=3, background="black")
    self.w.pack(side=RIGHT)
    self.algo={}

    # algorithms choice dropdown
    lst1 = getAlgoList()
    self.dropdownvalue = tk.StringVar()
    self.dropdownvalue.set("Please Select")
    drop = tk.OptionMenu(root,self.dropdownvalue, *lst1)
    drop.pack()

    #TODO : Create different frames for



    self.dropdownvalue.trace("w", self.callback)


    # options for buttons
    button_opt = {'fill': 'both' , 'padx': 5, 'pady': 5}

    # define buttons
    self.selectbtn = tk.Button(self, text='Select Image', command=self.askopenfilename).pack(**button_opt)
    self.runalgobtn = tk.Button(self, text='Run algo', command=self.runAlgorithm).pack(side=RIGHT, **button_opt)
    self.previewbtn = tk.Button(self, text='Preview', command=self.previewalgorithm).pack(**button_opt)



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

  def popUpAlgo(self,algo,nameAlgo):
    """
    :param algo: a list of algo
    :return:
    """
    button_opt = {'fill': 'both', 'padx': 5, 'pady': 5}
    popup=tk.Tk()
    popup.wm_title("Select your parameters")
    labelList=[]
    entryList=[]

    paramAlgo=algo[0]["params"]
    keyAlgo=list(paramAlgo.keys())
    nbrParam=len(paramAlgo)
    for i in range(nbrParam):
      labelList.append(tk.Label(popup,text=keyAlgo[i]))
      entryList.append(tk.Entry(popup))
      labelList[i].pack()
      entryList[i].pack()
    tk.Button(popup, text='Apply',command=lambda:self.appyAlgo(labelList,entryList,nameAlgo)).pack(**button_opt)
    tk.Button(popup, text='Done', command=popup.destroy).pack(**button_opt)
    popup.mainloop()


  def previewalgorithm(self):
    # Here, the algo should be run
    # in future releases, it should take the canvas image as input
    # and output it in the canvas
    pass
  def appyAlgo(self,labelList,entryList,nameAlgo):
    """
    Loads a
    :param labelList:
    :param entryList:
    :return:
    """
    for i in range(len(labelList)):
        self.parametre[labelList[i].cget("text")]=entryList[i].get()
    self.algo["name"]=nameAlgo
    self.algo["parametre"]=self.parametre
  def runAlgorithm(self):
    """
    Change configfile, launch algo
    :return:
    """
    addAlgorithme(self.configFile,"preprocessing",self.algo)
    #parse(self.configFile)


  def callback(self, *args):
    """
    Callback for our dropdown
    :param args:
    :return:
    """
    print(self.dropdownvalue.get())
    self.popUpAlgo(readAlgo(self.dropdownvalue.get()),self.dropdownvalue.get())

if __name__=='__main__':
  root = tk.Tk()
  GUI(root).pack()
  root.mainloop()