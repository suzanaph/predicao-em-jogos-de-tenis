from lxml import html
from bs4 import BeautifulSoup 
import requests
import numpy as np
from selenium import webdriver
import time
import datetime



start_year = '2000'
end_year = '2018'

def tournaments_info_to_str(td):
    td = td.replace('\\r', '')
    td = td.replace('\\n', '')
    td = td.strip()
    return td

"""
    Function to get tournaments info of a specific year
"""
def tournaments(year):

    year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
    soup = BeautifulSoup(requests.get(year_url).content, 'lxml')
    trs = soup.findAll('tr', class_='tourney-result')
    tourns = []        
    #foreach tournaments
    for tr in trs:
        title = tournaments_info_to_str(tr.find(class_='tourney-title').contents[0])
        location = tournaments_info_to_str(tr.find(class_='tourney-location').contents[0])
        date = tournaments_info_to_str(tr.find(class_='tourney-dates').contents[0])
        tds = tr.findAll(class_='tourney-details')
        qtd = tournaments_info_to_str(tds[0].find(class_='item-value').contents[0])
        surface = tournaments_info_to_str(tds[1].find(class_='item-value').contents[0])
        typeCourt = tournaments_info_to_str(tds[1].find(class_='item-details').contents[0])
        prize = tournaments_info_to_str(tds[2].find(class_='item-value').contents[0])
        winner_tag = tds[3].find(class_ = 'tourney-detail-winner')
        if(winner_tag.find('a')):
            winner = tournaments_info_to_str(winner_tag.find('a').contents[0])
        else:
            winner = ''    
        tourns.append([title, location, date, qtd, surface, typeCourt, prize, winner])
    return tourns


def getTournamentsData():
    tournaments_data = []
    tournaments_data += [['title', 'location', 'date', 'players', 'surface', 'court_type', 'prize', 'winner']]
    for y in range(int(start_year), int(end_year) + 1):
        year = str(y)  
        print('Getting '+year+' data')   
        tournaments_data += tournaments(year)
    filename = 'tournaments_' + start_year + '-' + end_year
    print('Writing Csv')
    np.savetxt(filename+".csv", tournaments_data, delimiter=";", fmt='%s', encoding='utf-8')
    print('Csv writed')

def getRanking(limit):
    driver = webdriver.Chrome()
    driver.get('https://www.ultimatetennisstatistics.com/rankingsTable')
    ranking = 0
    players = []
    players += [['ranking', 'player_id', 'player_name']]
    while ranking <= limit:           
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find(id='rankingsTable')
        trs = table.find('tbody').findAll('tr')
        for tr in trs:
            player = tr.findAll('td')[3].find('a').contents[0]
            playerid = tr.findAll('td')[3].find('a', href=True)
            playerid = playerid['href'].split('=')[1]            
            ranking = int(tr.findAll('td')[0].contents[0].strip())
            players += [[ranking, playerid, player]]
            if ranking > 50:
                break
        #CLICAR NA PAGINACAO
        button_next = driver.find_element_by_class_name("pagination").find_element_by_class_name("next")
        button = button_next.find_element_by_tag_name("a")
        driver.execute_script("arguments[0].click()", button)
        time.sleep(5)
    #ESCREVER NO CSV    
    filename = 'top50_atp_' + str(datetime.datetime.today().__format__('%d-%m-%Y'))    
    print('Writing Csv')
    np.savetxt(filename+".csv", players, delimiter=";", fmt='%s', encoding='utf-8')
    print('Csv writed')
 

    
def getPlayersData():
    #Ler CSv
    # adicionar a um panda
    #buscar infos na pagina referente a cada player

    return

getRanking(50)