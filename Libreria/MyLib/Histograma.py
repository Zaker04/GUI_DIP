# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 12:31:50 2019

@author: turtw
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:02:32 2019

@author: turtw
"""
"""Hist"""
import numpy as np
#********************************************************************
'''Histograma'''
def Histograma(Imagen):
    '''Make an histogram of the image, that goes from 0 to 255'''
    L=256
    fil,col=Imagen.shape
    Histograma=np.zeros(L)
    for i in range(fil):
        for j in range(col):
            Pixel=Imagen[i,j]
            Histograma[Pixel]+=1
    
    return Histograma
