# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 15:49:17 2018

Autor: fb
Modulo pproc

Base sobre la que actua:
Carpeta con archivos .xlsx, numerados, cada uno conteniendo un ejemplo
ejemplo: archivo de audio, texto, imagen, dataset

"""
import numpy as np

#=============================================================================
#1. Clase UsoEjemExcel (objetos "ejemplo" de un conjunto de datos desde Excel)
#=============================================================================
class UsoEjemExcel():
    
    def __init__(self,n):
        self.n = n
    
    """=======================================================================        
        1. Metodos para cargar datos e iniciar preprocesamiento
       ====================================================================""" 
    #Este metodo puede funcionar para varios formatos
    #si se le entrega como argumento la extension (.xlsx, .xls, .csv o .txt)
    #Recibe cadenas de caracteres 
    def numerarImagen(self,nombre_generico,nombre_extension):
                
        if self.n < 10:
            nombre_archivo = nombre_generico + "000" + str(self.n) + nombre_extension
        
        elif self.n > 9 and self.n < 100:
            nombre_archivo = nombre_generico + "00" + str(self.n) + nombre_extension
        
        elif self.n > 99 and self.n < 10000:
            nombre_archivo = nombre_generico + "0" + str(self.n) + nombre_extension
        
        return nombre_archivo
    
        
    """=======================================================================
        2. Metodo para obtener numero de filas y columnas de la matriz de 
        informacion de la imagen
        ==================================================================="""
    #recibe un objeto de la clase openpyxl        
    def dimensionarImagen(self,imagen):
        
        data_imagen = imagen.get_sheet_by_name("Hoja1")
        
        filas_imagen = data_imagen.max_row
        cols_imagen = data_imagen.max_column
         
        return filas_imagen, cols_imagen
    

    """=======================================================================
        3. Metodo para cargar matriz de pixeles de una imagen
       ====================================================================""" 
    #Recibe un objeto de la clase openpyxl
    def cargarImagen(self,imagen,filas_imagen,cols_imagen):
        
        data_imagen = imagen.get_sheet_by_name("Hoja1")
        info_imagen = np.zeros((filas_imagen,cols_imagen))
        
        for i in range(filas_imagen):
            for j in range(cols_imagen):
                info_imagen[i][j] =  data_imagen.cell(row = i+1, column = j+1).value
        
        return info_imagen
        
    
    """=======================================================================
        4. Metodo para vectorizar imagen
       ===================================================================="""
    #recibe un objeto de la clase openpyxl
    def vectorizarImagen(self,info_imagen, imagen):
        
        res_imagen = imagen.get_sheet_by_name("Hoja2")
        
        parteImagen = info_imagen[0][:]
        
        for i in range(info_imagen.shape[0]-1):
            parteImagen = np.concatenate((parteImagen,info_imagen[i+1][:]))
        for i in range(len(parteImagen)):
            res_imagen.cell(row = 1,column = i+1).value = parteImagen[i] 
        
        return parteImagen
        
                
    """=======================================================================
        5. Metodo para calcular el numero de pixeles de la imagen
       ===================================================================="""
    #Recibe enteros y cadenas
    def pixelar(self,filas_imagen,cols_imagen):
    
        numero_pixeles = filas_imagen*cols_imagen
        
        return numero_pixeles



    """=======================================================================
        6. Metodo para construir filtro
       ====================================================================""" 
    #Recibe enteros y cadenas
    def construirFiltro(self,dimFiltro,tipoFiltro):
        
        if tipoFiltro == "bordes_horizontales":
            if dimFiltro == 3:
                filtro = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        elif tipoFiltro == "bordes_verticales":
            if dimFiltro == 3:
                filtro = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
            
        elif tipoFiltro == "espacial_pasabajos":
            filtro = (1/(dimFiltro)**2)*np.ones((dimFiltro,dimFiltro))
        
        return filtro
    
    """=======================================================================
        7. Metodo para cargar base de datos existente
       ===================================================================="""
    #Recibe un objeto de la clase openpyxl
    def cargarBaseExist(self,bd):
        
        filas_bd = bd.max_row
        cols_bd = bd.max_column
        
        data = np.zeros((filas_bd,cols_bd))
        for i in range(filas_bd):
            for j in range(cols_bd):
                data[i][j] = bd.cell(row=i+1,column=j+1).value
        
        return data
    
    
    """=======================================================================
        8. Metodo para reensamblar imagenes desde su forma vectorial
       ===================================================================="""
    #Recibe matrices (objetos tipo numpy)
    def reensamblarImagen(self,vector,numColumnas):
        
        numFilas = int(vector.shape[1]/numColumnas)
        lim = [None for i in range(numFilas)]
        
        contador = 0
        for i in range(int(numFilas)):
            for j in range(numColumnas):
                contador +=1
            lim[i] = int(contador)
       
        imagen = vector[0][lim[0]-numColumnas:lim[0]].reshape(1,numColumnas)
        
        for i in range(len(lim)-1):
            imagen = np.concatenate((imagen,(vector[0][lim[i+1]-numColumnas:lim[i+1]]).reshape(1,numColumnas)))
        
        return imagen
 
    
    """=======================================================================
        9. Metodo para aplicar convolucion
       ===================================================================="""
    #Recibe matrices (objetos tipo numpy)
    def conv_hiperParam(self,data,map_car,filtro,dimFiltro):
        
        for i in range(map_car.shape[0]):
            for j in range(map_car.shape[1]):
                contador = data[i:i+dimFiltro,j:j+dimFiltro]*filtro
                
                for k in range(dimFiltro):
                    for l in range(dimFiltro):
                        map_car[i][j] = map_car[i][j]+contador[k][l]
        
        return map_car
    
    
    """=======================================================================
        10. Metodo para aplicar pooling de maximos
       ====================================================================""" 
    #Recibe matrices (objetos tipo numpy)
    def pooling_hiperParam_max(self,data,map_pool,dimFiltro):
        
        for i in range(map_pool.shape[0]):
            for j in range(map_pool.shape[1]):
                contador = data[i:i+dimFiltro,j:j+dimFiltro]
                
                map_pool[i][j] = contador.max()
                
        return map_pool
    
    
    """=======================================================================
        11. Metodo para aplicar pooling de promedios
       ====================================================================""" 
    #Recibe matrices (objetos tipo numpy)
    def pooling_hiperParam_prom(self,data,map_pool, dimFiltro):
        
        for i in range(map_pool.shape[0]):
            for j in range(map_pool.shape[1]):
                contador = data[i:i+dimFiltro,j:j+dimFiltro]
                
                map_pool[i][j] = contador.mean()
            
        return map_pool
    
        


class UsoEjemCSV:
    
    def __init__(self,n):
        self.n = n
    
    pass

    
    
    

        
        
    
    
    
