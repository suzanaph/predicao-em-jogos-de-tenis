from lxml import html
from bs4 import BeautifulSoup 
import requests
import numpy as np

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

tournaments_data = []
for y in range(int(start_year), int(end_year) + 1):
    year = str(y)  
    print('Getting '+year+' data')   
    tournaments_data += tournaments(year)
data = np.array(tournaments_data)
filename = 'tournaments_' + start_year + '-' + end_year
print('Writing Csv')
np.savetxt(filename+".csv", tournaments_data, delimiter=",", fmt='%s')
print('Csv writed')