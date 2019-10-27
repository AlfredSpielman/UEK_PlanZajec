from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

# --------------------------------------------------------------------------------------
# tutaj wklej adres do interesującego Cię planu zajęć w odpowiednim przedziale czasowym
PlanZajec_URL = 'http://planzajec.uek.krakow.pl/index.php?typ=G&id=82621&okres=3'
# --------------------------------------------------------------------------------------

uClient = uReq(PlanZajec_URL)
PlanZajec_html = uClient.read()
uClient.close()

PlanZajec_soup = soup(PlanZajec_html, 'html.parser')

NazwaKalendarza = PlanZajec_soup.title.get_text().split(' ')[-1]+'.csv'

Containers = PlanZajec_soup.find_all('tr', {'class':''})

Table = [['','','','','','','']]
for row in range(1, len(Containers)):
    if Containers[row].td.attrs['class'][0] != 'uwagi':
        StartDate = Containers[row].find_all('td',{'class':'termin'})[0].get_text()
        EndDate = StartDate
        
        Przedmiot = Containers[row].find_all('td',{'class':''})
        Subject = Przedmiot[0].get_text()
        Description = Przedmiot[1].get_text() + ' | ' + Przedmiot[2].get_text()
        Location = Przedmiot[3].get_text()

        Time = Containers[row].find_all('td',{'class':'dzien'})[0].get_text().split(' ')
        StartTime = Time[1]
        EndTime = Time[3]   
        
        Table.append([Subject,StartDate,StartTime,EndDate,EndTime,Description,Location])

cols = ['Subject','Start Date','Start Time','End Date','End Time','Description','Location']
dfPlanZajec = pd.DataFrame(data=Table[1:], columns=cols)

dfPlanZajec.to_csv(NazwaKalendarza, index=False)
