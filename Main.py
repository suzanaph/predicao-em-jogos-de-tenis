import RankingScrapper as rs
import PlayerScrapper as ps
import pandas as pd



#rs.getMaleRanking(200)

players = pd.read_csv("top200_atp_09-11-2019.csv", sep=";")
#ps.getGeneralData(players)
#ps.getPerformanceData(players)
ps.getStatisticsData(players)

