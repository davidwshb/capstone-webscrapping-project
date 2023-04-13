from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
row = table.find_all('a',  attrs={'class':'w'})

row_length = len(row)

temp = [] #initiating a list 

for i in range(0, row_length):
#insert the scrapping process here
    
    #get date
    date = table.find_all('a', attrs={'class':'w'})[i].text
    
    #get kurs
    kurs = table.find_all('span', attrs={'class':'w'})[i].text
    
    temp.append((date,kurs)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','kurs'))

#insert data wrangling here
df['kurs'] = df['kurs'].str.replace('$', '')
df['kurs'] = df['kurs'].str.replace('1 =','')
df['kurs'] = df['kurs'].str.replace('Rp','')
df['kurs'] = df['kurs'].str.replace(',','')

df['kurs'] = df['kurs'].astype('int64')
df['date'] = df['date'].astype('datetime64')

df = df.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["kurs"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)