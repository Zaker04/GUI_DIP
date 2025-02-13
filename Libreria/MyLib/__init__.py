# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:25:45 2019

@author: turtw
"""

from .Function import (Trapecio,Amibas,Splines,ChainCode)
from .Histograma import (Histograma)
from .Umbralizar import (UmbOtsu,MultiUmbral,UmbralizarPendienteColor,Ecualizacion,HighBoost,Gamma)
from .Filtros import(ButterPasoBajo,ButterPasoAlto,CirculoF)
__all__ = ['Trapecio','Histograma','UmbOtsu','MultiUmbral','UmbralizarPendienteColor','Ecualizacion','Amibas','HighBoost',
           'Gamma','ButterPasoBajo','ButterPasoAlto','CirculoF','Splines','ChainCode']