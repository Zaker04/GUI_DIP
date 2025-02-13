# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:40:23 2019

@author: turtw
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 20:11:52 2019

@author: turtw
"""

from PIL import Image
from pylab import *
#from drawnow import drawnow,figure
#from skimage import data,io,morphology
from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import (QAction, qApp, QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QInputDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QMessageBox, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from Libreria import MyLib
from os import getcwd,sep
#********************************************************************
import sys
import numpy as np
import matplotlib.pyplot as mpl
import cv2
#import cv2 as cv
#********************************************************************
'''GUI ImageProcesing'''
class Guimagenology(QMainWindow):
    def __init__(self, parent=None):
        super(Guimagenology, self).__init__(parent)             #'Permite Iniciar GUI'
        self.originalPalette = QApplication.palette()           #'Estilo de la GUI'
        self.setWindowTitle("Imagenologia GUI")                 #'Nombre de la Ventana (Aplicacion)'
        self.setGeometry(200, 150, 600, 400)                    #'Tamaño y posicion'
        self.setWindowIcon(QtGui.QIcon('pokeball.png'))         #'Icono de la APP'
        self.initUI()
        self.Widgett = WidgetG(self)
        self.setCentralWidget(self.Widgett)
        self.setStyleSheet("""QToolTip { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")
    #************************************************************
    '''Barra de Menu'''
    def initUI(self):
        '''Salir Aplicacion'''
        exitAction = QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)
        
        '''Ayuda'''
        helpAction = QAction(QtGui.QIcon('pokeball.png'), '&Info', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip('Created By Max Campos &'
                                ' Maya Rogina')
        
        StatusBar = self.statusBar()
        MenuBar = self.menuBar()
        FileMenu = MenuBar.addMenu('&File')
        EditMenu = MenuBar.addMenu('Aprobar')
        ViewMenu = MenuBar.addMenu('View')
        SearchMenu = MenuBar.addMenu('Search')
        ToolsMenu = MenuBar.addMenu('Tools')
        HelpMenu = MenuBar.addMenu('&Help')
        StatusBar.showMessage('UPIITA IPN 2019')
        #************************************************************
        '''Acciones del menu'''
        FileMenu.addAction(exitAction)
        HelpMenu.addAction(helpAction)
        self.show()
class WidgetG(QWidget):
    def __init__(self,parent):
        super(WidgetG, self).__init__(parent)             #'Permite Iniciar GUI'   
        self.originalPalette = QApplication.palette()           #'Estilo de la GUI'
        #************************************************************
        '''Barra de Operaciones'''
        styleComboBox = QComboBox()                             #'Crea la ventanta donde iran todos los objetos'
        styleComboBox.addItems({"Amibas","Binarizacion","BinarizaGauss","Correccion","Ecualizacion","Gamma","GrayScale","HighBoost","Histograma","Otsu","Umbralizar"})
        styleComboBox.activated[str].connect(self.Operaciones)
        styleLabel = QLabel("&Operacion:")
        styleLabel.setBuddy(styleComboBox)
        styleComboBox.setToolTip("Select a Filter to Apply")
        #************************************************************
        '''Apertura de la Imagen'''
        Open_Image = QPushButton("Open Image")
        Open_Image.setDefault(True)
        Open_Image.clicked.connect(self.OpenFile)
        Open_Image.setToolTip("Click to Open an Image File")
        #************************************************************
        '''TakeSnap'''
        Take_Image = QPushButton("Take Snap")
        Take_Image.setDefault(True)
        Take_Image.clicked.connect(self.TakePhoto)
        Take_Image.setToolTip("Click to Take a Photo (Snap Key e)")
        #************************************************************
        '''Imagenes Prueba'''
        PruebaComboBox = QComboBox()                             #'Crea la ventanta donde iran todos los objetos'
        PruebaComboBox.addItems({"astronaut","camera","chelsea","coffee","coins","horse","ihc","lenna","moon","phantom","retina","rocket"})
        PruebaComboBox.activated[str].connect(self.Tester)
        PruebaLabel = QLabel("&Imagenes. \n    Prueba·")
        PruebaLabel.setBuddy(PruebaComboBox)
        PruebaComboBox.setToolTip("Select an Image")
        #************************************************************
        '''Axis'''
        self.Axis = QLabel()
        self.Axis1 = QLabel()
        self.Axis2 = QLabel()
        #************************************************************
        '''Partes'''
        topLayout = QHBoxLayout()
        topLayout.addWidget(Take_Image,100,Qt.AlignLeft)
#        topLayout.addStretch(1)
        topLayout.addWidget(Open_Image,50,Qt.AlignCenter)
#        topLayout.addStretch(1)
        topLayout.addWidget(PruebaLabel,60,Qt.AlignRight)                         #Agrega los elementos a pantalla
        topLayout.addWidget(PruebaComboBox,60,Qt.AlignLeft)
        #
        topLayout.addWidget(styleLabel,40,Qt.AlignRight)                         #Agrega los elementos a pantalla
        topLayout.addWidget(styleComboBox,40,Qt.AlignRight)
        '''Posicion de los Objetos'''
        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        mainLayout.setSpacing(5)
        mainLayout.addLayout(topLayout, 0, 5, 1, 80)            #Posicion de los Objetos en Pantalla
#        mainLayout.setRowStretch(0, 1)
#        mainLayout.setRowStretch(1, 2)
        mainLayout.columnMinimumWidth(10)
        mainLayout.addWidget(self.Axis,1,0,Qt.AlignLeft)
        mainLayout.addWidget(self.Axis1,1,10,Qt.AlignCenter)
        mainLayout.addWidget(self.Axis2,1,15,Qt.AlignRight)
#        mainLayout.setColumnStretch(0, 1)
#        mainLayout.setColumnStretch(1, 1)
#        self.setLayout(mainLayout)
        '''Apariencia'''
        QApplication.setStyle(QStyleFactory.create('Fusion'))   #Estilo de la ventana
        QApplication.setPalette(self.originalPalette)
    #****************************************************************
    '''Definicion de Funciones'''
    #================================================================
    '''Mostra Imagen'''
    def ImageShow(self,Imagen):
        Size = Imagen.shape
        Step = Imagen.size/Size[0]
        qformat=QtGui.QImage.Format_Indexed8
        width=400
        height=400
        
        if len(Size)==3:
            if Size[2]==4:
                qformat=QtGui.QImage.Format_RGBA8888
            else:
                qformat=QtGui.QImage.Format_RGB888
#        elif(Size)==2:
#            qformat=QtGui.QImage.Format_RGBA8888      (Error en algunas cosas)
        Imag=QtGui.QImage(Imagen,Size[1],Size[0],Step,qformat)
        self.Axis.setPixmap(QtGui.QPixmap.fromImage(Imag).scaled(width,height,Qt.KeepAspectRatio))
#        self.resize(self.Axis.pixmap().size())
        self.Axis.show()
        
        if len(Size)==2:
            self.Gris= Imagen
            qformat=QtGui.QImage.Format_Indexed8
            Imag1=QtGui.QImage(self.Gris,Size[1],Size[0],Step,qformat)
        else:
            self.Gris= cv2.cvtColor(Imagen, cv2.COLOR_RGB2GRAY)
            qformat=QtGui.QImage.Format_Grayscale8
            Imag1=QtGui.QImage(self.Gris,Size[1],Size[0],Step/3,qformat)
            
        self.Axis1.setPixmap(QtGui.QPixmap.fromImage(Imag1).scaled(width,height,Qt.KeepAspectRatio))
#        self.resize(self.Axis1.pixmap().size())
        self.Axis1.show()
        
    def ImagenResult(self,Imagen):
        Size = Imagen.shape
        Step = Imagen.size/Size[0]
        qformat=QtGui.QImage.Format_Indexed8
        width=400
        height=400
        
        if len(Size)==3:
            if Size[2]==4:
                qformat=QtGui.QImage.Format_RGBA8888
            else:
                qformat=QtGui.QImage.Format_RGB888
            if len(Size)==1:
                qformat=QtGui.QImage.Format_Grayscale8
#        elif(Size)==2:
#            qformat=QtGui.QImage.Format_RGBA8888      (Error en algunas cosas)
        Imag=QtGui.QImage(Imagen,Size[1],Size[0],Step,qformat)
        self.Axis2.setPixmap(QtGui.QPixmap.fromImage(Imag).scaled(width,height,Qt.KeepAspectRatio))
#        self.resize(self.Axis2.pixmap().size())
        self.Axis2.show()    
    
    '''Abrir Archivos'''
    def OpenFile(self):
        name=QFileDialog.getOpenFileName(self,'Open File',"",'Images (*.png *.xpm *.jpg *.bmp *.gif *.jpeg)')
        self.Image = QtGui.QImage(name[0])
#        print(name)
        if self.Image.isNull():
            popup = QMessageBox(QMessageBox.Critical,"Image Load Error","Could not load image file!",QMessageBox.Ok,self)
            popup.show()
            return
        else:
            self.Ima=array(Image.open(name[0]))
            self.ImageShow(self.Ima)
        # Create widget
        
    '''Tomar Foto'''
    def TakePhoto(self):
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            self.Ima = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('frame',frame)
            if cv2.waitKey(5) & 0xFF == ord('e'):
                break
        cap.release()
        cv2.destroyAllWindows()
        self.ImageShow(self.Ima)
    '''Valores''' 
    def ValoresE(self,LowLimit, HighLimit):
        self.Vale, okPressed = QInputDialog.getInt(self, "Get integer","Valor:", 2, LowLimit, HighLimit, 1)
    
    def ValoresF(self,LowLimit, HighLimit):
        self.Valf, okPressed = QInputDialog.getDouble(self, "Get integer","Valor:", 1.00, LowLimit, HighLimit, 1.00)
    '''Abrir Imagen-Prueba'''
    def Tester(self, Value):
        Formato=['.jpg','.png','.jpeg','.bmp']
        ImagenPrueba=str(Value)
        Path=getcwd()
        Path.replace(sep,'/')
        Path=Path+'/Libreria/ImagesP/'
#        Path='C:/Users/turtw/Documents/PythonCh/Imagenologia/Libreria/ImagesP/'
        for i in range(3):
            self.Image = QtGui.QImage(Path+ImagenPrueba+Formato[i])
            if self.Image.isNull():
                if i==len(Formato):
                    popup = QMessageBox(QMessageBox.Critical,"Image Load Error","Could not load image file!",QMessageBox.Ok,self)
                    popup.show()
                    return
            else:
                self.Ima=array(Image.open(Path+ImagenPrueba+Formato[i]))
                self.ImageShow(self.Ima)
        
#        QFileDialog.
        
    '''Metodos Aplicables a Imagenes'''
    def Operaciones(self, Value):
        Imatratar=self.Ima
        gris=self.Gris
        mpl.close('all')
        selfWidget=self      #Self clase Widget
                
        class Switcher(object):
            def Aplicaciones(self,Value):
                """Dispatch methods"""     #Switch Creado
                method_name = str(Value)
                # Get the method from 'self'. Default to a lambda.
                method = getattr(self, method_name, lambda: "Invalid Operation")
                # Call the method as we return it
                return method()
        
            def Binarizacion(self):
                '''Binarizar'''
                try:
                    WidgetG.ValoresF(selfWidget,0.0,256.0)
                    umbral=selfWidget.Valf
                    nn,Bin= cv2.threshold(gris,umbral,255,cv2.THRESH_BINARY)
                    WidgetG.ImagenResult(selfWidget,Bin)
                except:
                    nn=1
                #mpl.imshow(Bin,cmap='gray')
                #mpl.show()
                #cv2.imshow(Bin)
                
            def Otsu(self):
                nn,Bin= cv2.threshold(gris,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                WidgetG.ImagenResult(selfWidget,Bin)
                #mpl.imshow(Bin,cmap='gray')
                #mpl.show()
                
            def BinarizaGauss(self):
                blur = cv2.GaussianBlur(gris,(5,5),0)
                nn,Bin= cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                WidgetG.ImagenResult(selfWidget,Bin)
                #mpl.imshow(Bin,cmap='gray')
                #mpl.show()
                                     
            
            def Histograma(self):
                '''Histograma'''
                histograma=[]
                Size=Imatratar.shape
                if len(Size)==3:
                    histograma.append(MyLib.Histograma(Imatratar[:,:,0]))
                    histograma.append(MyLib.Histograma(Imatratar[:,:,1]))
                    histograma.append(MyLib.Histograma(Imatratar[:,:,2]))
                else:
                    histograma.append(MyLib.Histograma(Imatratar))
                x=linspace(0,len(histograma[0]),len(histograma[0]))
                
                mpl.plot(x,histograma[0], color='r')
                #mpl.show()
                if len(Size)==3:
                    mpl.plot(x,histograma[1], color='g')
                    #mpl.show()
                    mpl.plot(x,histograma[2], color='b')
                mpl.show()
                
            def Correccion(self):
                a=[]
                for i in range(250):
                    a.append(MyLib.Trapecio(20,50,80,110,i))
                    mpl.figure(1)
                    mpl.plot(a,'r')
                mpl.show()
                print('Correccion')
                
            def GrayScale(self):
                '''Gray'''
                WidgetG.ImagenResult(selfWidget,gris)
                #mpl.imshow(gris,cmap='gray')
                #mpl.show()
                #print('Grayyyy')
            def Umbralizar(self):
                '''Umbralizar'''
                Imagen=MyLib.UmbralizarPendienteColor(Imatratar)
                WidgetG.ImagenResult(selfWidget,uint8(Imagen))
                #mpl.imshow(uint8(NewIma))
                #mpl.show()
                
            def Ecualizacion(self):
                '''Ecualizacion'''
                Salida=MyLib.Ecualizacion(gris)
                WidgetG.ImagenResult(selfWidget,uint8(Salida*255))
                #mpl.imshow(Salida,cmap='gray')
                #mpl.show()
                
            def Amibas(self):
                '''Crecimiento Regiones'''
                WidgetG.ValoresE(selfWidget,2,100)
                clicks=selfWidget.Vale
                WidgetG.ValoresE(selfWidget,0,255)
                LimitePixel=selfWidget.Vale
                def DrawnowT():
#                    WidgetG.ImagenResult(selfWidget,ImaPrueba)
                    mpl.imshow(ImaPrueba,cmap='gray')
                    mpl.show()
                ImaPrueba=MyLib.Amibas(gris,clicks,LimitePixel)
                WidgetG.ImagenResult(selfWidget,uint8(ImaPrueba*255))
            
            def HighBoost(self):
                '''HighBoost'''
                WidgetG.ValoresF(selfWidget,-1,100)
                A=selfWidget.Valf
                Unsharp=MyLib.HighBoost(gris,A)
                WidgetG.ImagenResult(selfWidget,uint8(Unsharp))
                #mpl.imshow(Unsharp,cmap='gray')
                #mpl.show()
            
            def Gamma(self):
                WidgetG.ValoresF(selfWidget,-1,100)
                Gama=selfWidget.Valf
                Salida=MyLib.Gamma(gris,Gama)
                WidgetG.ImagenResult(selfWidget,uint8(Salida))
#mpl.imshow(Salida,cmap='gray')
#                mpl.show()
#                mpl.imshow(gris,cmap='gray')
#                mpl.show()
                
        #print("combobox changed", str(Value))
        Metodo=Switcher()
        Metodo.Aplicaciones(Value)


'''Inicia GUI'''
#app=QApplication.instance() # checks if QApplication already exists 
#if not app: # create QApplication if it doesnt exist 
#app.aboutToQuit.connect(app.deleteLater)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWi = Guimagenology()
    MainWi.show()
    sys.exit(app.exec_())         