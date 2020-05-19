from selenium import webdriver
import pandas as pd
import time
import sys
import os
from selenium.webdriver.common.keys import Keys
from pathlib import Path
home = str(Path.home())
class Instagram:

	def __init__(self,username, password):
		
		self.driver = webdriver.Chrome("chromedriver.exe")
		self.username = username
		self.password = password
		self.numoff = 0

	def logIn(self):

		self.driver.get("https://www.instagram.com/")

		time.sleep(2)
		username = self.driver.find_element_by_xpath(
	        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input"
	    	)

		password = self.driver.find_element_by_xpath(
	        "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input"
	    	)
		username.send_keys(self.username)
		password.send_keys(self.password)

		self.driver.find_element_by_xpath(
			"/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div"
			).click()
		time.sleep(2)

		try:
			self.driver.find_element_by_xpath(
			"/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[7]/p"
			)
			print("Wrong username password")
			exit(0)
		except Exception:
			print("login successful")

	def navigate(self, username):
		
		self.driver.get('https://www.instagram.com/' + username + '/')
		time.sleep(2)

	def getFollowers(self, username):
		time.sleep(2)
		self.driver.get('https://www.instagram.com/' + username + '/')
		time.sleep(2)

		numb = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute('title')
		self.numoff = numb
		self.driver.find_element_by_xpath(
			"/html/body/div[1]/section/main/div/header/section/ul/li[2]/a"
			).click()
		time.sleep(2)

		self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul').click()
		followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
		numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
		actionChain = webdriver.ActionChains(self.driver)
		time.sleep(2)

		halt = 0
		while (numberOfFollowersInList < int(numb)-1):
			halt=halt+1
			if (halt%200)==0 :
				self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul').click()
			actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
			numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

		names = []
		for user in followersList.find_elements_by_css_selector('li'):
			userLink = user.find_element_by_css_selector('a').get_attribute('href')
			names.append(userLink)

		return names

	def search(self,list, platform):
	    for i in range(len(list)):
	        if list[i] == platform:
	            return True
	    return False

	def check_new_unfollowers(self, username):
		try:
			prev = pd.read_csv(home+"/Instagram_Followers_Data\\"+username+'.csv').Name.tolist()
		except Exception:
			print("Run '... -r <username> <password>' first")
			exit(0)
		names = self.getFollowers(username)
		self.updateList(username,names)
		unfoll = []
		for a in prev:
			if not self.search(names, a):
				unfoll.append(a)
		return unfoll

	def updateList(self,username,nlist):
		prev = pd.read_csv(home+"/Instagram_Followers_Data\\"+username+'.csv').Name.tolist()
		for a in nlist:
			if not self.search(prev, a):
				prev.append(a)
		df = pd.DataFrame({'Name':prev}) 
		df.to_csv(home+"/Instagram_Followers_Data\\"+username+ '.csv', index=False, encoding='utf-8')


def chkdir():

	try:
		os.mkdir(home+"/Instagram_Followers_Data")
	except FileExistsError:
		pass

def refreshList(username,password):
	bot = Instagram(username, password)
	bot.logIn()
	name = bot.getFollowers(username)
	df = pd.DataFrame({'Name':name}) 
	chkdir()
	df.to_csv(home+"/Instagram_Followers_Data\\"+username+ '.csv', index=False, encoding='utf-8')

def getFollowers(username,password):
	bot = Instagram(username, password)
	bot.logIn()
	name = bot.getFollowers(username)
	print("-----------------------------------------------------------------------------------------------\n\n\nYour Followers Are\n\n\n-----------------------------------------------------------------------------------------------")
	for a in name:
		print(a)
	print("-----------------------------------------------------------------------------------------------\n\n\nList End Here\n\n\n-----------------------------------------------------------------------------------------------")


def getUnfollowers(username,password):
	bot = Instagram(username, password)
	bot.logIn()
	unfollow = bot.check_new_unfollowers(username)
	df = pd.DataFrame({'Name':unfollow}) 
	df.to_csv(home+"/Instagram_Followers_Data\\"+'New_Unfollowers.csv', index=False, encoding='utf-8')
	if len(unfollow)==0:
		print("No new Unfollower")
		exit(0)
	print("-----------------------------------------------------------------------------------------------\n\n\nYour Unfollowers Are\n\n\n-----------------------------------------------------------------------------------------------")
	for a in unfollow:
		print(a[26:])
	print("-----------------------------------------------------------------------------------------------\n\n\nList End Here\n\n\n-----------------------------------------------------------------------------------------------")


if len(sys.argv)<2:
	print("ERROR, NO ARGUMENT\nTry '-help'")
	exit(0)

if sys.argv[1] == "-help":
	print("whole manual\n-a\tget followers\n-r\trefresh list\n-u\tget unfollowers\n")
	exit(0)

if sys.argv[1] == "-a":
	if len(sys.argv) == 4:
		getFollowers(sys.argv[2],sys.argv[3])
	else :
		print("ERROR, INVALID ARGUMENT\nTry '-help'")
	exit(0)

if sys.argv[1] == "-r":
	if len(sys.argv) == 4:
		refreshList(sys.argv[2],sys.argv[3])
	else :
		print("ERROR, INVALID ARGUMENT\nTry '-help'")
	exit(0)

if sys.argv[1] == "-u":
	if len(sys.argv) == 4:
		getUnfollowers(sys.argv[2],sys.argv[3])
	else :
		print("ERROR, INVALID ARGUMENT\nTry '-help'")
	exit(0)

print("ERROR, INVALID ARGUMENT\nTry '-help'")
exit(0)