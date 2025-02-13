# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:08:30 2019

@author: turtw
"""

import numpy as np
#import matplotlib.pyplot as mpl
import matplotlib.pyplot as plt
#*********************#
from pylab import *
from Libreria import MyLib
#********************************************************************
#********************************************************************
'''Otsu'''
'Parte 2'
def UmbOtsu(Histograma,fil,col):
    P=Histograma/(fil*col)
    Suma0=1*10e-10
    Suma2=0
    
    W0=[]
    W1=[]
    Mu0=[]
    Mu1=[]
    
    for i in range(len(Histograma)):
        Suma0+=P[i]
        Suma2+=i*P[i]
        W0.append(Suma0)
        Mu0.append(Suma2/Suma0)
        Suma3=1*10e-10
        Suma4=0.0
        for j in range(i+1,255,1):
            Suma3+=P[j]
            Suma4+=j*P[j]
        W1.append(Suma3)
        Mu1.append(Suma4/Suma3)
    Umbral=np.array(W0)*np.array(W1)*((np.array(Mu0)-np.array(Mu1))**2)
    return Umbral
	
#********************************************************************
'''Prubea'''
def Prueba(Histograma):
	a=Histograma/150
	return a
	
#********************************************************************
'''Multi-Umbralizacion con Fuzzy'''
def MultiUmbral(ima,a,b):
    if(a>b):
        S=-1
        m=-1
        return m,S
    ima=np.array(ima)
    u1=(ima>=a)
    u2=(ima<=b)
    x=np.multiply(u1,u2)
    y=np.multiply(ima,x)
    S=np.sum(x)
    m=np.sum(y)/S
    return S,m
	
#********************************************************************
'''Umbralizacion Por puntos en imagenes'''
def UmbralizarPendienteColor(Imatratar):
    '''Umbralizar'''
    plt.plot()
    clicks=2
    plt.axis([0,255,0,255])
    x = plt.ginput(clicks)
    #mpl.show()
    plt.close('all')
#    print('termino1')
    #********************************************************************
    '''Encuentra la Pendiente '''
    m=[]
    mp=(x[0][1]-0)/(x[0][0]-0)
    m.append(mp)
    for i in range (clicks-1):
        mp=(x[i+1][1]-x[i][1])/(x[i+1][0]-x[i][0])
        m.append(mp)
    mp=(x[clicks-1][1]-255)/(x[clicks-1][0]-255)
    m.append(mp)
    #********************************************************************
    '''Encuentra el desface '''
    b=[]
    bp=0
    b.append(bp)
    for i in range (clicks):
        bp=(x[i][1]-(m[i+1]*x[i][0]))
        b.append(bp)
     
    #********************************************************************
    '''Umbraliza '''
    Size=Imatratar.shape
    if len(Size)==3:
        NewIma=zeros((Size))
        for i in range (Size[0]):
            for j in range (Size[1]):
                for k in range (Size[2]):
                    if Imatratar[i,j,k]<=x[0][0]:
                        NewIma[i,j,k]=((m[0]*Imatratar[i,j,k])+b[0])
                    elif Imatratar[i,j,k]>x[0][0] and Imatratar[i,j,k]<= x[1][0]:
                        NewIma[i,j,k]=((m[1]*Imatratar[i,j,k])+b[1])
                    elif Imatratar[i,j,k]> x[1][0]:
                        NewIma[i,j,k]=((m[2]*Imatratar[i,j,k])+b[2])
    else:
        NewIma=zeros((Size))
        for i in range (Size[0]):
            for j in range (Size[1]):
                if Imatratar[i,j]<=x[0][0]:
                    NewIma[i,j]=((m[0]*Imatratar[i,j])+b[0])
                elif Imatratar[i,j]>x[0][0] and Imatratar[i,j]<= x[1][0]:
                    NewIma[i,j]=((m[1]*Imatratar[i,j])+b[1])
                elif Imatratar[i,j]> x[1][0]:
                    NewIma[i,j]=((m[2]*Imatratar[i,j])+b[2])
    return NewIma
#********************************************************************
'''Ecualizacion de Imagen'''
def Ecualizacion(gris):
    [fil,col]=gris.shape
    histograma=MyLib.Histograma(gris)
    x=linspace(0,len(histograma),len(histograma))
    pro=histograma/(fil*col)
    '''Ecualizar'''
    k=0
    pro2=zeros(256)
    for i in range(256):
        k=pro[i]+k
        pro2[i]=k
    Salida=zeros([fil,col])
    '''Mostrar'''
    for i in range(fil):
        for j in range(col):
            Pixel=gris[i,j]
            Salida[i,j]=pro2[Pixel]
    return Salida
#********************************************************************
''''HighBoost'''
def HighBoost(gris,A):
    '''HighBoost'''
    w=9*A-1
    HighB=np.array([[-1,-1,-1],[-1,w,-1],[-1,-1,-1]])
    fil,col=gris.shape
    Salida=np.zeros((fil,col))
    '''High Boost'''
    for i in range(1,fil-1):
        for j in range(1,col-1):
            Ventana=gris[i-1:i+2,j-1:j+2]
            Pixel=np.sum(HighB*Ventana)
            Salida[i,j]=Pixel               
    Unsharp=(gris+Salida)
    Mini=np.amin(Unsharp)
    Unsharp=Unsharp-Mini
    Maxi=np.amax(Unsharp)
    Unsharp=(Unsharp/Maxi)*255
    return Unsharp
    
#********************************************************************
''''Gamma'''
def Gamma(gris,Gamma):
    fil,col = gris.shape
    Salida=np.zeros([fil,col])
    for i in range(fil):
        for j in range(col):
            Salida[i,j]=np.power(gris[i,j],1/Gamma)
    Mini=np.amin(Salida)
    Salida=Salida-Mini
    Maxi=np.amax(Salida)
    Salida=(Salida/Maxi)*255
    return Salida