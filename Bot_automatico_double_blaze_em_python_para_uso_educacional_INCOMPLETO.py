from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from bs4 import BeautifulSoup
import pyautogui
import pyperclip
import clipboard
import requests
import threading



url ="https://blaze-1.com/pt/games/double"
headers='Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
#Entrando no site
option = Options()
option.add_argument(f"--user-agent={headers}")
option.binary_location=(r"C:\portapps\brave-portable\app\brave.exe")

driver= webdriver.Chrome(options=option)
driver.get(url)
time.sleep(5)

#Colocando os dados
click_botao_entrar= driver.find_element(by=By.XPATH, value="//*[@id='header']/div[2]/div/div[2]/div/div/div[1]")
click_botao_entrar.click()
time.sleep(3)
email_entrada= driver.find_element(by=By.XPATH,value="//*[@id='auth-modal']/div/form/div[1]/div/input")
email_entrada.send_keys()

senha_entrada= driver.find_element(by=By.XPATH,value="//*[@id='auth-modal']/div/form/div[2]/div/input")
senha_entrada.send_keys()
time.sleep(1)

botao_click= driver.find_element(by=By.XPATH, value="//*[@id='auth-modal']/div/form/div[4]/button")
botao_click.click()
time.sleep(15)

#Definindo os botões

botao_aposta_preto= driver.find_element(by=By.XPATH, value="//*[@id='roulette-controller']/div[1]/div[2]/div[2]/div/div[3]")
botao_aposta_preto.click()
time.sleep(1)

botao_aposta_branco= driver.find_element(by=By.XPATH, value="//*[@id='roulette-controller']/div[1]/div[2]/div[2]/div/div[2]")
botao_aposta_branco.click()
time.sleep(1)

botao_aposta_vermelho= driver.find_element(by=By.XPATH, value="//*[@id='roulette-controller']/div[1]/div[2]/div[2]/div/div[1]")
botao_aposta_vermelho.click()
time.sleep(1)

click_botao_jogar=driver.find_element(by=By.XPATH, value="//*[@id='roulette-controller']/div[1]/div[3]/button")
click_botao_jogar.click()
time.sleep(1)

#Aqui fazer um TRY, para verificar se entrou ou não na conta e se vai ter a quantia minima para rodar
saldo=driver.find_element(by=By.XPATH, value="//*[@id='header']/div[2]/div/div[2]/div/div[3]/div/a/div/div/div[1]").get_attribute("outerHTML")
soup=BeautifulSoup(saldo, "html.parser")
saldo_real= soup.get_text()
#print(saldo_real)
time.sleep(1)


def loop_para_pegar_dados():
    #Fazendo o check da barra e pegando o valor que caiu
    condicao_girando_em='class="progress-bar"'
    condiacao_girando='class="time-left">Girando...</div>'
    condicao_resultado='class="time-left">Blaze'
    
    while True:

        barra_de_progresso= driver.find_element(by=By.XPATH,value="//*[@id='roulette-timer']/div")
        barra_de_progresso_resultado_com_print= barra_de_progresso.get_attribute("outerHTML").split()
        #print(barra_de_progresso_resultado_com_print)
        time.sleep(2)
        
        if condicao_girando_em == barra_de_progresso_resultado_com_print[1]:
            #print(barra_de_progresso_resultado_com_print)
            time.sleep(2)
        elif condiacao_girando == barra_de_progresso_resultado_com_print[1]:
            #print(barra_de_progresso_resultado_com_print)
            time.sleep(2)
        elif condicao_resultado == barra_de_progresso_resultado_com_print[2]:
            dados_resultado= barra_de_progresso_resultado_com_print
            print(dados_resultado)
            time.sleep(2)
        else:
            print("ERROR")
            time.sleep(2)

#Chamando o LOOP para ficar em segundo plano
thread = threading.Thread(target=loop_para_pegar_dados)
thread.start()

#Fazendo os calculos para mandar o valor de apostar

def base_de_calculo():
    dados_resultado ="7"
    valor_calculado = 0.1
    while True:
               
        valor_aposta = driver.find_element(by=By.XPATH, value="//*[@id='roulette-controller']/div[1]/div[2]/div[1]/div/div[1]/input")
        valor_aposta.send_keys(valor_calculado)
                
       #ATENÇÃO: OLHAR O JEITO QUE OS DADOS VEM
        if dados_resultado <= "7":
            valor_calculado = valor_calculado *2
        elif dados_resultado >= "8" :
            valor_calculado = 0.1
        elif dados_resultado == "0":
            valor_calculado = valor_calculado *2
        else:
            print("EROO NA BASE DE CALCULO  ")    
            pass

        click_botao_jogar=driver.find_element(by=By.XPATH, value="//*[@id='roulette-controller']/div[1]/div[3]/button")
        click_botao_jogar.click()
        time.sleep(2)
            
       

print("passou")

thread_c = threading.Thread(target=base_de_calculo)
thread_c.start()

print("Código rodando")

time.sleep(1)

driver.quit()
