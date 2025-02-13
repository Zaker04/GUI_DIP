# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 20:39:14 2019

@author: turtw
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
#*********************#
from pylab import *
from Libreria import MyLib
#********************************************************************
"""Filtros"""
def CirculoF(Centro,Fc,Tamano,Relleno):
    Filas,Columnas=Tamano
    Centro=np.uint32(Centro)
    Fc=np.uint32(Fc)
    NewIma=np.zeros((Filas,Columnas),dtype=np.uint8)
    Radianes=np.linspace(0,2*pi,500)
    if Relleno==0:
        #Circulo Vacio
        Start=Fc-1
    else:
        Start=0
        
    for Radio in range(Start,Fc):
        x=Centro[1]+Radio*np.cos(Radianes)
        y=Centro[0]+Radio*np.sin(Radianes)
        NewIma[np.uint32(y),np.uint32(x)]=255
    struct1=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    NewIma=cv2.dilate(NewIma,struct1,iterations = 1)
    NewIma=cv2.erode(NewIma,struct1,iterations = 1)
    
    if Relleno==2:
        NewIma=np.where(NewIma<1,1,0)
    else:
        NewIma
    return NewIma
'''Pasa Bajas'''
def ButterPasoBajo(Filas,Columnas,Fcorte):
    NewIma=np.zeros((Filas,Columnas))
    for i in range(Filas):
        for j in range(Columnas):
            Radio=np.sqrt((Filas/2-i)**2+(Columnas/2-j)**2)
            NewIma[i,j]=1/(1+(Radio/Fcorte)**2)
    return NewIma
'''Pasa Altas'''
def ButterPasoAlto(Filas,Columnas,Fcorte):
    NewIma=np.zeros((Filas,Columnas))+1
    for i in range(Filas):
        for j in range(Columnas):
            Radio=np.sqrt((Filas/2-i)**2+(Columnas/2-j)**2)
            NewIma[i,j]=(1-1/(1+(Radio/Fcorte)**2))
    return NewIma