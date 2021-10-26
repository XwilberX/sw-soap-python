#!/usr/bin/env python

# -*- coding: utf-8 -*-

 

from suds.client import Client  # Importe la clase Client en el módulo suds.client

 

wsdl_url = "http://localhost:8000/?wsdl"

 

 

def say_hello_test(url, name, times):

    client = Client(url)                    # Crear un objeto de interfaz de servicio web

    res = client.service.sum(2, 3)   # Llame al método getMobileCodeInfo en esta interfaz y pase los parámetros

   

    # print (req)       # Mensaje de solicitud de impresión

    print (res)  # Imprimir mensaje de retorno


if __name__ == '__main__':

    say_hello_test(wsdl_url, 'Milton', 2)