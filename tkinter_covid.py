# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:31:30 2022

@author: Seyedmostafa Musavi
"""
import csv
import re
import datetime
from tkinter import *
import tkinter as tk 
import mplcursors
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)################################# Better Resolution
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


############################################################################### 
'''
def show_kreise(e):
    global bundesland_id
    # curselection function returns index of selected listbox item 
    # it returns a tuple, that the first item of tuple is item index
    #                                  (0,)
    bundesland_id = listbox_bundesland.curselection()[0] + 1
    listbox_kreis.delete(0,END) # everytime we must clear the listbox  
    
    for item in kreis: 
        # index [   0           1         2 ]
        # item  ['1001', 'SK Flensburg', '1']
        # kreis [KreisID ; Kreis Name ; BundeslandID]
        # bundesland_id is the index of selected bundesland from the list box 
        if int(item[2]) == bundesland_id:
                          #['1001', 'SK Flensburg', '1']
                          # item[1] = 'SK Flensburg'
                          # item[1][3:] = Flensburg
            listbox_kreis.insert(END, item[1][3:])
'''       
###############################################################################
def get_kreis_index(e):
        
    global kreis_name,kreis_id,bundesland_id

        # the get() function returns value of selected  item
        # it takes selected item from the list and return the value
        
        # here will be check if the value of selected item
        # is equal to value of kreis name
        #         listbox      i[0]       i[1]       i[2]
        # id=2 'Flensburg' == ['1001', 'SK Flensburg', '1']

    for i in kreis:                     
            #      Flensburg                      i= ['1001', 'SK Flensburg', '1']
            #                                                 i[1] = SK Flensburg
            #                              #(index,)          i[1][3:] = Flensburg  
        if listbox_kreis.get(listbox_kreis.curselection()[0]) == i[1][3:]:
            kreis_id = i[0] # 1001
            kreis_name = i[1] # SK Flensburg
                                #          0
                               # [['1', 'Schleswig-Holstein'].....]
            bundesland_id = int(bundesland[int(i[2])-1][0])
            break
def show_kreise(e):
    global bundesland_id
    selection = listbox_bundesland.curselection()
    if not selection:
        return  # No item is selected
    bundesland_id = selection[0] + 1
    listbox_kreis.delete(0, END)  # Clear the listbox
    
    for item in kreis:
        if int(item[2]) == bundesland_id:
            listbox_kreis.insert(END, item[1][3:])

############################################################################### 
def covid_statistik(check) :
    fig = Figure(figsize=(14,7),facecolor='#EEEBDD')
    ax = fig.add_subplot(1,1,1)
    ax.ticklabel_format(useOffset=False, style='plain')
    if check == 1:
        d = []
        b = []
        k = []
        with open('RKI_History.csv',newline='') as csv_history:
            file_reader = csv.reader(csv_history,delimiter =',')
            #headrow = next(file_reader) 
            for row in file_reader:
                if row[0] == '0':             
                    d.append([row[2].split(' ')[0],row[7]]) 
                if int(row[0]) == bundesland_id: 
                    b.append([row[2].split(' ')[0],row[7]])
                if  row[0] == kreis_id: 
                    k.append([row[2].split(' ')[0],row[7]])
            d = sorted(d)
            b = sorted(b)
            k = sorted(k)
###############################################################################
        d_x=[datetime.datetime.strptime(item[0],'%Y/%m/%d').date() for item in d]
        d_y=[int(item[1]) for item in d]
        b_x=[datetime.datetime.strptime(item[0],'%Y/%m/%d').date() for item in b]
        b_y=[int(item[1]) for item in b]
        k_x=[datetime.datetime.strptime(item[0],'%Y/%m/%d').date() for item in k]
        k_y=[int(item[1]) for item in k]
###############################################################################
        
        line1, = ax.plot(d_x,d_y) # for legend the axis must be assign to tuple  
        line2, = ax.plot(b_x,b_y)
        line3, = ax.plot(k_x,k_y)  
        
###############################################################################
        
        ax.set_xlabel('Datum',
                      color='#FF8C32',
                      fontsize=13,
                      weight='bold')
        ax.set_ylabel('Gemeldete Fälle',
                      color='#06113C',
                      fontsize=13,
                      weight='bold')
        fig.legend((line1,line2,line3),(f'Deutschland : {d_y[-1]}',
                                        f'{bundesland[bundesland_id-1][1]} : {b_y[-1]}',
                                        f'{kreis_name} : {k_y[-1]}'),
                                         'upper center',
                                         fontsize=12)
    mplcursors.cursor(ax)     
    ax.grid() 
###          
    canvas = FigureCanvasTkAgg(fig,window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=1,rowspan=5)
    # Here are 2 solutions, that we can use grid for NavigationToolbar
    # 1. we use a Frame as container then we can use grid of Frame to display Toolbar 
    # 2. by definition of Toolbar, we must disable pack_toolbar=False   
    # toolbarFrame = Frame(window)
    # toolbarFrame.grid(row=5,column=1,padx=200,sticky=(W,S))
    # toolbar = NavigationToolbar2Tk(canvas,toolbarFrame)
    toolbar = NavigationToolbar2Tk(canvas,
                                   window,
                                   pack_toolbar=False)
    toolbar.config(bg='#EEEBDD', cursor='hand2')
    toolbar.grid(row=5,column=1, padx=200,sticky=(W,S))
    
    
    for i,child in enumerate(toolbar.winfo_children()):
        if 3<i<6:
            child.config(background='#EEEBDD',bd=0)
        if 8<i<11:
            child.config(background='#EEEBDD',
                         foreground='#F4976C',
                         font=('Arial',13,'bold'))
        child.config(background='#EEEBDD',relief=FLAT)



############################################################################### import bunesland 
############################################################################### and Kreise data
bundesland = []
kreis = []
with open('RKI_AdmUnit.csv',encoding='utf-8') as csv_adm:
    file_reader_Adm = csv.reader(csv_adm,delimiter =',')
    headrow = next(file_reader_Adm)
    for row in file_reader_Adm:
        if 0 < int(row[0]) < 17 :       
            bundesland.append([row[0],row[1]]) 
        elif int(row[0]) > 16 :  #  1001 , sk kiel =>    1     
            kreis.append([row[0],row[1],bundesland[(int(row[0])//1000)-1][0]])

############################################################################### App GUI
window = Tk() # to begin with we should make a tk object
window.config(bg='#EEEBDD') # app bgcolor
width = window.winfo_screenwidth()   # Adjust as needed
height = window.winfo_screenheight()  # screen height
window.geometry(f'{height}x{width}') # app window default size by running
window.title('Covid-Fälle in Deutschland') # app title
covid_statistik(0) 


############################################################################### label bundesländer
lb_label = Label(window,
                 text='Bundesland',
                 width=15,
                 bg='#EEEBDD',
                 fg='#303c6c', #'Brush Script MT'
                 font=('Lucida Sans',14,'bold')).grid(row=0,
                                                      column=0,
                                                      padx=40,
                                                      pady=10,
                                                      sticky=W)

############################################################################### listbox Bundesländer
listbox_bundesland = Listbox(window,
                             activestyle='none',
                             height=16,
                             width=30,
                             bg='#EEEBDD',
                             relief='flat',
                             fg='#564f6f',
                             cursor='hand2',
                             highlightbackground='#303c6c',#564f6f
                             selectbackground = '#303c6c',#F4976C
                             selectforeground = '#F4976C',
                             font=('Consolas',10))

listbox_bundesland.grid(row=1,column=0,padx=25,sticky=W)

for element in bundesland: # [bundesId,bundesName]
    listbox_bundesland.insert(END,element[1]) # bundesland liste initialize 

############################################################################### label search

sl = Label(window,
           text='Suchen',
           width=15,
           bg='#EEEBDD',
           fg='#303c6c',# #F4976C
           font=('Lucida Sans',14,'bold')).grid(row=2,
                                                column=0,
                                                pady=5,
                                                padx=35,
                                                sticky=N)

############################################################################### search entry 

def callback(*args):#
    x = user_input.get().upper()
    listbox_kreis.delete(0,END)
    for item in kreis:
        if re.match(f'^{x}',item[1][3:].upper()):
            listbox_kreis.insert(END, item[1][3:])
user_input = StringVar()
entry = Entry(window,
              textvariable=user_input,
              width=30,
              bg='#F4976C',#F4976C #303c6c
              insertbackground='#303c6c',
              relief='flat',
              fg='#ffffff',
              font=('Consolas',10,'bold'))
entry.grid(row=3,column=0)
user_input.trace('w',callback)
user_input.trace_add("write", callback)
entry.config(validate='key',validatecommand=callback)


############################################################################### label kreise
lb_label = Label(window,
                 text='Kreis',
                 width=15,
                 bg='#EEEBDD',
                 fg='#303c6c',# #F4976C
                 font=('Lucida Sans',14,'bold')).grid(row=4,
                                                      column=0,
                                                      padx=43,
                                                      pady=(20,0),
                                                      sticky=W)

############################################################################### list box kreise
listbox_kreis = Listbox(window,
                        activestyle='none',
                        height=19,
                        width=30,
                        bg='#EEEBDD',
                        relief='flat',
                        fg='#4c495d',
                        cursor='hand2',
                        highlightbackground='#564f6f',
                        selectbackground = '#303c6c',#F4976C
                        selectforeground = '#F4976C',
                        font=('Consolas',10))
listbox_kreis.grid(row=5,column=0,pady=5,padx=25,sticky=W)

############################################################################### scrollbar for listbox kreise

sb = Scrollbar(window,orient=VERTICAL)
sb.grid(row=5,column=0,sticky=(NE,SE),padx=26,pady=6)
listbox_kreis.config(yscrollcommand=sb.set)
sb.config(command=listbox_kreis.yview)
############################################################################### list select event
 # to get list selected item , we use bind function and ListboxSelect event
 # to initialize listbox kreis, we need the listbox bundesland selected item 
 

listbox_bundesland.bind('<<ListboxSelect>>',show_kreise)
listbox_kreis.bind('<<ListboxSelect>>',get_kreis_index)

############################################################################### quit button
def enter_btn_close(e):
    btn_close['bg']='#F4976C'
def leave_btn_close(e):
    btn_close['bg']='#303c6c'
btn_close = Button(window,
                   text='Beenden',
                   bg='#303c6c',
                   fg='#ffffff',
                   relief='flat',
                   cursor='hand2',
                   width=10,
                   font=('Helvetica',10,'bold'),
                   command=window.destroy)
btn_close.grid(row=6,column=0,pady=6,padx=25,sticky=NE)
btn_close.bind('<Enter>',enter_btn_close)# mouse hover event
btn_close.bind('<Leave>',leave_btn_close)# mouse leave event 
############################################################################### Start button
def enter_btn_start(e):
    btn_start['bg']='#F4976C'
def leave_btn_start(e):
    btn_start['bg']='#303c6c'

btn_start = Button(window,
                   text='Anzeigen',
                   bg='#303c6c',
                   fg='#ffffff',
                   relief='flat',
                   cursor='hand2',
                   width=10,
                   font=('Helvetica',10,'bold'),
                   command=lambda:covid_statistik(1))
btn_start.grid(row=6,column=0,pady=6,sticky=NW,padx=25)

btn_start.bind('<Enter>',enter_btn_start)# mouse hover event 
btn_start.bind('<Leave>',leave_btn_start)# mouse leave event 


window.mainloop() # this function is finite loop to run the program 