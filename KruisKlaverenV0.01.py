import tkinter as tk
import sys
import logging
from logger import MyLogger
from math import ceil

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger("SYSTEM_OUTPUT", logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger("SYSTEM_ERROR", logging.ERROR)


def colorPicker(min,max,value):
  values=[256,154,100]
  #bepaal welk kwintiel
  kwintiel=ceil(5*value/(max-min+1))
  tussenwaarde=(value/(kwintiel*(max-min+1)/5))-1
  startKleur=100
  eindKleur=256
  kleur=int(tussenwaarde*(eindKleur-startKleur))
  print("kleurkiezer: {}: kwintiel: {} - {} : {}".format(value,kwintiel,tussenwaarde,kleur))

  return ["#ff9a9a","#ff6464"]


class MainApp(tk.Tk):
  def __init__(self):
    self.root = tk.Tk.__init__(self)
    self.keuzes=KeuzeFrame(self, side=tk.TOP)
    self.tafels=Tafels(self, side=tk.LEFT)

  def reset(self,nieuwKeuze):
   self.tafels.set(nieuwKeuze)


class KeuzeFrame(tk.Frame):
  def __init__(self,parent,*args,**kwargs):
    tk.Frame.__init__(self,parent)
    self.pack(kwargs)
    self.parent=parent
    self.keuze=tk.IntVar()
    self.keuzeArray=[4,5,6,7,8]
    self.keuzeMenu=tk.OptionMenu(self,self.keuze,*self.keuzeArray,command=self.parent.reset)
    self.keuzeMenu.pack()


class Tafels(list):
  def __init__(self,parent,*args,**kwargs):
    self.frame=tk.LabelFrame(parent,text="Tafels")
    self.frame.pack(kwargs)
    self.parent=parent
    self.rondeLabel=tk.Label(self.frame,text="ronde:")
    self.rondeLabel.grid(column=0,row=0)
    self.rondenummers=[]

  def set(self,numTafels):
    for tafel in self:
      tafel.reset()
    self.clear()
    for rondenummer in self.rondenummers:
      rondenummer.destroy()
    self.rondenummers=[]
    if numTafels:
      rondes=int((int(numTafels)*4-1)/3)
      for x in range(rondes):
        self.rondenummers.append(tk.Label(self.frame,text="{}".format(x+1)))
        self.rondenummers[-1].grid(row=x+1,column=0)
      for x in range(int(numTafels)):
         self.append(Tafel(self.frame,numTafels,x,rondes))


class Tafel(list):
  def __init__(self,parent,numTafels,tafelNummer,rondes):
    self.label=tk.Label(parent, text="Tafel {}".format(tafelNummer+1))
    self.label.grid(row=0,column=int(1+tafelNummer*4),padx=(25,0))
    for rondeNummer in range(rondes):
      self.append(Ronde(parent,numTafels,tafelNummer,rondeNummer,self.update))

  def reset(self):
    for ronde in self:
      ronde.reset()
    self.clear()
    self.label.destroy()

  def update(self):
    print("update Tafel")

class Ronde(list):
  def __init__(self,parent,numTafels,tafelNummer,rondeNummer,call_update):
    self.parent=parent
    self.tafelNummer=tafelNummer
    self.call_update=call_update
    self.optiesFrame=tk.Frame(self.parent,highlightbackground="black",highlightthickness=1)
    self.optiesFrame.grid(row=rondeNummer+1,column=1 + tafelNummer*4,columnspan=4)
    self.opties=[]
    for y in range(4):
      for x in range(numTafels):
        value=y*numTafels+x+1
        self.opties.append(Optie(self.optiesFrame,numTafels*4,value,self.update))

  def reset(self):
    for optie in self.opties:
      optie.reset()
    self.optiesFrame.destroy()

  def update(self):
    count=0
    for optie in self.opties:
      if optie.active and optie.chosen:
        count+=1
    print("update ronde: {}".format(count))


class Optie:
  def __init__(self,parent,numSpelers,value,call_update):
    self.parent=parent
    self.value=value
    self.call_update=call_update
    self.chosen=False
    self.active=True
    self.total=numSpelers
    self.colors=colorPicker(1,numSpelers,value)
    self.build()
    self.show()

  def build(self):
    if self.active:
      textsize='6' if (self.total>=7) else '9'
      if self.chosen:
        self.widget=tk.Label(self.parent,bg=self.colors[1],bd=1,font=('Helvetica', textsize),text="{}".format(self.value))
      else:
        self.widget=tk.Button(self.parent,bg=self.colors[0],bd=1,font=('Helvetica', textsize),text="{}".format(self.value),command=self.kiesOptie)

  def reset(self):
    if self.active:
      self.widget.destroy()

  def show(self):
    yMax=int(self.total/4)+1 if (self.total<=12) else 4
    xMax=int((self.total-self.total%yMax)/yMax)
    x=int((self.value-1)%xMax)
    y=int((self.value-1)/xMax)
    self.widget.grid(row=y,column=x,sticky='NESW')

  def setTotal(self, total):
    self.total=total
    self.widget.destroy()
    self.show()

  def disable(self):
    self.active=False
    self.widget.destroy()

  def kiesOptie(self,*args):
    print("kies optie: {}".format(self.value))
    self.chosen=True
    self.widget.destroy()
    self.build()
    self.show()
    self.call_update()


if __name__ == "__main__":
  app = MainApp()
  app.mainloop()
