from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import requests
import re
import sys
import time
import os

# number of arzigogoli by weeks
def weeksFromFirst():
	f_date = date(2019, 9, 30)
	l_date = date.today()
	delta = l_date - f_date
	return int(delta.days/7) + 1

# number of arzigogoli by website count
def scraper():
	page = requests.get("https://weblab.ing.unimore.it/people/andreoli/didattica/sistemi-operativi/index.html").text
	soup = BeautifulSoup(page, "html.parser")
	array = []
	for elem in soup.find_all('h4'):
		x = re.search(("Arzigogolo*"), elem.text)
		if x is not None:
			array.append(x)
	return len(array) # number of Arzigogoli

# send and pin message Telegram
def sendTelegram(numArz):
	bot_token = '' ### ADD
	UnimoreGroup = '' ###ADD
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
		UnimoreGroup + '&parse_mode=Markdown&text=' + "Arzigogolo " + str(numArz) + \
		" uscito: https://weblab.ing.unimore.it/people/andreolini/didattica/sistemi-operativi/2019-20/arzigogolo-" + \
		str(numArz) + "/A" + str(numArz) + "-testo.pdf"
	messageID = requests.get(send_text)
	pin_message = 'https://api.telegram.org/bot' + bot_token + '/pinChatMessage?chat_id=' + \
		UnimoreGroup + '&message_id=' + \
		str(messageID.json()["result"]["message_id"])
	requests.get(pin_message)


def main():
	while True:
		ArzByWeek = weeksFromFirst()
		ArzByWebsite = scraper()

		print("Arzigogolo settimana: " + str(ArzByWeek))
		print("Arzigogoli sul sito attualmente: " + str(ArzByWebsite))

		if ArzByWeek == ArzByWebsite:
			sendTelegram(ArzByWebsite)

			# days to next week
			daysToSunday = 6 - date.today().weekday()

			# difference hours
			diffHours = abs(datetime.now().replace(microsecond=0) - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

			# sleep to monday 8:00
			time.sleep(daysToSunday * 86400 + (86400 - diffHours + 28800)) # daysToSunday + (24h - current time + 8h)
		else:
			print("sleep for 15 minutes")
			time.sleep(900)

main()
