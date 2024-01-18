import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, messagebox
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import os
import Lockin_SR_class as Lockin_class
import Newport_XPS_class as DelayLine_class

class App:
    def __init__(self, root):
        #setting title
        self.root = root
        root.title("Pump probe")
        
        #setting window size
        width=1500
        height=1000
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
              
        # some variables
        self.lockin_id = 8 # set lock-in adress
        self.isStop = True #are measurements stopped?
        self.delay = {}
        self.measurement=[]        
        self.averagedMeasurement = 0
        self.scansCounter = 0
        
        x_space = 10 # horizontal space between gui elements
        y_space = 10 # vertical space between gui elements
        w_element = 130 # width of gui element
        h_element = 30 # hight of gui element
        fontsize = 12 # fontsize of gui elements
        ft = tkFont.Font(family='Times',size=fontsize)
        self.red = "#fc8d59"
        self.yellow = "#ffffbf"
        self.green = "#1a9850"
        self.blue = "#4575b4"
        
        
        StartPos_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        StartPos_Label["font"] = ft
        StartPos_Label["fg"] = "#333333"
        StartPos_Label["justify"] = "center"
        StartPos_Label["text"] = "Start position (mm)"
        StartPos_Label.place(x=x_space, y=(h_element+y_space),width=w_element,height=h_element)
        
        self.StartPos_Entry=tk.Entry(root)
        self.StartPos_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.StartPos_Entry["font"] = ft
        self.StartPos_Entry["fg"] = "#333333"
        self.StartPos_Entry["justify"] = "center"
        self.StartPos_Entry.insert(END, '100')
        self.StartPos_Entry.place(x=x_space+w_element, y=(h_element+y_space),width=w_element/2,height=h_element)
        
        NofScans_Label=tk.Label(root)
        NofScans_Label["font"] = ft
        NofScans_Label["fg"] = "#333333"
        NofScans_Label["anchor"] = "w"
        NofScans_Label["text"] = "N of scans"
        NofScans_Label.place(x=1.7*w_element, y=(h_element+y_space),width=w_element,height=h_element)
        
        self.NofScans_Entry=tk.Entry(root)
        self.NofScans_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.NofScans_Entry["font"] = ft
        self.NofScans_Entry["fg"] = "#333333"
        self.NofScans_Entry["justify"] = "center"
        self.NofScans_Entry.insert(END, '1')
        self.NofScans_Entry.place(x=2.4*w_element, y=(h_element+y_space),width=w_element/3,height=h_element)       

        EndPos_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        EndPos_Label["font"] = ft
        EndPos_Label["fg"] = "#333333"
        EndPos_Label["justify"] = "center"
        EndPos_Label["text"] = "End position (mm)"
        EndPos_Label.place(x=x_space, y=2*(h_element+y_space),width=w_element,height=h_element)

        self.EndPos_Entry=tk.Entry(root)
        self.EndPos_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.EndPos_Entry["font"] = ft
        self.EndPos_Entry["fg"] = "#333333"
        self.EndPos_Entry["justify"] = "center"
        self.EndPos_Entry.insert(END, '150')
        self.EndPos_Entry.place(x=x_space+w_element, y=2*(h_element+y_space),width=w_element/2,height=h_element)
        
        CurrScan_Label=tk.Label(root)
        CurrScan_Label["font"] = ft
        CurrScan_Label["fg"] = "#333333"
        CurrScan_Label["anchor"] = "w"
        CurrScan_Label["text"] = "Current scan"
        CurrScan_Label.place(x=1.7*w_element, y=2*(h_element+y_space),width=w_element,height=h_element)
        
        self.CurrScanN_Label=tk.Label(root)
        self.CurrScanN_Label["font"] = ft
        self.CurrScanN_Label["fg"] = "#333333"
        self.CurrScanN_Label["text"] = "0"
        self.CurrScanN_Label.place(x=2.4*w_element, y=2*(h_element+y_space),width=w_element/3,height=h_element)

        Step_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        Step_Label["font"] = ft
        Step_Label["fg"] = "#333333"
        Step_Label["justify"] = "center"
        Step_Label["text"] = "Step (mm)"
        Step_Label.place(x=x_space, y=3*(h_element+y_space),width=w_element,height=h_element)

        self.Step_Entry=tk.Entry(root)
        self.Step_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.Step_Entry["font"] = ft
        self.Step_Entry["fg"] = "#333333"
        self.Step_Entry["justify"] = "center"
        self.Step_Entry.insert(END, '10')
        self.Step_Entry.place(x=x_space+w_element, y=3*(h_element+y_space),width=w_element/2,height=h_element)
        
        NofAcc_Label=tk.Label(root)
        NofAcc_Label["font"] = ft
        NofAcc_Label["fg"] = "#333333"
        NofAcc_Label["anchor"] = "w"
        NofAcc_Label["text"] = "N of Acc"
        NofAcc_Label.place(x=1.7*w_element, y=3*(h_element+y_space),width=w_element,height=h_element)
        
        self.NofAcc_Entry=tk.Entry(root)
        self.NofAcc_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.NofAcc_Entry["font"] = ft
        self.NofAcc_Entry["fg"] = "#333333"
        self.NofAcc_Entry["justify"] = "center"
        self.NofAcc_Entry.insert(END, '1')
        self.NofAcc_Entry.place(x=2.4*w_element, y=3*(h_element+y_space),width=w_element/3,height=h_element)
        
        W8time_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        W8time_Label["font"] = ft
        W8time_Label["fg"] = "#333333"
        W8time_Label["anchor"] = "w"
        W8time_Label["text"] = "Wait time (ms)"
        W8time_Label.place(x=1.6*w_element, y=4*(h_element+y_space),width=w_element*2,height=h_element)
        
        self.W8time_Entry=tk.Entry(root)
        self.W8time_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.W8time_Entry["font"] = ft
        self.W8time_Entry["fg"] = "#333333"
        self.W8time_Entry["justify"] = "center"
        self.W8time_Entry.insert(END, '200')
        self.W8time_Entry.place(x=2.4*w_element, y=4*(h_element+y_space),width=w_element/3,height=h_element)
        
        Start_Button=tk.Button(root)
        Start_Button["bg"] = self.green        
        Start_Button["font"] = ft
        Start_Button["fg"] = "#000000"
        Start_Button["justify"] = "center"
        Start_Button["text"] = "Start"
        Start_Button.place(x=x_space, y=5*(h_element+y_space),width=w_element*0.75,height=h_element)
        Start_Button["command"] = self.Start_Button_command

        Stop_Button=tk.Button(root)
        Stop_Button["bg"] = self.red
        Stop_Button["font"] = ft
        Stop_Button["fg"] = "#000000"
        Stop_Button["justify"] = "center"
        Stop_Button["text"] = "Stop"
        Stop_Button.place(x=x_space+w_element, y=5*(h_element+y_space),width=w_element*0.75,height=h_element)
        Stop_Button["command"] = self.Stop_Button_command

        Save_Button=tk.Button(root)
        Save_Button["bg"] = self.yellow
#         ft = tkFont.Font(family='Times',size=10)
        Save_Button["font"] = ft
        Save_Button["fg"] = "#000000"
        Save_Button["justify"] = "center"
        Save_Button["text"] = "Save"
        Save_Button.place(x=x_space, y=6*(h_element+y_space),width=w_element*0.75,height=h_element)
        Save_Button["command"] = self.Save_Button_command

        #self.AutoSave_CheckBox=tk.Checkbutton(root)
        self.AutoSave_checkbox_value = tk.BooleanVar(value=False)
        self.AutoSave_CheckBox = tk.Checkbutton(root, text="AutoSave", variable=self.AutoSave_checkbox_value)
#         ft = tkFont.Font(family='Times',size=10)
        self.AutoSave_CheckBox["font"] = ft
        self.AutoSave_CheckBox["fg"] = "#333333"
        self.AutoSave_CheckBox["justify"] = "center"
#         self.AutoSave_CheckBox["text"] = "AutoSave"                       
        self.AutoSave_CheckBox.place(x=x_space+w_element, y=6*(h_element+y_space),width=w_element*0.75,height=h_element)         

        Adjust_Button=tk.Button(root)
        Adjust_Button["bg"] = "#f0f0f0"
#         ft = tkFont.Font(family='Times',size=10)
        Adjust_Button["font"] = ft
        Adjust_Button["fg"] = "#000000"
        Adjust_Button["justify"] = "center"
        Adjust_Button["text"] = "Adjast"
        Adjust_Button.place(x=2*w_element, y=6*(h_element+y_space),width=w_element*0.75,height=h_element)
        Adjust_Button["command"] = self.Adjust_Button_command

        self.LIAstatus_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        self.LIAstatus_Label["font"] = ft
        self.LIAstatus_Label["fg"] = "#333333"
        self.LIAstatus_Label["justify"] = "center"
        self.LIAstatus_Label["text"] = "Lock-in status: NOT initialized"
        self.LIAstatus_Label.place(x=x_space, y=7*(h_element+y_space),width=w_element*3,height=h_element)

        self.Delay_status_label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        self.Delay_status_label["font"] = ft
        self.Delay_status_label["fg"] = "#333333"
        self.Delay_status_label["justify"] = "center"
        self.Delay_status_label["text"] = "Delay stage status: NOT initialized"
        self.Delay_status_label.place(x=x_space, y=8*(h_element+y_space),width=w_element*3,height=h_element)
        
        bottom_shift = 22*(h_element+y_space)
        
        GoTo_Button=tk.Button(root)
        GoTo_Button["bg"] = self.green
#         ft = tkFont.Font(family='Times',size=10)
        GoTo_Button["font"] = ft
        GoTo_Button["fg"] = "#000000"
        GoTo_Button["justify"] = "center"
        GoTo_Button["text"] = "Go to"
        GoTo_Button.place(x=x_space, y=bottom_shift,width=w_element/2,height=h_element*1.5)
        GoTo_Button["command"] = self.GoTo_Button_command

        ReconnectDelay_Button=tk.Button(root)
        ReconnectDelay_Button["bg"] = self.yellow
#         ft = tkFont.Font(family='Times',size=10)
        ReconnectDelay_Button["font"] = ft
        ReconnectDelay_Button["fg"] = "#000000"
        ReconnectDelay_Button["justify"] = "center"
        ReconnectDelay_Button["text"] = "Reconnect Delay line"
        ReconnectDelay_Button.place(x=x_space+w_element/1.5, y=bottom_shift,width=w_element*1.2,height=h_element*1.5)
        ReconnectDelay_Button["command"] = self.ReconnectDelay_Button_command

        ReconnectLIA_button=tk.Button(root)
        ReconnectLIA_button["bg"] = self.yellow
#         ft = tkFont.Font(family='Times',size=10)
        ReconnectLIA_button["font"] = ft
        ReconnectLIA_button["fg"] = "#000000"
        ReconnectLIA_button["justify"] = "center"
        ReconnectLIA_button["text"] = "Reconnect LIA"
        ReconnectLIA_button.place(x=x_space+2*w_element, y=bottom_shift,width=w_element,height=h_element*1.5)
        ReconnectLIA_button["command"] = self.ReconnectLIA_button_command

        self.GoTo_Entry=tk.Entry(root)        
        self.GoTo_Entry["borderwidth"] = "1px"
        self.GoTo_Entry["font"] = ft
        self.GoTo_Entry["fg"] = "#333333"
        self.GoTo_Entry["justify"] = "center"
        self.GoTo_Entry.insert(END, '100')
        self.GoTo_Entry.place(x=x_space, y=bottom_shift+1.5*(h_element+y_space),width=w_element,height=h_element)

        mm_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        mm_Label["font"] = ft
        mm_Label["fg"] = "#333333"
        mm_Label["justify"] = "center"
        mm_Label["text"] = "mm"
        mm_Label.place(x=x_space*2+w_element, y=bottom_shift+1.5*(h_element+y_space),width=w_element/5,height=h_element)

        SelectFolder_Button=tk.Button(root)
        SelectFolder_Button["bg"] = "#f0f0f0"
#         ft = tkFont.Font(family='Times',size=10)
        SelectFolder_Button["font"] = ft
        SelectFolder_Button["fg"] = "#000000"
        SelectFolder_Button["justify"] = "center"
        SelectFolder_Button["text"] = "Select folder"
        SelectFolder_Button.place(x=2*(x_space+w_element), y=bottom_shift+1.5*(h_element+y_space),width=w_element,height=h_element)
        SelectFolder_Button["command"] = self.SelectFolder_Button_command

        self.FolderPath_Label=tk.Label(root)
#         ft = tkFont.Font(family='Times',size=10)
        self.FolderPath_Label["font"] = ft
        self.FolderPath_Label["fg"] = "#333333"
        self.FolderPath_Label["justify"] = "center"
        self.FolderPath_Label["text"] = "f:\\Data\\Nikolai Kh\\Test"
        self.FolderPath_Label.place(x=3*(x_space+w_element), y=bottom_shift+1.5*(h_element+y_space),width=w_element*3,height=h_element)

        self.FileName_Entry=tk.Entry(root)
        self.FileName_Entry["borderwidth"] = "1px"
#         ft = tkFont.Font(family='Times',size=10)
        self.FileName_Entry["font"] = ft
        self.FileName_Entry["fg"] = "#333333"
        self.FileName_Entry["justify"] = "center"
        self.FileName_Entry.insert(END, 'pump800nm_PWR8deg_L2_0deg_step0.5.dat')
        self.FileName_Entry.place(x=6*(x_space+w_element), y=bottom_shift+1.5*(h_element+y_space),width=w_element*4,height=h_element)
        
        # plots of data
        self.fig, self.ax = plt.subplots(3, 1)        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=3*w_element, y=(h_element+y_space),width=w_element*8,height=h_element*27)
        self.colors = [self.red, self.blue, self.green]
        self.labels = ['X', 'Y', 'R*sign(X)']

        self.prevMeasurements = []


    def Start_Button_command(self):
        self.isStop = False        
        
        # load the parameters of measurements      
        self.delay['start'] = float(self.StartPos_Entry.get())
        self.delay['stop'] = float(self.EndPos_Entry.get())
        self.delay['step'] = float(self.Step_Entry.get()) * np.sign(self.delay['stop'] - self.delay['start'])
        self.delay['NofScans'] = int(self.NofScans_Entry.get())
        self.delay['NofAcc'] = int(self.NofAcc_Entry.get())
        self.delay['WaitTime'] = float(self.W8time_Entry.get())     
       
        arrayoftime = np.arange(self.delay['start'], self.delay['stop']+self.delay['step'], self.delay['step'])
        averagedMeasurement = np.zeros(shape=(arrayoftime.size, 4))
        

        # N of scans over time
        for k in range(1, self.delay['NofScans'] + 1):
            self.CurrScanN_Label["text"] = k            
            self.measurement = np.zeros(shape=(arrayoftime.size, 4))

            # preparation of axes for fast redrawing
            for ax in self.ax:
                ax.clear()

            lines = {}
            lines_prev = {}
            for iaxis, axis in enumerate(self.ax):
                if len(self.prevMeasurements) > 0:
                    lines_prev[iaxis] = axis.plot(self.prevMeasurements[:, 0],
                                                  self.prevMeasurements[:, iaxis + 1], '--',
                                                  color=self.colors[iaxis],
                                                  label=self.labels[iaxis])
                    ymin = np.min(self.prevMeasurements[:, iaxis + 1])
                    ymax = np.max(self.prevMeasurements[:, iaxis + 1])
                    ymean = (ymin + ymax) / 2
                    ydelta = (abs(ymin - ymax) * 1.1) / 2
                    y_top = ymean + ydelta
                    y_bottom = ymean - ydelta
                lines[iaxis] = axis.plot(arrayoftime, averagedMeasurement[:, iaxis + 1], 'o-', color=self.colors[iaxis],
                                         label=self.labels[iaxis])
                axis.set_xlim(self.delay['start'] - self.delay['step'], self.delay['stop'] + self.delay['step'])
                axis.set_xlabel("Delay position (mm)")
                axis.set_ylabel("Lock-in signal (V)")
                # Add a title and legend
                axis.set_title(self.labels[iaxis])

            self.fig.tight_layout()
            self.canvas.draw()
            self.canvas.flush_events()

            # Let's capture the background of the figure
            backgrounds = [self.fig.canvas.copy_from_bbox(axis.bbox) for axis in self.ax]
            
        # scan over time
            for idx, pos in enumerate(arrayoftime):
                if not self.isStop:
                    self.Delay_move(pos)
                    x = 0
                    y = 0
                    r = 0
                    # avarege over N of acc at fixed time
                    for iter in range(1, self.delay['NofAcc'] + 1):
                        if iter == 1:
                            time.sleep(self.delay['WaitTime'] * 1e-3)  # pause
                        else:
                            time.sleep(0.5 * self.delay['WaitTime'] * 1e-3)  # pause
                        xi, yi, ri = self.LIA_get_xyr()  # get signal from Lock-in
                        x += xi
                        y += yi
                        r += ri * np.sign(x)
                        
                    x /= iter
                    y /= iter
                    r /= iter

                    self.measurement[idx] = [pos, x, y, r]

                    # visualization
                    for iaxis, axis in enumerate(self.ax):
                        self.fig.canvas.restore_region(backgrounds[iaxis])
                        lines[iaxis][0].set_xdata(self.measurement[0:idx+1, 0])
                        lines[iaxis][0].set_ydata(self.measurement[0:idx+1, iaxis+1])
                        # set y limits
                        ymin = np.min(self.measurement[0:idx+1, iaxis+1])
                        ymax = np.max(self.measurement[0:idx+1, iaxis+1])
                        ymean = (ymin + ymax)/2
                        ydelta = (abs(ymin - ymax)*1.1)/2
                        if len(self.prevMeasurements) > 0:
                            axis.set_ylim(min(ymean-ydelta, y_bottom), max(ymean+ydelta, y_top))
                        else:
                            axis.set_ylim(ymean - ydelta, ymean + ydelta)
                        ###################
                        axis.draw_artist(lines[iaxis][0])
                        self.fig.canvas.blit(axis.bbox) # it save the time for drawing. Info from https://stackoverflow.com/questions/40126176/fast-live-plotting-in-matplotlib-pyplot

                    # self.fig.tight_layout()
                    self.canvas.draw()
                    self.canvas.flush_events()
                    
            averagedMeasurement = averagedMeasurement + self.measurement
            self.prevMeasurements = averagedMeasurement / k
            self.prevMeasurements[:, 0] = arrayoftime
            
        self.measurement = averagedMeasurement / self.delay['NofScans']
        self.measurement[:, 0] = arrayoftime

        # visualization of averaged measurements
        for iaxis, axis in enumerate(self.ax):
            self.fig.canvas.restore_region(backgrounds[iaxis])
            lines[iaxis][0].set_xdata(self.measurement[0:idx + 1, 0])
            lines[iaxis][0].set_ydata(self.measurement[0:idx + 1, iaxis + 1])
            # set y limits
            ymin = np.min(self.measurement[0:idx + 1, iaxis + 1])
            ymax = np.max(self.measurement[0:idx + 1, iaxis + 1])
            ymean = (ymin + ymax) / 2
            ydelta = (abs(ymin - ymax) * 1.1) / 2
            axis.set_ylim(ymean - ydelta, ymean + ydelta)
            ###################
            axis.draw_artist(lines[iaxis][0])
            self.fig.canvas.blit(axis.bbox)

        # self.fig.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()
        
        if self.AutoSave_checkbox_value.get():
            self.Save_Button_command()


    def Stop_Button_command(self):
        self.isStop = True


    def Save_Button_command(self):
        #saving the data
        filename = self.FileName_Entry.get()
        folder = self.FolderPath_Label["text"]
        
        if not os.path.isdir(folder):
            messagebox.showerror("Error", "Folder does not exist!")
            return
        
        if not filename:
            messagebox.showerror("Error", "Please enter a file name")
            return

        fullname = os.path.join(folder, filename)

        if os.path.exists(fullname):            
            overwrite = messagebox.askyesno('File already exists', 'File already exists. Overwrite?')
            if overwrite:
                with open(fullname, "w") as file:
                    np.savetxt(file, self.measurement)
                    messagebox.showinfo("Save", "File saved successfully.")
        else:
            with open(fullname, "w") as file:
                np.savetxt(file, self.measurement)
                messagebox.showinfo("Save", "File saved successfully.")


    def Adjust_Button_command(self):
        print("This button does do anything")


    def GoTo_Button_command(self):
        position = float(self.GoTo_Entry.get())
        self.Delay_move(position)


    def ReconnectDelay_Button_command(self):
        controller = 'GROUP1.POSITIONER'
        self.delay_line = DelayLine_class.DelayLine(controller)
        self.curr_position = self.delay_line.get_position()
        self.Delay_status_label["text"] = "XPS delay line is connected"


    def ReconnectLIA_button_command(self):
        self.lia = Lockin_class.Lockin(self.lockin_id)
        self.LIAstatus_Label["text"] = self.lia.state
        

    def SelectFolder_Button_command(self):
        folder_path = filedialog.askdirectory()
        self.FolderPath_Label["text"] = folder_path
       
       
    def LIA_get_xyr(self):
        return self.lia.getXYR()
        
        
    def Delay_move(self, position):
        self.Delay_status_label["text"] = "XPS delay is moving"
        self.curr_position = self.delay_line.get_position()
        self.delay_line.move_to(position)
        # check the position accuracy. 5e-4 mm = 3 fs for single delay stage
        while abs(self.curr_position - position) > 0.0005:
            self.curr_position = self.delay_line.get_position()
            time.sleep(0.001)
        self.Delay_status_label["text"] = f"XPS delay is at {self.curr_position} mm"


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
