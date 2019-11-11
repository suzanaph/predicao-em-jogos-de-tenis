from lxml import html
from bs4 import BeautifulSoup 
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import Util


def td(feature):
    try:
        return soup.find(text=feature).parent.parent.find('td').contents[0]
    except Exception as e:
        return ''


def tdSpan(feature):
    try:
        return soup.find(text=feature).parent.parent.find('td').find('span').contents[0]
    except Exception as e:
        return ''

def tdA(feature):
    try:
        return soup.find(text=feature).parent.parent.find('td').find('a').contents[0]        
    except Exception as e:
        return ''


def tdSeasons(feature):
    try:
        return soup.findAll(text=feature)[1].parent.parent.find('td').find('span').contents[0]
    except Exception as e:
        return ''

def tdProgress(feature):
    try:
        return soup.find(id='playerPerformance').find(text=feature).parent.parent.find(class_='pct-data').contents[0]       
    except Exception as e:
        return ''

def tdStats(feature):
    try:
        if soup.find(id='playerStatsTab').find(text=feature).parent.parent.findAll('th')[0].find('a'):            
            return soup.find(id='playerStatsTab').find(text=feature).parent.parent.findAll('th')[0].find('a').contents[0]  
        else:
            if soup.find(id='playerStatsTab').find(text=feature).parent.parent.parent.name == 'thead':
                return soup.find(id='playerStatsTab').findAll(text=feature)[1].parent.parent.findAll('th')[0].contents[0]
            else:  
                return soup.find(id='playerStatsTab').find(text=feature).parent.parent.findAll('th')[0].contents[0]           
    except Exception as e:
        return ''

def getGeneralData(players):
    #settings
    url = 'https://www.ultimatetennisstatistics.com/playerProfile?playerId='
    driver = webdriver.Chrome(ChromeDriverManager().install())

    general_features = ['player_id', 'player_name', 'age', 'country', 'height', 'weight', 'favorite_hand', 'backhand', 'turned_Pro', 
                        'seasons', 'is_active', 'prize_money', 'titles', 'grand_slams', 'masters', 'finals', 'current_rank', 'best_rank'] 
    data = []
    data.append(general_features)

    for index, row in players.iterrows(): 

        print('Getting general data for '+row.player_name+' number: '+str(index))
        player_id = row.player_id
        driver.get(url+str(player_id))
        global soup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        data_player = [player_id, row.player_name, td('Age'), tdSpan('Country'), td('Weight'), td('Height'), td('Plays'),
                td('Backhand'), td('Turned Pro'), tdSeasons('Seasons'), td('Active'), td('Prize Money'),
                tdA('Titles'), tdA('Grand Slams'), tdA('Masters'), tdA('Tour Finals'), td('Current Rank'), td('Best Rank')]
        data.append(data_player)

    filename = 'players_general_' + str(datetime.datetime.today().__format__('%d-%m-%Y'))
    Util.saveDFtoCSV(data, filename)


def getPerformanceData(players):
    #settings
    url = 'https://www.ultimatetennisstatistics.com/playerProfile?playerId='
    driver = webdriver.Chrome(ChromeDriverManager().install())
  
    #performance header
    driver.get(url+str(players.iloc[0].player_id))
    button  = driver.find_element_by_id("performancePill")
    driver.execute_script("arguments[0].click()", button)
    time.sleep(1)
    sp = BeautifulSoup(driver.page_source, 'lxml')
    tds = sp.find(id='playerPerformance').findAll('td')
    header = []
    header.append('player_id')
    for td in tds:
        header.append(td.contents[0])
    #TODO tratar nomes do header

    data = []
    data.append(header)

    for index, row in players.iterrows():
        repeat = False
        counter = 0 
        while(not(repeat)):
            print('Getting performance data for '+row.player_name+' number: '+str(index))
            
            player_id = row.player_id
            driver.get(url+str(player_id))
            button  = driver.find_element_by_id("performancePill")
            driver.execute_script("arguments[0].click()", button)
            time.sleep(1)
            global soup
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            rowToAppend = []
            rowToAppend.append(player_id)
            for attr in header[1:]:
                rowToAppend.append(tdProgress(attr))
            if (rowToAppend[1] != ''):
                repeat = True
                data.append(rowToAppend)
            if (counter >= 5):
                repeat = True
            counter += 1

    filename = 'players_performance_' + str(datetime.datetime.today().__format__('%d-%m-%Y'))
    Util.saveDFtoCSV(data, filename)


def getStatisticsData(players):
    #settings
    url = 'https://www.ultimatetennisstatistics.com/playerProfile?playerId='
    driver = webdriver.Chrome(ChromeDriverManager().install())
  
    # statistics header
    driver.get(url+str(players.iloc[0].player_id))
    button  = driver.find_element_by_id("statisticsPill")
    driver.execute_script("arguments[0].click()", button)
    time.sleep(1)
    sp = BeautifulSoup(driver.page_source, 'lxml')
    tds = sp.find(id='playerStatsTab').find(class_='tab-content').findAll('td')
    header = []
    header.append('player_id')
    for td in tds:
        header.append(td.contents[0])
    #TODO tratar nomes do header

    data = []
    data.append(header)

    for index, row in players.iterrows(): 

        repeat = False
        counter = 0 
        while(not(repeat)):
            print('Getting stats data for '+row.player_name+' number: '+str(index))
        
            player_id = row.player_id
            driver.get(url+str(player_id))
            button  = driver.find_element_by_id("statisticsPill")
            driver.execute_script("arguments[0].click()", button)
            time.sleep(1)
            global soup
            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            rowToAppend = []
            rowToAppend.append(player_id)
            for attr in header[1:]:
                rowToAppend.append(str(tdStats(attr)))
            if (rowToAppend[1] != ''):
                repeat = True
                data.append(rowToAppend)
            if (counter >= 5):
                repeat = True
            counter += 1

    filename = 'players_stats_' + str(datetime.datetime.today().__format__('%d-%m-%Y'))
    Util.saveDFtoCSV(data, filename)