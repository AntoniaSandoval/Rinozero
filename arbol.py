# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 19:58:18 2018

@author: Usuario
rinozero.arbol
Implementacion de algortimo de arboles de decision

"""
import math as mt
import operator

#=============================================================================
#1. Clase Entrenador (Ordenador)
#=============================================================================

class Entrenador:
    
    def __init__(self,data,caracteristica,valor,VALOR_POSITIVO,VALOR_NEGATIVO):
        
        self.data = data
        self.caracteristica = caracteristica
        self.valor = valor
        self.VALOR_POSITIVO = VALOR_POSITIVO
        self.VALOR_NEGATIVO = VALOR_NEGATIVO
        
    """=======================================================================
        Metodo 1. calculo de entropia
       ===================================================================="""    

    def calc_entropia(self,positivos,negativos):
    
        if positivos == 0 and negativos == 0:
            entropia = 1.0
    
        elif positivos == 0 or negativos == 0:
            entropia = 0.0
    
        else: 
            ratioPositivos = (positivos/(positivos+negativos))
            ratioNegativos = (negativos/(positivos+negativos))
            entropia = -(ratioPositivos*mt.log(ratioPositivos,2)+ratioNegativos*mt.log(ratioNegativos,2))
    
        return entropia
    
    
    """=======================================================================
        Metodo 2. obtiene el numero de valoraciones positivas y negativas del
        conjunto de ejemplos
        ==================================================================="""
    
    def obtenerValor(self):
        
        pos = 0
        neg = 0
        
        for i in range(len(self.valor)):
            if self.valor[i][0] == self.VALOR_POSITIVO:
                pos +=1
            else:
                neg +=1
        num = [pos,neg]
        
        return num
    
    
    """=======================================================================
        Metodo 3. genera vector asociado a atributo
        ==================================================================="""            
        
    def vectorizarAtributo(self,numAtributo):
        
        filas = len(self.data)
        atributo = [None for i in range(filas)]
        
        for i in range(filas):
            atributo[i] = self.data[i][numAtributo]
        
        return atributo


    """=======================================================================
        Metodo 4. obtiene etiquetas por cada atributo
        ==================================================================="""

    def listarValoresXatributo(self,valores):
        
        valoresXatributo = []
        
        for i in range(len(self.data)):
            if i == 0:
                valoresXatributo.append(valores[i])
            else:
                if valores[i] not in valoresXatributo:
                    valoresXatributo.append(valores[i])
        
        return valoresXatributo
    
        
    """=======================================================================
        Metodo 5. obtiene tasa de positivos y negativos asociados a un atributo
        ==================================================================="""
    
    def obtenerPosNeg(self, atributos, valoresXatributo):
        
        tasaPos = 0
        contador = 0
        pos = [None for i in range(len(valoresXatributo))]
        neg = [None for i in range(len(valoresXatributo))]

        for i in range(len(valoresXatributo)):
            for j in range(len(self.valor)):
                if atributos[j] == valoresXatributo[i]:
                    contador +=1
                    if self.valor[j][0] == self.VALOR_POSITIVO:
                        tasaPos +=1
        
            pos[i] = tasaPos/contador
            neg[i] = 1- pos[i]
            
            tasaPos = 0
            contador = 0
        
        return pos,neg
        
    """=======================================================================
        Metodo 6. obtiene cantidad de positivos y negativos asociados a un atributo
        ==================================================================="""

    def obtenerCanPosNeg(self, atributos, valoresXatributo):
    
        pos = [0 for i in range(len(valoresXatributo))]
        neg = [0 for i in range(len(valoresXatributo))]
        
        for i in range(len(valoresXatributo)):
            for j in range(len(self.valor)):
                if atributos[j] == valoresXatributo[i]:
                    if self.valor[j][0] == self.VALOR_POSITIVO:
                        pos[i] +=1
                    else:
                        neg[i] +=1
        
        return pos,neg
    
    """=======================================================================
        Metodo 7. genera un diccionario con la ganancia de informacion
        para cada caracteristica
        ==================================================================="""    

    def obtenerGanInformacion(self,entropia):
        
        entropiaXcaract = [0 for i in range(len(self.caracteristica))]
        ganancia = [0 for i in range(len(entropiaXcaract))]
        ganInfo = {}
        
        
        for i in range(len(self.caracteristica)):
            vector = self.vectorizarAtributo(i)
            etiquetasXcaract = self.listarValoresXatributo(vector)
            
            tasaPosNeg = self.obtenerPosNeg(vector, etiquetasXcaract)
            canPosNeg = self.obtenerCanPosNeg(vector, etiquetasXcaract)
            
            entropias = [0 for i in range(len(etiquetasXcaract))]
            for j in range(len(etiquetasXcaract)):
                entropias[j] = self.calc_entropia(tasaPosNeg[0][j],tasaPosNeg[1][j])
            
            suma = 0
            for j in range(len(etiquetasXcaract)):
                suma += (canPosNeg[0][j] + canPosNeg[1][j])*entropias[j]
            
            suma /= len(self.data)
            entropiaXcaract[i] = suma 
        
        for i in range(len(entropiaXcaract)):
            ganancia[i] = entropia - entropiaXcaract[i]
            ganInfo[self.caracteristica[i]] = ganancia[i]
        
        return ganInfo
        
    """=======================================================================
        Metodo 8. genera una lista con caracteristicas ordenadas en funcion
        de su valor de ganancia
        ==================================================================="""

    def ordenarCaract(self,ganInfo):

        caractOrd = sorted(ganInfo.items(),key=operator.itemgetter(1))
        caractOrd = caractOrd[::-1]
        
        return caractOrd

#=============================================================================
#3. Clase Generador (Ramificador)
#=============================================================================
        
class Generador:
    
    def __init__(self,data,caracteristica,valor,VALOR_POSITIVO,VALOR_NEGATIVO,atributosOrdenados):
        self.data = data
        self.caracteristica = caracteristica
        self.valor = valor
        self.VALOR_POSITIVO = VALOR_POSITIVO
        self.VALOR_NEGATIVO = VALOR_NEGATIVO
        self.atributosOrdenados = atributosOrdenados
        
    
    
    
    