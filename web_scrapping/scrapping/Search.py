from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from web_scrapping.scrapping.util import Util

import time


## Clase de Dia 
##### Esta calase contendra toda logica para buscar los productos en el supermercado Dia
class SearchDia(Util):
    def SearchDiaName(self):
        self.driver.get('https://www.dia.es/compra-online/')
        #Acciones basicas para acceder a los productos
        ## Aceptamos las cookies
        btn_cookie = self.obtenerXpath('//*[@id="onetrust-accept-btn-handler"]')
        time.sleep(3)
        btn_cookie.click()
        
        ## Buscamos el producto
        search_input = self.obtenerXpath('//*[@id="app"]/div/div/div/div[1]/div[1]/div[2]/div/input')
        search_input.send_keys(self.product_name)
        ## Nos dirigimos a la pagina de los productos
        search_button = self.obtenerXpath('//*[@id="app"]/div/div/div/div[1]/div[1]/div[2]/div/button')
        search_button.click()
        # Parte donde recogeremos la informacion de los productos
        resultado = self._ComprobacionDia()
        return resultado
    # Vamos uno a uno para recoger los 5 primeros productos que aparezcan en la pagina
    def _ComprobacionDia(self):
            lista = []
            lista_productos = len(self.ObtenerListaElementosClassName('search-product-card-list__item-container'))
            for index in range(lista_productos):
                #Metodo para saltarse la publicidad.
                #TODO: Posible Modificacion
                if index == 7:
                    continue
                if lista_productos>=index and index < 16:
                        self._RecuperarProductosDia(index, lista)

            return lista
    #Recuperamos la informacion del producto 
    def _RecuperarProductosDia(self, index, lista):
            index += 1
        
            title = self.obtenerClassNames("search-product-card__product-name")[index].text
            imagen = self.obtenerClassNames("search-product-card__product-image")[index].get_attribute('src')
            precio = self.obtenerClassNames("search-product-card__active-price")[index].text
            if "\n" in precio:
                new_precio = precio.split("\n")
                precio = new_precio[1]
            resultado = (title, precio, imagen)
            lista.append(resultado)


## Clase Carrefour
##### Esta clase contendra toda logica para buscar los productos en el supermercado Carrefour
class SearchCarrefour(Util):
    def SearchCarrefourName(self):
        self.driver.get('https://www.carrefour.es/?gclid=Cj0KCQiAgaGgBhC8ARIsAAAyLfHJZAkh3PZU6zJ6jhoAhxnOvsCcPahmWyNHF4xUuQiT2F9gBk3rdloaAkgGEALw_wcB&gclsrc=aw.ds')
        #Acciones basicas para acceder a los productos
        ## Aceptamos las cookies
        btn_cookie = self.obtenerXpath('//*[@id="onetrust-accept-btn-handler"]')
        btn_cookie.click()
        # A la hora de buscar hay dos inputs diferentes el segundo se crea cuando clickamos el primero
        input_text_search_parent = self.obtenerXpath('//*[@id="search-input"]')
        input_text_search_parent.click()
        # Introducimos el texto en el segundo input
        input_text_search_child = self.obtenerXpath('//*[@id="empathy-x"]/header/div[1]/div/input[3]')
        input_text_search_child.send_keys(self.product_name)
        ## Nos dirigimos a la pagina de los productos
        button_submit = self.obtenerXpath('//*[@id="empathy-x"]/header/div/button[1]')
        button_submit.click()
        resultado = self._ComprobarCarrefour()        
        return resultado

    def _ComprobarCarrefour(self):
        lista = []
        try:
            lista_productos = self.ObtenerListaElementos('//*[@id="ebx-grid"]/article')
        except:
            lista_productos = []
        if len(lista_productos)>0:
            for index in (range(len(lista_productos))):
                if index <3 and len(lista_productos)>=index:
                    self._RecuperarProductosCarrefour(index, lista)
                if 3 >=len(lista_productos) and index<=len(lista_productos):
                    self._RecuperarProductosCarrefour(index, lista)

            
        return lista
        #Recuperamos la informacion del producto 
    def _RecuperarProductosCarrefour(self, index, lista):
            title = self.obtenerClassNames("ebx-result__title")[index].text 
            imagen = self.obtenerClassNames("ebx-result-figure__img")[index].get_attribute('src')
            precio = self.obtenerClassNames("ebx-result-price__value")[index].text
            resultado = (title, precio, imagen)
            lista.append(resultado)


## Clase AhorraMas
##### Esta clase contendra toda logica para buscar los productos en el supermercado AhorraMas
class SearchAhorraMas(Util):
    def SearchAhorraMasName(self):
        self.driver.get('https://www.ahorramas.com/')
        btn_cookies = self.obtenerXpath('//*[@id="onetrust-accept-btn-handler"]')
        btn_cookies.click()
        # Introducimos el texto en el input
        input_text = self.obtenerClassName('search-field')
        input_text.click()
        input_text.send_keys(self.product_name)
        #Clickamos al button de buscar de la página
        search_button = self.obtenerClassName('fa-search')
        search_button.click()
        resultado = self._ComprobarAhorraMas()
        return resultado


    def _ComprobarAhorraMas(self):
        lista = []
        lista_productos = len(self.ObtenerListaElementosClassName('product'))
        listaTitulos = self.ObtenerListaElementosClassName('product-name-gtm')
        listaImagenes = self.ObtenerListaElementosClassName('tile-image')
        for index in range(lista_productos):
            if index <=3 and lista_productos>=index:
                self._RecuperarProductosAhorraMas(index, lista,listaTitulos,listaImagenes)
            if 3 >=lista_productos:
                self._RecuperarProductosAhorraMas(index, lista,listaTitulos,listaImagenes)
        return lista
        
        
        #Recuperamos la informacion del producto 
    def _RecuperarProductosAhorraMas(self, index, lista, listaTitulos, listaImagenes):
            cadena_title = listaTitulos[index]
            title = cadena_title.text
            cadena_image = listaImagenes[index]
            imagen = cadena_image.get_attribute('src')
            index +=1 
            precio = self.obtenerCssSelector(f'#product-search-results > div:nth-child(2) > div.col-sm-12.col-lg-9 > div.row.product-grid > div:nth-child({index}) > div > div > div.tile-body > div.price > div:nth-child(1) > div > span > span')
            resultado = (title, precio[0].text, imagen)
            lista.append(resultado)

class Search(SearchDia, SearchCarrefour, SearchAhorraMas):
    def SearchAll(self):
        resultados_dia = self.SearchDiaName()        
        resultados_carrefour = self.SearchCarrefourName()
        resultados_ahorra_mas = self.SearchAhorraMasName()
        return resultados_dia, resultados_carrefour, resultados_ahorra_mas