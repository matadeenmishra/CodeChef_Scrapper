import requests
from bs4 import BeautifulSoup
import os

base_url="https://www.codechef.com/"

def crawl(username):
	url = "https://www.codechef.com/users/" + str(username) 
	source_code = requests.get(url)
	plain_text = source_code.text
	#soup =BeautifulSoup(plain_text)
	soup = BeautifulSoup(plain_text, "lxml")
	section = soup.findAll('section',{'class':'rating-data-section problems-solved'})
	links = section[0].findAll('a')
	#links = section[0].find_all('a')

	os.makedirs(username,0o777,exist_ok=True)
	os.chdir(username) # go down #2

	for link in links:
		problem_status_url=base_url+ link['href']
		name = link.string
		crawl_some_more(problem_status_url,name,username)
	
	os.chdir('..') # go up #2
		
def crawl_some_more(url,name,username):
	url = url + "?sort_by=All&sorting_order=asc&language=All&status=15&Submit=GO" #show only Correct Submissions!
	source_code = requests.get(url)
	plain_text = source_code.text
	#soup = BeautifulSoup(plain_text)
	soup = BeautifulSoup(plain_text, "lxml")
	id_list = soup.findAll('td',{'width':'60'})
	submission_id=""
	try:
		print(id_list)
		submission_id=id_list[0].string  #taking the latest correct submission's ID
	except:
		if len(id_list)!=0:
			submission_id=id_list.string	
	lang_list = soup.findAll('td',{'width':'70'})
	try:
		print(lang_list)
		lang = lang_list[0].string       #taking the language of latest correct submission
	except:
		
		if len(lang_list)!=0:
			lang = lang_list.string 
	if submission_id!="":	
		submission_url = base_url + "viewplaintext/" + str(submission_id) 
		code = a_little_more_crawl(submission_url)

		name = name + ".txt"
		f = open(name,'w')	
		f.write(code)
		f.close()
		
def a_little_more_crawl(url):
	source_code = requests.get(url)
	plain_text = source_code.text
	#soup = BeautifulSoup(plain_text)
	soup = BeautifulSoup(plain_text, "lxml")
	problem_code = soup.get_text()
	return problem_code 
	
	

username = input("Enter the username: ")	
crawl(str(username))

