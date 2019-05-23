# -*- coding: utf-8 -*-
"""
Created on Thu May 10 20:56:30 2018

@author: Usuario
rinozero.arbol
Implementacion de algortimo de clasificacion logistica

"""
import math as mt
import numpy as np
import random as rd


#-----------------------------------------------------------------------------
#Funciones
#----------------------------------------------------------------------------- 
    
def funcionSigmoide(x,P):
    x= np.hstack((np.ones((1,1)),x))
    u= x.dot(P)
    u= 1/(1+np.exp(-u))
    
    return u   

#=============================================================================
#1. Clase 1 Constructor
#=============================================================================

class Constructor:
    
    def __init__(self, numeroParametros):
        
        self.numeroParametros = numeroParametros

        
    """=======================================================================
        Metodo 1. Inicializar parametros aleatorios
       ===================================================================="""     
    
    def iniciarParamAleatorios(self):
        
        param = np.ones((1,self.numeroParametros))
        for i in range(self.numeroParametros):
            param[0][i] =rd.random()*param[0][i]
        
        return param
 
    """=======================================================================
        Metodo 2. Inicializar parametros unidad
       ===================================================================="""     
    
    def iniciarParamUnos(self):
        
        param = np.ones((1,self.numeroParametros))
                
        return param       

#=============================================================================
#2. Clase 2 Entrenador
#=============================================================================        

class Entrenador:
    
    def __init__(self,alpha,Lambda,tol,data,param,y):
        
        self.alpha = alpha
        self.Lambda = Lambda
        self.tol = tol
        self.data = data
        self.param = param
        self.y = y
    
    """=======================================================================
        Metodo 1. calcular funcion de costo asociado a parametros, conjunto de 
        datos y salidas conocidas
       ===================================================================="""     
    def calcularCosto(self):
        
        sumatoria = 0
        terminoReg = 0
        for i in range(1,self.param.shape[1]):
            terminoReg += self.param[0][i]**2
        terminoReg *= self.Lambda
        
        #data_param = (np.hstack((np.ones(data.shape[0],1),data))).dot(param.reshape(param.shape[1],1)) 
        
        
        for i in range(self.data.shape[1]):
#            sumatoria += (np.hstack((np.ones(1),data[i])).dot(param.reshape(param.shape[1],1))-
#                          y[i][0])**2+terminoReg
            data_param = 1/(1+mt.exp(-(np.hstack((np.ones(1),self.data[i])).dot(self.param.reshape(self.param.shape[1],1)))[0]))
            sumatoria += (data_param-self.y[i][0])**2+terminoReg        
        
        sumatoria = 0.5*sumatoria/self.data.shape[0]
        
        return sumatoria

    """=======================================================================
        Metodo 2. calcular derivada parciales
       ===================================================================="""     
    #----corregir----
    def calcularDerivadaParcial(self):
             
        dparam = [0 for j in range(self.param.shape[1])]
        for j in range(self.param.shape[1]):
            sumatoria = 0
            for i in range(self.data.shape[0]):
                
                sumatoria += (1/(1+mt.exp(-(np.hstack((np.ones(1),self.data[i])))))).dot(self.param.reshape(self.param.shape[1],1)-
                              self.y[i][0])*np.hstack((np.ones((self.data.shape[0],1)),self.data))[i][j]
            dparam[j] = sumatoria*self.alpha/self.data.shape[0]
        
        return dparam

    """=======================================================================
        Metodo 3. actualizar parametros
       ===================================================================="""     
    
    def actualizarParametros(self,dparam):
        
        for j in range(self.param.shape[1]):
            if j==0:
                self.param[0][j] = self.param[0][j] - dparam[j]
            else:
                self.param[0][j] = self.param[0][j]*(1-self.Lambda*self.alpha/self.data.shape[0])-dparam[j]
        
        return self.param
        
    """=======================================================================
        Metodo 4. computa metodo del descenso de gradiente
       ====================================================================""" 
    def optimizar(self):
       
        costo = self.calcularCosto()
        contador = 0
        
        while costo > self.tol:
            derivada = self.calcularDerivadaParcial()
            self.param = self.actualizarParametros(derivada)
            costo = self.calcularCosto()
            contador += 1
            print("Iter: ",contador," Funcion Costo: ",costo)
