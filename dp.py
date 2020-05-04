import selenium
import requests
import json
import io
import webbrowser
from PIL import Image
from bs4 import BeautifulSoup
# from saveFiles import saveFile
class DP:
	def getImage(username):
		if username[0] == "@":
			username = username[1:]
		response = requests.get("https://www.instagram.com/"+username)
		bsobject = BeautifulSoup(response.content,'html.parser')
		bsobject.prettify()
		rr = bsobject.find_all("script",type="text/javascript")
		span = bsobject.find_all("img",class_="_6q-tv")
		print(response.status_code)
		jsnstr = rr[3].contents[0][20:len(rr[3].contents[0])-1]
		jsn = json.loads(jsnstr)
		ppurl = jsn["entry_data"]["ProfilePage"][0]["graphql"]["user"]["profile_pic_url_hd"]
		response = requests.get(ppurl)
		file = open(username+".jpg","wb")
		file.write(response.content)
		return username+".jpg"

im = Image.open("c:Users\chitr\OneDrive\Desktop\lol.png")
webbrowser.open("c:Users\chitr\OneDrive\Desktop\lol.png")