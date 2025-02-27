import concurrent.futures
import os
from fake_useragent import UserAgent
import requests, bs4, httpx

class Search:
	def __init__(self, type, data):
		self.type = type
		self.data = data

	def download(self, count , path="./img", threads=1):
		if self.type == "images":
			Threads(path, count, threads).download_images(self.data)
			return True
		else:
			return False

	def __repr__(self):
		return str(self.data)

	def __getitem__(self, key):
		if isinstance(self.data, dict):
			return self.data.get(key)
		elif isinstance(self.data, list):
			return self.data[key]
		else:
			raise Exception("Error")

class Threads:
	def __init__(self, path, count, threads):
		self.requests = httpx.Client(http2=True)
		self.ua = UserAgent()
		self.path = path
		self.threads = threads
		os.makedirs(self.path, exist_ok=True)
		self.count = count

	def download_image(self, idx, img_url):
		try:
			response = self.requests.get(img_url, headers={
				"User-Agent": self.ua.random
			}, timeout=2)
			if response.status_code in [200, 201]:
				with open(f"{self.path}/img_{idx}.png", "wb") as file:
					file.write(response.content)
		except Exception as e:
			pass

	# Загрузка изображений с многопоточностью
	def download_images(self, results):
		results = results[:self.count]
		with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
			futures = []
			for idx, i in enumerate(results):
				futures.append(executor.submit(self.download_image, idx, i["url"]))

#Переводчик
def interpreter(text, lang="en"):
    base_url = f"https://translate.google.com/m?tl={lang}&sl=auto&q={text}"
    response = requests.get(base_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    translated_div = soup.find('div', class_='result-container')
    return translated_div.text