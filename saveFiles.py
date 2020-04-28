import requests
from dataclasses import dataclass
@dataclass
class SaveFile:
	def saveImage(url,path):
		try:
			response = requests.get(url)
			file = open(path+".jpg","wb")
			file.write(response.content)
		except Exception:
			return False
		return True
