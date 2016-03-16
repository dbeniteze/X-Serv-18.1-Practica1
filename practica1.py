#! /usr/bin/python
#! -*- coding: utf-8 -*-

import webapp, sys, urllib

class RecortaUrls(webapp.webApp):

    num_secuencia = -1
    real_a_corta = {}
    corta_a_real = {}
    
       
    def recortador(self,direcc):
        self.num_secuencia = self.num_secuencia + 1
        recortada = "http://" + direcc + "/" + str(self.num_secuencia)
        return(recortada)
        
    def imprimeHTML(self):
        """Formulario con las urls introducidas y las acortadas"""
        html = ""
        for keys, values in self.real_a_corta.iteritems():
            html = (html
            + "<a href=" + keys + ">"
            + keys + "</a>" 
            + " ==> " 
            + "<a href=" + keys + ">"
            + values + "</a><br>")
        return html
            

    def parse(self, request):
        """Parsea la solicitud y extrae la informacion relevante"""

        metodo = request.split()[0]
        url = request.split("\n")[1].split()[1]
        recurso = request.split()[1]
        body = request.split("\r\n\r\n")[1]
        return (metodo, url, recurso, body)


    def process(self, parsedRequest):
        
        metodo, url, recurso, body = parsedRequest

        if metodo == "GET":
            if recurso == "/":
                httpCode = "200 OK"
                httpBody = ("<html><body><form action='/' method='POST'>"
                            + "Recorte una URL <br>"
                            + "<input type='text' name='url'/></br>"
                            + "<input type='submit' value='Recorta URL' "
                            + "/></form><br><br>"
                            + "<h2>Anteriores URLs acortadas</h2>"
                            + self.imprimeHTML()
                            + "</body></html>")
            else:
                num_recurso = int(recurso.split("/")[1])
                print num_recurso
                print self.corta_a_real
                if self.corta_a_real.has_key(num_recurso):
                      httpCode = "301"
                      httpBody = ("<html><body><meta http-equiv='refresh'"
                                + "content='0;" + " url="
                                + self.corta_a_real[num_recurso]
                                + "' /></body></html>")
                else:
                    
                    httpCode = "404 Not Found"
                    httpBody = ("<html><body><h3>"
                                + "404 Recurso no disponible"
                                + "</h3></body></html>")
                            
        elif metodo == "POST":
            if recurso == "/":
                httpCode = "200 OK"
                direccion = urllib.unquote(body.split("=")[1])
                prueba = direccion.split("://")[0]
                url = "http://" + url
                if prueba != "http":
                    direccion = "http://" + direccion
                   
                if not self.real_a_corta.has_key(direccion):
                    url_acortada = self.recortador(url)
                    self.real_a_corta[direccion] = url_acortada
                    self.corta_a_real[self.num_secuencia] = direccion
                    httpBody = ("<html><body>" 
                                + "<a href=" + direccion + ">"
                                + direccion + "</a>"  
                                + " ==> " 
                                + "<a href=" + direccion + ">"
                                + url_acortada + "</a><br>"
                                + '<input type="button" value="Inicio"'
                                + 'onClick="location.href' + "='" + url + "'"
                                + '"/></body></html>')
                      
                else:
                    
                    httpBody = ("<html><body><h3>URL ya acortada \n</h3>" 
                                + "<a href=" + direccion + ">"
                                + direccion + "</a>"
                                + " ==> " 
                                + "<a href=" + direccion + ">"
                                + self.real_a_corta[direccion] + "</a><br>"
                                + '<input type="button" value="Inicio"'
                                + 'onClick="location.href' + "='" + url + "'"
                                + '"/></body></html>')
                          
        else:
            httpCode = "405 Method Not Allowed"
            httpBody = ("<html><body><h3>405 Metodo " 
                        + metodo
                        + " no permitido</h3></body></html>")
                            
                            
        return (httpCode,httpBody)
       
if __name__ == '__main__':
    try:
        testRecortaUrls = RecortaUrls("localhost", 1234)
    except KeyboardInterrupt:
        sys.exit()

