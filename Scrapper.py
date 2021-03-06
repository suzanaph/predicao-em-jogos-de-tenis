from lxml import html
from bs4 import BeautifulSoup 
import requests
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import pandas as pd

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
 
def getTd(word):
    try:
        return soup.find(text=word).parent.parent.find('td').contents[0]
    except AttributeError:
        return ''

def getTdSeasons(word):
    try:
        return soup.findAll(text=word)[1].parent.parent.find('td').find('span').contents[0]
    except AttributeError:
        return ''

def getTdSpan(word):
    try:
        return soup.find(text=word).parent.parent.find('td').find('span').contents[0]
    except AttributeError:
        return ''


def getTdA(word):
    try:
        return soup.find(text=word).parent.parent.find('td').find('a').contents[0]        
    except AttributeError:
        return ''

def getTdProgress(word):
    try:
        return soup.find(id='playerPerformance').find(text=word).parent.parent.find(class_='pct-data').contents[0]       
    except AttributeError:
        return ''

def getTdStats(word):
    try:
        if soup.find(id='playerStatsTab').find(text=word).parent.parent.findAll('th')[0].find('a'):            
            return soup.find(id='playerStatsTab').find(text=word).parent.parent.findAll('th')[0].find('a').contents[0]  
        else:
            if soup.find(id='playerStatsTab').find(text=word).parent.parent.parent.name == 'thead':
                return soup.find(id='playerStatsTab').findAll(text=word)[1].parent.parent.findAll('th')[0].contents[0]
            else:  
                return soup.find(id='playerStatsTab').find(text=word).parent.parent.findAll('th')[0].contents[0]           
    except AttributeError:
        return ''
    
def getPlayersData():
    #settings
    url = 'https://www.ultimatetennisstatistics.com/playerProfile?playerId='
    df = pd.read_csv('top50_atp_13-02-2019.csv', sep=';')
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    
    #necessário pois páginas são diferentes para cada jogador
    #profile header
    profile_header = ['Player_id', 'Player', 'Age', 'Country', 'Height', 'Weight', 'Plays', 'Backhand', 'Turned_Pro', 'Seasons', 'Active', 
            'Prize_Money', 'Titles', 'Grand_Slam', 'Masters', 'Finals', 'Current_Rank', 'Best_Rank', 
            'Current_Elo_Rank', 'Best_Elo_Rank', 'Pick_Elo_Rank', 'Goat_Rank']      
     
        
    #go to performance tab
    playerid = df.iloc[[0]].player_id[0]
    driver.get(url+str(playerid))  

    #performance header
    button  = driver.find_element_by_id("performancePill")
    driver.execute_script("arguments[0].click()", button)
    time.sleep(1)
    global soup    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tds = soup.find(id='playerPerformance').findAll('td')
    performance_header = []
    for td in tds:
        performance_header.append(td.contents[0])
    #until score breakdown
    performance_header = performance_header[0:performance_header.index('Best of 5: 0:3')+1]

    #stats header
    button  = driver.find_element_by_id("statisticsPill")
    driver.execute_script("arguments[0].click()", button)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tds = soup.find(id='playerStatsTab').find(class_='tab-content').findAll('td')
    stats_header = []
    for td in tds:
        stats_header.append(td.contents[0])
    stats_header = list(set(stats_header))
        
    data = []
    data.append(profile_header+[item.replace(' ', '_') for item in performance_header]+[item.replace(' ', '_') for item in stats_header])
   
    for playerid in df.player_id:        
        data_player = []
        #profile data
        driver.get(url+str(playerid))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        player_name = df.loc[df.player_id== playerid].iloc[0].player_name
        print(player_name)
        data_player.extend([str(playerid), player_name, getTd('Age'), getTdSpan('Country'), getTd('Weight'), getTd('Height'), getTd('Plays'),
                getTd('Backhand'), getTd('Turned Pro'), getTdSeasons('Seasons'), getTd('Active'), getTd('Prize Money'),
                getTdA('Titles'), getTdA('Grand Slams'), getTdA('Masters'), getTdA('Tour Finals'),
                getTd('Current Rank'), getTd('Best Rank'), getTd('Current Elo Rank'), getTd('Best Elo Rank'),
                getTd('Peak Elo Rating'), getTd('GOAT Rank')])
        #performance data
        button  = driver.find_element_by_id("performancePill")
        driver.execute_script("arguments[0].click()", button)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for header in performance_header:
            data_player.append(getTdProgress(header))
        
        
        #stats data
        button  = driver.find_element_by_id("statisticsPill")
        driver.execute_script("arguments[0].click()", button)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for header in stats_header:           
            data_player.append(str(getTdStats(header)))
        [item.replace('\n', '') for item in data_player]
        data.append(data_player)
        

    
    #TODO: RESULT BREAKDOWN

 
    #Save to CSV
    filename = 'players_stats_' + str(datetime.datetime.today().__format__('%d-%m-%Y'))    
    print('Writing Csv')
    np.savetxt(filename+".csv", data, delimiter=";", fmt='%s', encoding='utf-8')
    print('Csv writed')

    return

soup = ''
getRanking(100)