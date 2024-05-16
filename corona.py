import csv
import matplotlib.pyplot as plt
import datetime
plt.figure(figsize=(16,4))
plt.title('Covid 19',color='magenta')
deutschland = []
bundesland = []
kreis = []
##########################################################################################

with open('RKI_History.csv','rb') as csv_history:
    file_reader = csv.reader(csv_history,delimiter =',')
#AdmUnitId BundeslandId Datum                  AnzFallNeu AnzFallVortag AnzFallErkrankung AnzFallMeldung KumFall ObjectId
# 0            0        2020/11/06 00:00:00+00  0         21579         8550             10663           656750    1
# 5            5        2021/09/10 00:00:00+00  0         2868          1303             1154            926058   4656
# 5158         5        2020/11/17 00:00:00+00  0         85            42               55              5963     70801

    headrow = next(file_reader) # split the header
    for row in file_reader:
        if row[0] == '0': #AdmUnitId 0 == deutschland
            deutschland.append([row[2].split(' ')[0],row[7]])
        if row[0] == '5': #AdmUnitId 5 == Nordrhein-Westfalen
            bundesland.append([row[2].split(' ')[0],row[7]])
        if row[0] =='5158': #AdmUnitId 5158 == Kreis Mettmann
            kreis.append([row[2].split(' ')[0],row[7]])
    deutschland = sorted(deutschland)
    bundesland = sorted(bundesland)
    kreis = sorted(kreis)
#########################################################################################
        #    Datum      KumFall
        #['2020/11/06','656750']
d_x = [datetime.datetime.strptime(item[0],'%Y/%m/%d').date() for item in deutschland ]
d_y = [int(item[1]) for item in deutschland]
b_x =  [datetime.datetime.strptime(item[0],'%Y/%m/%d').date() for item in bundesland ]
b_y = [int(item[1]) for item in bundesland]
k_x =  [datetime.datetime.strptime(item[0],'%Y/%m/%d').date() for item in kreis ]
k_y = [int(item[1]) for item in kreis]
###########################################################################################
plt.plot(d_x,d_y,label='Deutschland')
plt.plot(b_x,b_y,label='Nordrhein-Westfalen')
plt.plot(k_x,k_y,label='Kreis Mettmann')
##########################################################################################
plt.xlabel('Datum',color='red')
plt.ylabel('Kumulative Fall',color='blue')
plt.text(datetime.datetime(2022,2,15),23000000,f'{d_y[-1]}')
plt.text(datetime.datetime(2022,3,1),5200000,f'{b_y[-1]}')
plt.text(datetime.datetime(2022,3,15),400000,f'{k_y[-1]}')
plt.legend()
plt.grid()
plt.show()