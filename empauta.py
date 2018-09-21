#RASPAR TODO O SITE #### CODIGO COMPLETO 

# 20/setembro/2018


import requests  
from bs4 import BeautifulSoup as bs # não está no tutorial
import time
import csv
from datetime import datetime

localtime = time.localtime(time.time())

#now = datetime.now()
###########
################### indice 0 => all_noticias[0] => Entidade 1  - CNI
################### indice 1 => all_noticias[1] => Entidade 2  - SENAI
indice_entidade=0
indice_noticia=0

##############
session_requests = requests.Session()
referer_url = "http://cni.empauta.com/e2/" 
url = "http://cni.empauta.com"# login_url
#url = "http://cni.empauta.com/e2/?setdata=20180919"
headers_cni={"referer":"http://cni.empauta.com/e2/",  "cookie":"SESSIP=192.168.109.247; PHPSESSID=vs6sipdc5k6ct7auparbtph008; _eus=6690; __utmc=7507693; __utmz=7507693.1535492475.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cod_cookie=60513013; cod_cookie_17=60513013; __utma=7507693.273240049.1535492475.1536688451.1536866021.16; SESSIP=192.168.109.247"}
session_requests.post(url, headers = headers_cni)
result = session_requests.get(url,headers = headers_cni)
p = requests.get(url)
s = bs(p.content, 'html.parser')  
###############
filename = "cni_empauta.csv"
f = open(filename,"w")
headers = "ENTIDADE;NUM_NOTICIA;DATA;HORA;VEÍCULO;ESTADO;TITULO;LINK\n"
f.write(headers)
##############
all_noticias = s.findAll("div",{"class":"info-section"})

lista_entidades = [] # contruir array
for k in all_noticias[0:]: lista_entidades.append(k.find("div",{"class":"info-section-title"})) # contruir array

print("ARRAY:  ",len(all_noticias))
inicio = time.time()

for indice_entidade in range(0, len(lista_entidades)):
    #indice_noticia = 
    #for l in range(0, len(lista_noticia)):
    lista_noticia = all_noticias[indice_entidade].findAll("div",{"class":"noticia"}) # indice 0 => NOTICIA 1
    print("===============================>",indice_entidade, "tamanho: ",len(lista_noticia))
    for indice_noticia in range(0, len(lista_noticia)):
        inicio = time.time()
        #lista_noticia = all_noticias[indice_entidade].findAll("div",{"class":"noticia"}) # indice 0 => NOTICIA 1

        print("===============================>",indice_entidade,"   -    ", indice_noticia)

        entidade = lista_entidades[indice_entidade].text
        num_noticia = indice_noticia+1
        print("Quantidade de notícias em",entidade, " é de ", len(lista_noticia))
        print("Notícia número: ",num_noticia)


        identificador_noticia=lista_noticia[indice_noticia].text.split('\n')
        data_noticia=identificador_noticia[1].split('|')
        data = data_noticia[0]
        print("Data: ",data)
        veiculo = data_noticia[1]
        print("Veículo: ",veiculo)
        estado = data_noticia[len(data_noticia)-1]
        print("Estado: ",estado)
        titulo = identificador_noticia[2]
        print("Título: ",titulo)
        href=lista_noticia[indice_noticia].find("div",{"class":"titulo-noticia"}).a
        link=url+href['href']
        print("VALOR: ",link)
        fim = time.time()
        print(fim - inicio)
        data_consulta = time.strftime("%d/%m/%Y", time.localtime())
        hora_consulta = time.strftime("%H:%M:%S", time.localtime(time.time()))
        print(data_consulta)
        print (hora_consulta)
        f.write(entidade + ";" + str(num_noticia) +";"+ data +";"+hora_consulta+";"+ veiculo +";"+ estado +";"+ titulo +";"+ link +"\n")

f.close()


##### fim codigo
