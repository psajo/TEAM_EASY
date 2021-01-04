import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mydao
import matplotlib.font_manager as fm




class MyVisualize(mydao.MyDAO) :
    def getLeagueEntrys(self):
        self.connectDB()
        sql = "SELECT summonerName, char_length(replace(summonerName, ' ','')), tier FROM leagueEntryDto WHERE rank='I'"
        self.cur.execute(sql)
        rows =self.cur.fetchall()
        self.closeDB()
        return rows

if __name__ == '__main__':
    # import matplotlib
    # import matplotlib.font_manager as fm
    # fm.get_fontconfig_fonts()
    # # font_location = '/usr/share/fonts/truetype/nanum/NanumGothicOTF.ttf'
    # font_location = 'C:/WINDOWS/Fonts/NanumGothic.ttf'  # For Windows
    # font_name = fm.FontProperties(fname=font_location).get_name()
    # matplotlib.rc('font', family=font_name)
    tiers = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
    mv = MyVisualize()
    rows = mv.getLeagueEntrys()
    df1 =pd.DataFrame(rows,columns=['summonerName','length of Name','tier'])
    plt.subplots(figsize=(12, 5))
    ax =sns.barplot(data=df1, order=tiers ,x='tier', y='length of Name')
    ax.set_title('average length of summonerName by tier')

    plt.show()
