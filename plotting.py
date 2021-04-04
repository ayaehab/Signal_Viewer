from PyQt5 import QtWidgets, uic, QtGui
from PyQt5 import QtCore
import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene
from pyqtgraph import PlotWidget, PlotItem
import pyqtgraph as pg
import os
import img_rc
from scipy import signal
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
import pyqtgraph.exporters


class SignalViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

        # creating timers
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()

        # Connecting Buttons
        self.actionAdd_Signals.triggered.connect(lambda: self.open_file())
        self.actionCloseAll.triggered.connect(lambda: self.clear_all())
        self.actionExit.triggered.connect(lambda: self.close())
        self.actionPrint_to_PDF.triggered.connect(lambda: self.export_pdf())

        self.play_button.clicked.connect(lambda: self.play())
        self.stop_button.clicked.connect(lambda: self.stop())

        self.right_button.clicked.connect(lambda: self.right())
        self.left_button.clicked.connect(lambda: self.left())
        self.up_button.clicked.connect(lambda: self.up())
        self.down_button.clicked.connect(lambda: self.down())

        self.zoom_in.clicked.connect(lambda: self.zoomin())
        self.zoom_out.clicked.connect(lambda: self.zoomout())

        self.actionChannel_1.triggered.connect(
            lambda checked: (self.select_signal(1)))
        self.actionChannel_4.triggered.connect(
            lambda checked: (self.select_signal(2)))
        self.actionChannel_5.triggered.connect(
            lambda checked: (self.select_signal(3)))
        self.graphicsView_1.setXRange(min=0, max=10)
        self.graphicsView_2.setXRange(min=0, max=10)
        self.graphicsView_3.setXRange(min=0, max=10)

        self.pens = [pg.mkPen('r'), pg.mkPen('b'), pg.mkPen('g')]

        # Content for PDF
        self.fileName = "Signal Report.pdf"
        self.documentTitle = 'Signals report'
        self.title = 'Signal Comparison'

        # Signals imgs
        self.ch1_sig_img = 'ch1_sig_img.png'
        self.ch2_sig_img = 'ch2_sig_img.png'
        self.ch3_sig_img = 'ch3_sig_img.png'
        self.ch1_spec_img = 'ch1_spec_img.png'
        self.ch2_spec_img = 'ch2_spec_img.png'
        self.ch3_spec_img = 'ch3_spec_img.png'

        #  Create document

        self.pdf = canvas.Canvas(self.fileName)
        self.pdf.setTitle(self.documentTitle)

        #  Title :: Set fonts

        self.pdf.setFont('Courier-Bold', 36)
        self.pdf.drawCentredString(300, 770, 'Signals Comparison')

        #  Sub-Title

        self.pdf.setFont('Courier-Bold', 14)
        self.pdf.drawString(200, 665, 'Signal')
        self.pdf.drawString(430, 665, 'Spectrogram')

        #  Draw all lines
        self.pdf.line(10, 650, 570, 650)
        self.pdf.line(10, 450, 570, 450)
        self.pdf.line(10, 250, 570, 250)

        self.pdf.line(110, 50, 110, 700)
        self.pdf.line(350, 50, 350, 700)

    # ###################################
    # plotting the signals
    def sigName(self, signal1, signal2, signal3):
        self.pdf.drawString(50, 550, signal1)
        self.pdf.drawString(50, 350, signal2)
        self.pdf.drawString(50, 150, signal3)

    def sigImage(self, img1, img2, img3):
        self.pdf.drawInlineImage(img1, 120, 465, width=190,
                                 height=170, preserveAspectRatio=False, showBoundary=True)
        self.pdf.drawInlineImage(img2, 120, 265, width=190,
                                 height=170, preserveAspectRatio=False, showBoundary=True)
        self.pdf.drawInlineImage(img3, 120, 65, width=190,
                                 height=170, preserveAspectRatio=False, showBoundary=True)

    def spectroImage(self, img1, img2, img3):
        self.pdf.drawInlineImage(img1, 370, 465, width=190,
                                 height=170, preserveAspectRatio=False)
        self.pdf.drawInlineImage(img2, 370, 265, width=190,
                                 height=170, preserveAspectRatio=False)
        self.pdf.drawInlineImage(img3, 370, 65, width=190,
                                 height=170, preserveAspectRatio=False)

    def export_pdf(self):
        self.sigName('ECG', 'EOG', 'EMG')
        self.sigImage(self.ch1_sig_img, self.ch2_sig_img, self.ch3_sig_img)
        self.spectroImage(self.ch1_spec_img,
                          self.ch2_spec_img, self.ch3_spec_img)

        self.pdf.save()

    def get_extention(self, s):
        for i in range(1, len(s)):
            if s[-i] == '.':
                return s[-(i - 1):]
    
    # Clear all signals function
    def clear_all(self): 
        self.graphicsView_1.clear()
        self.graphicsView_2.clear()
        self.graphicsView_3.clear()

    def open_file(self):
        self.fname1 = QtGui.QFileDialog.getOpenFileNames(
            self, 'Open only txt or CSV or xls', os.getenv('HOME'))
        # print(self.fname1)
        
        #pass the elements of list in the tuple to the read_file function
        self.read_file1(self.fname1[0][0])  
        self.read_file2(self.fname1[0][1])
        self.read_file3(self.fname1[0][2])

    def read_file1(self, file_path):
        path = file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex == 'txt':
            data1 = pd.read_csv(path)
            self.y1 = data1.values[:, 0]
            self.x1 = np.linspace(0, 0.001 * len(self.y1), len(self.y1)) #generates time values corresponding to amplitudes in y
        if self.file_ex == 'csv':
            data1 = pd.read_csv(path)
            #contain the amplitudes
            self.y1 = data1.values[:, 1]
            #containe the time values
            self.x1 = data1.values[:, 0]
        
        #plotting the signal 'static'
        self.data_line1 = self.graphicsView_1.plot(
            self.x1, self.y1, pen=self.pens[0])

        exporter = pg.exporters.ImageExporter(self.graphicsView_1.scene())
        exporter.export('ch1_sig_img.png')

        plt.specgram(self.y1, Fs=10e3)  #specgram function takes the amplitude column and sampling frequency
        plt.xlabel('Time')  
        plt.ylabel('Frequency')

        plt.savefig('ch1_spec_img.png', dpi=300, bbox_inches='tight')

    def update_plot_data1(self):
        x = self.x1[:self.idx1]
        y = self.y1[:self.idx1]
        self.idx1 += 50
        # shrink range of x-axis
        self.graphicsView_1.plotItem.setXRange(
            max(x, default=0)-9, max(x, default=0))
        # Plot the new data
        self.data_line1.setData(x, y)

    def read_file2(self, file_path):
        path = file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex == 'txt':
            data2 = pd.read_csv(path)
            self.y2 = data2.values[:, 0]
            self.x2 = np.linspace(0, 0.001 * len(self.y2), len(self.y2))
        if self.file_ex == 'csv':
            data2 = pd.read_csv(path)
            self.y2 = data2.values[:, 1]
            self.x2 = data2.values[:, 0]
        self.data_line2 = self.graphicsView_2.plot(
            self.x2, self.y2, pen=self.pens[1])

        exporter = pg.exporters.ImageExporter(self.graphicsView_2.scene())
        exporter.export('ch2_sig_img.png')

        plt.specgram(self.y2,Fs=10e3)
        plt.xlabel('Time')
        plt.ylabel('Frequency')

        plt.savefig('ch2_spec_img.png', dpi=300, bbox_inches='tight')

    def update_plot_data2(self):
        x = self.x2[:self.idx2]
        y = self.y2[:self.idx2]
        self.idx2 += 50
        self.graphicsView_2.plotItem.setXRange(
            max(x, default=0)-18, max(x, default=0))  # shrink range of x-axis
        self.data_line2.setData(x, y)

    def read_file3(self, file_path):
        path = file_path
        self.file_ex = self.get_extention(path)
        if self.file_ex == 'txt':
            data3 = pd.read_csv(path)
            self.y3 = data3.values[:, 0]
            self.x3 = np.linspace(0, 0.001 * len(self.y3), len(self.y3))
        if self.file_ex == 'csv':
            data3 = pd.read_csv(path)
            self.y3 = data3.values[:, 1]
            self.x3 = data3.values[:, 0]
        self.data_line3 = self.graphicsView_3.plot(
            self.x3, self.y3, pen=self.pens[2])

        exporter = pg.exporters.ImageExporter(self.graphicsView_3.scene())
        exporter.export('ch3_sig_img.png')

        plt.specgram(self.y3, NFFT=None, Fs=10e3, Fc=None)
        plt.xlabel('Time')
        plt.ylabel('Frequency')

        plt.savefig('ch3_spec_img.png', dpi=300, bbox_inches='tight')

    def update_plot_data3(self):
        x = self.x3[:self.idx3]
        y = self.y3[:self.idx3]
        self.idx3 += 20
        self.graphicsView_3.plotItem.setXRange(
            max(x, default=0)-4, max(x, default=0))
        self.data_line3.setData(x, y)

    # Which channel is controlled
    def select_signal(self, signal):
        if signal == 1:
            self.actionChannel_1.setChecked(True)
            self.actionChannel_4.setChecked(False)
            self.actionChannel_5.setChecked(False)

        elif signal == 2:
            self.actionChannel_1.setChecked(False)
            self.actionChannel_4.setChecked(True)
            self.actionChannel_5.setChecked(False)

        elif signal == 3:
            self.actionChannel_1.setChecked(False)
            self.actionChannel_4.setChecked(False)
            self.actionChannel_5.setChecked(True)

    # Play function connected to play button based on which channel is controlled
    def play(self):
        if self.actionChannel_1.isChecked():
            self.idx1 = 0
            self.timer1.setInterval(80)
            self.timer1.timeout.connect(self.update_plot_data1)
            self.timer1.start()

        if self.actionChannel_4.isChecked():
            self.idx2 = 0
            self.timer2.setInterval(30)
            self.timer2.timeout.connect(self.update_plot_data2)
            self.timer2.start()

        if self.actionChannel_5.isChecked():
            self.idx3 = 0
            self.timer3.setInterval(30)
            self.timer3.timeout.connect(self.update_plot_data3)
            self.timer3.start()

    # Stop function connected to Stop button based on which channel is controlled
    def stop(self):
        if self.actionChannel_1.isChecked():
            self.timer1.stop()

        if self.actionChannel_4.isChecked():
            self.timer2.stop()

        if self.actionChannel_5.isChecked():
            self.timer3.stop()

    # Zoomin function connected to Zoomin button based on which channel is controlled
    def zoomin(self):
        if self.actionChannel_1.isChecked():
            self.graphicsView_1.plotItem.getViewBox().scaleBy((0.5, 0.5))

        if self.actionChannel_4.isChecked():
            self.graphicsView_2.plotItem.getViewBox().scaleBy((0.5, 0.5))

        if self.actionChannel_5.isChecked():
            self.graphicsView_3.plotItem.getViewBox().scaleBy((0.5, 0.5))

    # Zoomout function connected to zoomout button based on which channel is controlled
    def zoomout(self):
        if self.actionChannel_1.isChecked():
            self.graphicsView_1.plotItem.getViewBox().scaleBy((1.5, 1.5))

        if self.actionChannel_4.isChecked():
            self.graphicsView_2.plotItem.getViewBox().scaleBy((1.5, 1.5))

        if self.actionChannel_5.isChecked():
            self.graphicsView_3.plotItem.getViewBox().scaleBy((1.5, 1.5))

    def right(self):
        if self.actionChannel_1.isChecked():
            self.graphicsView_1.getViewBox().translateBy(x=+1, y=0)

        if self.actionChannel_4.isChecked():
            self.graphicsView_2.getViewBox().translateBy(x=+1, y=0)

        if self.actionChannel_5.isChecked():
            self.graphicsView_3.getViewBox().translateBy(x=+1, y=0)

    def left(self):
        if self.actionChannel_1.isChecked():
            self.graphicsView_1.getViewBox().translateBy(x=-1, y=0)

        if self.actionChannel_4.isChecked():
            self.graphicsView_2.getViewBox().translateBy(x=-1, y=0)

        if self.actionChannel_5.isChecked():
            self.graphicsView_3.getViewBox().translateBy(x=-1, y=0)

    def up(self):
        if self.actionChannel_1.isChecked():
            self.graphicsView_1.getViewBox().translateBy(x=0, y=+0.5)

        if self.actionChannel_4.isChecked():
            self.graphicsView_2.getViewBox().translateBy(x=0, y=+0.5)

        if self.actionChannel_5.isChecked():
            self.graphicsView_3.getViewBox().translateBy(x=0, y=+0.5)

    def down(self):
        if self.actionChannel_1.isChecked():
            self.graphicsView_1.getViewBox().translateBy(x=0, y=-0.5)

        if self.actionChannel_4.isChecked():
            self.graphicsView_2.getViewBox().translateBy(x=0, y=-0.5)

        if self.actionChannel_5.isChecked():
            self.graphicsView_3.getViewBox().translateBy(x=0, y=-0.5)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = SignalViewer()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
