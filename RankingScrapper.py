# Imports
from lxml import html
from bs4 import BeautifulSoup 
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
#import pandas as pd
import Util


def getMaleRanking(limit):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.ultimatetennisstatistics.com/rankingsTable')
    ranking = 0
    players = []

    # SET HEADER
    players += [['ranking', 'player_id', 'player_name']]
    
    while ranking <= limit:           
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find(id='rankingsTable')
        trs = table.find('tbody').findAll('tr')
        for tr in trs:
            player = tr.findAll('td')[3].find('a').contents[0]
            playerid = tr.findAll('td')[3].find('a', href=True)['href'].split('=')[1]          
            ranking = int(tr.findAll('td')[0].contents[0].strip())
            # ADD PLAYER
            players += [[ranking, playerid, player]]
            if ranking >= limit:
                break
        #PROXIMA PAGINA
        button_next = driver.find_element_by_class_name("pagination").find_element_by_class_name("next")
        button = button_next.find_element_by_tag_name("a")
        driver.execute_script("arguments[0].click()", button)
        time.sleep(5)

    #SALVA CSV    
    filename = 'top'+ str(limit) + '_atp_' + str(datetime.datetime.today().__format__('%d-%m-%Y'))    
    Util.saveDFtoCSV(players, filename)