"""
python file for scraping face book friends of a facebook profile
"""
import http.cookiejar
import requests
import urllib.request
import bs4

cj=http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj ))

urllib.request.install_opener(opener)

authentication_url ="https://m.facebook.com/login.php"
payload ={

	'email': "amjadhkhan.ga3@iiitmk.ac.in",
	'pass': "Apple@12345"
}
data= urllib.parse.urlencode(payload).encode('utf-8')
req = urllib.request.Request(authentication_url,data)
res = urllib.request.urlopen(req)
contents = res.read()
# print(contents)

url = "https://m.facebook.com/amjad.rkz/friends"
result_data=requests.get(url,cookies=cj)
soup=bs4.BeautifulSoup(result_data.text, 'html.parser')


z=0
for i in soup.find_all('a'):
	if i.text.lower()=="see more friends":
		break
	if z>15 and i.text.lower()!="add friend":
		print(i.text)
	z=z+1
