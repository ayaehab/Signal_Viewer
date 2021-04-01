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
import img_rc

class SignalViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

                #creating timers
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()

        #Connecting Buttons
        self.actionAdd_Signals.triggered.connect(lambda : self.open_file() )
        self.actionCloseAll.triggered.connect(lambda : self.clear_all())
        self.actionExit.triggered.connect(lambda: self.close())
        self.play_button.clicked.connect(lambda : self.play())
        self.stop_button.clicked.connect(lambda : self.stop())
        self.zoom_in.clicked.connect(lambda : self.zoomin())
        self.zoom_out.clicked.connect(lambda : self.zoomout())
        self.actionChannel_2.triggered.connect(lambda checked: (self.select_signal(1)))
        self.actionChannel_3.triggered.connect(lambda checked: (self.select_signal(2)))
        self.actionChannel_6.triggered.connect(lambda checked: (self.select_signal(3)))
        self.graphicsView_1.setXRange(min=0, max=10)
        self.graphicsView_2.setXRange(min=0, max=10)
        self.graphicsView_3.setXRange(min=0, max=10)

        self.pens = [pg.mkPen('r'), pg.mkPen('b'), pg.mkPen('g')]


    def clear_all(self):
        self.graphicsView_1.clear()
        self.graphicsView_2.clear()
        self.graphicsView_3.clear()



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
            data1 = pd.read_csv(path)
            self.y1= data1.values[:, 0]
            self.x1 = np.linspace(0, 0.001 * len(self.y1), len(self.y1))
        if self.file_ex == 'csv':
            data1 = pd.read_csv(path)
            self.y1 = data1.values[:, 1]
            self.x1 = data1.values[:, 0]
        self.data_line1= self.graphicsView_1.plot(self.x1, self.y1, pen=self.pens[0])
        

    def update_plot_data1(self):
        x = self.x1[:self.idx1]
        y = self.y1[:self.idx1]  
        self.idx1 +=50
        self.graphicsView_1.plotItem.setXRange(max(x, default=0)-9, max(x,default=0))        
        self.data_line1.setData(x, y) 


    def read_file2(self, file_path) :  
        path=file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex== 'txt':
            data2 = pd.read_csv(path)
            self.y2= data2.values[:, 0]
            self.x2 = np.linspace(0, 0.001 * len(self.y2), len(self.y2))
        if self.file_ex == 'csv':
            data2 = pd.read_csv(path)
            self.y2 = data2.values[:, 1]
            self.x2 = data2.values[:, 0]
        self.data_line2= self.graphicsView_2.plot(self.x2, self.y2, pen=self.pens[1])
        
    def update_plot_data2(self):
        x = self.x2[:self.idx2]
        y = self.y2[:self.idx2]  
        self.idx2 +=50
        self.graphicsView_2.plotItem.setXRange(max(x, default=0)-18, max(x,default=0))    #shrink range of x-axis     
        self.data_line2.setData(x, y)

    def read_file3(self, file_path) :  
        path=file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex== 'txt':
            data3 = pd.read_csv(path)
            self.y3= data3.values[:, 0]
            self.x3 = np.linspace(0, 0.001 * len(self.y3), len(self.y3))
        if self.file_ex == 'csv':
            data3 = pd.read_csv(path)
            self.y3 = data3.values[:, 1]
            self.x3 = data3.values[:, 0]
        self.data_line3= self.graphicsView_3.plot(self.x3, self.y3, pen=self.pens[2])
        

    def update_plot_data3(self):
        x = self.x3[:self.idx3]
        y = self.y3[:self.idx3]  
        self.idx3 +=20
        self.graphicsView_3.plotItem.setXRange(max(x, default=0)-4, max(x,default=0))  
        self.data_line3.setData(x, y) 

    def select_signal(self, signal):
        if signal == 1:
            self.actionChannel_2.setChecked(True)
            self.actionChannel_3.setChecked(False)
            self.actionChannel_6.setChecked(False)
            
        elif signal == 2:
            self.actionChannel_2.setChecked(False)
            self.actionChannel_3.setChecked(True)
            self.actionChannel_6.setChecked(False)

        elif signal == 3:
            self.actionChannel_2.setChecked(False)
            self.actionChannel_3.setChecked(False)
            self.actionChannel_6.setChecked(True)

    
    def play(self):
        if self.actionChannel_2.setChecked():
            self.idx1=0
            self.timer1.setInterval(80)
            self.timer1.timeout.connect(self.update_plot_data1)
            self.timer1.start() 
        elif self.actionChannel_3.setChecked():
            self.idx2=0
            self.timer2.setInterval(30)
            self.timer2.timeout.connect(self.update_plot_data2)
            self.timer2.start() 
        elif self.actionChannel_6.setChecked():
            self.idx3=0
            self.timer3.setInterval(30)
            self.timer3.timeout.connect(self.update_plot_data3)
            self.timer3.start() 

    def stop(self):
        if self.actionChannel_2.setChecked():
            self.timer1.stop()
        elif self.actionChannel_3.setChecked():
            self.timer2.stop()
        elif self.actionChannel_6.setChecked():
            self.timer3.stop()
            
    def zoomin(self):
        if self.actionChannel_2.setChecked():        
        self.graphicsView_1.plotItem.getViewBox().scaleBy((0.5, 0.5))
        if self.actionChannel_3.setChecked():        
        self.graphicsView_2.plotItem.getViewBox().scaleBy((0.5, 0.5))
        if self.actionChannel_6.setChecked():        
        self.graphicsView_3.plotItem.getViewBox().scaleBy((0.5, 0.5))
        

    def zoomout(self):
        if self.actionChannel_2.setChecked():
        self.graphicsView_1.plotItem.getViewBox().scaleBy((1.5, 1.5))
        if self.actionChannel_3.setChecked():
        self.graphicsView_2.plotItem.getViewBox().scaleBy((1.5, 1.5))
        if self.actionChannel_6.setChecked():
        self.graphicsView_3.plotItem.getViewBox().scaleBy((1.5, 1.5))
        


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


"""
# Scrolling Buttons

        # Channel 1
        self.right_button.clicked.connect(lambda : self.right1())
        self.left_button.clicked.connect(lambda : self.left1())
        self.up_button.clicked.connect(lambda : self.up1())
        self.down_button.clicked.connect(lambda : self.down1())
        
        # Channel 2
        self.right_button.clicked.connect(lambda : self.right2())
        self.left_button.clicked.connect(lambda : self.left2())
        self.up_button.clicked.connect(lambda : self.up2())
        self.down_button.clicked.connect(lambda : self.down2())
        
        # Channel 3
        self.right_button.clicked.connect(lambda : self.right2())
        self.left_button.clicked.connect(lambda : self.left2())
        self.up_button.clicked.connect(lambda : self.up2())
        self.down_button.clicked.connect(lambda : self.down2())
        
        
# Scrolling Functions

    # Channel 1
    
    def right1(self):
        self.graphicsView_1.getViewBox().translateBy(x=+1,y=0)

    def left1(self):
        self.graphicsView_1.getViewBox().translateBy(x=-1,y=0)

    def up1(self):
        self.graphicsView_1.getViewBox().translateBy(x=0,y=+0.5)
    
    def down1(self):
        self.graphicsView_1.getViewBox().translateBy(x=0,y=-0.5)
        
    # Channel 2
    
    def right2(self):
        self.graphicsView_2.getViewBox().translateBy(x=+1,y=0)

    def left2(self):
        self.graphicsView_2.getViewBox().translateBy(x=-1,y=0)

    def up2(self):
        self.graphicsView_2.getViewBox().translateBy(x=0,y=+0.5)
    
    def down2(self):
        self.graphicsView_2.getViewBox().translateBy(x=0,y=-0.5)
        
    # Channel 3
    
    def right3(self):
        self.graphicsView_3.getViewBox().translateBy(x=+1,y=0)

    def left3(self):
        self.graphicsView_3.getViewBox().translateBy(x=-1,y=0)

    def up3(self):
        self.graphicsView_3.getViewBox().translateBy(x=0,y=+0.5)
    
    def down3(self):
        self.graphicsView_3.getViewBox().translateBy(x=0,y=-0.5)
"""
