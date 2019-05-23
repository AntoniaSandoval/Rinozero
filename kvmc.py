# -*- coding: utf-8 -*-
"""
Created on Tue May  1 18:45:00 2018

@author: Usuario
rinozero.kvc
Implementacion de algortimo k vecinos más cercanos

"""
import math as mt
import operator

#=============================================================================
#Clase 1. Entrenador
#=============================================================================    

class Entrenador:
    
    def __init__(self,k):
        self.k = k
            
    """=======================================================================
        Metodo 1. Ordenar distancias en diccionario diccDis
       ===================================================================="""    
    
    def ordenarCaract(self,itemDis):

        itemDis_ord = sorted(itemDis.items(),key=operator.itemgetter(1))
        itemDis_ord = itemDis_ord[::1]
        
        return itemDis_ord
    
    """=======================================================================
        Metodo 2. generar estructura de datos de valores
       ===================================================================="""
    
    def generarItemVal(self,valor):
        
        itemVal ={}
        for i in range(len(valor)):
            itemVal["item"+str(i)] = valor[i][0]
        
        return itemVal
    
    """=======================================================================
        Metodo 3. calcular distancias del ejemplo a los ejemplos del dataset
       ===================================================================="""
    
    def calcularDistancia(self,data,ejemplo):
        
        itemDis = {}
        distancia = [None for i in range(len(data))]
        
        for i in range(len(data)):
            sumatoria = 0
            for j in range(len(data[0])):
                sumatoria += (data[i][j]-ejemplo[j])**2
            
            distancia[i] = mt.sqrt(sumatoria)
            itemDis["item"+str(i)] = distancia[i]
        
        itemDis_ord = self.ordenarCaract(itemDis)
        
        return itemDis_ord

    """=======================================================================
        Metodo 4. ejecutar clasificacion
       ===================================================================="""
    
    def identificarVal(self,valor):
        
        valor_id = []
        for i in range(len(valor)):
            if valor[i][0] not in valor_id:
                valor_id.append(valor[i][0])
        
        return valor_id

    """=======================================================================
        Metodo 5. ejecutar clasificacion
       ===================================================================="""
       
    def clasificar(self,itemVal,itemDis_ord,valor_id):
        
        contador = [0 for i in range(len(valor_id))]
        
        for i in range(len(valor_id)):
            for j in range(self.k):
                if itemVal[itemDis_ord[j][0]] == valor_id[i]:
                    contador[i] += 1
            
        maxVal = max(contador)
        for i in range(len(valor_id)):
            if contador[i] == maxVal:
                prediccion = valor_id[i]
                break
    
        return prediccion
    