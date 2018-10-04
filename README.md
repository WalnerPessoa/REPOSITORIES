#### REPOSITORIES
Materiais de estudo em Python
###### RASPAR TODO O SITE #### CODIGO COMPLETO 

### -*- coding: utf-8 -*-

### 3/outubro/2018


import requests  
import datetime
from bs4 import BeautifulSoup as bs # não está no tutorial
import time
import csv
from datetime import datetime as dt

localtime = time.localtime(time.time())




from time import sleep
#sleep(0.1) # Time in seconds.


indice_entidade=0
indice_noticia=0

##############
session_requests = requests.Session()
referer_url = "http://cni.empauta.com/e2/" 

#######  PROBLEMA NA DATA ===>   date(2018,5,20)

data_inicio = datetime.date(2018,5,25)



filename = "cni_empauta"+str(data_inicio)+".csv"

f = open(filename,"w", encoding='utf-8')
###f = open(filename,"w", encoding='iso-8859-1')

headers = "ENTIDADE;NUM_NOTICIA;DATA;HORA;VEÍCULO;SEÇÃO;ESTADO;TITULO;LINK\n"
f.write(headers)
#### 269 DIAS DO ANO
for i in range(1, 70):
    delta = datetime.timedelta(days=i)
    data = data_inicio + delta
    nova_data  = dt.strftime(data, '%Y%m%d')
    print (nova_data)
    url = "http://cni.empauta.com/e2/?setdata="+nova_data
    #########
    headers_cni={"referer":"http://cni.empauta.com/e2/",  "cookie":"SESSIP=192.168.109.246; PHPSESSID=vs6sipdc5k6ct7auparbtph008; _eus=6690; __utmc=7507693; __utmz=7507693.1535492475.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); SESSIP=192.168.109.247; cod_cookie=60872943; cod_cookie_17=60872943; __utma=7507693.273240049.1535492475.1538660901.1538672459.57"}
    
    sleep(150)
    
    result = session_requests.get(url,headers = headers_cni)
    s = bs(result.content, 'html.parser')  
    ###############
    
    ##############
    all_noticias = s.findAll("div",{"class":"info-section"}) ## primeiro nível

    #
    # variável << all_noticias >> é o array para classe:"info-section" => entidades + notícias
    #
    
    lista_entidades = [] # contruir array
    for k in all_noticias[0:]: lista_entidades.append(k.find("div",{"class":"info-section-title"})) # contruir array
    #
    # variável << lista_entidades >> é array para classe: "info-section-title" = nome da entidade
    #
    print("ARRAY ENTIDADES:  ",len(all_noticias))
    inicio = time.time()
    
    print('***********> resposta servidor: '+str(result))
    
    for indice_entidade in range(0, len(lista_entidades)):
        lista_noticia = all_noticias[indice_entidade].findAll("div",{"class":"noticia"}) # indice 0 => NOTICIA 1
        #
        # variável << lista_noticia >> é o array para classe:"noticia" = notícia individual
        #
        # variável << indice_entidade >> é o incremento para classe: "info-section-title" = nome da entidade
        #
        #
        for indice_noticia in range(0, len(lista_noticia)):
            #
            # variável << indice_noticia >> é o incremento para classe:"noticia"
            #
            inicio = time.time()

            print("===============================>",indice_entidade,"   -    ", indice_noticia)

            entidade = lista_entidades[indice_entidade].text
            num_noticia = indice_noticia+1
            print("Quantidade de notícias em",entidade, " é de ", len(lista_noticia))
            print("Notícia número: ",num_noticia)

           
            data = lista_noticia[indice_noticia].find("span",{"class":"data"}).text.replace('\n', '').replace('\r', '').replace(';', '')
            print("Data: ",data)
            veiculo = lista_noticia[indice_noticia].find("span",{"class":"nome_veiculo"}).text.replace('\n', '').replace('\r', '').replace(';', '')
                      
            try:
                secao = lista_noticia[indice_noticia].find("span",{"class":"secao"}).text.replace('\n', '').replace('\r', '').replace(';', '')
                print ("seção: ",secao)

            except : 
                secao = ""
                print (indice_noticia," - Ausente")

            estado = lista_noticia[indice_noticia].find("span",{"class":"sigla"}).text.replace('\n', '').replace('\r', '').replace(';', '')
            print("Estado: ",estado)
       
            href=lista_noticia[indice_noticia].find("div",{"class":"titulo-noticia"}).a
            
            link=url+href['href']
            titulo=href.text.replace('\n', '').replace('\r', '').replace(';', '')

            fim = time.time()
            data_consulta = time.strftime("%d/%m/%Y", time.localtime())
            hora_consulta = time.strftime("%H:%M:%S", time.localtime(time.time()))

            f.write(entidade + ";" + str(num_noticia) +";"+ data +";"+hora_consulta+";"+ veiculo +";"+secao +";"+estado +";"+ titulo +";"+ link +"\n")
f.close()

##### fim codigo
