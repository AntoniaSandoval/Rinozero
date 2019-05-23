# -*- coding: utf-8 -*-
""" 
RinoZero V4.0
Creada el dia: 30-12-2018, 08:26
Autor: Felipe Barahona B.

Libreria RinoZero, version 4.0 (V4.0)
Se estructura con dos clases:
    - Clase Constructor
    - Clase Entrenador


"""
import numpy as np
#import time as tm

#=============================================================================
#1. Clase Constructor. Estructura de Red
#=============================================================================

class Constructor():
    
    def __init__(self,neuronasXcapaLista):
        self.neuronasXcapaLista = neuronasXcapaLista
        
    def armar(self):
       
       capas = len(self.neuronasXcapaLista)
       neuronasXcapa = np.zeros((1,capas)) 
       neuronasEntrada = self.neuronasXcapaLista[0]
       neuronasSalida = self.neuronasXcapaLista[capas-1]
       
       for i in range(capas):
       
           neuronasXcapa[0][i] = self.neuronasXcapaLista[i]
       
       return capas, neuronasEntrada, neuronasSalida, neuronasXcapa
   
    
    
#=============================================================================
#2. Clase Entrenador. Entrenamiento mediante descenso de Gradiente
#=============================================================================
#
# Procedimientos para reducir sobreajuste
# 1. Regularizacion
# 2. Drop-out (apagado)
# 3. Normalizacion por lotes (Batch normalization)
        
    
class Entrenador():
    
    def __init__(self,capas,neuronasXcapa,funcionActivacion,funcionCosto):
        
        self.capas = capas
        self.neuronasXcapa = neuronasXcapa
        self.funcionActivacion = funcionActivacion
        self.funcionCosto = funcionCosto
        self.chequear()
        
   
    def chequear(self):
        
        activaciones_admisibles = ['sigmoide','relu','leaky','tanh','softmax']
        optimizaciones_admisibles = ['entropia_cruzada','logaritmica','cuadratica']
        
        if list(set(self.funcionActivacion).intersection(activaciones_admisibles))==[]:
            print('Error: Una de las funciones de activacion declaradas no es admisible.')
        
        if self.funcionCosto not in optimizaciones_admisibles:
            print('Error. La funcion de costo declarada no es admisible.')
    
    
    
    """====================================================================
       Metodos para inicializar pesos
       ===================================================================="""

    def inicializarPesosAleatorios(self):
        
        pesosIniciales = [None for i in range(self.capas-1)]

        for capa in range(1,self.capas):
            pesosIniciales[capa-1] = np.random.random_sample((int(self.neuronasXcapa[0][capa-1])+
                                         1,int(self.neuronasXcapa[0][capa])))-0.5
        
        return pesosIniciales
    
    """====================================================================
     Metodos de pasada adelante
     ===================================================================="""
       
    def propagarAdelante(self,x,pesos):
        
        for i in range(len(pesos)):
            
            if self.funcionActivacion[i] == 'sigmoide':y = self.funcionSigmoide(x,pesos[i])
                
            elif self.funcionActivacion[i] == 'relu':y = self.funcionRelu(x,pesos[i])
            
            elif self.funcionActivacion[i] == 'leaky':y = self.funcionLeakyRelu(x,pesos[i])

            elif self.funcionActivacion[i] == 'tanh':pass

            elif self.funcionActivacion[i] == 'softmax':pass
                   
            x = y
            
        return y
    
    
    def funcionSigmoide(self,x,pesos):
        
        x = np.dot(np.hstack((np.ones((x.shape[0],1)),x)),pesos)
        x = 1/(1+np.exp(-x))
        
        return x
               
        
    def funcionRelu(self,x,pesos):
        
        x = np.dot(np.hstack((np.ones((x.shape[0],1)),x)),pesos)
        zeros = np.zeros(x.shape)
        x = np.maximum(zeros,x)
        
        return x
    
    def funcionLeakyRelu(self,x,pesos):
        
        x = np.dot(np.hstack((np.ones((x.shape[0],1)),x)),pesos)
        x = np.maximum(0.01*x,x)
        
        return x

    def funcionTanh(self,x,pesos):

        return x

    def funcionSoftmax(self,x,pesos):

        return x
    
    

    """====================================================================
     Metodos de retropropagacion
     ===================================================================="""

    def retroPropagar(self,dy,pesos):pass


    """====================================================================
     Metodos de optimizacion
     ===================================================================="""
    
    def calcularCosto(self,y_pred,y):
        
        if self.funcionCosto == "cuadratica":costo = self.costoCuadratico(y_pred,y)
        
        elif self.funcionCosto == "logaritmica":costo = self.costoLogaritmico(y_pred,y)
        
        elif self.funcionCosto == "entropia_cruzada":costo = self.costoEntropiaCruzada(y_pred,y)
        
        return costo
    
        
    
    def costoCuadratico(self,y_pred,y):
        
        costo = (1/(2*y_pred.shape[0]))*((y_pred-y)**2).sum()
        
        return costo
    
    
    def costoLogaritmico(self,y_pred,y):pass
        
    
    def costoEntropiaCruzada(self,y_pred,y):pass
    

    def optimizar(self,x,y,pesos,metodo,tasa,iteraciones,lotes,batch_norm):pass
    
