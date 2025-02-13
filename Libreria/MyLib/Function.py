# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:02:32 2019

@author: turtw
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt
import sympy as spy
#*********************#
from pylab import *
from Libreria import MyLib
#********************************************************************
"""Funciones de Fuzzyficado"""
def Trapecio(P1,P2,P3,P4,x):
    if x<=P1:
        Salida=0
    elif x>P1 and x<P2:
        Salida=(x-P1)/(P2-P1)
    elif x>=P2 and x<=P3:
        Salida=1
    elif x>P3 and x<P4:
        Salida=(P4-x)/(P4-P3)
    else:
        Salida=0
    return Salida
#********************************************************************
'''Crecimiento de Regiones'''
def Amibas(gris,clicks,Limite):
    fil,col=gris.shape
    ImaPrueba=zeros((fil,col))
    ImaDilate=zeros((fil,col))
    ImagenF=ones((fil,col))
    plt.imshow(gris,cmap='gray')
    cord = (plt.ginput(clicks))
#                cord = (plt.ginput(0,0))
    cord=array(uint(cord))
    x=(cord[:,1])
    y=(cord[:,0])
    #********************************************************************
    '''Punto y Crecimiento'''
    ValorPunto=np.mean(gris[x,y])
    rr=np.where((gris[x,y]>ValorPunto-Limite) & (gris[x,y]<ValorPunto+Limite))
    ImaPrueba[x[rr],y[rr]]=1
    ImaDilate[x[rr],y[rr]]=1
    Tolerancia=20
    plt.close()
    while(True):
        ImagenF1=np.copy(ImagenF)
        #struct1 = sp.ndimage.generate_binary_structure(2, 2)
        #ImaDilate=morphology.binary_dilation(ImaDilate,struct1)
        struct1=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        ImaDilate=cv2.dilate(ImaDilate,struct1,iterations = 1)
        ImagenF=ImaDilate-ImaPrueba
        #********************************************************************
        '''Checar valores y Modificarlos'''
        Posiciones=np.where(ImagenF)
        Valores=gris[Posiciones]
        Amiba=np.where((Valores>ValorPunto-Limite) & (Valores<ValorPunto+Limite))
        xx=Posiciones[0][Amiba]
        yy=Posiciones[1][Amiba]
        ImaPrueba[xx,yy]=1
        if  np.array_equal(ImagenF,ImagenF1)==True:
            break
        ImaDilate=np.copy(ImaPrueba)
#                    drawnow(DrawnowT)
        #mpl.show()
        #mpl.close()
    return ImaPrueba
#********************************************************************
'''Splines'''
def Splines(n,cord,step):
	#********************************************************************
	'''Xcomponent'''
	Ax=spy.symbols('ax0:'+str(n))
	Bx=spy.symbols('bx0:'+str(n))
	Cx=spy.symbols('cx0:'+str(n))
	Dx=spy.symbols('dx0:'+str(n))
	'''Ycomponent'''
	Ay=spy.symbols('ay0:'+str(n))
	By=spy.symbols('by0:'+str(n))
	Cy=spy.symbols('cy0:'+str(n))
	Dy=spy.symbols('dy0:'+str(n))
	t=spy.Symbol('t')
	'''Ecuacion'''
	ec=[]
	Derivada0=[]
	Derivada1=[]
	Derivada2=[]
	i=0
	for i in range(n-1):
		a=Ax[i]+Bx[i]*t+Cx[i]*t**2+Dx[i]*t**3,Ay[i]+By[i]*t+Cy[i]*t**2+Dy[i]*t**3
		ec.append(a)

	'''Derivada0 '''
	for i in range(n-1):
		a=[spy.Eq(ec[i][0].subs(t,0)-cord[0][i]),spy.Eq(ec[i][1].subs(t,0)-cord[1][i]),spy.Eq(ec[i][0].subs(t,1)-cord[0][i+1]),spy.Eq(ec[i][1].subs(t,1)-cord[1][i+1])]
		Derivada0.append(a)
	'''Derivada1 y 2'''
	for i in range(n-2):
		a=[spy.Eq(spy.diff(ec[i][0],t,1).subs(t,1)-spy.diff(ec[i+1][0],t,1).subs(t,0)),spy.Eq(spy.diff(ec[i][1],t,1).subs(t,1)-spy.diff(ec[i+1][1],t,1).subs(t,0))]
		Derivada1.append(a)
		a=[spy.Eq(spy.diff(ec[i][0],t,2).subs(t,1)-spy.diff(ec[i+1][0],t,2).subs(t,1)),spy.Eq(spy.diff(ec[i][1],t,2).subs(t,1)-spy.diff(ec[i+1][1],t,2).subs(t,1))]
		Derivada2.append(a)
	'''Derivada3'''
	Derivada3=[spy.Eq(spy.diff(ec[0][0],t,2).subs(t,0)-0),spy.Eq(spy.diff(ec[0][1],t,2).subs(t,0)-0),spy.Eq(spy.diff(ec[n-2][0],t,2).subs(t,1)-0),spy.Eq(spy.diff(ec[n-2][1],t,2).subs(t,1)-0)]
	DerivadaT=Derivada0+Derivada1+Derivada2+Derivada3
	#********************************************************************
	'''Terminos X e Y'''
	TerminosX=[]
	TerminosY=[]
	for k in range(len(DerivadaT)):
		if k==len(DerivadaT)-len(Derivada3):
			TerminosX.append(DerivadaT[k:][::2])
			TerminosY.append(DerivadaT[k:][::-1][::2])
			break
		TerminosX.append(DerivadaT[k][::2])
		TerminosY.append(DerivadaT[k][::-1][::2])
	ecx=[]
	ecy=[]
	#********************************************************************
	'''Solucion del Sistema'''
	for i in range(0,len(TerminosX),2):
		if i+1>len(TerminosX)-1:
			ecx=ecx+TerminosX[i]
			ecy=ecy+TerminosY[i]
			break
		a=TerminosX[i]+TerminosX[i+1]
		ecx=ecx+a
		a=TerminosY[i]+TerminosY[i+1]
		ecy=ecy+a
	solx=spy.solve(ecx,Ax+Bx+Cx+Dx)
	soly=spy.solve(ecy,Ay+By+Cy+Dy)
	Res=[]
	for i in range(len(ec)):
		a=ec[i][0].subs(solx),ec[i][1].subs(soly)
		Res.append(a)
	for i in range(len(Res)):
		x=[]
		y=[]
		for k in range(0,101,1):
			x.append(Res[i][0].subs(t,k/100))
			y.append(Res[i][1].subs(t,k/100))
	return x,y
#********************************************************************
'''ChainCode'''
def ChainCode(Borde):
    fil,col=Borde.shape
    k=0
    obj=0
    datos=[]
    pixel=[]
    for i in range (fil-1):
        for j in range (col-1):
            if Borde[i,j] == 1:
                obj=obj+1
                k=k+1
                I=i
                J=j
                Borde[I,J]=0
                pixel=[obj,k,I,J]
                datos.append(pixel)
                while(k!=0):
                    if Borde[I-1,J]==1:
                        k=k+1
                        I=I-1
                        J=J
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I-1,J+1]==1:
                        k=k+1
                        I=I-1
                        J=J+1
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I,J+1]==1:
                        k=k+1
                        I=I
                        J=J+1
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I+1,J+1]==1:
                        k=k+1
                        I=I+1
                        J=J+1
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I+1,J]==1:
                        k=k+1
                        I=I+1
                        J=J
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I+1,J-1]==1:
                        k=k+1
                        I=I+1
                        J=J-1
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I,J-1]==1:
                        k=k+1
                        I=I
                        J=J-1
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    elif Borde[I-1,J-1]==1:
                        k=k+1
                        I=I-1
                        J=J-1
                        Borde[I,J]=0
                        pixel=[obj,k,I,J]
                        datos.append(pixel)
                    else: 
                        k=0
                        #drawnow(dibuja())
    x,y=np.array(datos).shape
    adatos=np.array(datos)
    filas=[]
    columnas=[]
    obj1=[]
    frey=[]
    area=[]
    k=0
    Cosas=max(adatos[:,0])
    for j in range(Cosas):
        k=k+1
        filas=[]
        columnas=[]
        area=[]
        for i in range (x):
            if adatos[i,0]==k:
                filas.append(adatos[i,2])
                columnas.append(adatos[i,3])
                area.append(adatos[i,1])
        frey=[filas,columnas,max(area)]
        obj1.append(frey)
    obj1=np.array(obj1)
    return obj1,Cosas