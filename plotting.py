from PyQt5 import QtWidgets, uic, QtGui
from PyQt5 import QtCore
import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
import pyedflib
import math
from pyqtgraph import PlotWidget ,PlotItem
import pyqtgraph as pg 
import os 
import pathlib
import random


class SignalViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

                #creating timers
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()

        #Connecting Buttons
        self.actionchannel_1.triggered.connect(lambda : self.open_file() )
        self.play_button.clicked.connect(lambda : self.play1())
        self.stop_button.clicked.connect(lambda : self.stop1())
        self.down_button.clicked.connect(lambda : self.resume1())
        self.graphicsView_1.setXRange(min=0, max=10)
        self.graphicsView_2.setXRange(min=0, max=10)
        self.graphicsView_3.setXRange(min=0, max=10)

        self.pens = [pg.mkPen('r'), pg.mkPen('b'), pg.mkPen('g')]

    def open_file(self):
        self.fname1 = QtGui.QFileDialog.getOpenFileNames( self, 'Open only txt or CSV or xls', os.getenv('HOME') )
        print(self.fname1)
        self.read_file1(self.fname1[0][0])
        self.read_file2(self.fname1[0][1])
        self.read_file3(self.fname1[0][2])

      
        

    def read_file1(self, file_path) :  
        path=file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex== 'txt':
            data = pd.read_csv(path)
            self.y1= data.values[:, 0]
            self.x1 = np.linspace(0, 0.001 * len(self.y1), len(self.y1))
        if self.file_ex == 'csv':
            data = pd.read_csv(path)
            self.y1 = data.values[:, 1]
            self.x1 = data.values[:, 0]

        # initializing signal
        self.pen = pg.mkPen(color=(0,160, 0))
        self.data_line1= self.graphicsView_1.plot(self.x1, self.y1, pen=self.pens[0])
        
    def play1(self):
        self.idx1=0
        self.timer1.setInterval(30)
        self.timer1.timeout.connect(self.update_plot_data3)
        self.timer1.start() 
    
    def stop1(self):
        self.timer1.stop()
    
    def resume1(self):
        self.timer1.start()

    def update_plot_data1(self):
        x = self.x1[:self.idx1]
        y = self.y1[:self.idx1]  
        self.idx1 +=80
        if self.idx1 > len(self.x1) :
            self.idx1 = 0 
        
        if  self.x1[self.idx1] >0.5:
            self.graphicsView_1.setLimits(xMin =-0.6, xMax=max(x, default=0)) #disable paning over xlimits
        self.graphicsView_1.plotItem.setXRange(max(x, default=0)-3, max(x,default=0))        

        self.data_line1.setData(x, y) 
  
    def read_file2(self, file_path) :  
        path=file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex== 'txt':
            data = pd.read_csv(path)
            self.y1= data.values[:, 0]
            self.x1 = np.linspace(0, 0.001 * len(self.y1), len(self.y1))
        if self.file_ex == 'csv':
            data = pd.read_csv(path)
            self.y1 = data.values[:, 1]
            self.x1 = data.values[:, 0]

        # initializing signal
        self.pen = pg.mkPen(color=(0,160, 0))
        self.data_line1= self.graphicsView_2.plot(self.x1, self.y1, pen=self.pens[1])
        

    def play2(self):
        self.idx1=0
        self.timer1.setInterval(30)

        self.timer1.timeout.connect(self.update_plot_data2)
        self.timer1.start() 

    def update_plot_data2(self):
        x = self.x1[:self.idx1]
        y = self.y1[:self.idx1]  
        self.idx1 +=50
        if self.idx1 > len(self.x1) :
            self.idx1 = 0 
        
        if  self.x1[self.idx1] > 0.5:
            self.graphicsView_2.setLimits(xMin =-0.6, xMax=max(x, default=0)) #disable paning over xlimits
        self.graphicsView_2.plotItem.setXRange(max(x, default=0)-3, max(x,default=0))        

        self.data_line1.setData(x, y)

    def read_file3(self, file_path) :  
        path=file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex== 'txt':
            data = pd.read_csv(path)
            self.y1= data.values[:, 0]
            self.x1 = np.linspace(0, 0.001 * len(self.y1), len(self.y1))
        if self.file_ex == 'csv':
            data = pd.read_csv(path)
            self.y1 = data.values[:, 1]
            self.x1 = data.values[:, 0]

        # initializing signal
        self.pen = pg.mkPen(color=(0,160, 0))
        self.data_line1= self.graphicsView_3.plot(self.x1, self.y1, pen=self.pens[2])
        

    def play3(self):
        self.idx1=0
        self.timer1.setInterval(30)

        self.timer1.timeout.connect(self.update_plot_data3)
        self.timer1.start() 

    def update_plot_data3(self):
        x = self.x1[:self.idx1]
        y = self.y1[:self.idx1]  
        self.idx1 +=5
        if self.idx1 > len(self.x1) :
            self.idx1 = 0 
        
        if  self.x1[self.idx1] > 0.5:
            self.graphicsView_3.setLimits(xMin =-0.2, xMax=max(x, default=0)) #disable paning over xlimits
        self.graphicsView_3.plotItem.setXRange(max(x, default=0)-4, max(x,default=0))        

        self.data_line1.setData(x, y) 


    def get_extention(self, s):
        for i in range(1, len(s)):
            if s[-i] == '.':
                return s[-(i - 1):]


        


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = SignalViewer()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()