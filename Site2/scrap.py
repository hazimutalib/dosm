from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
uClient = uReq(my_url)

page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, 'html.parser')

containers = page_soup.findAll('div', {'class':'_4ddWXP'})

for container in conatiners:
	model = container.div.div.div.img["alt"]
	rating = container.span.div.text.astype('float')
	count = container.findAll("span", {"class":"_2_R_DZ"})[0].text
	sale_price = container.findAll("div", {"class":"_30jeq3"})[0].text
	original_price = container.findAll("div", {"class":"_3I9_wc"})[0].text


